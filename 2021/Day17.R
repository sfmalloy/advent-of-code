library('sets')

input <- read.table("inputs/test.in")
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
        pos[[length(pos)+1]] <- pair(pos=y, step=step)
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
    while (vel > 0 && x <= max) {
        pos[[length(pos)+1]] <- pair(pos=x, step=step)
        x = x + vel
        vel = vel - 1
        step = step + 1
    }

    return(pos)
}

x_dist <- function(vel, steps) {
    dist <- (seq_sum(vel) - seq_sum(vel - steps))
    if (dist < 0) {
        return (0)
    }
    return (dist)
}

part1 <- seq_sum(abs(y_min) - 1)
part2 <- (y_max - y_min + 1) * (x_max - x_min + 1)

# for (y in :y_max) {

#     for (x in )
#     for (r in ys) {

#     }
# }

for (y_vel in (y_max+1):(abs(y_min)-1)) {
    ys = simulate_y(y_vel, y_min, y_max)
    for (x_vel in 0:x_min) {
        xs = simulate_x(x_vel, x_min, x_max)
        if (length(xs) > 0) {
            for (r in xs) {
                
            }
        }
    }
}

cat(part1,"\n")
cat(part2,"\n")
