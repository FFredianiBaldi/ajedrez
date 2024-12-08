import pygame, sys
from src.GUI.config import *
from src.GUI.Board import *
from src.logic.GameState import *

class Game:
    def __init__(self) -> None:
        """Configuraciones iniciales"""
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("PyChess")
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))

        self.board = Board(self.screen, 8, 8)

        self.clock = pygame.time.Clock()

        self.game_state = GameState(self.screen)

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            # Se dibuja el tablero
            self.board.draw_board()

            # El mouse cambia a la manito en caso de que el mouse pase por una pieza o movimientos posibles
            mouse_pos = pygame.mouse.get_pos()
            if self.game_state.is_mouse_over_piece_in_turn(mouse_pos) or self.game_state.is_mouse_over_possible_move(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            
            # Si los hay, dibuja los movimientos posibles
            if len(self.game_state.possible_moves) > 0:
                self.game_state.draw_possible_moves()

            # Dibuja las piezas
            self.game_state.draw_pieces()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Si se hace click, se mueve la pieza o se elige la pieza y se almacenan los posibles movimientos si corresponde
                        self.game_state.move_piece(mouse_pos)
                        self.game_state.select_piece(mouse_pos)
                        self.game_state.save_possible_moves()

                        # Si se mueven, el rey o torres se actualiza la variable que almacena esa informacion
                        # (no me gusta para nada como quedo esto, me siento yanderedev)
                        if self.game_state.state[0][4] != 'bK':
                            self.game_state.black_king_moved = True
                        if self.game_state.state[0][0] != 'bR':
                            self.game_state.long_black_rook_moved = True
                        if self.game_state.state[0][7] != 'bR':
                            self.game_state.short_black_rook_moved = True

                        if self.game_state.state[7][4] != 'wK':
                            self.game_state.white_king_moved = True
                        if self.game_state.state[7][0] != 'wR':
                            self.game_state.long_white_rook_moved = True
                        if self.game_state.state[7][7] != 'wR':
                            self.game_state.short_white_rook_moved = True

                        # Para depurar
                        if self.game_state.selected_piece != None:
                            print(f'piece: {self.game_state.selected_piece['piece']}')
                            print(f'row: {self.game_state.selected_piece['position'][0]}')
                            print(f'column: {self.game_state.selected_piece['position'][1]}')
                        else:
                            print('None')
                            
            pygame.display.flip()
            self.clock.tick(FPS)