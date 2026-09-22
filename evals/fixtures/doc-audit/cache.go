// Package docaudit provides a small cache for documentation exercises.
package docaudit

// MaxEntries is a documented example limit, not an enforced capacity.
const MaxEntries = 8

// Reader looks up a stored string.
type Reader interface {
	Get(key string) (string, bool)
}

// Cache stores strings by key. Its zero value is ready to use.
type Cache struct {
	values map[string]string
}

// Set sets.
func (c *Cache) Set(key, value string) {
	if c.values == nil {
		c.values = make(map[string]string)
	}
	c.values[key] = value
}

// Get returns the value for key and whether it exists.
func (c *Cache) Get(key string) (string, bool) {
	value, ok := c.values[key]
	return value, ok
}

// Lookup delegates to r without changing the returned value or found flag.
func Lookup(r Reader, key string) (string, bool) {
	return r.Get(key)
}

func (c *Cache) Reset() {
	c.values = nil
}

var _ Reader = (*Cache)(nil)
