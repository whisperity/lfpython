default: all

all: style test

style:
	flake8 src/ test/
.PHONY: style

test:
	python3 -m pytest src test/
	cd test; PYTHONPATH="../src" bash ./test_shell.sh; cd ..
.PHONY: test

package: dist
dist: setup.py
	python3 -m build

distclean:
	rm -rf ./build ./dist ./lpython*.egg.info
.PHONY: clean
