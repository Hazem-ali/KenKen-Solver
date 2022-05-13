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

        # for x in range(0, int(self.square_side / self.block_size)):
        #     for y in range(0, int(self.square_side / self.block_size)):

        #         X, Y = x * self.block_size, y * self.block_size
        #         # x is the row, y is the column

        #         if x == 0 and y == 2:
        #             drawRect((x, y), BLACK, "9")
        #         else:
        #             drawRect((x, y), (0, 255, 150), "X")

        return

    def drawRect(self, coordinates: tuple, color: tuple, digit: str) -> None:
        """
            Draws a rectangle on the screen.
            :param coordinates: The coordinates of the rectangle.
            :param color: The color of the rectangle.
            :param digit: The digit to be displayed on the rectangle.
        """
        # x, y are the coordinates of the rectangle: starts at the top left corner (0, 0)
        # x is the row, y is the column
        x, y = coordinates
        X, Y = x * self.block_size, y * self.block_size

        # create the rectangle
        rect = pygame.Rect(X, Y, self.block_size, self.block_size)

        # Add text
        font = pygame.font.SysFont("comicsansms", 30)
        text = font.render(digit, True, (0, 0, 0))

        # center the text
        textRect = text.get_rect()
        textRect.center = (X + self.block_size / 2, Y + self.block_size / 2)

        # Draw the rectangle
        pygame.draw.rect(self.screen, color, rect)
        self.screen.blit(text, textRect)

        return

    def run(self):

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.square_side, self.square_side))
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))

        while True:
            self.drawGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

        return


if __name__ == "__main__":
    board = Board(3,80)


    board.setData([
        ((0, 0), (0, 255, 150), "1"),
        ((0, 1), (0, 255, 150), "2"),
        ((0, 2), (0, 255, 150), "F"),
        ((1, 0), (150, 255, 150), "4"),
        ((1, 1), (0, 255, 150), "M"),
        ((1, 2), (255, 255, 150), "T"),
        ((2, 0), (0, 18, 150), "7"),
        ((2, 1), (0, 255, 150), "O"),
        ((2, 2), (0, 255, 150), "Y"),


    ])
    board.run()


# # WORKING
# BLACK = (0, 0, 0)
# WHITE = (200, 200, 200)
# NO_OF_BLOCKS = 9
# BLOCK_SIZE = 50
# WINDOW_HEIGHT = NO_OF_BLOCKS * BLOCK_SIZE
# WINDOW_WIDTH = NO_OF_BLOCKS * BLOCK_SIZE


# def main():
#     global SCREEN, CLOCK
#     pygame.init()
#     SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#     CLOCK = pygame.time.Clock()
#     SCREEN.fill(WHITE)

#     while True:
#         drawGrid()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         pygame.display.update()


# def drawRect(coordinates: tuple, color: tuple, digit: str) -> None:
#     """
#         Draws a rectangle on the screen.
#         :param coordinates: The coordinates of the rectangle.
#         :param color: The color of the rectangle.
#         :param digit: The digit to be displayed on the rectangle.
#     """

#     x, y = coordinates
#     X, Y = x * BLOCK_SIZE, y * BLOCK_SIZE

#     rect = pygame.Rect(X, Y, BLOCK_SIZE, BLOCK_SIZE)

#     # Add text
#     font = pygame.font.SysFont("comicsansms", 30)
#     text = font.render(digit, True, BLACK)

#     # center the text
#     textRect = text.get_rect()
#     textRect.center = (X + BLOCK_SIZE / 2, Y + BLOCK_SIZE / 2)

#     # Draw the rectangle
#     pygame.draw.rect(SCREEN, color, rect)
#     SCREEN.blit(text, textRect)

#     return


# def drawGrid():
#     for x in range(0, int(WINDOW_WIDTH / BLOCK_SIZE)):
#         for y in range(0, int(WINDOW_HEIGHT / BLOCK_SIZE)):

#             X, Y = x * BLOCK_SIZE, y * BLOCK_SIZE
#             # x is the row, y is the column

#             if x == 0 and y == 2:
#                 drawRect((x, y), BLACK, "9")
#             else:
#                 drawRect((x, y), (0, 255, 150), "X")

#             # if x == 0 and y == 2:
#             #     drawRect((x, y), BLACK, "9")
#             # #     pygame.draw.rect(SCREEN, BLACK, (X, Y, BLOCK_SIZE, BLOCK_SIZE))
#             # #     # add text
#             # #     font = pygame.font.SysFont("comicsansms", 30)
#             # #     text = font.render("X", True, WHITE)

#             # #     # center the text
#             # #     textRect = text.get_rect()
#             # #     textRect.center = (X + BLOCK_SIZE / 2, Y + BLOCK_SIZE / 2)
#             # #     SCREEN.blit(text, textRect)

#             # #     # SCREEN.blit(text, (X,Y))
#             # else:
#             #     # print(x, y)
#             #     # rect = pygame.Rect(X, Y, BLOCK_SIZE, BLOCK_SIZE)

#             #     # # pygame.draw.rect(SCREEN, BLACK, rect)
#             #     # pygame.draw.rect(SCREEN, (255, 0, 0), rect)
#             #     drawRect((x, y), (0, 255, 150), "X")
#             # # pygame.draw.rect(, BLACK, rect,1)


# if __name__ == "__main__":
#     main()
