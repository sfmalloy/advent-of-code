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
	splits := 0
	q := list.New()
	q.PushBack(board.start)
	for q.Len() > 0 {
		curr := q.Back()
		q.Remove(curr)
		pos := curr.Value.(complex128)

		elem := at(pos, board.R, board.C, board.data)
		if elem == nil || *elem == '|' {
			continue
		}
		switch *elem {
		case '^':
			q.PushBack(pos + 0 + 1i)
			q.PushBack(pos + 0 - 1i)
			splits += 1
		default:
			q.PushBack(pos + 1 + 0i)
		}
		*elem = '|'
	}
	return splits
}

type SplitNode struct {
	prevSplit complex128
	pos       complex128
}

func (d Day07) Part2(board Board) int {
	cache := map[SplitNode]int{}
	return drop(SplitNode{pos: board.start, prevSplit: board.start}, board, cache)
}

func drop(node SplitNode, board Board, cache map[SplitNode]int) int {
	if val, exists := cache[node]; exists {
		return val
	}
	elem := at(node.pos, board.R, board.C, board.data)
	if elem == nil {
		cache[node] = 1
	} else if *elem == '^' {
		lhs := drop(SplitNode{pos: node.pos + 0 - 1i, prevSplit: node.pos}, board, cache)
		rhs := drop(SplitNode{pos: node.pos + 0 + 1i, prevSplit: node.pos}, board, cache)
		cache[node] = lhs + rhs
	} else {
		cache[node] = drop(SplitNode{pos: node.pos + 1 + 0i, prevSplit: node.prevSplit}, board, cache)
	}
	return cache[node]
}

func at(pos complex128, R int, C int, board []byte) *byte {
	r := int(real(pos))
	c := int(imag(pos))
	if r < 0 || c < 0 || r >= R || c >= C {
		return nil
	}
	return &board[r*C+c]
}
