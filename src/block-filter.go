package blocks

import "strings"

type Mode uint

const (
	Nofilter Mode = iota
	Include
	Exclude
)

type Block struct {
	lines []string
}

func (b Block) Contains(searchterm string) bool {
	for _, line := range b.lines {
		if strings.Index(line, searchterm) >= 0 {
			return true
		}
	}
	return false
}

func FilterBlocks(searchterm string, mode Mode, blocks []Block) []Block {
	if mode == Nofilter {
		return blocks
	}

	var resblocks []Block
	for _, block := range blocks {
		if mode == Include && block.Contains(searchterm) {
			resblocks = append(resblocks, block)
		} else if mode == Exclude && !block.Contains(searchterm) {
			resblocks = append(resblocks, block)
		}
	}
	return resblocks
}
