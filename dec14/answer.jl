file = "test"
io = open(file)
Polymer = split(readline(io), "")
Rules = Dict()
readline(io)
for line in readlines(io)
	line = split(line, " -> ")
	push!(Rules, line[1]=>line[2])

end

for step in 1:40
	newPolymer = []
	println(step)
	for (i,element) in enumerate(Polymer)
		if i < length(Polymer)
			if haskey(Rules, element*Polymer[i+1])
				push!(newPolymer, element)
				push!(newPolymer, Rules[element*Polymer[i+1]])
			end
		end
	end
	push!(newPolymer, last(Polymer))
	global Polymer = newPolymer
end
using DataStructures

c = counter(Polymer)
occurences = sort(collect(values(c)),rev=true)
println(occurences)

# Pairs = Dict()
# for (i,element) in enumerate(Polymer)

