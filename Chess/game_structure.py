import chess

def main():
    board = chess.Board()

    while (not board.is_checkmate()):
        print(board)
        while True:
            print(board.legal_moves)
            start_square = input('Starting square:')
            end_square = input('Ending square:')
            try:
                move = board.find_move(chess.parse_square(start_square), chess.parse_square(end_square))
                if move in board.legal_moves:
                    break
            except:
                print('Invalid move try again')

        board.push(move)
    print(board.outcome().result())
    
if __name__ == '__main__':
    main()
