input = []
for line in readlines(stdin)
	push!(input, parse(Int, line))
end

# part 1
counts = 0
for i = 2:2000
	if input[i] > input[i-1]
		global counts += 1
	end
end
println("Answer to part 1: ", counts)
# end of part1

# part 2
counts = 0
N = length(input)
for i = 2:N-2
	s = sum(input[i:i+2])
	if sum(input[i:i+2]) > sum(input[i-1:i+1])
		global counts += 1
	end
end
println(counts)
