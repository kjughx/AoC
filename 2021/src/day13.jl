mutable struct Paper
	Height::Int64
	Width::Int64
	Dots::Matrix{Int64}
end
gridInput = []
instructions = []
for line in readlines(stdin)
	if length(line) > 0
		if length(line) < 11
			line = split(line, ",")
			push!(gridInput, (parse(Int64, line[2]) + 1, parse(Int64, line[1]) + 1))
		else
			push!(instructions, line)
		end
	end
end
function fold(paper, direction)
	if direction == :horizontal
		y = paper.Height
		height = div(y,2)
		global newPaper = Paper(height, paper.Width, zeros(Int64, height, paper.Width))
		for j = 1:paper.Width
			for i = 1:height
				newPaper.Dots[i,j] = (paper.Dots[i,j] + paper.Dots[y-i+1,j]) > 0 ? 1 : 0
			end
		end
	elseif direction == :vertical
		x = paper.Width
		width = div(x,2)
		global newPaper = Paper(paper.Height, width, zeros(Int64, paper.Height, width))
		for j = 1:width
			for i = 1:paper.Height
				newPaper.Dots[i,j] = (paper.Dots[i,j] + paper.Dots[i,x-j+1]) > 0 ? 1 : 0
			end
		end
	end

	newPaper
end
rows = 0
cols = 0
for (i,j) in gridInput
	if i > rows
		global rows = i
	end
	if j > cols
		global cols = j
	end
end

paper = Paper(rows, cols, zeros(Int64, rows,cols))
for (i,j) in gridInput
	paper.Dots[i,j] = 1
end
# instruction = split(instructions[1], " ")[3]
# direction = split(instruction, "")[1] == "x" ? (:vertical) : (:horizontal)
# paper = fold(paper, direction)
# display(paper.Dots)
# println()
# println(sum(paper.Dots))

for instruction in instructions
	instruction = split(instruction, " ")[3]
	direction = split(instruction, "")[1] == "x" ? (:vertical) : (:horizontal)
	global paper = fold(paper, direction)
end

for
display(paper.Dots)
