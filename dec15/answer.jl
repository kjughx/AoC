input = []
for line in readlines("input")
	line = split(line,"")
	push!(input, parse.(Int64, line))
end
N = length(input)
riskMap = Matrix{Int64}(undef, N, N)
for row in 1:N
	global riskMap[row, :] = input[row]
end
function findNeighbors((i,j), N)
	neighbors = Set()
	for dir in [(0,1), (1,0)]
		point = (i,j) .+ dir
		if all(1 .<= point .<= N)
			push!(neighbors, point)
		end
	end
	neighbors
end

function findPath(risk, lowestRisk, nPaths, riskMap, path, pos)
	for (i,j) in findNeighbors(pos, size(riskMap, 1))
		push!(path, (i,j))
		risk += riskMap[i,j]
		if (i,j) == (size(riskMap, 1), size(riskMap, 2))
			if risk < lowestRisk
				lowestRisk = risk
			end
			continue	
		end
		if risk < lowestRisk
			findPath(risk, lowestRisk, riskMap, path, (i,j))
			

		end
	end
end

# path, risk = findPath(sum(riskMap), riskMap, [], (1,1))

