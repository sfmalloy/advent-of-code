input <- read.table("inputs/Day17.in")
x_str <- strsplit(input[1,3], "\\.\\.|,|x|=")[[1]][3:4]
y_str <- strsplit(input[1,4], "\\.\\.|,|y|=")[[1]][3:4]

x_min <- strtoi(x_str[1])
x_max <- strtoi(x_str[2])
y_min <- strtoi(y_str[1])
y_max <- strtoi(y_str[2])

seq_sum <- function(n) {
    return ((n * (n + 1)) / 2)
}

simulate_y <- function(vel, min, max) {
    y <- 0
    step <- 0
    while (y > max) {
        y = y + vel
        vel = vel - 1
        step = step + 1
    }

    pos <- list()
    while (y >= min) {
        pos[[length(pos)+1]] <- list(pos=y, step=step)
        y = y + vel
        vel = vel - 1
        step = step + 1
    }

    return(pos)
}

simulate_x <- function(vel, min, max) {
    x <- 0
    step <- 0
    while (vel > 0 && x < min) {
        x = x + vel
        vel = vel - 1
        step = step + 1
    }

    pos <- list()
    while (vel >= 0 && x >= min && x <= max) {
        pos[[length(pos)+1]] <- list(pos=x, step=step, vel=vel)
        x = x + vel
        vel = vel - 1
        step = step + 1
    }

    return(pos)
}

part1 <- seq_sum(abs(y_min) - 1)
part2 <- (y_max - y_min + 1) * (x_max - x_min + 1)

for (y_vel in (y_min):(abs(y_min)-1)) {
    ys = simulate_y(y_vel, y_min, y_max)
    for (x_vel in 0:x_min-1) {
        xs = simulate_x(x_vel, x_min, x_max)
        for (yt in ys) {
            found <- FALSE
            for (xt in xs) {
                if (yt$step == xt$step || ((xt$step == x_vel) && (yt$step > xt$step))) {
                    part2 = part2 + 1
                    found <- TRUE
                    break
                } 
            }
            if (found)
                break
        }
    }
}

cat(part1,"\n")
cat(part2,"\n")
