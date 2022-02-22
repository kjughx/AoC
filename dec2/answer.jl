struct Command
	Direction::String
	Amount::Int
end
mutable struct Position 
	Horizontal::Int64
	Depth::Int64
	Aim::Int64
end
# part1 functions #
function changeHorizontal(pos::Position, amount)
	pos.Horizontal += amount # part 1
end
function changeDepth(pos::Position, amount)
	pos.Depth += amount
end
function changeAim(pos::Position, amount)
	pos.Aim += amount
end
function changePosition(pos::Position, command::Command)
	dir = command.Direction
	amo = command.Amount

	# if dir == "forward"
		# changeHorizontal(pos, amo)
	# elseif dir == "down"
		# changeDepth(pos, +amo)
	# elseif dir == "up"
		# changeDepth(pos, -amo)
	# end
	if dir == "down"
		changeAim(pos, amo)
	elseif dir == "up"
		changeAim(pos, -amo)
	elseif dir == "forward"
		changeHorizontal(pos, amo)
		changeDepth(pos, pos.Aim*amo)
	end
end
	
input = []
for line in readlines("input.txt")
	line = split(line)
	command = Command(line[1], parse(Int, (line[2])))
	push!(input, command)
end
position = Position(0,0,0)

for command in input
	changePosition(position, command)
end

println(position.Horizontal* position.Depth)
