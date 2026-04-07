.PHONY: all extract lint validate html pdf build-all clean help quick

# ============================================================================
# Zebra Programming Book - Comprehensive Build System
# ============================================================================

# Directories
EXAMPLES_DIR := examples
DOCS_DIR := docs
OUTPUT_DIR := build

# Tools
PYTHON := python3
ZEBRA := zebra
PANDOC := pandoc

# Files
BUILD_SCRIPTS := extract-examples.py validate-examples.py lint-chapters.py build-html.py

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# ============================================================================
# DEFAULT TARGETS
# ============================================================================

.DEFAULT_GOAL := help

# ============================================================================
# MAIN TARGETS
# ============================================================================

all: extract lint validate html pdf
	@echo "$(GREEN)✅ Complete build successful!$(NC)"
	@echo ""
	@echo "Generated:"
	@echo "  - $(DOCS_DIR)/index.html (HTML documentation)"
	@echo "  - $(OUTPUT_DIR)/zebra-programming-book.pdf (PDF book)"
	@echo "  - $(EXAMPLES_DIR)/ (Extracted code examples)"
	@echo ""
	@echo "Reports:"
	@echo "  - lint-report.txt"
	@echo "  - validation-report.json"

quick: extract validate
	@echo "$(GREEN)✅ Quick build complete!$(NC)"
	@echo ""
	@echo "Examples extracted and validated."
	@echo "Run 'make html' or 'make pdf' to generate documentation."

# ============================================================================
# BUILD STEPS
# ============================================================================

extract: check-python
	@echo "$(BLUE)📚 Extracting code examples from chapters...$(NC)"
	@$(PYTHON) extract-examples.py
	@echo ""

lint: check-python extract
	@echo "$(BLUE)✏️  Linting chapters for consistency...$(NC)"
	@$(PYTHON) lint-chapters.py
	@echo ""

validate: check-python extract
	@echo "$(BLUE)🧪 Validating all examples compile...$(NC)"
	@$(PYTHON) validate-examples.py
	@echo ""

html: check-python extract
	@echo "$(BLUE)🌐 Building HTML documentation...$(NC)"
	@mkdir -p $(DOCS_DIR)
	@$(PYTHON) build-html.py
	@echo "$(GREEN)✅ HTML ready: $(DOCS_DIR)/index.html$(NC)"
	@echo ""

pdf: check-pandoc extract
	@echo "$(BLUE)📖 Building PDF book...$(NC)"
	@mkdir -p $(OUTPUT_DIR)
	@echo "Converting markdown to PDF (this may take a minute)..."
	@bash build-pdf.sh 2>/dev/null || (echo "$(RED)Note: build-pdf.sh failed, try Windows batch file if on Windows$(NC)")
	@echo ""

# ============================================================================
# UTILITY TARGETS
# ============================================================================

check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { \
		echo "$(RED)❌ Python 3 not found. Install Python first.$(NC)"; \
		exit 1; \
	}

check-pandoc:
	@command -v $(PANDOC) >/dev/null 2>&1 || { \
		echo "$(RED)❌ Pandoc not found. Install:$(NC)"; \
		echo "   Mac: brew install pandoc"; \
		echo "   Linux: sudo apt-get install pandoc"; \
		echo "   Windows: choco install pandoc"; \
		exit 1; \
	}

verify-scripts:
	@echo "$(BLUE)Checking for build scripts...$(NC)"
	@for script in $(BUILD_SCRIPTS); do \
		if [ ! -f "$$script" ]; then \
			echo "$(RED)❌ Missing: $$script$(NC)"; \
			exit 1; \
		fi; \
	done
	@echo "$(GREEN)✅ All build scripts present$(NC)"

status:
	@echo "$(BLUE)Build System Status$(NC)"
	@echo ""
	@echo "Scripts:"
	@for script in $(BUILD_SCRIPTS); do \
		if [ -f "$$script" ]; then \
			echo "  $(GREEN)✓$(NC) $$script"; \
		else \
			echo "  $(RED)✗$(NC) $$script"; \
		fi; \
	done
	@echo ""
	@echo "Output Directories:"
	@[ -d "$(EXAMPLES_DIR)" ] && echo "  $(GREEN)✓$(NC) $(EXAMPLES_DIR)/" || echo "  $(RED)✗$(NC) $(EXAMPLES_DIR)/"
	@[ -d "$(DOCS_DIR)" ] && echo "  $(GREEN)✓$(NC) $(DOCS_DIR)/" || echo "  $(RED)✗$(NC) $(DOCS_DIR)/"
	@[ -d "$(OUTPUT_DIR)" ] && echo "  $(GREEN)✓$(NC) $(OUTPUT_DIR)/" || echo "  $(RED)✗$(NC) $(OUTPUT_DIR)/"
	@echo ""
	@echo "Tools:"
	@command -v $(PYTHON) >/dev/null 2>&1 && echo "  $(GREEN)✓$(NC) Python" || echo "  $(RED)✗$(NC) Python"
	@command -v $(ZEBRA) >/dev/null 2>&1 && echo "  $(GREEN)✓$(NC) Zebra" || echo "  $(YELLOW)⊝$(NC) Zebra (optional)"
	@command -v $(PANDOC) >/dev/null 2>&1 && echo "  $(GREEN)✓$(NC) Pandoc" || echo "  $(YELLOW)⊝$(NC) Pandoc (for PDF)"

clean:
	@echo "$(YELLOW)🗑️  Cleaning build artifacts...$(NC)"
	@rm -rf $(EXAMPLES_DIR) $(DOCS_DIR) $(OUTPUT_DIR) lint-report.txt validation-report.*
	@echo "$(GREEN)✅ Cleaned$(NC)"

distclean: clean
	@echo "$(YELLOW)Removing all generated files...$(NC)"
	@rm -rf zebra-programming-book.pdf
	@echo "$(GREEN)✅ Distribution clean$(NC)"

# ============================================================================
# DEVELOPMENT TARGETS
# ============================================================================

watch:
	@echo "$(BLUE)👁️  Watching for changes (requires fswatch)...$(NC)"
	@while true; do \
		find Part-* -name "*.md" | fswatch -o | xargs -n1 -I {} bash -c 'clear; make lint'; \
	done

dev: extract
	@echo "$(GREEN)Development mode ready$(NC)"
	@echo "Edit markdown files and run: make lint validate"

# ============================================================================
# DOCUMENTATION
# ============================================================================

readme:
	@cat BUILD_PDF_README.md

info:
	@echo "$(BLUE)Zebra Programming Book - Build System$(NC)"
	@echo ""
	@echo "This Makefile orchestrates the complete book build pipeline:"
	@echo ""
	@echo "  1. $(BLUE)extract$(NC)  - Extract code examples to individual .zbr files"
	@echo "  2. $(BLUE)lint$(NC)     - Check chapters for consistency"
	@echo "  3. $(BLUE)validate$(NC) - Compile all examples"
	@echo "  4. $(BLUE)html$(NC)     - Generate HTML documentation"
	@echo "  5. $(BLUE)pdf$(NC)      - Generate PDF book"
	@echo ""
	@echo "Run 'make help' for all targets."

help:
	@echo ""
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║   Zebra Programming Book - Build System$(NC)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)QUICK START:$(NC)"
	@echo "  make                    # Build everything (extract, lint, validate, html, pdf)"
	@echo "  make quick              # Quick build (extract & validate only)"
	@echo ""
	@echo "$(YELLOW)INDIVIDUAL TARGETS:$(NC)"
	@echo "  make extract            # Extract code examples from chapters"
	@echo "  make lint               # Check chapters for consistency"
	@echo "  make validate           # Compile all examples and report results"
	@echo "  make html               # Generate HTML documentation site"
	@echo "  make pdf                # Generate PDF book (requires pandoc)"
	@echo ""
	@echo "$(YELLOW)UTILITIES:$(NC)"
	@echo "  make status             # Check build system status"
	@echo "  make verify-scripts     # Verify all build scripts are present"
	@echo "  make clean              # Remove build artifacts"
	@echo "  make distclean          # Remove all generated files"
	@echo "  make watch              # Watch markdown files for changes (requires fswatch)"
	@echo "  make dev                # Setup development mode"
	@echo "  make help               # Show this help message"
	@echo "  make info               # Show build system information"
	@echo ""
	@echo "$(YELLOW)INSTALLATION:$(NC)"
	@echo "  Python 3:               Already required"
	@echo "  Pandoc (for PDF):       brew install pandoc (Mac) | apt-get install pandoc (Linux)"
	@echo "  Zebra (for validation): Install Zebra compiler for example validation"
	@echo ""
	@echo "$(YELLOW)OUTPUT:$(NC)"
	@echo "  $(EXAMPLES_DIR)/                  - Extracted code examples"
	@echo "  $(DOCS_DIR)/index.html           - HTML documentation site"
	@echo "  $(OUTPUT_DIR)/zebra-programming-book.pdf - PDF book"
	@echo "  lint-report.txt                 - Lint findings"
	@echo "  validation-report.json          - Validation results"
	@echo ""
