YEAR=2020
CURRENT := $(shell date +%s)
TARGET := $(shell date -d "$(YEAR)-12-$(DAY) 06:00" +%s)

SRC := src/day$(DAY).c
INPUT := inputs/day$(DAY)

CFLAGS= -Wall -Wextra -Wno-unused-function -I./

all: $(SRC) $(INPUT)
	gcc $(CFLAGS) $(SRC) -o day$(DAY)
	./day$(DAY) < $(INPUT)

$(INPUT):
	@if [ "$(CURRENT)" -lt  "$(TARGET)" ]; then \
		echo "Day $(DAY) is not here yet :("; \
		make --silent _wait; \
	fi

	curl https://adventofcode.com/$(YEAR)/day/$(DAY)/input \
		--cookie session="$(shell cat ../.session)" > inputs/day$(DAY)

$(SRC):
	cp ./template.c $(SRC)

test: $(INPUT)_test
	gcc $(CFLAGS) $(SRC) -o day$(DAY)
	./day$(DAY) < $(INPUT)_test

.PHONY: wait
wait: $(SRC) $(INPUT)
	@nvim $(SRC) $(INPUT)

_wait:
	@echo "Waiting until $(DAY)/12 6:00 AM..."
	@while [ "$$(date +%s)" != "$(TARGET)" ]; do \
		sleep 1; \
	done
