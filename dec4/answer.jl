mutable struct Board
	size::Int64
	numberMat::Matrix{Int64}
	bingoMat::Matrix{Int64}
	hasBingo::Bool
end
function markNumber!(board::Board, n)
	for i = 1:board.size
		for j = 1:board.size
			if board.numberMat[i,j] == n
				board.bingoMat[i,j] = 1
			end
		end
	end
end

function hasBingo(board::Board)
	for r in 1:board.size
		row = board.bingoMat[r,:]
		if sum(row) == board.size
			return true
		end
		col = board.bingoMat[:,r]
		if sum(col) == board.size
			return true
		end
	end
	return false
end

function Score(board, finalNumber)
	unmarkedSum = 0
	for i = 1:board.size
		for j = 1:board.size
			unmarkedSum += board.bingoMat[i,j]==0 ? board.numberMat[i,j] : 0
		end
	end
	totalScore = unmarkedSum * finalNumber
end

function playBingo(drawNumbers, boards)
	for number in drawNumbers
		for (i, board) in enumerate(boards)
			markNumber!(board, number)
			if(hasBingo(board))
				score = Score(board, number)
				println("Board ", i, " has bingo, with a total score of: ", score)
				return
			end
		end
	end
end
function playBadBingo(drawNumbers, boards)
	N_boards = length(boards)
	for number in drawNumbers
		for(i, board) in enumerate(boards)
			if !board.hasBingo
				markNumber!(board, number)
				if(hasBingo(board))
					board.hasBingo = true
					if N_boards == 1
						score = Score(board, number)
						println("Board ", i, " is the last to win, with a total score of: ", score)
						return
					end
					N_boards -= 1
				end
			end
		end
	end
end





drawNumbers = []
io = open("input.txt", "r")
line = readline(io)
for el in split(line, ',')
	push!(drawNumbers, parse(Int, el))
end
readline(io)



boards = []
rows = []
for line in eachline(io)
	if length(rows) == 5

		global rows = []
	else
		row = parse.(Int, split(line))
		push!(rows, row')
	end
	if length(rows) == 5
		n =  5
		nMat = zeros(Int64, n, n)
		for r = 1:n
			nMat[r,:] = rows[r]'
		end
		board = Board(n, nMat, zeros(Int64, n, n), false)
		push!(boards, board)
	end
end

playBingo(drawNumbers, boards)
playBadBingo(drawNumbers, boards)

