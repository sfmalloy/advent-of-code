import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Day04 {
    public static class Square {
        public int id;
        public boolean marked;

        public Square(int id) {
            this.id = id;
            this.marked = false;
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        Scanner input = new Scanner(new File("inputs/Day04.in"));

        // all possible sums
        List<Integer> nums = Arrays.asList(input.nextLine().split(",")).stream().map(Integer::parseInt).collect(Collectors.toList());
        ArrayList<Square[][]> boards = new ArrayList<>();

        input.useDelimiter("\n\n");
        while (input.hasNext()) {
            String[] lines = input.next().strip().split("\n");
            if (lines.length == 5) {
                Square[][] board = new Square[5][5];
                for (int i = 0; i < 5; ++i) {
                    List<Integer> line = Arrays.stream(lines[i].split(" ")).filter(s -> s.length() > 0).map(Integer::parseInt).collect(Collectors.toList());
                    for (int j = 0; j < 5; ++j) {
                        board[i][j] = new Square(line.get(j));
                    }
                }
                boards.add(board);
            }
        }

        HashSet<Integer> won = new HashSet<>();
        for (var key : nums) {
            int idx = 1;
            for (var board : boards) {
                // marks the key
                boolean found = false;
                for (var row : board) {
                    for (var col : row) {
                        if (col.id == key) {
                            col.marked = true;
                            found = true;
                            break;
                        }
                    }
                    if (found)
                        break;
                }

                if (found && !won.contains(idx)) {
                    // rows
                    for (int i = 0; i < 5; ++i) {
                        int marked = 0;
                        for (int j = 0; j < 5; ++j) {
                            marked += board[i][j].marked ? 1 : 0;
                        }
                        if (marked == 5)
                            won.add(idx);
                    }

                    if (won.contains(idx)) {
                        if (won.size() == 1 || won.size() == boards.size())
                            System.out.println(boardSum(board) * key);
                    }

                    if (!won.contains(idx)) {
                        // cols
                        for (int j = 0; j < 5; ++j) {
                            int marked = 0;
                            for (int i = 0; i < 5; ++i) {
                                marked += board[i][j].marked ? 1 : 0;
                            }
                            if (marked == 5)
                                won.add(idx);
                        }

                        if (won.contains(idx)) {
                            if (won.size() == 1 || won.size() == boards.size())
                                System.out.println(boardSum(board) * key);
                        }
                    }
                }
                ++idx;
            }
        }
    }

    public static int boardSum(Square[][] board) {
        int sum = 0;
        for (var row : board) {
            for (var col : row) {
                if (!col.marked)
                    sum += col.id;
            }
        }
        return sum;
    }
}
