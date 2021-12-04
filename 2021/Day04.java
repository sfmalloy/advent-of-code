import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.time.Duration;
import java.time.Instant;
import java.util.HashSet;
import java.util.ArrayList;
import java.util.Scanner;

public class Day04 {
    public static void main(String[] args) throws FileNotFoundException {
        Instant start = Instant.now();

        Scanner input = new Scanner(new BufferedReader(new InputStreamReader(new FileInputStream("inputs/Day04.in"))));
        ArrayList<Integer> nums = new ArrayList<>();
        for (var n : input.nextLine().split(",")) {
            nums.add(Integer.parseInt(n));
        }

        ArrayList<int[][]> boards = new ArrayList<>();
        input.useDelimiter("\n\n");
        while (input.hasNext()) {
            String[] lines = input.next().strip().split("\n");
            if (lines.length == 5) {
                int[][] board = new int[5][5];
                for (int i = 0; i < 5; ++i) {
                    int j = 0;
                    for (var elem : lines[i].split(" ")) {
                        if (elem.length() > 0) {
                            board[i][j++] = Integer.parseInt(elem);
                        }
                    }

                }
                boards.add(board);
            }
        }

        int first = 0;
        int last = 0;
        HashSet<Integer> won = new HashSet<>();
        for (var key : nums) {
            int b = 1;
            for (var board : boards) {
                if (!won.contains(b)) {
                    // mark the key in the board
                    boolean found = false;
                    for (var row : board) {
                        for (int c = 0; c < 5; ++c) {
                            if (row[c] == key) {
                                row[c] *= -1;
                                found = true;
                                break;
                            }
                        }
                        if (found)
                            break;
                    }

                    // check for win if board hasn't already been won
                    if (found) {
                        for (int i = 0; i < 5; ++i) {
                            int markedRows = 0;
                            int markedCols = 0;
                            for (int j = 0; j < 5; ++j) {
                                markedRows += board[i][j] < 0 ? 1 : 0;
                                markedCols += board[j][i] < 0 ? 1 : 0;
                            }
                            if (markedRows == 5 || markedCols == 5)
                                won.add(b);
                        }

                        if (won.contains(b)) {
                            if (won.size() == 1)
                                first = boardSum(board) * key;
                            else if (won.size() == boards.size())
                                last = boardSum(board) * key;
                        }
                    }
                }
                ++b;
            }
        }
        Instant end = Instant.now();
        System.out.printf("%d\n%d\n", first, last);
        System.out.printf("Time: %f ms\n", Duration.between(start, end).toNanos() / 1000000.0);
    }

    public static int boardSum(int[][] board) {
        int sum = 0;
        for (var row : board) {
            for (var col : row) {
                if (col > 0)
                    sum += col;
            }
        }
        return sum;
    }
}
