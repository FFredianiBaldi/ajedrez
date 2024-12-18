import pygame

class Board:
    def __init__(self, screen:pygame.Surface, columns:int, rows:int) -> None:
        """Constructor

        Args:
            screen (pygame.Surface): ventana donde se va a dibujar todo
            columns (int): cantidad de columnas
            rows (int): cantidad de filas
        """
        self.columns = columns
        self.rows = rows
        self.screen = screen

        self.tiles_width = self.screen.get_width() // 8
        self.tiles_height = self.screen.get_height() // 8
        
    def draw_board(self):
        """Funcion que dibuja el tablero en pantalla
        la recorre como una matriz
        """
        for row in range(self.rows):
            for column in range(self.columns):
                if (row + column) % 2 == 0:
                    color = (234,240,238)
                else:
                    color = (109,135,186)

                x = column * self.tiles_width
                y = row * self.tiles_height

                pygame.draw.rect(self.screen, color, (x, y, self.tiles_width, self.tiles_height))