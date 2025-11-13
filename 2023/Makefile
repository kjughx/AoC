YEAR=2022
CURRENT := $(shell date +%s)
TARGET := $(shell date -d "$(YEAR)-12-$(DAY) 06:00" +%s)

EXT=py
SRC := src/day$(DAY).$(EXT)
INPUT := inputs/day$(DAY)


all: $(SRC) $(INPUT)
	@python $(SRC) < $(INPUT)

$(INPUT):
	@if [ "$(CURRENT)" -lt  "$(TARGET)" ]; then \
		echo "Day $(DAY) is not here yet :("; \
		make --silent _wait; \
	fi

	curl https://adventofcode.com/$(YEAR)/day/$(DAY)/input \
		--cookie session="$(shell cat ../.session)" > inputs/day$(DAY)

$(SRC):
	cp template.$(EXT) $(SRC)

.PHONY: wait
wait: $(SRC) $(INPUT)
	@nvim $(SRC) $(INPUT)

_wait:
	@echo "Waiting until $(DAY)/12 6:00 AM..."
	@while [ "$$(date +%s)" != "$(TARGET)" ]; do \
		sleep 1; \
	done
