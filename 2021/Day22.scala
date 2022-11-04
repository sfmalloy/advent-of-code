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
        val file = Source.fromFile("./inputs/Day22.in")
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
    }
}
