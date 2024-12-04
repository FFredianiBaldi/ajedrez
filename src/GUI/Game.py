import pygame, sys
from src.GUI.config import *
from src.GUI.Board import *
from src.logic.GameState import *

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("PyChess")

        self.board = Board(self.screen, 8, 8)

        self.clock = pygame.time.Clock()

        self.game_state = GameState(self.screen)

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.game_state.select_piece(mouse_pos)
                        if self.game_state.selected_piece != None:
                            print(f'row: {self.game_state.selected_piece[0]} column: {self.game_state.selected_piece[1]}')
                        else:
                            print('None')
            self.board.draw_board()
            self.game_state.draw_pieces()


            mouse_pos = pygame.mouse.get_pos()
            if self.game_state.is_mouse_over_piece_in_turn(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



            pygame.display.flip()
            self.clock.tick(FPS)