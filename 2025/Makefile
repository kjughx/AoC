YEAR=2025
CURRENT := $(shell date +%s)
TARGET := $(shell date -d "$(YEAR)-12-$(DAY) 06:00" +%s)

SRC := src/day$(DAY).c libpj.h
INPUT := inputs/day$(DAY)

CFLAGS= -Wall -Wextra -g -ggdb -Wno-unused-function -I./ -lm

test: $(SRC) inputs/test
	gcc -DTEST $(CFLAGS) $(SRC) -o day$(DAY)
	./day$(DAY) < inputs/test

part%: $(SRC) $(INPUT)
	gcc -DPART$* $(CFLAGS) $(SRC) -o day$(DAY)
	./day$(DAY) < $(INPUT)

$(SRC):
	cp ./template.c $(SRC)

$(INPUT):
	@if [ "$(CURRENT)" -lt  "$(TARGET)" ]; then \
		echo "Day $(DAY) is not here yet :("; \
		make --silent _wait; \
	fi

	curl https://adventofcode.com/$(YEAR)/day/$(DAY)/input \
		--cookie session="$(shell cat ../.session)" > inputs/day$(DAY)

.PHONY: wait
wait: $(SRC) $(INPUT)
	@nvim $(SRC) $(INPUT)

_wait:
	@echo "Waiting until $(DAY)/12 6:00 AM..."
	@while [ "$$(date +%s)" != "$(TARGET)" ]; do \
		sleep 1; \
	done
