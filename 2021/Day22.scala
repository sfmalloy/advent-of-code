import kotlin.ULong

import scala.collection.mutable
import scala.io.Source
import scala.math.{max, min}

object Day22 {
    class Cube(val state: Boolean, val xMin: Long, val xMax: Long, val yMin: Long, val yMax: Long, val zMin: Long, val zMax: Long, val onCount: Long = 0) {
        def overlap(other: Cube): Long = {
            val dx = max(min(xMax + 1, other.xMax + 1) - max(xMin, other.xMin), 0)
            val dy = max(min(yMax + 1, other.yMax + 1) - max(yMin, other.yMin), 0)
            val dz = max(min(zMax + 1, other.zMax + 1) - max(zMin, other.zMin), 0)
            dx * dy * dz
        }

        def volume(): Long = {
            (xMax + 1 - xMin) * (yMax + 1 - yMin) * (zMax + 1 - zMin)
        }
    }

    def main(args: Array[String]): Unit = {
        val file = Source.fromFile("inputs/test.in")
        val stateRanges: mutable.ArrayBuffer[(Boolean, (Long, Long), (Long, Long), (Long, Long))] = mutable.ArrayBuffer()
        val cubes: mutable.ArrayBuffer[Cube] = mutable.ArrayBuffer()

        for (line <- file.getLines()) {
            val (stateLine, rangeLine) = line.split(" ") match { case Array(s, r) => (s, r) }
            val (xRange, yRange, zRange) = rangeLine.split(",").map((s:String) => {
                val nums = s.split("=")(1).split("\\.\\.")
                (nums(0).toLong, nums(1).toLong)
            }) match {
                case Array(xRange, yRange, zRange) => (xRange, yRange, zRange)
            }

            stateRanges.addOne(stateLine.equals("on"), xRange, yRange, zRange)
        }

        val currentState: mutable.HashMap[(Long, Long, Long), Boolean] = mutable.HashMap()
        for ((state, (xBegin, xEnd), (yBegin, yEnd), (zBegin, zEnd)) <- stateRanges) {
            cubes.addOne(new Cube(state, xBegin, xEnd, yBegin, yEnd, zBegin, zEnd))
            for (x <- max(-50, xBegin) to min(xEnd, 50)) {
                for (y <- max(-50, yBegin) to min(yEnd, 50)) {
                    for (z <- max(-50, zBegin) to min(zEnd, 50)) {
                        currentState((x, y, z)) = state
                    }
                }
            }
        }

        var part1 = 0
        for ((_, state) <- currentState) {
            if (state) {
                part1 += 1
            }
        }
        println(part1)
        currentState.clear()
        file.close()

        var totalOn: Long = 0L
        var totalOff: Long = 0L
        // brute force to find all of the actual overlapping cubes, not just their volumes
        // then see whether they are supposed to be on or off
        for (i <- cubes.indices) {
            if (cubes(i).state) {
                var localOn = cubes(i).volume()
                for (j <- 0 until i) {
                    if (cubes(j).state)
                        localOn -= cubes(j).overlap(cubes(i))
                    else
                        localOn += cubes(j).overlap(cubes(i))
                }
                printf("On => %d\n", localOn)
                totalOn += localOn
            } else {
                var localOff = 0L
                for (j <- 0 until i) {
                    if (cubes(j).state) {
                        localOff += cubes(j).overlap(cubes(i))
                        for (k <- 0 until j) {
                            if (cubes(k).state) {
                                localOff -= cubes(k).overlap(cubes(j))
                            }
                        }
                    }
                }
                printf("Off => %d\n", localOff)
                totalOff += localOff
            }
        }
        printf("Unique cubes that have been turned on at one point: %d\n", totalOn)
        printf("Unique cubes that have been turned on at one point: %d\n", totalOff)
        // 2758514936282235
        // 2520680994726215
    }

//    def simulateRange(state: Boolean, xBegin: Int, xEnd: Int, yBegin: Int, yEnd: Int, zBegin: Int, zEnd: Int): Unit = {
//
//    }
}
