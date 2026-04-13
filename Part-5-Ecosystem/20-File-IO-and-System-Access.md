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

Most real-world programs interact with the filesystem. Zebra's file API focuses on safety and clarity, using the Result type to handle errors that inevitably occur (file not found, permission denied, disk full).

Key principles:
- All file operations return `Result(T, E)` for error handling
- Always check for errors—silence is not an option
- Use appropriate reading strategies for different file sizes
- Close resources properly (Zebra handles this with scoping)

---

## Reading Files

### Simple File Reading

The simplest approach: load the entire file into memory. Good for small files.

```zebra
# file: file-read-simple.zbr
# teaches: simple file reading with error handling
# chapter: 20

def main()
    var filename = "example.txt"
    
    var result = File.read(filename)
    
    branch result
        on ok(content)
            print "File contents:"
            print content
        on err(error)
            print "Error reading file: ${error}"
```

### Safe Extraction with the Result Pattern

When you're sure the file should exist, you can use unwrap methods carefully.

```zebra
# file: file-read-unwrap.zbr
# teaches: safe error handling for file reads
# chapter: 20

def main()
    var filename = "config.txt"
    
    var result = File.read(filename)
    
    # Option 1: Check then access
    if result.isOk()
        var content = result.value()  # Safe to access
        print "Read ${content.len} characters"
    else
        var error = result.error()
        print "Cannot read config: ${error}"
    
    # Option 2: Using unwrapOr with fallback
    var content = File.read(filename).unwrapOr("")
    if content.len == 0
        print "Using default configuration"
    else
        print "Configuration loaded: ${content.len} bytes"
```

### Processing Large Files: Line by Line

For files too large to fit in memory, read line-by-line.

```zebra
# file: file-read-lines.zbr
# teaches: efficient line-by-line file reading
# chapter: 20

def main()
    var filename = "large_log.txt"
    
    # Read entire file first
    var result = File.read(filename)
    
    if result.isErr()
        print "Error: ${result.error(}")
        return
    
    var content = result.value()
    var lines = content.split("\n")
    
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
            print "Line ${line_count}: ${line}"
    
    print "Total lines: ${line_count}"
    print "Errors found: ${error_count}"
```

### Counting and Analyzing Files

```zebra
# file: file-analyze.zbr
# teaches: analyzing file contents
# chapter: 20

def main()
    var filename = "document.txt"
    
    var result = File.read(filename)
    
    if result.isErr()
        print "Cannot read file"
        return
    
    var content = result.value()
    
    # Line count
    var lines = content.split("\n")
    print "Lines: ${lines.count(}")
    
    # Word count
    var word_count = 0
    for line in lines
        var words = line.split(" ")
        word_count = word_count + words.count()
    print "Words: ${word_count}"
    
    # Character count
    print "Characters: ${content.len}"
    
    # Find longest line
    var longest_line = ""
    for line in lines
        if line.len > longest_line.len
            longest_line = line
    
    print "Longest line (${longest_line.len} chars: ${longest_line.substring(0, 50)}")
```

---

## Writing Files

### Simple File Writing

Write content to a file, overwriting if it exists.

```zebra
# file: file-write-simple.zbr
# teaches: basic file writing
# chapter: 20

def main()
    var content = "Hello, File!\nLine 2\nLine 3\n"
    var filename = "output.txt"
    
    var result = File.write(filename, content)
    
    if result.isOk()
        print "File written successfully"
    else
        print "Error: ${result.error(}")
```

### Building Content Then Writing

Don't write to a file in a loop. Build the content first, then write once.

```zebra
# file: file-write-building.zbr
# teaches: efficiently building and writing file content
# chapter: 20

def main()
    # Build content in memory
    var lines = List()
    
    # Generate report
    lines.add("Sales Report")
    lines.add("=" + "=" + "=" + "=" + "=" + "=")
    lines.add("")
    
    var items = List()
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
    var result = File.write("report.txt", content)
    
    if result.isOk()
        print "Report written to report.txt"
```

### Appending to Files

```zebra
# file: file-append.zbr
# teaches: appending content to existing files
# chapter: 20

def main()
    var filename = "log.txt"
    
    # Read existing content
    var existing = File.read(filename).unwrapOr("")
    
    # Append new content
    var timestamp = "2025-03-15 14:30:00"
    var message = "Application started"
    
    var new_content = existing + timestamp + " - " + message + "\n"
    
    var result = File.write(filename, new_content)
    
    if result.isOk()
        print "Log entry added"
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
    var files = List()
    files.add("data1.txt")
    files.add("data2.txt")
    files.add("data3.txt")
    
    var results = HashMap()
    
    for filename in files
        print "Processing ${filename}... "
        var content_result = File.read(filename)
        
        if content_result.isErr()
            print "FAILED: ${content_result.error(}")
            results.set(filename, 0)
            continue
        
        var content = content_result.value()
        var line_count = content.split("\n").count()
        
        results.set(filename, line_count)
        print "OK (${line_count} lines")
    
    # Summary
    print "\nSummary:"
    var total = 0
    for filename in results.keys()
        var count = results.get(filename)
        if count != nil
            total = total + count
            print "${filename}: ${count} lines"
    
    print "Total: ${total} lines"
```

### Converting and Reformatting Files

```zebra
# file: file-convert.zbr
# teaches: reading one format and writing another
# chapter: 20

def main()
    # Read CSV
    var csv_result = File.read("data.csv")
    
    if csv_result.isErr()
        print "Error reading CSV"
        return
    
    var csv_content = csv_result.value()
    var lines = csv_content.split("\n")
    
    # Convert to tab-separated
    var output_lines = List()
    
    for line in lines
        var fields = line.split(",")
        var tab_separated = fields.join("\t")
        output_lines.add(tab_separated)
    
    var output = output_lines.join("\n")
    
    # Write TSV
    var write_result = File.write("data.tsv", output)
    
    if write_result.isOk()
        print "Conversion complete: data.tsv"
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
        print "Configuration file found"
        var content = File.read(config_file)
        # Process config
    else
        print "No configuration file. Using defaults."
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
        var result = File.delete(temp_file)
        
        if result.isOk()
            print "Temporary file deleted"
        else
            print "Error deleting file: ${result.error(}")
    else
        print "File doesn't exist"
```

### Working with Paths

```zebra
# file: file-paths.zbr
# teaches: path operations and directory access
# chapter: 20

def main()
    var cwd = sys.cwd()
    print "Current directory: ${cwd}"
    
    # Build path (simple string concatenation)
    var data_dir = cwd + "/data"
    var file_path = data_dir + "/input.txt"
    print "Full path: ${file_path}"
    
    # Extract filename from path
    var path = "/home/user/documents/report.txt"
    var filename = path.substring(path.lastIndexOf("/") + 1, path.len)
    print "Filename: ${filename}"
    
    # Extract directory from path
    var last_slash = path.lastIndexOf("/")
    if last_slash > 0
        var directory = path.substring(0, last_slash)
        print "Directory: ${directory}"
```

---

## Practical Patterns: Config File Management

```zebra
# file: file-config-management.zbr
# teaches: loading and parsing configuration files
# chapter: 20

class Config
    var host as str = "localhost"
    var port as int = 8080
    var debug as bool = false
    
    shared
        def from_file(filename as str) as Config throws
            var content_result = File.read(filename)
            
            if content_result.isErr()
                raise "Cannot read config file: ${content_result.error(}")
            
            var content = content_result.value()
            var config = Config()
            var lines = content.split("\n")
            
            for line in lines
                line = line.trim()
                
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
                elif key == "port"
                    var port_val = value.toInt()
                    if port_val != nil
                        config.port = port_val
                elif key == "debug"
                    config.debug = value.lower() == "true"
            
            return config

def main()
    var result = Config.from_file("app.conf")
    
    if result.isErr()
        print "Error: ${result.error(}")
        return
    
    var config = result.value()
    print "Server: ${config.host}:${config.port}"
    print "Debug: ${config.debug}"
```

---

## Practical Patterns: Log File Generation

```zebra
# file: file-logging.zbr
# teaches: generating timestamped log files
# chapter: 20

class Logger
    var filename as str
    var entries as List(str)
    
    def init(filename as str)
        this.filename = filename
        this.entries = List()
    
    def log(message as str)
        var timestamp = get_timestamp()
        var entry = "${timestamp} [INFO] ${message}"
        this.entries.add(entry)
        print entry
    
    def error(message as str)
        var timestamp = get_timestamp()
        var entry = "${timestamp} [ERROR] ${message}"
        this.entries.add(entry)
        print entry
    
    def save() as bool
        var content = entries.join("\n")
        var result = File.write(filename, content)
        return result.isOk()

def get_timestamp() as str
    # Placeholder—in real code, use actual time
    return "2025-03-15 14:30:00"

def main()
    var logger = Logger("app.log")
    
    logger.log("Application started")
    logger.log("Configuration loaded")
    logger.error("Failed to connect to database")
    logger.log("Retrying connection...")
    logger.log("Connection successful")
    
    if logger.save()
        print "Log saved to ${logger.filename}"
    else
        print "Failed to save log"
```

---

## Practical Patterns: Data Import/Export

```zebra
# file: file-data-import.zbr
# teaches: importing and exporting structured data
# chapter: 20

class Person
    var name as str
    var age as int
    var email as str
    
    shared
        def from_csv_line(line as str) as Person?
            var parts = line.split(",")
            if parts.count() != 3
                return nil
            
            var age_val = parts.at(1).trim().toInt()
            if age_val == nil
                return nil
            
            var person = Person()
            person.name = parts.at(0).trim()
            person.age = age_val
            person.email = parts.at(2).trim()
            return person
        
        def load_from_csv(filename as str) as List(Person) throws
            var content_result = File.read(filename)
            
            if content_result.isErr()
                raise content_result.error()
            
            var content = content_result.value()
            var people = List()
            var lines = content.split("\n")
            
            for line in lines
                if line.trim().len == 0
                    continue
                
                var person = from_csv_line(line)
                if person != nil
                    people.add(person)
            
            return people
    
    def to_csv_line() as str
        return "${name},${age},${email}"

def main()
    # Load data
    var result = Person.load_from_csv("people.csv")
    
    if result.isErr()
        print "Error: ${result.error(}")
        return
    
    var people = result.value()
    print "Loaded ${people.count(} people")
    
    # Filter and export
    var adults = List()
    for person in people
        if person.age >= 18
            adults.add(person)
    
    # Save filtered data
    var output_lines = List()
    for person in adults
        output_lines.add(person.to_csv_line())
    
    var csv_output = output_lines.join("\n")
    var write_result = File.write("adults.csv", csv_output)
    
    if write_result.isOk()
        print "Exported ${adults.count(} adults to adults.csv")
```

---

## Key Takeaways

1. **Always Handle Errors** — File operations fail. Use Result types and check them.

2. **Think About Scale** — Small files? Load all at once. Large files? Process line-by-line.

3. **Build First, Write Once** — Never write in a loop. Build your content, then write it all at once.

4. **Close Files Properly** — Zebra's scoping ensures this, but be aware of resource management.

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
