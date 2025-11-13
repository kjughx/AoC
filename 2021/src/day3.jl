input = []
for line in readlines(stdin)
	# push!(input, parse(String, line))
	push!(input, line)
end

N = length(input)
Nb = length(input[1])
gamma = "0b"
epsilon = "0b"

# part 1
for i = 1:Nb
	s = 0
	for j = 1:N
		s += parse(Int, input[j][i])
	end
	global gamma *= string(s > N/2 ? 1 : 0)
	global epsilon *= string(s < N/2 ? 1 : 0)
end
powerConsumption=parse(Int, gamma) * parse(Int, epsilon)
println(powerConsumption)

finalOxy = "0b"
finalCo2 = "0b"
oxy = deepcopy(input)
co2 = deepcopy(input)

for i = 1:Nb
	s = 0
	Nh = length(oxy)
	for j = 1:Nh
		s += parse(Int, oxy[j][i])
	end
	mcv = s >= Nh/2 ? 1 : 0
	filter!(e->parse(Int, e[i])==mcv, oxy)
	if length(oxy) == 1
		global finalOxy *= oxy[1]
		break
	end
end

for i = 1:Nb
	s = 0
	Nh = length(co2)
	for j = 1:Nh
		s += parse(Int, co2[j][i])
	end
	lcv = s >= Nh/2 ? 0 : 1
	filter!(e->parse(Int, e[i])==lcv, co2)
	if length(co2) == 1
		global finalCo2 *= co2[1]
		break
	end
end

println(finalOxy, "\t", finalCo2)
lifeSupport = parse(Int, finalOxy) * parse(Int, finalCo2)
println(lifeSupport)
