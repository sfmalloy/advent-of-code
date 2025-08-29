<?php

function enhance_pixel($img, $alg, $row, $col, $step) {
    $idx = 0;
    $pow2 = 1;
    for ($r = $row + 1; $r >= $row - 1; --$r) {
        for ($c = $col + 1; $c >= $col - 1; --$c) {
            $idx += $pow2 * ($img[$r][$c] ?? (($step % 2 == 1 && $alg[0] == '#') ? 1 : 0));
            $pow2 *= 2;
        }
    }

    return $alg[$idx] == '#' ? 1 : 0;
}

function enhance($img, $alg, $step) {
    $enhanced = array(array());
    $rbegin = min(array_keys($img));
    $rend = max(array_keys($img));
    $cbegin = min(array_keys($img[0]));
    $cend = max(array_keys($img[0]));

    $d = 1;
    for ($r = $rbegin - $d; $r <= $rend + $d; ++$r) {
        for ($c = $cbegin - $d; $c <= $cend + $d; ++$c) {
            $enhanced[$r][$c] = enhance_pixel($img, $alg, $r, $c, $step);
        }
    }
    
    return $enhanced;
}

function print_image($img) {
    $rbegin = min(array_keys($img));
    $rend = max(array_keys($img));
    $cbegin = min(array_keys($img[0]));
    $cend = max(array_keys($img[0]));

    for ($r = $rbegin; $r <= $rend; ++$r) {
        for ($c = $cbegin; $c <= $cend; ++$c) {
            if ($img[$r][$c] == 1)
                echo "#";
            else
                echo ".";    
        }
        echo "\n";
    }
}

function get_lit_count($img) {
    $rbegin = min(array_keys($img));
    $rend = max(array_keys($img));
    $cbegin = min(array_keys($img[0]));
    $cend = max(array_keys($img[0]));

    $count = 0;
    for ($r = $rbegin; $r <= $rend; ++$r) {
        for ($c = $cbegin; $c <= $cend; ++$c) {
            if ($img[$r][$c] == 1)
                $count += 1;
        }
    }
    return $count;
}

$input = fopen("inputs/Day20.in", "r");
$alg = trim(fgets($input));
fseek($input, 1, SEEK_CUR);

$img = array(array());
$r = 0;
while (!feof($input)) {
    $row = trim(fgets($input));
    for ($c = 0; $c < strlen($row); ++$c) {
        $img[$r][$c] = $row[$c] == '#' ? 1 : 0;
    }
    ++$r;
}

$part1 = 0;
$part2 = 0;
for ($i = 0; $i < 50; ++$i) {
    $img = enhance($img, $alg, $i);
    if ($i == 1) {
        $part1 = get_lit_count($img);
    }
}

$part2 = get_lit_count($img);
printf("%d\n%d\n", $part1, $part2);

?>
