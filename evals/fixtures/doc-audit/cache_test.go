package docaudit_test

import (
	"fmt"

	"example.com/docaudit"
)

func ExampleLookup() {
	var cache docaudit.Cache
	cache.Set("name", "Ada")
	value, found := docaudit.Lookup(&cache, "name")
	fmt.Println(value, found)
	// Output: Ada true
}

func ExampleCache_Get() {
	var cache docaudit.Cache
	value, found := cache.Get("missing")
	fmt.Println(value, found)
}
