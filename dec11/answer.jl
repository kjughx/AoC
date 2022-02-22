input = []
for line in readlines("input")
	line = split(line,"")
	push!(input, parse.(Int64, line))
end
global Nx = length(input)
global Ny = length(input[1])
grid = Matrix{Int64}(undef, Nx, Ny)
for (i,row) in enumerate(input)
	global grid[i, :] = row
end

function inBounds((i,j))
	if 1 <= i <= Nx && 1 <= j <= Ny
		return true
	end
	false
end

function findNeighbors((i,j))
	neighbors = Set()
	for dir in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
		point = (i,j) .+ dir
		if inBounds(point)
			push!(neighbors, (i,j) .+ dir)
		end
	end
	neighbors
end

function flash((i,j), grid, hasFlashed)
	neighbors = findNeighbors((i,j))
	hasFlashed[i,j] = 1
	for (k,l) in neighbors
		grid[k,l] += 1
		if grid[k,l] > 9 && !hasFlashed[k,l]
			flash((k,l), grid, hasFlashed)
		end
	end
end 


function simulate(grid, steps)
	global flashes = 0
	global step = 1

	while true
		hasFlashed = grid .> 20
		grid = grid .+ 1
		for j = 1:size(grid, 2)
			for i = 1:size(grid, 1)
				if grid[i,j] > 9 && !hasFlashed[i,j]
					flash((i,j), grid, hasFlashed)
				end
			end
		end
		for j = 1:size(grid, 2)
			for i = 1:size(grid, 1)
				if hasFlashed[i,j]
					grid[i,j] = 0
				end
			end
		end
		global flashes += sum(hasFlashed)
		if sum(hasFlashed) == size(grid, 1)*size(grid,2)
			return step
		end
		step += 1 
	end
	flashes
end
nFlashes = simulate(grid, 100)
println(nFlashes)

