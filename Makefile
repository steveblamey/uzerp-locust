objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

.PHONY: all
all: $(outputs)

%.txt: %.in
	pip-compile -v --output-file $@ $<

test.txt: requirements.txt

.PHONY: check
check:
	@which pip-compile > /dev/null

.PHONY: clean
clean: check
	- rm *.txt
