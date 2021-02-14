default: all

all: style test

style:
	flake8 src/ test/
.PHONY: style

test:
	python3 -m pytest src test/
.PHONY: test
