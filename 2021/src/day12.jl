Caves = Dict()
for line in readlines(stdin)
	key1,key2 = String.(split(line, "-"))
	key1, key2 = key1, key2
	if !haskey(Caves, key1)
		Caves[key1] = [key2]
	elseif haskey(Caves, key1)
		push!(Caves[key1], key2)
	end
	if !haskey(Caves, key2)
		Caves[key2] = [key1]
	elseif haskey(Caves, key2)
		push!(Caves[key2], key1)
	end
end
smallCaves = []
for (cave, caves) in Caves
	if !(cave in ["start", "end"])
		if all(c->islowercase(only(c)), cave)
			push!(smallCaves, cave)
		end
	end
end

function genPath(Caves, start, Paths, path, smallCaves)
	push!(path, start)
	for stop in Caves[start]
		if !(stop in path && stop in keys(smallCaves))
			path1 = deepcopy(path)
			if stop == "end"
				push!(path1, "end")
				push!(Paths, path1)
				smallCaves = Dict(cave => 0 for cave in keys(smallCaves))
				continue
			elseif stop != "start"
				genPath(Caves, stop, Paths, path1, smallCaves)
			end
		end
	end
end

smallCaves = Dict(zip(smallCaves, [0 for cave in smallCaves]))

Paths = []
path = []
genPath(Caves, "start", Paths, path, smallCaves)
println(length(Paths))
