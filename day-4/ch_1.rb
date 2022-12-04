# frozen-string-literal: true

# <https://adventofcode.com/2022/day/4> 'Advent of Code - Day 4'
#
# # Advent of Code 2022 --- Day 4
#
# ## Camp Cleanup
#
# Space needs to be cleared before the last supplies can be unloaded from the
# ships, and so several Elves have been assigned the job of cleaning up sections
# of the camp. Every section has a unique **ID number**, and each Elf is assigned
# a range of section IDs.
#
# However, as some of the Elves compare their section assignments with each
# other, they've noticed that many of the assignments **overlap**. To try to
# quickly find overlaps and reduce duplicated effort, the Elves pair up and make
# a **big list of the section assignments for each pair** (your puzzle input).
#
# For example, consider the following list of section assignment pairs:
#
# ```
# 2-4,6-8
# 2-3,4-5
# 5-7,7-9
# 2-8,3-7
# 6-6,4-6
# 2-6,4-8
# ```
#
# For the first few pairs, this list means:
#
# - Within the first pair of Elves, the first Elf was assigned sections `2-4`
#   (sections `2`, `3`, and `4`), while the second Elf was assigned sections
#   `6-8` (sections `6`, `7`, `8`).
# - The Elves in the second pair were each assigned two sections.
# - The Elves in the third pair were each assigned three sections: one got
#   sections `5`, `6`, and `7`, while the other also got `7`, plus `8` and `9`.
#
# This example list uses single-digit section IDs to make it easier to draw; your
# actual list might contain larger numbers. Visually, these pairs of section
# assignments look like this:
#
# ```
# .234..... 2-4
# .....678. 6-8
#
# .23...... 2-3
# ...45.... 4-5
#
# ....567.. 5-7
# ......789 7-9
#
# .2345678. 2-8
# ..34567.. 3-7
#
# .....6... 6-6
# ...456... 4-6
#
# .23456... 2-6
# ...45678. 4-8
# ```
#
# Some of the pairs have noticed that one of their assignments **fully contains**
# the other. For example, `2-8` fully contains `3-7`, and `6-6` is fully
# contained by `4-6`. In pairs where one assignment fully contains the other, one
# Elf in the pair would be exclusively cleaning sections their partner will
# already be cleaning, so these seem like the most in need of reconsideration.
# In this example, there are `2` such pairs.
#
# **In how many assignment pairs does one range fully contain the other?**

# Converts a range_string to a range (i.e.: '3-4' -> (3..4))
def string_to_range(range_string)
  x, y = range_string.split('-').map(&:to_i)
  (x..y)
end

# Parse line into a list of two ranges (i.e.: '1-4,3-5' -> [(1..4), (3..5)])
def parse_line(line)
  range_str1, range_str2 = line.split(',')
  range1 = string_to_range(range_str1)
  range2 = string_to_range(range_str2)
  [range1, range2]
end

# Returns true if one range fully contains the other
def one_range_contains?(range1, range2)
  range1.cover?(range2) || range2.cover?(range1)
end

# Grab file from args if available
file = ARGV[0] || './input.txt'

# Print usage if no file
puts 'Usage: ruby ch_1.rb <path to input file>' or exit unless File.file?(file)

# Read and filter input lines to those where one range fully overlaps the other
overlapping = File.read(file).chomp.split("\n")
                  .map { |line| parse_line(line) }
                  .filter { |r1, r2| one_range_contains?(r1, r2) }
# Print result
puts "There are #{overlapping.length} fully overlapping assignment pairs" # 503
