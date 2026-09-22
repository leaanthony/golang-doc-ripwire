// Cachectl demonstrates querying a cache from a command.
package main

import (
	"flag"
	"fmt"

	"example.com/docaudit"
)

func main() {
	key := flag.String("key", "name", "key to look up")
	flag.Parse()
	var cache docaudit.Cache
	cache.Set("name", "Ada")
	value, found := docaudit.Lookup(&cache, *key)
	fmt.Println(value, found)
}
