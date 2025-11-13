input = []
for line in readlines(stdin)
	push!(input, line)
end

openBraces = [ "(" , "[", "{", "<",]
closeBraces = [")", "]" , "}" , ">",]
matchingBraces = Dict(zip(closeBraces, openBraces))
bracePoints = Dict(")" => 3, "]" => 57, "}" => 1197, ">" => 25137)

corruptBraces = []
discardLines = []
for (i,line) in enumerate(input)
	braces = []
	for brace in split(line, "")
		if brace in openBraces
			push!(braces, brace)
		elseif last(braces) == matchingBraces[brace]
			pop!(braces)
		else
			push!(corruptBraces, brace)
			push!(discardLines, i)
			break
		end
	end
end

points1 = 0
for corruptBrace in corruptBraces
	global points1 += bracePoints[corruptBrace]
end

matchingBraces = Dict(zip(closeBraces, openBraces))
matchBrace = Dict(zip(openBraces, closeBraces))
bracePoints = Dict(")" => 1, "]" => 2, "}" => 3, ">" => 4)

deleteat!(input, discardLines)

CompleteBraces = []
for line in input
	braces = []
	completeBraces = "" 
	for brace in split(line, "")
		if brace in openBraces
			push!(braces, brace)
		elseif last(braces) == matchingBraces[brace]
			pop!(braces)
		end
	end
	for brace in reverse(braces)
		completeBraces *= matchBrace[brace]
	end
	push!(CompleteBraces, completeBraces)
end

scores = []
for completeBraces in CompleteBraces
	score = 0
	for brace in split(completeBraces,"")
		score = 5*score + bracePoints[brace]
	end
	push!(scores, score)
end

sort!(scores)
n = length(scores)
mid = div(n,2)+1
println(scores[mid])
