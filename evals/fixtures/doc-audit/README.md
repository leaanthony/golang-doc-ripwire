# Cache

The library exposes `Cache` and `Lookup`; `cmd/cachectl` builds the cachectl command.

`MaxEntries = 99`.

See `missing.go:12` for the implementation.

`Cache` is safe for concurrent reads and writes.

The command's `-key` flag defaults to `user`.

Both examples run under `go test` and verify their output.

```go
value := RemovedLookup("name")
fmt.Println(value)
```
