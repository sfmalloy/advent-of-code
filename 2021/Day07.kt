import java.io.File
import kotlin.math.min
import kotlin.math.max
import kotlin.text.toULong

fun main() {
    val startTime = System.nanoTime()
    val dists: List<ULong> = File("inputs/Day07.in").bufferedReader().readLine().split(",").map { s -> s.toULong() }
    val maxPos = dists.maxOrNull()

    var part1 = ULong.MAX_VALUE
    var part2 = ULong.MAX_VALUE
    for (dist in 0UL..maxPos!!) {
        var total1 = 0UL
        var total2 = 0UL
        for (d in dists) {
            val delta = max(d, dist) - min(d, dist)
            total1 += delta
            total2 += delta * (delta + 1UL) / 2UL
        }
        part1 = min(part1, total1)
        part2 = min(part2, total2)
    }

    val endTime = System.nanoTime()

    println(part1)
    println(part2)
    println("Time %.3f ms".format((endTime - startTime) / 1e6))
}
