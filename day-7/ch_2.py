#!/usr/bin/python3

"""
<https://adventofcode.com/2022/day/7> 'Advent of Code - Day 7'

# Advent of Code 2022 --- Day 7

## Part Two

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is `70000000`. To run the
update, you need unused space of at least `30000000`. You need to find a
directory you can delete that will **free up enough space** to run the update.

In the example above, the total size of the outermost directory (and thus the
total amount of used space) is `48381165`; this means that the size of the
unused space must currently be `21618835`, which isn't quite the `30000000`
required by the update. Therefore, the update still requires a directory with
total size of at least `8381165` to be deleted before it can run.

To achieve this, you have the following options:

- Delete directory `e`, which would increase unused space by `584`.
- Delete directory `a`, which would increase unused space by `94853`.
- Delete directory `d`, which would increase unused space by `24933642`.
- Delete directory `/,` which would increase unused space by `48381165`.

Directories `e` and `a` are both too small; deleting them would not free up
enough space. However, directories `d` and `/` are both big enough! Between
these, choose the smallest: `d`, increasing unused space by `24933642`.

Find the smallest directory that, if deleted, would free up enough space on the
filesystem to run the update. **What is the total size of that directory?**
"""

import argparse
import functools
import os
import re
import sys


class FileNode():
    """Class FileNode represets a file instance in a FileTree

    Attributes:
        children (Union[list[FileNode], None]): List of child FileNodes or None
        file (str): File name
        parent (Union[FileNode, None]): Parent node
        size (int): File size
    """

    def __init__(self, file, size=None, directory=None, parent=None):
        """Constructor

        Args:
            file (str): File name
            size (int): File size if not a directory
            directory (bool): True if creating directory
            parent (FileNode): Parent node or None if root
        """
        self.children = directory and []
        self.file = file
        self.parent = parent
        self.size = size

    def add(self, obj):
        """Adds a new FileNode to instance children

        Args:
            obj (FileNode): New file to add
        Returns:
            self
        """
        if self.is_dir() and isinstance(obj, FileNode):
            obj.parent = self
            self.children.append(obj)
            return self
        print(f'{self.file} is not a directory')
        return None

    def get_file(self, file):
        """Returns child matching child node (not recursive)

        Args:
            file (str): File name to match
        Returns:
            FileNode: matching child
        """
        if self.is_dir():
            for child in self.children:
                if child.file == file:
                    return child
        return None

    def is_dir(self):
        """Returns True if FileNode is a directory"""
        return self.children is not None

    def get_size(self):
        """Recursively sums file sizes in the case of a directory else returns
        size attribute

        Returns:
            int: Size of file or total size of child files
        """
        if self.is_dir():
            size = 0
            for child in self.children:
                size = size + child.get_size()
            return size
        return self.size


class FileTree():
    """Class FileTree acts as the root to chile FileNodes

    Attributes:
        root (FileNode): root node, always a directory, no parent
        cwd (FileNode): current working directory, cursor
    """

    def __init__(self):
        """Constructor"""
        self.root = FileNode('', directory=True)
        self.cwd = self.root

    def add(self, obj):
        """Adds a file node at current working directory (cwd)

        Args:
            obj (FileNode): New file

        Returns:
            self
        """
        self.cwd.add(obj)
        return self

    def cd(self, path):
        """Changes current working directory (cwd)

        Args:
            path (str): Target directory

        Returns
            self
        """
        if path == '..':  # up a directory
            self.cwd = self.cwd.parent or self.root
            return self

        if path == '/':  # cd to root
            self.cwd = self.root
            return self

        new_node = self.cwd.get_file(path)
        # check for validity
        if (new_node and new_node.is_dir()):
            self.cwd = new_node
        else:
            print(f'{path} is not a valid directory')
        return self

    def crawl(self, callback, node=None):
        """Crawls FileNodes and executes callback

        Args:
            callback (func): Executes on every node

        Returns:
            self
        """
        if node is None:
            node = self.root

        for child in node.children:
            callback(child)

            if child.is_dir():
                self.crawl(callback, node=child)
        return self

    def ls(self):
        """Prints files in current working directory (cwd)

        Not necessary for solution, but good for debugging

        Returns:
            self
        """
        for node in self.cwd.children:
            if node.is_dir():
                print(f'dir {node.file}')
            else:
                print(f'{node.size} {node.file}')

        return self

    def pwd(self):
        """Prints complete file path from root to current working directory

        Not necessary for solution, but good for debugging

        Returns:
            self
        """
        parts = []
        cursor = self.cwd
        while cursor.file and cursor.parent:
            parts.append(cursor.file)
            cursor = cursor.parent
        print('/' + '/'.join(parts))
        return self

    def get_dirs_larger_than(self, limit):
        """Returns a list of directory files that have a total size greater
        than or equal to limit

        Args:
            limit (int): Filter for directories returns

        Returns:
            list[FileNode]: A list of matching FileNodes
        """
        dirs = []

        self.crawl(
            lambda x: x.is_dir() and x.get_size() >= limit and dirs.append(x)
        )
        return dirs


def main():
    """Parses args, builds FileTree, executes input, and prints result"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        help='path to input file',
        default="input.txt",
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        parser.print_usage()
        sys.exit()

    with open(args.file, encoding='utf8') as file:
        lines = file.readlines()

    file_tree = FileTree()

    for line in lines:
        tokens = line.split()

        if len(tokens) == 0:  # Blank line
            continue

        if tokens[0] == '$' and tokens[1] == 'cd':  # Change directory
            file_tree.cd(tokens[2])

        if tokens[0] == 'dir':  # Create the directory listed in input
            file_tree.add(FileNode(tokens[1], directory=True))

        if re.match(r'^\d+$', tokens[0]):  # Create file listed in input
            size = int(tokens[0])
            file_tree.add(FileNode(tokens[1], size=size))

    MAX_FILE_SPACE = 70000000
    used_space = file_tree.root.get_size()
    space_available = MAX_FILE_SPACE - used_space
    UPDATE_SIZE = 30000000
    space_needed = abs(space_available - UPDATE_SIZE) \
        if UPDATE_SIZE > space_available \
        else 0

    dirs = file_tree.get_dirs_larger_than(space_needed)  # Grab candidates

    smallest_candidate = functools.reduce(
        lambda a, b: a if a.get_size() < b.get_size() else b, dirs
    )
    print('Smallest directory that allows for update:')
    # dir wvq - 4183246
    print(f'dir {smallest_candidate.file} - {smallest_candidate.get_size()}')


if __name__ == '__main__':
    main()
