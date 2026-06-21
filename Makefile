.PHONY: help list check-links

help:  ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

list:  ## List all topic markdown files
	@ls -1 *.md | grep -v CHANGELOG | grep -v SECURITY

check-links:  ## Verify internal markdown links resolve to existing files
	@python3 scripts/check_links.py
