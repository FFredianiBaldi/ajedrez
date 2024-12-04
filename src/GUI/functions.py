def is_piece_selected_in_turn(white_turn:bool, color:str):
    if white_turn and color == 'w':
        return True
    elif white_turn == False and color == 'b':
        return True
    else:
        return None