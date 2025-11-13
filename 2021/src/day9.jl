input = []
for line in readlines(stdin)
	line = (split(line, ""))
	push!(input, parse.(Int64, line))
end
Nx = length(input)
Ny = length(input[1])
println(Nx, "\t", Ny)
grid = Matrix{Int64}(undef, Nx, Ny)
for (i,row) in enumerate(input)
	global grid[i, :] = row
end

function inBounds(point, Nx, Ny)
	(i,j) = point
	if 1 <= i <= Nx && 1 <= j <= Ny
		return true
	end
	return false
end

function findNeighbors(i,j, Nx, Ny)
	neighbors = Set()

	for s in [-1, 1]
		point = (i, j + s)
		if inBounds(point, Nx, Ny)
			push!(neighbors, point)
		end
		point = (i + s, j)
		if inBounds(point, Nx, Ny)
			push!(neighbors, point)
		end
	end
	neighbors
end

lowPoints = Set()
for i = 1:Nx
	for j = 1:Ny
		neighbors = findNeighbors(i,j, Nx, Ny)
		test = 0
		for (k,l) in neighbors
			test += grid[i, j] < grid[k,l] ? 1 : 0
		end
		if test == length(neighbors)
			push!(lowPoints, (i,j))
		end
	end
end

Risk = 0
for (i,j) in lowPoints
	global Risk += 1 + grid[i,j]
end

function findBasin!(basin, (i,j) , grid)
	Nx = size(grid, 1)
	Ny = size(grid, 2)

	neighbors = findNeighbors(i,j, Nx,Ny)
	for (k, l) in neighbors
		if grid[k,l] > grid[i,j]  && grid[k,l] != 9
			push!(basin, (k,l))
			findBasin!(basin, (k,l), grid)
		end
	end
end

Basins = Set()
for (i,j) in lowPoints
	basin = []
	push!(basin, (i,j))
	findBasin!(basin, (i,j), grid)
	push!(Basins, unique(basin))
end

lengths = length.(Basins)
println(prod(partialsort(lengths, 1:3, rev = true)))
