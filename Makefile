default: all

all: style test

style:
	flake8 src/ test/
.PHONY: style

test:
	python3 -m pytest -vv src test/
.PHONY: test
