{-# LANGUAGE OverloadedStrings #-}

import System.IO
import Data.Text (splitOn, Text, pack, unpack)

-- Move function for part 1
move :: (Int, Int) -> (String, Int) -> (Int, Int)
move (x, y) (dir, dist)
    | dir == "down" = (x, y + dist)
    | dir == "up" = (x, y - dist)
    | dir == "forward" = (x + dist, y)

-- Move function for part 2
moveAim :: (Int, Int, Int) -> (String, Int) -> (Int, Int, Int)
moveAim (x, y, aim) (dir, dist)
    | dir == "down" = (x, y, aim + dist)
    | dir == "up" = (x, y, aim - dist)
    | dir == "forward" = (x + dist, y + (aim * dist), aim)

-- Convert string pair from input
makePair :: [Text] -> (String, Int)
makePair [dir, dist] = (unpack dir, read (unpack dist))

-- Move through all points
follow :: (Int, Int) -> [(String, Int)] -> (Int, Int)
follow = foldl move

-- Move through all points with aim
followAim :: (Int, Int, Int) -> [(String, Int)] -> (Int, Int, Int)
followAim = foldl moveAim

main :: IO()
main = do
    content <- readFile "inputs/Day02.in"
    let dirs = map (makePair . splitOn " " . pack) (lines content)
    let part1 = follow (0, 0) dirs
    let part2 = followAim (0, 0, 0) dirs
    print (uncurry (*) part1)
    print ((\ (x, y, _) -> x * y) part2)
