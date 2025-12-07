package solutions

import (
	"container/list"
	"io"
	"os"
)

type Day07 struct{}

type Board struct {
	R     int
	C     int
	data  []byte
	start complex128
}

func (d Day07) Parse(file *os.File, part int) (Board, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return Board{}, err
	}
	C := 0
	start := 0
	for col, char := range data {
		if char == 'S' {
			start = col
		}
		if char == '\n' {
			C = col + 1
			break
		}
	}

	return Board{R: len(data) / C, C: C, start: complex(0.0, float64(start)), data: data}, nil
}

func (d Day07) Part1(board Board) int {
	splits := map[complex128]bool{}
	seen := map[complex128]bool{}

	q := list.New()
	q.PushBack(board.start)
	for q.Len() > 0 {
		curr := q.Back()
		q.Remove(curr)
		pos := curr.Value.(complex128)
		if seen[pos] {
			continue
		}

		elem := at(pos, board.R, board.C, board.data)
		seen[pos] = true
		switch elem {
		case 0:
			continue
		case '^':
			q.PushBack(pos + 0 + 1i)
			q.PushBack(pos + 0 - 1i)
			splits[pos] = true
		default:
			q.PushBack(pos + 1 + 0i)
		}
	}
	return len(splits)
}

type SplitNode struct {
	prevSplit complex128 // -1 == left, 1 == right
	pos       complex128
}

func (d Day07) Part2(board Board) int {
	cache := map[SplitNode]int{}
	return visit(SplitNode{pos: board.start, prevSplit: board.start}, board, cache)
}

func visit(node SplitNode, board Board, cache map[SplitNode]int) int {
	val, exists := cache[node]
	if exists {
		return val
	}
	elem := at(node.pos, board.R, board.C, board.data)
	switch elem {
	case 0:
		cache[node] = 1
	case '^':
		lhs := visit(SplitNode{pos: node.pos + 0 - 1i, prevSplit: node.pos}, board, cache)
		rhs := visit(SplitNode{pos: node.pos + 0 + 1i, prevSplit: node.pos}, board, cache)
		cache[node] = lhs + rhs
	default:
		cache[node] = visit(SplitNode{pos: node.pos + 1 + 0i, prevSplit: node.prevSplit}, board, cache)
	}
	return cache[node]
}

func at(pos complex128, R int, C int, board []byte) byte {
	r := int(real(pos))
	c := int(imag(pos))
	if r < 0 || c < 0 || r >= R || c >= C {
		return 0
	}
	return board[r*C+c]
}
