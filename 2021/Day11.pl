#!/usr/bin/perl

use warnings;
use strict;
use Time::HiRes qw(clock_gettime CLOCK_MONOTONIC);

use constant TRUE => 1;
use constant FALSE => 0;

sub light_flash {
    my @grid = @{$_[2]};
    for (my $i = $_[0] - 1; $i <= $_[0] + 1; ++$i) {
        if ($i >= 0 && $i < scalar @grid) {
            for (my $j = $_[1] - 1; $j <= $_[1] + 1; ++$j) {
                if ($j >= 0 && $j < scalar @{$grid[$i]} && $grid[$i][$j] != 0) {
                    ++$grid[$i][$j];
                }
            }
        }
    }
}

# Increment elements of given 2d array by 1
sub inc_elems {
    my $num_flash = 0;
    # Initial pass
    for (my $i = 0; $i < scalar @_; ++$i) {
        for (my $j = 0; $j < scalar @{$_[$i]}; ++$j) {
            ++$_[$i][$j];
        }
    }

    while (TRUE) {
        my $found = FALSE;
        for (my $i = 0; $i < scalar @_; ++$i) {
            for (my $j = 0; $j < scalar @{$_[$i]}; ++$j) {
                if ($_[$i][$j] >= 10) {
                    $_[$i][$j] = 0;
                    light_flash $i, $j, \@_;
                    $found = TRUE;
                    ++$num_flash;
                }
            }
        }
        last if (!$found);
    }

    return $num_flash;
}

my $start_time = clock_gettime(CLOCK_MONOTONIC);

open my $fh, '<', 'inputs/Day11.in' or die $!;
my @grid = ();
while (<$fh>) {
    chomp $_;
    my @row = split '', $_;
    push @grid, \@row;
}
close($fh);

my $num_flashes = 0;
for (my $i = 0; $i < 100; ++$i) {
    $num_flashes += inc_elems @grid;
}

my $step = 101;
my $num_rows = scalar @grid;
my $num_cols = scalar @{$grid[0]};
my $total_octopi = $num_rows * $num_cols;

while ((inc_elems @grid) != $total_octopi) {
    ++$step;
}

my $end_time = clock_gettime(CLOCK_MONOTONIC);

print "$num_flashes\n";
print "$step\n";
printf "Time: %.3fms\n", 1000 * ($end_time - $start_time);
