# Chapter 20: File I/O and System Access

**Time:** 90 min | **Audience:** Intermediate | **Prerequisites:** Chapters 06, 12

---

## Learning Outcomes

After this chapter, you will:
- Read and write text files safely
- Handle file operation errors gracefully
- Process files line-by-line for memory efficiency
- Work with directories and path operations
- Access environment variables and command-line arguments
- Build file-based utilities and tools

---

## Overview: Reading and Writing Files

Most real-world programs interact with the filesystem. Zebra's file API is a set of plain
static calls on `File` and `Dir` — `File.read(path)` returns a `str` directly, not a
`Result` or an error union. There is no `.isOk()` / `.isErr()` / `.unwrapOr()` / `.value()`
/ `.error()` family in the language.

That has a real consequence: **`File.read` and `File.write` are not `throws`.** If the
file doesn't exist (or can't be read for some other reason), `File.read` panics the
process — there's no `catch` clause and no `?` that can intercept it, because both of
those only work on an error union, and `File.read`'s return type is a bare `str`.

Key principles:
- `File.read` / `File.write` / `File.readLines` / `File.append` return plain values, not
  a Result — check `File.exists(path)` **before** you call them if the file might be
  missing, since there's no error to catch afterward.
- If you want the `raise` / `catch` / `?` idiom from Chapter 12, wrap the file call in
  your own `throws` function — see "Safe Reading With Your Own throws Wrapper" below.
- Use appropriate reading strategies for different file sizes.
- There's no separate "close" step in this API — `File.read`/`File.write` are one-shot
  calls, not a handle you open and close.

---

## Reading Files

### Simple File Reading

The simplest approach: load the entire file into memory. Good for small files.
`File.read` returns the content directly — no wrapper type to unwrap:

```zebra
# file: file-read-simple.zbr
# teaches: simple file reading
# chapter: 20

def main()
    var filename = "example.txt"

    if File.exists(filename)
        var content = File.read(filename)
        print("File contents:")
        print(content)
    else
        print("Error reading file: not found")
```

### Safe Reading With Your Own `throws` Wrapper

`File.read` itself can't be `catch`-ed or `?`-propagated — it isn't `throws`. If you want
that idiom (from Chapter 12), write a small wrapper that checks first and raises:

```zebra
# file: file-read-unwrap.zbr
# teaches: wrapping File.read in a throws function for catch/? handling
# chapter: 20

def readOrThrow(path: str): str throws
    if not File.exists(path)
        raise "cannot read ${path}: not found"
    return File.read(path)

def main()
    var filename = "config.txt"

    # Option 1: catch with a fallback value
    var content = readOrThrow(filename) catch ""
    if content.len == 0
        print("Using default configuration")
    else
        print("Configuration loaded: ${content.len} bytes")

    # Option 2: method-level catch, printing the error
    var loaded = readOrThrow(filename)
    print("Read ${loaded.len} characters")
catch |e|
    print("Cannot read config: ${e.message}")
```

### Processing Large Files: Line by Line

For files too large to fit in memory as one string, use `File.readLines`, which splits
the file the same way `str.lines()` does — no trailing empty entry after a final `\n`.

```zebra
# file: file-read-lines.zbr
# teaches: efficient line-by-line file reading
# chapter: 20

def main()
    var filename = "large_log.txt"

    if not File.exists(filename)
        print("Error: large_log.txt not found")
        return

    var lines = File.readLines(filename)

    # Process line by line
    var line_count = 0
    var error_count = 0

    for line in lines
        line_count = line_count + 1

        # Skip empty lines
        if line.trim().len == 0
            continue

        # Check for errors (assuming "ERROR" in log means error line)
        if line.contains("ERROR")
            error_count = error_count + 1
            print("Line ${line_count}: ${line}")

    print("Total lines: ${line_count}")
    print("Errors found: ${error_count}")
```

### Counting and Analyzing Files

```zebra
# file: file-analyze.zbr
# teaches: analyzing file contents
# chapter: 20

def main()
    var filename = "document.txt"

    if not File.exists(filename)
        print("Cannot read file")
        return

    var content = File.read(filename)

    # Line count
    var lines = content.split("\n")
    print("Lines: ${lines.count()}")

    # Word count
    var word_count = 0
    for line in lines
        var words = line.split(" ")
        word_count = word_count + words.count()
    print("Words: ${word_count}")

    # Character count
    print("Characters: ${content.len}")

    # Find longest line
    var longest_line = ""
    for line in lines
        if line.len > longest_line.len
            longest_line = line

    print("Longest line (${longest_line.len} chars): ${longest_line.substring(0, 50)}")
```

---

## Writing Files

### Simple File Writing

Write content to a file, overwriting if it exists. `File.write` returns `void` — there's
nothing to check, the call either succeeds or panics on a real I/O failure (e.g. the
directory doesn't exist):

```zebra
# file: file-write-simple.zbr
# teaches: basic file writing
# chapter: 20

def main()
    var content = "Hello, File!\nLine 2\nLine 3\n"
    var filename = "output.txt"

    File.write(filename, content)
    print("File written successfully")
```

### Building Content Then Writing

Don't write to a file in a loop. Build the content first, then write once.

```zebra
# file: file-write-building.zbr
# teaches: efficiently building and writing file content
# chapter: 20

def main()
    # Build content in memory
    var lines = List(str)()
    
    # Generate report
    lines.add("Sales Report")
    lines.add("=" + "=" + "=" + "=" + "=" + "=")
    lines.add("")
    
    var items = List(str)()
    items.add("Product A")
    items.add("Product B")
    items.add("Product C")
    
    for item in items
        lines.add("- ${item}: $100")
    
    lines.add("")
    lines.add("Total: $300")
    
    # Join with newlines
    var content = lines.join("\n")
    
    # Write once
    File.write("report.txt", content)
    print("Report written to report.txt")
```

### Appending to Files

`File.append(path, data)` appends without you needing to re-read and re-write the whole
file. Use it directly rather than the read-concatenate-write dance:

```zebra
# file: file-append.zbr
# teaches: appending content to existing files
# chapter: 20

def main()
    var filename = "log.txt"

    # Append new content — creates the file if it doesn't exist yet
    var timestamp = "2025-03-15 14:30:00"
    var message = "Application started"

    File.append(filename, "${timestamp} - ${message}\n")
    print("Log entry added")
```

---

## Working with Multiple Files

### Batch Processing

```zebra
# file: file-batch-process.zbr
# teaches: processing multiple files
# chapter: 20

def main()
    # List of files to process
    var files: List(str) = ["data1.txt", "data2.txt", "data3.txt"]

    var results = HashMap(str, int)()

    for filename in files
        print("Processing ${filename}... ")

        if not File.exists(filename)
            print("FAILED: not found")
            results.set(filename, 0)
            continue

        var content = File.read(filename)
        var line_count = content.split("\n").count()

        results.set(filename, line_count)
        print("OK (${line_count} lines)")

    # Summary
    print("\nSummary:")
    var total = 0
    for filename, count in results
        total = total + count
        print("${filename}: ${count} lines")

    print("Total: ${total} lines")
```

### Converting and Reformatting Files

```zebra
# file: file-convert.zbr
# teaches: reading one format and writing another
# chapter: 20

def main()
    # Read CSV
    if not File.exists("data.csv")
        print("Error reading CSV")
        return

    var csv_content = File.read("data.csv")
    var lines = csv_content.split("\n")

    # Convert to tab-separated
    var output_lines: List(str) = []

    for line in lines
        var fields = line.split(",")
        var tab_separated = fields.join("\t")
        output_lines.add(tab_separated)

    var output = output_lines.join("\n")

    # Write TSV
    File.write("data.tsv", output)
    print("Conversion complete: data.tsv")
```

---

## File and Directory Information

### Checking File Existence

```zebra
# file: file-exists.zbr
# teaches: checking if files exist
# chapter: 20

def main()
    var config_file = "config.ini"
    
    if File.exists(config_file)
        print("Configuration file found")
        var content = File.read(config_file)
        # Process config
    else
        print("No configuration file. Using defaults.")
        # Use defaults
```

### File Deletion

```zebra
# file: file-delete.zbr
# teaches: safely deleting files
# chapter: 20

def main()
    var temp_file = "temp.txt"

    if File.exists(temp_file)
        File.delete(temp_file)
        print("Temporary file deleted")
    else
        print("File doesn't exist")
```

`File.delete` is a no-op if the file is already missing, so the `File.exists` check above
is purely to control the print message — you don't need it to avoid a panic here, unlike
`File.read`.

### Working with Paths

```zebra
# file: file-paths.zbr
# teaches: path operations and directory access
# chapter: 20

def main()
    # NOTE: annotate the type here — an un-annotated `var cwd = sys.cwd()` currently
    # prints as a raw byte array instead of text when interpolated (a codegen bug in
    # today's compiler); `var cwd: str = sys.cwd()` sidesteps it.
    var cwd: str = sys.cwd()
    print("Current directory: ${cwd}")
    
    # Build path (simple string concatenation)
    var data_dir = cwd + "/data"
    var file_path = data_dir + "/input.txt"
    print("Full path: ${file_path}")
    
    # Extract filename from path
    var path = "/home/user/documents/report.txt"
    var filename = path.substring(path.lastIndexOf("/") + 1, path.len)
    print("Filename: ${filename}")
    
    # Extract directory from path
    var last_slash = path.lastIndexOf("/")
    if last_slash > 0
        var directory = path.substring(0, last_slash)
        print("Directory: ${directory}")
```

---

## Network I/O

Network sockets are a natural extension of file I/O — same idea
("read/write a byte stream"), different transport. Zebra's stdlib covers
four protocols: TCP, UDP, WebSocket, and HTTP.

### TCP

```zebra
# Client:
def main()
    var conn = Tcp.connect("example.com", 80)
    conn.send("GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")
    var response = conn.recv(4096)
    print(response)
    conn.close()

# Server:
def main()
    Tcp.serve(8080, def(conn)
        var msg = conn.recv(1024)
        conn.send("echo: ${msg}")
        conn.close()
    )
```

| Call | Notes |
|---|---|
| `Tcp.connect(host, port)` | Client: open a connection; returns a `TcpConn` |
| `Tcp.serve(port, handler)` | Server: accept connections; calls `handler(conn)` for each |
| `conn.send(data)` / `conn.recv(n)` / `conn.close()` | I/O primitives on a connection |

### UDP

```zebra
def main()
    var sock = Udp.bind(9000)                  # listen
    var msg = sock.recv(1024)                  # blocks; returns the datagram bytes
    print("received: ${msg}")
    sock.send("alice.example.com", 9001, "ack")
    sock.close()
```

| Call | Notes |
|---|---|
| `Udp.bind(port)` | Server: bind a local port |
| `Udp.socket()` | Client: ephemeral socket for outbound sends |
| `sock.send(host, port, data)` | Send a datagram |
| `sock.recv(n)` | Receive a datagram; returns the data as `str` (**not** a `(data, sender_addr)` tuple — the sender's address isn't exposed by `recv` itself) |

UDP is fire-and-forget; there's no connection state, no ordering, and
no retransmission. Use it for telemetry, game state updates, DNS — and
not for anything that needs delivery guarantees.

### WebSocket

```zebra
# Client:
def main()
    var ws = Ws.connect("wss://echo.example.com/")
    ws.send("hello")
    var reply = ws.recv()
    if reply as msg
        print(msg)
    ws.close()

# Server:
def main()
    Ws.serve(8081, def(conn)
        var msg: str? = conn.recv()
        if msg as m
            conn.send("echo: ${m}")
        conn.close()
    )
```

| Call | Notes |
|---|---|
| `Ws.connect(url)` | Client: `ws://` or `wss://` (TLS); returns a `WsConn` |
| `Ws.serve(port, handler)` | Server: accept WebSocket connections |
| `conn.send(text)` | Send a text frame |
| `conn.recv()` | Receive a text frame; returns `str?` (nil if closed) |
| `conn.close()` | Send a close frame and shut down |

TLS is automatic when the URL scheme is `wss://`; the runtime negotiates
with the system's certificate store.

### HTTP

For HTTP-specific code there's a dedicated `Http` module covering both
client and server with the right request/response abstractions:

```zebra
# Server with route handler:
def main()
    Http.serve(8080, def(req: HttpRequest, res: HttpResponse)
        if req.path == "/health"
            res.status = 200
            res.body = "ok"
        else
            res.status = 404
            res.body = "not found"
    )
```

For a typical small server (under 1000 RPS) the server primitives are
sufficient. For high-traffic services or HTTP/2 / HTTP/3, drop into the
underlying Zig modules via `zig"..."` — see Chapter 22.

---

## Practical Patterns: Config File Management

```zebra
# file: file-config-management.zbr
# teaches: loading and parsing configuration files
# chapter: 20

class Config
    var host: str = "localhost"
    var port: int = 8080
    var debug: bool = false
    
    static
        def from_file(filename: str): Config throws
            if not File.exists(filename)
                raise "Cannot read config file: ${filename} not found"

            var content = File.read(filename)
            var config = Config()
            var lines = content.split("\n")
            
            for raw_line in lines
                var line = raw_line.trim()
                
                # Skip empty lines and comments
                if line.len == 0 or line.startsWith("#")
                    continue
                
                # Parse key=value
                if not line.contains("=")
                    continue
                
                var parts = line.split("=")
                if parts.count() != 2
                    continue
                
                var key = parts.at(0).trim()
                var value = parts.at(1).trim()
                
                # Set config values
                if key == "host"
                    config.host = value
                else if key == "port"
                    if value.tryInt() as port_val
                        config.port = port_val
                else if key == "debug"
                    config.debug = value.lower() == "true"
            
            return config

def main()
    var config = Config.from_file("app.conf")
    print("Server: ${config.host}:${config.port}")
    print("Debug: ${config.debug}")
catch |e|
    print("Error: ${e.message}")
```

---

## Practical Patterns: Log File Generation

```zebra
# file: file-logging.zbr
# teaches: generating timestamped log files
# chapter: 20

class Logger
    var filename: str
    var entries: List(str)
    
    cue init(filename: str)
        .filename = filename
        .entries = List(str)()
    
    def log(message: str)
        var timestamp = get_timestamp()
        var entry = "${timestamp} [INFO] ${message}"
        .entries.add(entry)
        print(entry)
    
    def error(message: str)
        var timestamp = get_timestamp()
        var entry = "${timestamp} [ERROR] ${message}"
        .entries.add(entry)
        print(entry)
    
    def save()
        var content = .entries.join("\n")
        File.write(.filename, content)

def get_timestamp(): str
    # Placeholder—in real code, use actual time
    return "2025-03-15 14:30:00"

def main()
    var logger = Logger("app.log")
    
    logger.log("Application started")
    logger.log("Configuration loaded")
    logger.error("Failed to connect to database")
    logger.log("Retrying connection...")
    logger.log("Connection successful")
    
    logger.save()
    print("Log saved to ${logger.filename}")
```

`save()` has no way to report failure back to the caller — `File.write` doesn't return a
success flag, it either writes or panics the process (permissions, a missing parent
directory, disk full). If you need a save that can fail gracefully, give it a `throws`
signature and check `Dir.exists` on the parent directory yourself before writing.

---

## Practical Patterns: Data Import/Export

```zebra
# file: file-data-import.zbr
# teaches: importing and exporting structured data
# chapter: 20

class Person
    var name: str
    var age: int
    var email: str
    
    static
        def from_csv_line(line: str): Person?
            var parts = line.split(",")
            if parts.count() != 3
                return nil
            
            var age_val = parts.at(1).trim().tryInt()
            if age_val == nil
                return nil
            
            var person = Person()
            person.name = parts.at(0).trim()
            person.age = age_val!
            person.email = parts.at(2).trim()
            return person
        
        def load_from_csv(filename: str): List(Person) throws
            if not File.exists(filename)
                raise "cannot read ${filename}: not found"

            var content = File.read(filename)
            var people: List(Person) = []
            var lines = content.split("\n")
            
            for line in lines
                if line.trim().len == 0
                    continue
                
                if from_csv_line(line) as person
                    people.add(person)
            
            return people
    
    def to_csv_line(): str
        return "${.name},${.age},${.email}"

def main()
    # Load data
    var people = Person.load_from_csv("people.csv")
    print("Loaded ${people.count()} people")
    
    # Filter and export
    var adults: List(Person) = []
    for person in people
        if person.age >= 18
            adults.add(person)
    
    # Save filtered data
    var output_lines: List(str) = []
    for person in adults
        output_lines.add(person.to_csv_line())
    
    var csv_output = output_lines.join("\n")
    File.write("adults.csv", csv_output)
    print("Exported ${adults.count()} adults to adults.csv")
catch |e|
    print("Error: ${e.message}")
```

---

## Key Takeaways

1. **Always Handle Errors** — `File.read`/`File.write` aren't `throws`; a missing file
   panics. Check `File.exists` first, or wrap the call in your own `throws` function if
   you want `catch`/`?` handling.

2. **Think About Scale** — Small files? Load all at once. Large files? Process line-by-line.

3. **Build First, Write Once** — Never write in a loop. Build your content, then write it all at once.

4. **No Handles to Manage** — `File.read`/`File.write`/`File.append` are one-shot calls,
   not an open-handle API, so there's no separate close step to forget.

5. **Paths Are Strings** — Treat filesystem paths carefully. Consider cross-platform separators.

---

## Exercises

1. **Word Count Tool** — Read a file, count words, lines, characters. Report summary.
2. **Log Analyzer** — Read a log file, count errors/warnings, extract timestamps.
3. **CSV Merger** — Read two CSV files, merge them, remove duplicates, write result.
4. **Configuration Validator** — Load config file, validate required fields are present, report errors.
5. **Backup Tool** — Read all .txt files in a directory, copy to backup directory with timestamp.

---

## What's Next

Now that you can read and write files reliably, Chapter 21 explores regular expressions—a powerful tool for finding patterns within those files.
