package blocks

func lineIndentChange(size uint, line string) int {
	// TODO
	// count spaces at start of line
	// return -1, 0, 1 for to parent, to same, to child, respectively
}

func BlocksFromStdin(indent uint) []Block {
	var all_blocks []Block

	current_block := Block{[]string{}}
	var accumulating bool

	renew := func() {
		all_blocks = append(all_blocks, current_block)
		current_block = Block{[]string{}}
	}

	for line := range stdin_lines { // TODO read line by line
		switch lineIndentChange(indent, line) {
		case 0:
			if accumulating {
				renew()
			}
			accumulating = true
		case -1:
			if accumulating {
				renew()
			}
			accumulating = false
		case 1:
			accumulating = true
		}
		if accumulating {
			current_block = append(current_block, line)
		}
	}
	renew()

	return all_blocks
}
