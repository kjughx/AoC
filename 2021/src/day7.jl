crabs = parse.(Int64, split(readline(stdin), ","))

function calcFuel(initial, final)
	abs(initial - final)
end



# smallestFuel = sum(crabs)
# position = 0
# for pos in crabs
	# fuel = 0
	# for crab in crabs
		# fuel += abs(crab - pos)
	# end
	# if fuel < smallestFuel
		# global position = pos
		# global smallestFuel = fuel
	# end
# end
# print(position, "\t", smallestFuel)


smallestFuel = 1e8
position = 0
for pos in 0:maximum(crabs)
	fuel = 0
	for crab in crabs
		n = abs(crab-pos)
		fuel += Int(n*(n+1)/2)
	end
	if fuel < smallestFuel
		global smallestFuel = fuel
		global position = pos
	end
end
print(position, "\t", smallestFuel)
