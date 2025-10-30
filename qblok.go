package main

import (
	"fmt"
	"os"

	blocks "qblok/src"

	"github.com/taikedz/goargs/goargs"
)

type Options struct {
	indent  uint
	pattern string
	mode    blocks.Mode
}

func fail(code int, message string, tokens ...any) {
	fmt.Printf("%s\n", fmt.Sprintf(message, tokens...))
	os.Exit(code)
}

func failIf(err error, code int, message string, tokens ...any) {
	if err != nil {
		fmt.Printf("%v\n", err)
		fail(code, message, tokens...)
	}
}

func parseArgs() Options {
	var options Options
	parser := goargs.NewParser("qblok - query by indent blocks")
	parser.UintVar(&options.indent, "indent", 0, "Block indent level")
	ipat := parser.String("grep-include", "", "Inclusion pattern")
	epat := parser.String("grep-exclude", "", "Exclusion pattern")

	parser.SetShortFlag('g', "grep-include")
	parser.SetShortFlag('G', "grep-exclude")
	parser.SetShortFlag('i', "indent")

	err := parser.ParseCliArgs()
	failIf(err, 1, "CLI args parse failure")

	if len(*ipat) > 0 && len(*epat) > 0 {
		fail(1, "Both inclusion and exclusion patterns have been set - please use only one.")
	}
	if len(*ipat) > 0 {
		options.pattern = *ipat
		options.mode = blocks.Include
	} else if len(*epat) > 0 {
		options.pattern = *epat
		options.mode = blocks.Exclude
	}

	return options
}

func main() {
	args := parseArgs()
}
