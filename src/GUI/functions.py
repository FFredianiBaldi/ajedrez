def is_piece_selected_in_turn(white_turn:bool, color:str)->bool:
    """Funcion que define si la pieza seleccionada corresponde al turno

    Args:
        white_turn (bool): True si es el turno de blancas, False si no
        color (str): Color de la pieza seleccionada

    Returns:
        bool: True si la pieza seleccionada concuerda con el turno, False si no
    """
    if white_turn and color == 'w':
        return True
    elif not white_turn and color == 'b':
        return True
    else:
        return None

def get_position_color(position)->str:
    """Funcion que devuelve de que color es la casilla

    Args:
        position (_type_): posicion de la casilla

    Returns:
        str: white/black
    """
    if (position[0] + position[1]) % 2 == 0:
        return "white"
    return "black"