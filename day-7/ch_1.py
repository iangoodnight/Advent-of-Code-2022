#!/usr/bin/python3

"""
<https://adventofcode.com/2022/day/7> 'Advent of Code - Day 7'

# Advent of Code 2022 --- Day 7

## No Space Left on Device

You can hear birds chirping and raindrops hitting leaves as the expedition
proceeds. Occasionally, you can even hear much louder sounds in the distance;
how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its
communication system. You try to run a system update:

```
$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
```

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting
terminal output (your puzzle input). For example:

```
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
```

The filesystem consists of a tree of files (plain data) and directories (which
can contain other directories or files). The outermost directory is called `/`.
You can navigate around the filesystem, moving into or out of directories and
listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with `$` are **commands you
executed**, very much like some modern computers:

- `cd` means **change directory**. This changes which directory is the current
  directory, but the specific result depends on the argument:
  - `cd x` moves **in** one level: it looks in the current directory for the
    directory named `x` and makes it the current directory.
  - `cd ..` moves **out** one level: it finds the directory that contains the
    current directory, then makes that directory the current directory.
  - `cd /` switches the current directory to the outermost directory, `/`.
- `ls` means **list**. It prints out all of the files and directories
  immediately contained by the current directory:
  - `123 abc` means that the current directory contains a file named `abc` with
    size `123`.
  - `dir xyz` means that the current directory contains a directory named
    `xyz`.

Given the commands and output in the example above, you can determine that the
filesystem looks visually like this:

```
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
```

Here, there are four directories: `/` (the outermost directory), `a` and `d`
(which are in `/`), and `e` (which is in `a`). These directories also contain
files of various sizes.

Since the disk is full, your first step should probably be to find directories
that are good candidates for deletion. To do this, you need to determine the
**total size** of each directory. The total size of a directory is the sum of
the sizes of the files it contains, directly or indirectly. (Directories
themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

- The total size of directory `e` is **584** because it contains a single file
  `i` of size 584 and no other directories.
- The directory `a` has total size **94853** because it contains files `f`
  (size 29116), `g` (size 2557), and `h.lst` (size 62596), plus file `i`
  indirectly (`a` contains `e` which contains `i`).
- Directory `d` has total size **24933642**.
- As the outermost directory, `/` contains every file. Its total size is
  **48381165**, the sum of the size of every file.

To begin, find all of the directories with a total size of **at most 100000**,
then calculate the sum of their total sizes. In the example above, these
directories are `a` and `e`; the sum of their total sizes is `95437` (94853 +
584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. **What is the
sum of the total sizes of those directories?**
"""

import argparse
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

    def get_dirs_by_size(self, limit):
        """Returns a list of directory files that have a total size up to the
        limit

        Args:
            limit (int): Filter for directories returns

        Returns:
            list[FileNode]: A list of matching FileNodes
        """
        dirs = []

        self.crawl(
            lambda x: x.is_dir() and x.get_size() <= limit and dirs.append(x)
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

    dirs = file_tree.get_dirs_by_size(100000)  # Grab matching directories

    total_size = 0

    for directory in dirs:  # Find sum
        total_size = total_size + directory.get_size()
    # Total size: 1454188
    print(f'The sum of the size of directories that match is {total_size}')


if __name__ == '__main__':
    main()
