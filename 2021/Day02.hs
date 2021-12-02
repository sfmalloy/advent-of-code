{-# LANGUAGE OverloadedStrings #-}

import Text.Printf
import System.IO
import Data.Text (splitOn, Text, pack, unpack)

move :: (Int, Int) -> (String, Int) -> (Int, Int)
move (x, y) (dir, dist)
    | dir == "down" = (x, y + dist)
    | dir == "up" = (x, y - dist)
    | dir == "forward" = (x + dist, y)

moveAim :: (Int, Int, Int) -> (String, Int) -> (Int, Int, Int)
moveAim (x, y, aim) (dir, dist)
    | dir == "down" = (x, y, aim + dist)
    | dir == "up" = (x, y, aim - dist)
    | dir == "forward" = (x + dist, y + (aim * dist), aim)

makePair :: [Text] -> (String, Int)
makePair [dir, dist] = (unpack dir, read (unpack dist))

follow :: (Int, Int) -> [(String, Int)] -> (Int, Int)
follow = foldl move

followAim :: (Int, Int, Int) -> [(String, Int)] -> (Int, Int, Int)
followAim = foldl moveAim

main :: IO()
main = do
    content <- readFile "inputs/Day02.in"
    let lst = lines content
    let splitLines = map (splitOn " " . pack) lst
    let dirs = map makePair splitLines
    let part1 = follow (0, 0) dirs
    let part2 = followAim (0, 0, 0) dirs
    print (uncurry (*) part1)
    print ((\ (x,y,_) -> x * y) part2)
