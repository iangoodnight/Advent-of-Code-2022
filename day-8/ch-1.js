#!/usr/bin/env node
/**
 * <https://adventofcode.com/2022/day/8> 'Advent of Code - Day 8'
 *
 * # Advent of Code 2022 --- Day 8
 *
 * ## Treetop Tree House
 *
 * The expedition comes across a peculiar patch of tall trees all planted
 * carefully in a grid. The Elves explain that a previous expedition planted
 * these trees as a reforestation effort. Now, they're curious if this would be
 * a good location for a **tree house**.
 *
 * First, determine whether there is enough tree cover here to keep a tree house
 * **hidden**. To do this, you need to count the number of trees that are
 * **visible from outside the grid** when looking directly along a row or
 * column.
 *
 * The Elves have already launched a **quadcopter** to generate a map with the
 * height of each tree (your puzzle input). For example:
 *
 * ```
 * 30373
 * 25512
 * 65332
 * 33549
 * 35390
 * ```
 *
 * Each tree is represented as a single digit whose value is its height, where
 * `0` is the shortest and `9` is the tallest.
 *
 * A tree is **visible** if all of the other trees between it and an edge of the
 * grid are **shorter** than it. Only consider trees in the same row or column;
 * that is, only look up, down, left, or right from any given tree.
 *
 * All of the trees around the edge of the grid are **visible** - since they are
 * already on the edge, there are no trees to block the view. In this example,
 * that only leaves the **interior nine trees** to consider:
 *
 * - The top-left `5` is **visible** from the left and top. (It isn't visible
 *   from the right or bottom since other trees of height `5` are in the way.)
 * - The top-middle `5` is **visible** from the top and right.
 * - The top-right `1` is not visible from any direction; for it to be visible,
 *   there would need to only be trees of height `0` between it and an edge.
 * - The left-middle `5` is **visible**, but only from the right.
 * - The center `3` is not visible from any direction; for it to be visible,
 *   there would need to be only trees of at most height `2` between it and an
 *   edge.
 * - The right-middle `3` is **visible** from the right.
 * - In the bottom row, the middle `5` is visible, but the `3` and `4` are not.
 *
 * With 16 trees visible on the edge and another 5 visible in the interior, a
 * total of `21` trees are visible in this arrangement.
 *
 * Consider your map; **how many trees are visible from outside the grid?**
 *
 * @format
 */

const fs = require('node:fs');

/** Reads a file and returns data as a single string
 * @param {string} path - Input file path
 * @returns {Promise} Promise object represents file content as a single string
 */
function readFileInputAsync(path = './input.txt') {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) reject(err);
      resolve(data);
    });
  });
}

/** Parses a block of raw text into a two-dimensional array (forest)
 * @param {string=''} rawText - Block of input text
 * @returns {Array.<number[]>} Two dimensional array
 */
function parseFileText(rawText = '') {
  const validRe = /^\d+$/; // valid lines contain only digits

  return rawText.split('\n').reduce((reduced, line) => {
    // filter out empty lines
    if (validRe.test(line)) {
      // split line, map to integers, push row to results
      reduced.push(line.split('').map((char) => parseInt(char, 10)));
    }
    return reduced;
  }, []);
}

/** Returns true if tree is taller than any of the other trees
 * @param {number} tree - Height of tree to check
 * @param {number[]=[]} otherTrees - An array of trees to compare
 * @returns {boolean} True is tree is tallest
 */
function isTallest(tree, otherTrees = []) {
  // Array.prototype.some short circuits on true
  return !otherTrees.some((compare) => compare >= tree);
}

/** Takes a two-dimensional array (forest) and a cursor (x, y) and returns true
 * if cursor points to a tree that is visible from the forest edge.
 * @param {Array.<number[]>=[[]]} forest - A two dimensional array of integers
 * @param {number[]} cursor - an array with the x and y coordinates of cursor
 * @returns {boolean} True if tree is visible from any edge
 */
function isTreeVisible(forest = [[]], [x, y] = [0, 0]) {
  const row = forest[y];
  // Any tree on the edge is visible
  if (!x || !y || x === row.length - 1 || y === forest.length - 1) return true;

  const column = forest.map((forestRow) => forestRow[x]);

  const tree = forest[y][x];
  // check cardinal directions
  const toTheNorth = column.slice(0, y);
  // return true if tree is visible from any direction
  if (isTallest(tree, toTheNorth)) return true;

  const toTheEast = row.slice(x + 1);

  if (isTallest(tree, toTheEast)) return true;

  const toTheSouth = column.slice(y + 1);

  if (isTallest(tree, toTheSouth)) return true;

  const toTheWest = row.slice(0, x);

  return isTallest(tree, toTheWest);
}

(async function main() {
  try {
    const inputFilePath = process.argv[2] || 'input.txt';
    // check for valid path
    if (!fs.existsSync(inputFilePath)) {
      console.log('Usage: node ch-1.js <input file>');
      process.exit(0);
    }
    const fileText = await readFileInputAsync(inputFilePath);

    const forest = parseFileText(fileText);

    const isVisibleInForest = isTreeVisible.bind(null, forest);

    let totalVisibleTrees = 0;

    // eslint-disable-next-line no-restricted-syntax
    for (const y of forest.keys()) {
      const row = forest[y];

      // eslint-disable-next-line no-restricted-syntax
      for (const x of row.keys()) {
        if (isVisibleInForest([x, y])) totalVisibleTrees += 1;
      }
    }
    console.log(`There are ${totalVisibleTrees} trees visible from the edge`);
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
})();
