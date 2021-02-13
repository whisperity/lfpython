default: all

all: style test

style:
	flake8 src/ test/
.PHONY: style

test: unit_test
.PHONY: test

unit_test:
	python3 -m pytest src test/unit
.PHONY: unit_test
