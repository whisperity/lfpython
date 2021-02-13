default: all

all: test

test: unit_test
.PHONY: test

unit_test:
	python3 -m pytest src test/unit
