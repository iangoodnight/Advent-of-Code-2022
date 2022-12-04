#!/usr/bin/perl

=begin comment

<https://adventofcode.com/2022/day/1> "Advent of Code - Day 1"

## Part Two

By the time you calculate the answer to the Elves' question, they've already
realized that the Elf carrying the most Calories of food might eventually
**run out of snacks**.

To avoid this unacceptable situation, the Elves would instead like to know the
total Calories carried by the **top three** Elves carrying the most Calories.
That way, even if one of those Elves runs out of snacks, they still have two
backups.

In the example above, the top three Elves are the fourth Elf (with `24000`
Calories), then the third Elf (with `11000` Calories), then the fifth Elf (with
`10000` Calories). The sum of the Calories carried by these three elves is
`45000`.

Find the top three Elves carrying the most Calories.
**How many Calories are those Elves carrying in total?**

=end comment
=cut

use strict;
use warnings;
use Carp;
use English qw( -no_match_vars );
use List::Util qw ( sum );
use Term::ANSIColor;

our $VERSION = 0.0.1;

if ( !( -p STDIN ) ) {
    print color('yellow'), "Usage:\n", color('reset') or croak $ERRNO;
    print "\t\$> ", color('green'), "cat input.txt | ./ch-2.pl\n",
      color('reset')
      or croak $ERRNO;
    exit 0;
}

my $data = do { local $RS = undef; <> };

my @elves = map {
    [ split / \n /x ]    ## no critic (RegularExpressions)
} split / \n \n /x, $data;    ## no critic (RegularExpressions)

my @totals = reverse sort { $a <=> $b } map { sum @{$_}; } @elves;

my @top_3        = @totals[ 0 .. 2 ];
my $top_3_totals = sum @top_3;

print 'Top three totaled: ', color('green'), $top_3_totals, "\n", color('reset')
  or croak $ERRNO;            # 203002
