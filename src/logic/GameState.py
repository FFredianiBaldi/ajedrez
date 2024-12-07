import pygame
from src.GUI.functions import *

class GameState:
    def __init__(self, screen:pygame.Surface) -> None:
        self.state = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]

        self.white_turn = True

        self.screen = screen
        self.tiles_width = self.screen.get_width() // 8
        self.tiles_height = self.screen.get_height() // 8

        self.selected_piece = None
        self.possible_moves = []

        self.white_king_moved = False
        self.black_king_moved = False

        self.short_black_rook_moved = False
        self.long_black_rook_moved = False

        self.short_white_rook_moved = False
        self.long_white_rook_moved = False
    def draw_pieces(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                color, piece = list(self.state[i][j])
                if color != '-':
                    piece_img = pygame.image.load(f"assets/pieces/{color}/{piece}.png")
                    piece_img = pygame.transform.scale(piece_img, (self.tiles_width, self.tiles_height)).convert_alpha()

                    self.screen.blit(piece_img, (j * self.tiles_width, i * self.tiles_height))

    def is_mouse_over_piece_in_turn(self, mouse_pos:tuple)->bool:
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
        x, y = mouse_pos
        column = x // self.tiles_width
        row = y // self.tiles_height

        if (column, row) in self.possible_moves:
            return True
        return False
    
    def select_piece(self, mouse_pos:tuple):
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
        for row, col in self.possible_moves:
            x, y = col * self.tiles_width, row * self.tiles_height
            position_color = get_position_color((row, col))
            color = (245, 219, 195) if position_color == "white" else (187, 87, 70)
            pygame.draw.rect(self.screen, color, (x, y, self.tiles_width, self.tiles_height))


    
    def horizontal_vertical_possible_moves(self) -> None:
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
            if 0 <= row < rows and 0 <= col < cols:
                if self.is_valid_move(row, col):
                    self.possible_moves.append((row, col))

    def king_possible_moves(self):
        initial_row, initial_col = self.selected_piece['position']
        rows = len(self.state)
        cols = len(self.state[0])

        moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        if self.selected_piece['color'] == 'w' and not self.white_king_moved:
            if not self.short_white_rook_moved and self.state[7][5] == '--':
                moves.append((0, 2))
            if not self.long_white_rook_moved and self.state[7][2] == self.state[7][3] == '--':
                moves.append((0, -2))

        elif self.selected_piece['color'] == 'b' and not self.black_king_moved:
            if not self.short_black_rook_moved and self.state[0][5] == '--':
                moves.append((0, 2))
            if not self.long_black_rook_moved and self.state[0][2] == self.state[0][3] == '--':
                moves.append((0, -2))
        

        for r, c in moves:
            row, col = initial_row + r, initial_col + c
            if 0 <= row < rows and 0 <= col < cols:
                if self.is_valid_move(row, col):
                    self.possible_moves.append((row, col))
    
    def pawn_possible_moves(self):
        initial_row, initial_col = self.selected_piece['position']
        rows = len(self.state)
        cols = len(self.state[0])

        if self.selected_piece['color'] == 'w':
            moves = [
                (-1, 0), (-1, -1), (-1, 1)
            ]
            if self.is_pawn_first_move() and self.state[initial_row - 1][initial_col] == '--':
                moves.append((-2, 0))
            
        if self.selected_piece['color'] == 'b':
            moves = [
                (1, 0), (1, -1), (1, 1)
            ]
            if self.is_pawn_first_move() and self.state[initial_row + 1][initial_col] == '--':
                moves.append((2, 0))

        for r, c in moves:
            row, col = initial_row + r, initial_col + c
            if c != 0:
                diagonal = True
            else:
                diagonal = False
            if 0 <= row < rows and 0 <= col < cols:
                if self.is_pawn_valid_move(row, col, diagonal):
                    self.possible_moves.append((row, col))

    def is_valid_move(self, row:int, column:int)->bool:
        piece_color = self.selected_piece['color']
        comparing_tile = self.state[row][column]

        if comparing_tile == '--':
            return True
        elif self.state[row][column][0] != piece_color:
            self.possible_moves.append((row, column))
            return False
        else:
            return False

    def is_pawn_valid_move(self, row:int, column:int, diagonal:bool)->bool:
        # La logica del peon es tan compleja que tengo que hacer un is_valid aparte peon de mrd
        if not diagonal and self.state[row][column] == '--':
            return True
        elif diagonal and self.state[row][column] != '--' and self.state[row][column][0] != self.selected_piece['color']:
            return True
        else:
            return False
        
    def is_pawn_first_move(self):
        row, col = self.selected_piece['position']
        if self.selected_piece['color'] == 'w' and row == 6:
            return True
        elif self.selected_piece['color'] == 'b' and row == 1:
            return True
        else:
            return False
    def move_piece(self, mouse_pos:tuple)->None:
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
            
            # Promocion de peones
            elif self.selected_piece['piece'] == 'P':
                if (self.selected_piece['color'] == 'w' and row == 0) or (self.selected_piece['color'] == 'b' and row == 7):
                    self.selected_piece['piece'] = 'Q'
            self.state[self.selected_piece['position'][0]][self.selected_piece['position'][1]] = '--'
            self.state[row][col] = f"{self.selected_piece['color']}{self.selected_piece['piece']}"
            self.selected_piece = None
            self.possible_moves = []
            self.white_turn = not self.white_turn