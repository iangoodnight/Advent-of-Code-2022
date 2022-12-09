#!/usr/bin/env node
/**
 * <https://adventofcode.com/2022/day/8> 'Advent of Code - Day 8'
 *
 * # Advent of Code 2022 --- Day 8
 *
 * ## Part Two
 *
 *
 * Content with the amount of tree cover available, the Elves just need to know
 * the best spot to build their tree house: they would like to be able to see a
 * lot of **trees**.
 *
 * To measure the viewing distance from a given tree, look up, down, left, and
 * right from that tree; stop if you reach an edge or at the first tree that is
 * the same height or taller than the tree under consideration. (If a tree is
 * right on the edge, at least one of its viewing distances will be zero.)
 *
 * The Elves don't care about distant trees taller than those found by the rules
 * above; the proposed tree house has large **eaves** to keep it dry, so they
 * wouldn't be able to see higher than the tree house anyway.
 *
 * In the example above, consider the middle `5` in the second row:
 *
 * ```
 * 30373
 * 25512
 * 65332
 * 33549
 * 35390
 * ```
 *
 * - Looking up, its view is not blocked; it can see `1` tree (of height `3`).
 * - Looking left, its view is blocked immediately; it can see only `1` tree (of
 *   height `5`, right next to it).
 * - Looking right, its view is not blocked; it can see `2` trees.
 * - Looking down, its view is blocked eventually; it can see `2` trees (one of
 *   height `3`, then the tree of height `5` that blocks its view).
 *
 * A tree's **scenic score** is found by **multiplying together** its viewing
 * distance in each of the four directions. For this tree, this is `4` (found by
 * multiplying `1 * 1 * 2 * 2`).
 *
 * However, you can do even better: consider the tree of height `5` in the
 * middle of the fourth row:
 *
 * ```
 * 30373
 * 25512
 * 65332
 * 33549
 * 35390
 * ```
 *
 * - Looking up, its view is blocked at `2` trees (by another tree with a height
 *   of `5`).
 * - Looking left, its view is not blocked; it can see `2` trees.
 * - Looking down, its view is also not blocked; it can see `1` tree.
 * - Looking right, its view is blocked at `2` trees (by a massive tree of
 *   height `9`).
 *
 * This tree's scenic score is `8` (`2 * 2 * 1 * 2`); this is the ideal spot for
 * the tree house.
 *
 * Consider each tree on your map. **What is the highest scenic score possible
 * for any tree?**
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

/** Gets the number of array elements (trees) iterated through (visible) before
 * finder a tree taller than the origin tree
 * @params {number} tree - The height or origin tree
 * @params {number[]} lineOfSight - An array of the trees in the line of sight
 * @returns {number} The total of trees iterated through before finding a tree
 * taller than the origin tree
 */
function getViewingDistance(tree, lineOfSight = []) {
  // guard against edge
  let viewingDistance = 0;
  // eslint-disable-next-line no-restricted-syntax
  for (const nextTree of lineOfSight) {
    viewingDistance += 1;
    if (nextTree >= tree) return viewingDistance;
  }
  return viewingDistance;
}

/** Takes a two-dimensional array (forest) and a cursor (x, y) and returns the
 * total scenic score (north * east * south * west) for the tree indexed by the
 * cursor
 * @param {Array.<number[]>=[[]]} forest - A two dimensional array of integers
 * @param {number[]} cursor - an array with the x and y coordinates of the
 * cursor
 * @returns {number} The multipled scores from each cardinal direction
 */
function getScenicScore(forest = [[]], [x, y] = [0, 0]) {
  const row = forest[y];
  // Edges have at least one score of 0
  if (!x || !y || x === row.length - 1 || y === forest.length - 1) {
    return 0;
  }
  const column = forest.map((forestRow) => forestRow[x]);

  const tree = forest[y][x];
  // chop up cardinal directions, reverse north and west
  const north = column.slice(0, y).reverse();

  const east = row.slice(x + 1);

  const south = column.slice(y + 1);

  const west = row.slice(0, x).reverse();
  // start at 1 and multiple
  let scenicScore = 1;
  // eslint-disable-next-line no-restricted-syntax
  for (const direction of [north, east, south, west]) {
    const viewScore = getViewingDistance(tree, direction);
    // any score of 0 returns 0 overall
    if (viewScore === 0) return viewScore;
    scenicScore *= viewScore;
  }
  return scenicScore;
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

    const getScenicScoresInForest = getScenicScore.bind(null, forest);

    const forestScores = [];

    // eslint-disable-next-line no-restricted-syntax
    for (const y of forest.keys()) {
      const row = forest[y];

      // eslint-disable-next-line no-restricted-syntax
      for (const x of row.keys()) {
        forestScores.push(getScenicScoresInForest([x, y]));
      }
    }
    const maxScenicScore = Math.max(...forestScores);
    // The highest scenic score possible is 504000   
    console.log(`The highest scenic score possible is ${maxScenicScore}`);
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
})();
