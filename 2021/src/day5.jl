struct Line
	Start::Tuple{Int64, Int64}
	End::Tuple{Int64, Int64}
	Direction::Symbol # vertical / horizontal
end
function findPoints(line::Line)
	if line.Direction == :vertical
		step = line.End[2] - line.Start[2] > 0 ? 1 : -1
		return Set([(line.Start[1], y) for y = line.Start[2] :step: line.End[2]])
	elseif line.Direction == :horizontal
		step = line.End[1] - line.Start[1] > 0 ? 1 : -1
		return Set([(x, line.Start[2]) for x = line.Start[1] :step: line.End[1]])
	elseif line.Direction == :diagonal
		stepx = line.End[1] - line.Start[1] > 0 ? 1 : -1
		stepy = line.End[2] - line.Start[2] > 0 ? 1 : -1
		steps = abs(line.End[1] - line.Start[1])
		return Set([(line.Start[1] + stepx*i, line.Start[2] + stepy*i) for i = 0:steps])
	end
end


Lines = []
for line in readlines(stdin)
	line = split(line, ' ')[1:2:3]
	s, e = split(line[1], ",") , split(line[2], ",")

	s = (parse(Int64, s[1]), parse(Int64, s[2]))
	e = (parse(Int64, e[1]), parse(Int64, e[2]))
	dir = s .- e
	if dir[1] !=  0 && dir[2] == 0
		push!(Lines, Line(s, e, :horizontal))
	elseif dir[1] == 0 && dir[2] != 0
		push!(Lines, Line(s, e, :vertical))
	elseif dir[1] != 0 && dir[2] != 0
		push!(Lines, Line(s, e, :diagonal))
	end
end

grid = Dict()
for line in Lines
	points = findPoints(line)
	for point in points
		if haskey(grid, point)
			grid[point] +=1
		else
			grid[point] = 1
		end
	end
end

numberPoints = 0
for key in keys(grid)
	if grid[key] >= 2
		global numberPoints += 1
	end
end

println(numberPoints)
