import pygame
from src.GUI.functions import is_piece_selected_in_turn

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
    
    def select_piece(self, mouse_pos:tuple):
        x, y = mouse_pos
        column = x // self.tiles_width
        row = y // self.tiles_height

        piece = self.state[row][column]

        if piece != '--':
            color = list(piece)[0]
            if is_piece_selected_in_turn(self.white_turn, color):
                self.selected_piece = (row, column)
            else:
                self.selected_piece = None
        else:
            self.selected_piece = None