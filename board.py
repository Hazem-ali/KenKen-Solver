import pygame


class Board:
    def __init__(self, number_of_blocks, block_size=50):
        self.number_of_blocks = number_of_blocks
        self.block_size = block_size
        self.square_side = self.block_size * self.number_of_blocks
        self.screen = ''
        self.clock = 0
        self.data_list = []

    def setData(self, data):
        """
            Sets the data to be displayed on the board.
            :param data: The data to be displayed on the board.
            data contains a list of tuples. Each tuple contains the data of a single block (coordinates: tuple, color: tuple, digit: str).
        """
        self.data_list = data
        return

    def getData(self):
        return self.data_list

    def drawGrid(self):

        for element in self.data_list:
            coordinates, color, digit = element
            self.drawRect(coordinates, color, digit)

        return

    def drawRect(self, coordinates: tuple, color: tuple, digit: str) -> None:
        """
            Draws a rectangle on the screen.
            :param coordinates: The coordinates of the rectangle. Coordinates start at top left (1, 1)
            :param color: The color of the rectangle.
            :param digit: The digit to be displayed on the rectangle.
        """

        # x, y are the coordinates of the rectangle: starts at the top left corner (0, 0)
        # x is the row number, y is the column number
        y, x = coordinates[0] - 1, coordinates[1] - 1
        Y, X = y * self.block_size, x * self.block_size

        # create the rectangle
        rect = pygame.Rect(Y, X, self.block_size, self.block_size)

        # Add text
        font = pygame.font.SysFont("comicsansms", 30)
        text = font.render(digit, True, (0, 0, 0))

        # center the text
        textRect = text.get_rect()
        textRect.center = (Y + self.block_size / 2, X + self.block_size / 2)

        # add edge text
        smaller_font = pygame.font.SysFont("comicsansms", 15)
        edge_text = smaller_font.render("5/", True, (0, 0, 0))
        edge_text_rect = edge_text.get_rect()
        edge_text_rect.center = (Y + 10, X+10)

        # draw the rectangle
        pygame.draw.rect(self.screen, color, rect)

        # Draw the rectangle
        pygame.draw.rect(self.screen, color, rect)
        self.screen.blit(text, textRect)
        self.screen.blit(edge_text, edge_text_rect)

        # Drawing kenken borders


        # # Draw the top border
        # pygame.draw.line(self.screen, (0, 0, 0), (Y, X), (Y + self.block_size, X))

        # # Draw the bottom border
        # pygame.draw.line(self.screen, (0, 0, 0), (Y, X + self.block_size), (Y + self.block_size, X + self.block_size))

        # # Draw the left border
        # pygame.draw.line(self.screen, (0, 0, 0), (Y, X), (Y, X + self.block_size))

        # # Draw the right border
        # pygame.draw.line(self.screen, (0, 0, 0), (Y + self.block_size, X), (Y + self.block_size, X + self.block_size))


        return

    def display(self):
        pygame.quit()
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.square_side, self.square_side))
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))
        while True:
            self.drawGrid()
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
            except:
                return
                
            pygame.display.update()



if __name__ == "__main__":
    board = Board(3, 80)

    board.setData([

        # 4x4 board

        # ((0, 0), (0, 255, 150), "1"),
        # ((1, 0), (150, 255, 150), "4"),
        # ((2, 0), (0, 18, 150), "7"),
        # ((3, 0), (158, 255, 12), "7"),
        # ((0, 1), (255, 0, 150), "2"),
        # ((1, 1), (0, 255, 150), "M"),
        # ((2, 1), (0, 255, 150), "O"),
        # ((3, 1), (0, 255, 150), "O"),
        # ((0, 2), (0, 255, 150), "F"),
        # ((1, 2), (255, 255, 150), "T"),
        # ((2, 2), (0, 255, 150), "Y"),
        # ((3, 2), (0, 255, 150), "Y"),
        # ((0, 3), (0, 255, 150), "K"),
        # ((1, 3), (0, 255, 150), "N"),
        # ((2, 3), (0, 255, 150), "K"),
        # ((3, 3), (0, 255, 0), "N"),

        # 3x3 board
        ((1, 1), (12, 0, 150), "X"),
        ((2, 1), (150, 255, 150), '4'),
        ((3, 1), (0, 18, 150), "7"),
        ((4, 1), (158, 255, 12), "7"),
        ((1, 2), (255, 0, 150), "2"),
        ((2, 2), (0, 255, 150), "M"),
        ((3, 2), (0, 255, 150), "O"),
        ((4, 2), (0, 255, 150), "O"),
        ((1, 3), (0, 255, 150), "F"),
        ((2, 3), (255, 255, 150), "T"),
        ((3, 3), (0, 255, 150), "Y"),
        ((4, 3), (0, 255, 150), "Y"),



    ])

    board.display()
