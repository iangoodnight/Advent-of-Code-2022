#!/usr/bin/perl
## no critic (PodSections DotMatchAnything LineBoundaryMatching)

=begin comment

<https://adventofcode.com/2022/day/6> 'Advent of Code - Day 6'

## Part Two

Your device's communication system is correctly detecting packets, but still
isn't working. It looks like it also needs to look for **messages**.

A **start-of-message** marker is just like a start-of-packet marker, except it
consists of 14 distinct characters rather than 4.

Here are the first positions of start-of-message markers for all of the above
examples:

- `mjqjpqmgbljsphdztnvjfqwrcgsmlb`: first marker after character `19`
- `bvwbjplbgvbhsrlpgdmjqwftvncz`: first marker after character `23`
- `nppdvjthqldpwncqszvftbrmjlhg`: first marker after character `23`
- `nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg`: first marker after character `29`
- `zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw`: first marker after character `26`

**How many characters need to be processed before the first start-of-message
marker is detected?**

=end comment
=cut

use strict;
use warnings;
use Carp;
use English qw( -no_match_vars );
use Readonly;

our $VERSION = 0.0.1;

Readonly my $MARKER_LENGTH => 14;   # start-of-message marker, 14 distinct chars

# Returns 1 if all list values are unique
sub all_unique {
    my @list = @{ +shift };

    my %tmp;
    for my $char (@list) {
        if ( exists $tmp{$char} ) {    # if found duplicate, return 0
            return 0;
        }
        $tmp{$char}++;                 # else, autovivify and continue
    }
    return 1;
}

sub main {
    if ( !( -p STDIN ) ) {             # Check for input
        print "Usage:\n\$> cat input.txt | ./ch-2.pl\n" or croak $ERRNO;
        exit 0;
    }
    my $message = do { local $RS = undef; <> };    # slurp
    ## no critic (DotMatchAnything LineBoundaryMatching)
    my @characters = split qr{}, $message;         # split into list

    for my $i ( 0 .. $#characters - $MARKER_LENGTH - 1 ) {   # start cursor at 0
            # take a packet-sized slice
        my @slice = @characters[ $i .. $i + $MARKER_LENGTH - 1 ];

        if ( all_unique( \@slice ) ) {    # test for marker
            my $processed_count = $i + $MARKER_LENGTH;

            print "$processed_count characters processed\n" or croak $ERRNO;

            # 2265
            return;
        }
    }
    print "No start-of-message marker found\n" or croack $ERRNO;

    return;
}

main();
