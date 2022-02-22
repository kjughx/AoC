Signals = []
Outputs = []
for line in readlines("input")
	line = split(line, " | ")
	signals = split(line[1], " ")
	outputs = split(line[2], " ")
	push!(Signals, signals)
	push!(Outputs, outputs)
end
Digits = Dict(2 => [1,],
			  3 => [7,],
			  4 => [4,],
			  5 => [2, 3, 5],
			  6 => [0, 6, 9],
			  7 => [8]
			  )

## part 1 -----------
uniqueLengths = [2, 3, 4, 7]
uniqueCount = 0
for output in Outputs
	for digit in output
		if length(digit) in uniqueLengths
			global uniqueCount += 1
		end
	end
end
#end part1 -------------------------------------


## part2 ------------------------------
somedict = Dict()
for line in readlines("input")
	line = split(line, " | ")
	signals = split(line[1], " ")
	outputs = split(line[2], " ")
	for signal in signals
		push!(somedict, Set(split(signal,"")) => Digits[length(signal)])
	end
	break
end

## union \ intersection
# println(setdiff(union(set1,set2), intersect(set1,set2)))

