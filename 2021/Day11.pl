#!/usr/bin/perl

use warnings;
use strict;
use Time::HiRes qw(clock_gettime CLOCK_MONOTONIC);

use constant TRUE => 1;
use constant FALSE => 0;

sub light_flash {
    for (my $i = $_[0] - 1; $i <= $_[0] + 1; ++$i) {
        if ($i >= 0 && $i < @{$_[2]}) {
            for (my $j = $_[1] - 1; $j <= $_[1] + 1; ++$j) {
                if ($j >= 0 && $j < @{$_[2][$i]} && $_[2][$i][$j] != 0) {
                    ++$_[2][$i][$j];
                }
            }
        }
    }
}

sub inc_elems {
    for (my $i = 0; $i < @_; ++$i) {
        for (my $j = 0; $j < @{$_[$i]}; ++$j) {
            ++$_[$i][$j];
        }
    }

    my $num_flashes = 0;
    while (TRUE) {
        my $found = FALSE;
        for (my $i = 0; $i < @_; ++$i) {
            for (my $j = 0; $j < @{$_[$i]}; ++$j) {
                if ($_[$i][$j] >= 10) {
                    $_[$i][$j] = 0;
                    light_flash $i, $j, \@_;
                    $found = TRUE;
                    ++$num_flashes;
                }
            }
        }
        last if (!$found);
    }

    return $num_flashes;
}

my $start_time = clock_gettime(CLOCK_MONOTONIC);

open my $fh, '<', 'inputs/Day11.in' or die $!;
my @grid = ();
while (<$fh>) {
    chomp;
    push @grid, [split '', $_];
}
close $fh;

my $num_flashes = 0;
for (my $i = 0; $i < 100; ++$i) {
    $num_flashes += inc_elems @grid;
}

my $step = 101;
my $total_octopi = @grid * @{$grid[0]};
++$step while ((inc_elems @grid) != $total_octopi);

my $end_time = clock_gettime(CLOCK_MONOTONIC);

print "$num_flashes\n";
print "$step\n";
printf "Time: %.3fms\n", 1000 * ($end_time - $start_time);
