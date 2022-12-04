#!/usr/bin/env node
/**
 * @format
 *
 * <https://adventofcode.com/2022/day/3 'Advent of Code - Day 2'>
 *
 * # Advent of Code 2022 --- Day 3
 *
 * ## Part Two
 *
 * As you finish identifying the misplaced items, the Elves come to you with
 * another issue.
 *
 * For safety, the Elves are divided into groups of three. Every Elf carries a
 * badge that identifies their group. For efficiency, within each group of three
 * Elves, the badge is the **only item type carried by all three Elves**. That
 * is, if a group's badge is item type `B`, then all three Elves will have item
 * type `B` somewhere in their rucksack, and at most two of the Elves will be
 * carrying any other item type.
 *
 * The problem is that someone forgot to put this year's updated authenticity
 * sticker on the badges. All of the badges need to be pulled out of the
 * rucksacks so the new authenticity stickers can be attached.
 *
 * Additionally, nobody wrote down which item type corresponds to each group's
 * badges. The only way to tell which item type is the right one is by finding
 * the one item type that is **common between all three Elves** in each group.
 *
 * Every set of three lines in your list corresponds to a single group, but each
 * group can have a different badge item type. So, in the above example, thefirst
 * group's rucksacks are the first three lines:
 *
 * ```
 * vJrwpWtwJgWrhcsFMMfFFhFp
 * jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
 * PmmdzqPrVvPwwTWBwg
 * ```
 *
 * And the second group's rucksacks are the next three lines:
 *
 * ```
 * wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
 * ttgJtRGJQctTZtZT
 * CrZsJsPPZsGzwwsLwLmpwMDw
 * ```
 *
 * In the first group, the only item type that appears in all three rucksacks is
 * lowercase `r`; this must be their badges. In the second group, their badge
 * item type must be `Z`.
 *
 * Priorities for these items must still be found to organize the sticker
 * attachment efforts: here, they are 18 (`r`) for the first group and 52 (`Z`)
 * for the second group. The sum of these is **70**.
 *
 * Find the item type that corresponds to the badges of each three-Elf group.
 * **What is the sum of the priorities of those item types?**
 */

const fs = require('fs');

/** Reads a file and returns data as a single string
 * @param {string} path - Input file path
 * @returns {Promise} Promise object represts file content as a single string
 */
function readFileInputAsync(path = './input.txt') {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) reject(err);
      resolve(data);
    });
  });
}

/**
 * An array of three strings
 * @typedef {Array.<string, string, string>} BadgeGroup
 */

/** Parses input string
 * @param {string} data - File input
 * @returns {BadgeGroup[]} List of arrays containing three strings each
 */
function parseInputData(data = '') {
  const validRe = /^[a-z]{2,}$/i; // Validate input line

  return (
    data
      .split('\n') // split by line
      .filter((line) => validRe.test(line)) // filter out blanks lines and junk
      // reduce to a BadgeGroup
      .reduce(
        ([tmpArr, reduced], line) => {
          if (tmpArr.length < 3) tmpArr.push(line); // Build group of three lines
          if (tmpArr.length === 3) {
            reduced.push(tmpArr); // Push each group of three to reduced
            return [[], reduced];
          }
          return [tmpArr, reduced];
        },
        [[], []]
      )
      // pop off the reduced list
      .pop()
  );
}

/** Returns a list of characters common to each of its string arguments
 * @param {...string} strings - One or more strings to check for common
 * characters
 * @returns {string[]} - A list of single-character strings
 */
function findDuplicateCharacters(...strings) {
  const uniqueChars = [
    /** create a list of unique characters from each string */
    ...new Set([...strings.reduce((reduced, str) => reduced + str)]),
  ];
  // the prompt implies only one "badge" unique character per group, but we'll
  // check anyway
  return uniqueChars.filter((char) =>
    /* filter unique characters by characters found in every string */
    strings.reduce((isDuplicated, string) => {
      if (isDuplicated && string.includes(char)) return true;
      return false;
    }, true)
  );
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
  /* difference between character code and offset represents "priority" */
  return char.toLowerCase().charCodeAt(0) + offset;
}

/** Reduces a list of BadgeGroups to the sum of their badge priorities
 * @param {BadgeGroup[]} groups - A list of BadgeGroups
 * @returns {number} Sum of group badge priorities
 */
function getSumDuplicatePriorities(groups = []) {
  return groups.reduce((total, group) => {
    /** these should always be single-member arrays */
    const [badge] = findDuplicateCharacters(...group);
    /** convert badge to priority score and add to total */
    return total + charToPriority(badge);
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

  const parsed = parseInputData(inputData); // Parse into list of BadgeGroups

  const total = getSumDuplicatePriorities(parsed); // Find total

  console.log(`Priority total: ${total}`); // 2760
})();
