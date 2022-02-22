using DataStructures
Fish = parse.(Int64, split(readline("input"),","))


# Days are between 0 - 8, make list of days and count how many fish 
#

days = Vector{Int64}()
for day in 1:9
	push!(days, 0)
end
for fish in Fish
	days[fish+1] += 1
end


function evolveDays(days)
	f = first(days)
	popfirst!(days)
	days[7] += f
	push!(days, f)
end

for day in 1:256
	evolveDays(days)
end
nFish = sum(days)
println(nFish)
