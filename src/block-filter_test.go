package blocks

import (
	"testing"
)

func TestFilterBlocks(t *testing.T) {
	blocks := []Block {
		Block{[]string{"fish curry", "salad", "spinach"}},
		Block{[]string{"currying", "functional", "monads"}},
		Block{[]string{"fish", "bird", "mammal"}},
	}

	if len(FilterBlocks("fish", Include, blocks)) != 2 {
		t.Fail()
	}

	if len(FilterBlocks("curry", Include, blocks)) != 2 {
		t.Fail()
	}

	if len()
}