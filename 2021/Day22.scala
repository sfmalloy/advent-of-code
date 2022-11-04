import scala.collection.mutable
import scala.io.Source
import scala.math.{max, min}

object Day22 {
    class Cube(val state: Boolean, val xMin: Long, val xMax: Long, val yMin: Long, val yMax: Long, val zMin: Long, val zMax: Long) {
        private var offOverlaps: mutable.ArrayBuffer[Cube] = mutable.ArrayBuffer()

        def overlap(other: Cube): Long = {
            val dx = max(min(xMax + 1, other.xMax + 1) - max(xMin, other.xMin), 0)
            val dy = max(min(yMax + 1, other.yMax + 1) - max(yMin, other.yMin), 0)
            val dz = max(min(zMax + 1, other.zMax + 1) - max(zMin, other.zMin), 0)
            dx * dy * dz
        }

        def volume(): Long = {
            (xMax + 1 - xMin) * (yMax + 1 - yMin) * (zMax + 1 - zMin)
        }

        def addOffOverlap(other: Cube): Unit = {
            val o = overlap(other)
            if (o > 0) {
                for (cube <- offOverlaps) {
                    cube.addOffOverlap(other)
                }
                offOverlaps.addOne(new Cube(false, max(xMin, other.xMin), 
                    min(xMax, other.xMax), 
                    max(yMin, other.yMin), 
                    min(yMax, other.yMax), 
                    max(zMin, other.zMin), 
                    min(zMax, other.zMax))
                )
            }
        }

        def onCount(level: Int = 0): Long = {
            var lightsOff = 0L
            for (cube <- offOverlaps) {
                lightsOff += cube.onCount(level + 1)
            }
            volume() - lightsOff
        }

        override def toString(): String = {
            s"(${xMin} ${xMax}) (${yMin} ${yMax}) (${zMin} ${zMax})"
        }
    }

    def totalVolume(cubes: mutable.ArrayBuffer[Cube]): Long = {
        for (c <- 0 to cubes.length - 1) {
            for (p <- 0 to c - 1) {
                cubes(p).addOffOverlap(cubes(c))
            }
        }

        var on: Long = 0
        for (cube <- cubes) {
            if (cube.state) {
                on += cube.onCount()
            }
        }
        return on
    }

    def main(args: Array[String]): Unit = {
        val startTime = System.nanoTime()

        val file = Source.fromFile("./inputs/Day22.in")
        val stateRanges: mutable.ArrayBuffer[(Boolean, (Long, Long), (Long, Long), (Long, Long))] = mutable.ArrayBuffer()
        val cubes: mutable.ArrayBuffer[Cube] = mutable.ArrayBuffer()
        val smallCubes: mutable.ArrayBuffer[Cube] = mutable.ArrayBuffer()

        for (line <- file.getLines()) {
            val (stateLine, rangeLine) = line.split(" ") match { case Array(s, r) => (s, r) }
            val ((xMin, xMax), (yMin, yMax), (zMin, zMax)) = rangeLine.split(",").map((s:String) => {
                val nums = s.split("=")(1).split("\\.\\.")
                (nums(0).toLong, nums(1).toLong)
            }) match {
                case Array(xRange, yRange, zRange) => (xRange, yRange, zRange)
            }

            cubes.addOne(new Cube(stateLine.equals("on"), xMin, xMax, yMin, yMax, zMin, zMax))
            if (xMin >= -50 && xMax <= 50 && yMin >= -50 && yMax <= 50 && zMin >= -50 && zMax <= 50)
                smallCubes.addOne(new Cube(stateLine.equals("on"), xMin, xMax, yMin, yMax, zMin, zMax))
        }

        println(totalVolume(smallCubes))
        println(totalVolume(cubes))
        file.close()
        val endTime = System.nanoTime()
        printf("%.3fms\n", (endTime - startTime) / 1000000.0)
    }
}
