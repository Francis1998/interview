.PHONY: help list check-links serve demo-gif install-dev

help:  ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

list:  ## List all topic markdown files
	@ls -1 *.md | grep -v CHANGELOG | grep -v SECURITY

check-links:  ## Verify internal markdown links resolve to existing files
	@python3 scripts/check_links.py

install-dev:  ## Install preview server and GIF dependencies
	pip install -r requirements-dev.txt

serve:  ## Start local handbook preview at http://127.0.0.1:8080
	@if [ -x .venv/bin/python ]; then .venv/bin/python scripts/serve.py --host 127.0.0.1 --port 8080; else python3 scripts/serve.py --host 127.0.0.1 --port 8080; fi

demo-gif:  ## Regenerate assets/demo-handbook.gif
	@if [ -x .venv/bin/python ]; then .venv/bin/python scripts/generate_demo_gif.py; else python3 scripts/generate_demo_gif.py; fi
