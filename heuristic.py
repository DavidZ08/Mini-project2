def heuristic(board, win, p1, p2):
    height, width = list(range(len(board))), list(range(len(board[0])))
    avail_p1 = 0
    avail_p2 = 0

    board_p1 = (board == '.') | (board == p1)
    board_p2 = (board == '.') | (board == p2)

    for i in height: 
        for j in width:
            ver_p1, ver_p2 = board_p1[i:i+win, j], board_p2[i:i+win, j]
            hor_p1, hor_p2 = board_p1[i, j:j+win], board_p2[i, j:j+win]
            top_right_p1, top_right_p2 = np.diagonal(board_p1[i: i+win, j: j+win]), np.diagonal(board_p2[i: i+win, j: j+win])
            top_left_p1, top_left_p2 = np.diagonal(np.fliplr(board_p1[i: i+win, 1+j-win:j+1])), np.diagonal(np.fliplr(board_p2[i: i+win, 1+j-win:j+1]))

            if hor_p1.all() and hor_p1.size == win:
                avail_p1 += 1
            if ver_p1.all() and ver_p1.size == win:
                avail_p1 += 1
            if top_right_p1.all() and top_right_p1.size == win:
                avail_p1 += 1
            if top_left_p1.all() and top_left_p1.size == win:
                avail_p1 += 1
            if hor_p2.all() and hor_p2.size == win:
                avail_p2 += 1
            if ver_p2.all() and ver_p2.size == win:
                avail_p2 += 1
            if top_right_p2.all() and top_right_p2.size == win:
                avail_p2 += 1
            if top_left_p2.all() and top_left_p2.size == win:
                avail_p2 += 1
                
    return avail_p1 - avail_p2