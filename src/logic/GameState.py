import pygame, sys
from src.GUI.functions import *

class GameState:
    def __init__(self, screen:pygame.Surface) -> None:
        """Constructor de la clase del juego

        Args:
            screen (pygame.Surface): En que ventana se va a dibujar todo
        """
        self.state = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','wP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]

        # Booleano que permite saber si es turno de blancas o negras
        self.white_turn = True

        # Configuro la pantalla y el tamaño de las casillas
        self.screen = screen
        self.tiles_width = self.screen.get_width() // 8
        self.tiles_height = self.screen.get_height() // 8

        # Variable que va a almacenar que pieza se eligio
        self.selected_piece = None
        # Posibles movimientos de la misma
        self.possible_moves = []

        # Variables para ver si se movieron los reyes y torres para el enroque
        self.white_king_moved = False
        self.black_king_moved = False

        self.short_black_rook_moved = False
        self.long_black_rook_moved = False

        self.short_white_rook_moved = False
        self.long_white_rook_moved = False
    def draw_pieces(self):
        """Funcion que dibuja las piezas
        recorre el tablero como una matriz, y en base al contenido
        de la casilla, no dibuja nada (--), o dibuja la pieza que tenga
        """
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                color, piece = list(self.state[i][j])
                if color != '-':
                    piece_img = pygame.image.load(f"assets/pieces/{color}/{piece}.png")
                    piece_img = pygame.transform.scale(piece_img, (self.tiles_width, self.tiles_height)).convert_alpha()

                    self.screen.blit(piece_img, (j * self.tiles_width, i * self.tiles_height))

    def is_mouse_over_piece_in_turn(self, mouse_pos:tuple)->bool:
        """Funcion que dice si el mouse esta sobre una pieza
        del color al que corresponde el turno

        Args:
            mouse_pos (tuple): posicion del mouse

        Returns:
            bool: True si el mouse esta en una pieza del color que corresponde
            False si no lo esta 
        """
        x, y = mouse_pos
        column = x // self.tiles_width
        row = y // self.tiles_height

        piece = self.state[row][column]
        if piece != '--':
            color = list(piece)[0]
            if self.white_turn and color == 'w':
                return True
            elif self.white_turn == False and color == 'b':
                return True
        return False
    
    def is_mouse_over_possible_move(self, mouse_pos:tuple)->bool:
        """Funcion que dice si el mouse esta sobre un posible movimiento

        Args:
            mouse_pos (tuple): posicion del mouse

        Returns:
            bool: True si el mouse esta sobre un posible movimiento
            False si no lo esta
        """
        x, y = mouse_pos
        column = x // self.tiles_width
        row = y // self.tiles_height

        if (column, row) in self.possible_moves:
            return True
        return False
    
    def select_piece(self, mouse_pos:tuple):
        """Funcion que guarda en la variable self.selected_piece:
        - La pieza
        - El color
        - La posicion

        Args:
            mouse_pos (tuple): posicion del mouse
        """
        x, y = mouse_pos
        column = x // self.tiles_width
        row = y // self.tiles_height

        self.possible_moves = []

        piece = self.state[row][column]

        if piece != '--':
            color = list(piece)[0]
            if is_piece_selected_in_turn(self.white_turn, color):
                self.selected_piece = {
                    'piece' : piece[1],
                    'color' : piece[0],
                    'position' : (row, column)
                }
            else:
                self.selected_piece = None
        else:
            self.selected_piece = None

    def save_possible_moves(self):
        """Funcion que guarda en self.possible_moves los posibles
        movimientos dependiendo de que pieza se haya elegido
        """
        if self.selected_piece != None:
            if self.selected_piece['piece'] == 'R':
                self.horizontal_vertical_possible_moves()
            elif self.selected_piece['piece'] == 'B':
                self.diagonal_possible_moves()
            elif self.selected_piece['piece'] == 'Q':
                self.horizontal_vertical_possible_moves()
                self.diagonal_possible_moves()
            elif self.selected_piece['piece'] == 'N':
                self.knight_possible_moves()
            elif self.selected_piece['piece'] == 'K':
                self.king_possible_moves()
            elif self.selected_piece['piece'] == 'P':
                self.pawn_possible_moves()
        else:
            self.possible_moves = []

    def draw_possible_moves(self):
        """Funcion que dibuja las casillas de posibles movimientos
        en un tono mas rojizo
        """
        for row, col in self.possible_moves:
            x, y = col * self.tiles_width, row * self.tiles_height
            position_color = get_position_color((row, col))
            color = (245, 219, 195) if position_color == "white" else (187, 87, 70)
            pygame.draw.rect(self.screen, color, (x, y, self.tiles_width, self.tiles_height))


    
    def horizontal_vertical_possible_moves(self) -> None:
        """Funcion que determina cuales son los posibles movimientos
        en el eje vertical y horizontal en base a la posicion de la
        pieza seleccionada y los guarda en self.possible_moves
        usado en: la torre y la reina (comparten ese movimiento)
        """
        row, col = self.selected_piece['position']

        # Right moves
        for c in range(col + 1, 8):
            if not self.is_valid_move(row, c):
                break
            self.possible_moves.append((row, c))
        # Left moves
        for c in range(col - 1, -1, -1):
            if not self.is_valid_move(row, c):
                break
            self.possible_moves.append((row, c))

        # Up moves
        for r in range(row + 1, 8):
            if not self.is_valid_move(r, col):
                break
            self.possible_moves.append((r, col))
        # Down moves
        for r in range(row - 1, -1, -1):
            if not self.is_valid_move(r, col):
                break
            self.possible_moves.append((r, col))

    def diagonal_possible_moves(self) -> None:
        """Funcion que determina cuales son los posibles movimientos
        en diagonal en base a la posicion de la pieza seleccionada
        y los guarda en self.possible_moves
        usado en: el alfil y la reina (comparten ese movimiento)
        """
        initial_row, initial_col = self.selected_piece['position']

        rows = len(self.state)
        cols = len(self.state[0])

        # UpLeft moves
        row, col = initial_row - 1, initial_col - 1
        while row >= 0 and col >= 0:
            if not self.is_valid_move(row, col):
                break
            self.possible_moves.append((row, col))
            row -= 1
            col -= 1

        # UpRight moves
        row, col = initial_row - 1, initial_col + 1
        while row >= 0 and col <= cols-1:
            if not self.is_valid_move(row, col):
                break
            self.possible_moves.append((row, col))
            row -= 1
            col += 1

        # UpLeft moves
        row, col = initial_row + 1, initial_col - 1
        while row <= rows-1 and col >= 0:
            if not self.is_valid_move(row, col):
                break
            self.possible_moves.append((row, col))
            row += 1
            col -= 1
        
        # UpRight moves
        row, col = initial_row + 1, initial_col + 1
        while row <= rows-1 and col <= cols-1:
            if not self.is_valid_move(row, col):
                break
            self.possible_moves.append((row, col))
            row += 1
            col += 1

    def knight_possible_moves(self):
        """Funcion que determina cuales son los posibles movimientos
        en L en base a la posicion de la pieza seleccionada
        y los guarda en self.possible_moves
        """
        initial_row, initial_col = self.selected_piece['position']
        rows = len(self.state)
        cols = len(self.state[0])

        moves = [
            (-2, -1), (-2, 1),
            (-1, 2), (1, 2),
            (2, 1), (2, -1),
            (1, -2), (-1, -2)
        ]

        for r, c in moves:
            row, col = initial_row + r, initial_col + c
            # Se asegura de que el movimiento este dentro del rango de self.state
            if 0 <= row < rows and 0 <= col < cols:
                if self.is_valid_move(row, col):
                    self.possible_moves.append((row, col))

    def king_possible_moves(self):
        """Funcion que determina cuales son los posibles movimientos
        en todos los sentidos pero de una sola casilla en base a la
        posicion de la pieza seleccionada y los guarda en self.possible_moves

        tambien considera el enroque
        """
        initial_row, initial_col = self.selected_piece['position']
        rows = len(self.state)
        cols = len(self.state[0])

        moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]


        # Enroque blanco
        if self.selected_piece['color'] == 'w' and not self.white_king_moved:
            # Enroque corto
            if not self.short_white_rook_moved and self.state[7][5] == '--':
                moves.append((0, 2))
            # Enroque largo
            if not self.long_white_rook_moved and self.state[7][2] == self.state[7][3] == '--':
                moves.append((0, -2))

        # Enroque negro
        elif self.selected_piece['color'] == 'b' and not self.black_king_moved:
            # Enroque corto
            if not self.short_black_rook_moved and self.state[0][5] == '--':
                moves.append((0, 2))
            # Enroque largo
            if not self.long_black_rook_moved and self.state[0][2] == self.state[0][3] == '--':
                moves.append((0, -2))
        

        for r, c in moves:
            row, col = initial_row + r, initial_col + c
            # Se asegura de que el movimiento este dentro del rango de self.state
            if 0 <= row < rows and 0 <= col < cols:
                if self.is_valid_move(row, col):
                    self.possible_moves.append((row, col))
    
    def pawn_possible_moves(self):
        """Funcion que determina los movimientos posibles de un peon
        Tiene en cuenta:
        - Si es el primer movimiento puede mover 2
        - Si hay una pieza enemiga en diagonal, puede mover en esa direccion
        """
        initial_row, initial_col = self.selected_piece['position']
        rows = len(self.state)
        cols = len(self.state[0])

        if self.selected_piece['color'] == 'w':
            moves = [
                (-1, 0), (-1, -1), (-1, 1)
            ]
            # Si no hay nada adelante y es la primera vez que se mueve, puede moverse 2 casillas
            if self.is_pawn_first_move() and self.state[initial_row - 1][initial_col] == '--':
                moves.append((-2, 0))
            
        if self.selected_piece['color'] == 'b':
            moves = [
                (1, 0), (1, -1), (1, 1)
            ]
            # Si no hay nada adelante y es la primera vez que se mueve, puede moverse 2 casillas
            if self.is_pawn_first_move() and self.state[initial_row + 1][initial_col] == '--':
                moves.append((2, 0))

        for r, c in moves:
            row, col = initial_row + r, initial_col + c
            # Verifica si el movimiento que se esta por analizar es diagonal, ya que asi lo requiere self.is_pawn_valid_move
            if c != 0:
                diagonal = True
            else:
                diagonal = False
            if 0 <= row < rows and 0 <= col < cols:
                if self.is_pawn_valid_move(row, col, diagonal):
                    self.possible_moves.append((row, col))

    def is_valid_move(self, row:int, column:int)->bool:
        """Funcion que verifica si un movimiento es valido

        Args:
            row (int): fila del movimiento a analizar
            column (int): columna del movimiento a analizar

        Returns:
            bool: True si el movimiento es valido
            False si no lo es
        """
        piece_color = self.selected_piece['color']
        comparing_tile = self.state[row][column]

        # Si no hay nada en la casilla, el movimiento es valido
        if comparing_tile == '--':
            return True
        # Si hay una pieza en la casilla, pero es pieza enemiga, la casilla es valida
        # pero las que siguen no
        elif self.state[row][column][0] != piece_color:
            self.possible_moves.append((row, column))
            return False
        # Si hay una pieza del mismo color, la casilla no es valida
        else:
            return False

    def is_pawn_valid_move(self, row:int, column:int, diagonal:bool)->bool:
        # La logica del peon es tan compleja que tengo que hacer un is_valid aparte peon de mrd

        # Si no es diagonal, solo revisa que no haya nada en esa casilla
        # En ese caso, es casilla valida
        if not diagonal and self.state[row][column] == '--':
            return True
        # Si es diagonal, solo es valida si hay una pieza enemiga
        elif diagonal and self.state[row][column] != '--' and self.state[row][column][0] != self.selected_piece['color']:
            return True
        else:
            return False
        
    def is_pawn_first_move(self)->bool:
        """Funcion que define si es el primer movimiento de un peon

        Returns:
            bool: True si es el primer movimiento
            False si no lo es
        """
        row, col = self.selected_piece['position']
        # Si es pieza blanca y esta en la fila 6, es el primer movimiento
        if self.selected_piece['color'] == 'w' and row == 6:
            return True
        # Si es pieza negra y esta en la fila 1, es el primer movimiento
        elif self.selected_piece['color'] == 'b' and row == 1:
            return True
        else:
            return False
    def move_piece(self, mouse_pos:tuple)->None:
        """Funcion que mueve la pieza seleccionada

        Args:
            mouse_pos (tuple): posicion del mouse
        """
        x, y = mouse_pos
        row = y // self.tiles_width
        col = x // self.tiles_height

        if self.selected_piece != None and (row, col) in self.possible_moves:
            # Caso de enroque
            if self.selected_piece['piece'] == 'K' and abs(col - self.selected_piece['position'][1]) == 2:
                # Enroque corto
                if col > self.selected_piece['position'][1]:
                    self.state[row][7] = '--'
                    self.state[row][col - 1] = f"{self.selected_piece['color']}R"
                # Enroque largo
                else:
                    self.state[row][0] = '--'
                    self.state[row][col + 1] = f"{self.selected_piece['color']}R"
            
            self.state[self.selected_piece['position'][0]][self.selected_piece['position'][1]] = '--'
            self.state[row][col] = f"{self.selected_piece['color']}{self.selected_piece['piece']}"
            # Promocion de peones
            if self.selected_piece['piece'] == 'P':
                if (self.selected_piece['color'] == 'w' and row == 0) or (self.selected_piece['color'] == 'b' and row == 7):
                    self.selected_piece['piece'] = self.pawn_promotion(row, col)
                    self.state[row][col] = f"{self.selected_piece['color']}{self.selected_piece['piece']}"
            self.selected_piece = None
            self.possible_moves = []
            self.white_turn = not self.white_turn

    def pawn_promotion(self, row, col)->str:
        clock = pygame.time.Clock()
        if self.selected_piece['color'] == 'w':
            selection_rect = pygame.Rect(col * self.tiles_width, row * self.tiles_height, self.tiles_width, self.tiles_height*4)
        else:
            selection_rect = pygame.Rect(col * self.tiles_width, (row * self.tiles_height) - self.tiles_height * 3, self.tiles_width, self.tiles_height*4)
    
        pieces_buttons = [
            {'piece' : 'Q'},
            {'piece' : 'R'},
            {'piece' : 'B'},
            {'piece' : 'N'}
        ]

        initial_position_x, initial_position_y = selection_rect.x, selection_rect.y

        for i, piece in enumerate(pieces_buttons):
            image = pygame.image.load(f"assets/pieces/{self.selected_piece['color']}/{piece['piece']}.png")
            piece['surface'] = pygame.transform.scale(image, (self.tiles_width, self.tiles_height))
            piece['position'] = (initial_position_x, initial_position_y + i * self.tiles_height)
            piece['rect'] = piece['surface'].get_rect()
            piece['rect'].topleft = piece['position']
            piece['pressed'] = False


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for piece in pieces_buttons:
                        if piece['rect'].collidepoint(event.pos):
                            piece['pressed'] = not piece['pressed']

            pygame.draw.rect(self.screen, 'white', selection_rect)
            for piece in pieces_buttons:
                self.screen.blit(piece['surface'], piece['position'])
                if piece['pressed']:
                    return piece['piece']

            pygame.display.flip()
            clock.tick(60)
