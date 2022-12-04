#!/usr/bin/env node
/**
 * @format
 *
 * <https://adventofcode.com/2022/day/3 'Advent of Code - Day 2'>
 *
 * # Advent of Code 2022 --- Day 3
 *
 *   ## Rucksack Reorganization
 *
 *   One Elf has the important job of loading all of the **rucksacks** with
 *   supplies for the jungle journey. Unfortunately, that Elf didn't quite follow
 *   the packing instructions, and so a few items now need to be rearranged.
 *
 *   Each rucksack has two large **compartments**. All items of a given type are
 *   meant to go into exactly one of the two compartments. The Elf that did the
 *   packing failed to follow this rule for exactly one item type per rucksack.
 *
 *   The Elves have made a list of all of the items currently in each rucksack
 *   (your puzzle input), but they need your help finding the errors. Every item
 *   type is identified by a single lowercase or uppercase letter (that is, `a`
 *   and `A` refer to different types of items).
 *
 *   The list of items for each rucksack is given as characters all on a single
 *   line. A given rucksack always has the same number of items in each of its
 *   two compartments, so the first half of the characters represent items in the
 *   first compartment, while the second half of the characters represent items
 *   in the second compartment.
 *
 *   For example, suppose you have the following list of contents from six
 *   rucksacks:
 *
 *   ```
 *   vJrwpWtwJgWrhcsFMMfFFhFp
 *   jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
 *   PmmdzqPrVvPwwTWBwg
 *   wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
 *   ttgJtRGJQctTZtZT
 *   CrZsJsPPZsGzwwsLwLmpwMDw
 *   ```
 *
 *   - The first rucksack contains the items `vJrwpWtwJgWrhcsFMMfFFhFp`, which
 *     means its first compartment contains the items `vJrwpWtwJgWr`, while the
 *     second compartment contains the items `hcsFMMfFFhFp`. The only item type
 *     that appears in both compartments is lowercase `p`.
 *   - The second rucksack's compartments contain `jqHRNqRjqzjGDLGL` and
 *     `rsFMfFZSrLrFZsSL`. The only item type that appears in both compartments
 *     is uppercase `L`.
 *   - The third rucksack's compartments contain `PmmdzqPrV` and `vPwwTWBwg`; the
 *     only common item type is uppercase `P`.
 *   - The fourth rucksack's compartments only share item type `v`.
 *   - The fifth rucksack's compartments only share item type `t`.
 *   - The sixth rucksack's compartments only share item type `s`.
 *
 *   To help prioritize item rearrangement, every item type can be converted to a
 * *priority**:
 *
 *   - Lowercase item types `a` through `z` have priorities 1 through 26.
 *   - Uppercase item types `A` through `Z` have priorities 27 through 52.
 *
 *   In the above example, the priority of the item type that appears in both
 *   compartments of each rucksack is 16 (`p`), 38 (`L`), 42 (`P`), 22 (`v`), 20
 *   (`t`), and 19 (`s`); the sum of these is `157`.
 *
 *   Find the item type that appears in both compartments of each rucksack.
 *   **What is the sum of the priorities of those item types?**
 */

const fs = require('fs');

const process = require('process');

/** Reads a file and returns data as a single string
 * @param {string} path - Input file path
 * @returns {Promise} Promise object represts file content as a single string
 */
function readFileInputAsync(filePath = './input.txt') {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) reject(err);
      resolve(data);
    });
  });
}

/**
 * An array representing a "rucksack", containing two equal-length strings or
 * "pockets"
 * @typedef {Array.<string, string>} RuckSack
 */

/**
 * A list of RucksSacks
 * @typedef {RuckSack[]} PackList
 */

/** Parses input string
 * @param {string} data - File input
 * @returns {PackList} List of RuckSacks
 */
function parseInputData(data = '') {
  const validRe = /^[a-z]{2,}$/i; // Validate input line

  return data
    .split('\n') // split by line
    .filter((line) => validRe.test(line)) // filter out blank lines and junk
    .map((line) => {
      const { length } = line;

      const firstHalf = line.slice(0, length / 2); // split the string in half

      const secondHalf = line.slice(length / 2, length);

      return [firstHalf, secondHalf]; // return as a RuckSack
    });
}

/** Returns a list of characters common to both input strings
 * @param {string} str1 - String 1
 * @param {string} str2 - String 2
 * @returns {string[]} A list of characters found in both strings
 */
function findDuplicateCharacters(str1 = '', str2 = '') {
  /** @type {string[]} */
  const repeated = str1.split('').reduce((duplicates, character) => {
    if (str2.includes(character)) duplicates.push(character);
    return duplicates;
  }, []);
  // there shouldn't ever be more than one duplicate character, but it doesn't
  // hurt to treat it as if there might be more
  return [...new Set(repeated)];
}

/** Converts an alphabetic character to an ordinal value (a = 1, b = 2..., A =
 * 27...)
 * @param {string} char - Single character string
 * @returns {number} Integer representing character priority (1-52)
 */
function charToPriority(char = '') {
  /** @type {26|0} */
  const capitalOffset = char.toUpperCase() === char ? 26 : 0;
  /** character code for 'a' starts at 96, but we want to treat 'a' as 1 */
  const offset = capitalOffset - 'a'.charCodeAt(0) + 1;
  /** difference between character code and offset represents "priority" */
  return char.toLowerCase().charCodeAt(0) + offset;
}

/** Reduces a PackList to the sum of its priorities
 * @param {PackList} packList - List of RuckSacks
 * strings)
 * @returns {number} Sum of packList priorities
 */
function getSumDuplicatePriorities(packList = []) {
  return packList.reduce((total, rucksack) => {
    /** unpack each pocket */
    const [pocket1, pocket2] = rucksack;
    /** find duplicate characters */
    const duplicated = findDuplicateCharacters(pocket1, pocket2);
    /** there should only be one, so this isn't really necessary */
    const sum = duplicated.reduce(
      (score, char) => charToPriority(char) + score,
      0
    );
    return total + sum;
  }, 0);
}

(async function main() {
  const filePath = process.argv[2] || './input.txt'; // Defaults to local file

  if (!fs.existsSync(filePath)) {
    /** If file not found or passed bad argument, print usage and exit */
    console.log('Usage: ./ch-1.js <path to input file>');
    process.exit(0);
  }
  const inputData = await readFileInputAsync(); // Read file

  const parsed = parseInputData(inputData); // Parse into PackList

  const total = getSumDuplicatePriorities(parsed); // Find total

  console.log(`Priority total: ${total}`);
})();
