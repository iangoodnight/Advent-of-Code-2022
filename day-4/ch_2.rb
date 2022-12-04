# frozen-string-literal: true

# <https://adventofcode.com/2022/day/4> 'Advent of Code - Day 4'
#
# ## Part Two
#
# It seems like there is still quite a bit of duplicate work planned. Instead,
# the Elves would like to know the number of pairs that **overlap at all**.
#
# In the above example, the first two pairs (`2-4,6-8` and `2-3,4-5`) don't
# overlap, while the remaining four pairs (`5-7,7-9`, `2-8,3-7`, `6-6,4-6`, and
# `2-6,4-8`) do overlap:
#
# - `5-7,7-9` overlaps in a single section, `7`.
# - `2-8,3-7` overlaps all of the sections `3` through `7`.
# - `6-6,4-6` overlaps in a single section, `6`.
# - `2-6,4-8` overlaps in sections `4`, `5`, and `6`.
#
# So, in this example, the number of overlapping assignment pairs is `4`.
#
# **In how many assignment pairs do the ranges overlap?**
#
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

# Returns true if either range overlaps
def overlaps?(range1, range2)
  range1.cover?(range2.min) || range1.cover?(range2.max) ||
    range2.cover?(range1.min) || range2.cover?(range1.max)
end

# Grab file from args if available
file = ARGV[0] || './input.txt'

# Print usage if no file
puts 'Usage: ruby ch_1.rb <path to input file>' or exit unless File.file?(file)

# Read and filter input lines to those where one range fully overlaps the other
overlapping = File.read(file).chomp.split("\n")
                  .map { |line| parse_line(line) }
                  .filter { |r1, r2| overlaps?(r1, r2) }
# Print result
puts "There are #{overlapping.length} fully overlapping assignment pairs" # 827
