# qblok

Select blocks from program outputs, by chunking on block indents.

Many programs use some sort of indentiation for visual output usage without offering a parsing-friendly output. qblok aims to ease some of that pain

## Example

```sh
# Top-level blocks, retain any that contain "loop" - outputs the loopback block only
$> ip a | qblok -g loop

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever

# Further filter blocks to any containing 'inet' - outputs two blocks
$> ip a | qblok -g loop | qblok -i 4 -g 'inet'

    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever

# Further filter blocks to any containing '127' - outputs one block
$> ip a | qblok -g loop | qblok -i 4 -g '127'

    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever

# Further filter blocks to any not containing 'inet6' - outputs two blocks
$> ip a | qblok -g loop | qblok -i 4 -G 'inet6'

    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever

# Same as before, using a custom separator
$> ip a | qblok -g loop | qblok -i 4 -G 'inet6' -S "---"

    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
---
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
```

## Rules

* Input
    * Input is done through stdin exclusively.

* Block limits
    * By default, each line starting with the specified indent starts a new block
    * except if `--run-in` specified, un which case a run of lines with the same indent, plus sub-sections on further indents, creates a single block.

* Output
    * Ouput is simply the raw data
    * Except if `--separator` is specified in which case the separator is inserted between blocks
