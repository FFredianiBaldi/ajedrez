import pygame
from src.GUI.functions import *

class GameState:
    def __init__(self, screen:pygame.Surface) -> None:
        self.state = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','wR','--','--','--','--'],
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


    def draw_possible_moves(self):
        for row, col in self.possible_moves:
            x, y = col * self.tiles_width, row * self.tiles_height
            position_color = get_position_color((row, col))
            color = (245, 219, 195) if position_color == "white" else (187, 87, 70)
            pygame.draw.rect(self.screen, color, (x, y, self.tiles_width, self.tiles_height))


    
    def rook_possible_moves(self) -> None:
        row, col = self.selected_piece['position']
        self.possible_moves = []

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
        for r in range(row - 1, -1, -1):
            if not self.is_valid_move(r, col):
                break
            self.possible_moves.append((r, col))
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
