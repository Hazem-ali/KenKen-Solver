import pygame
import helpers


class Board:
    def __init__(self, number_of_blocks, block_size=50):

        # drawing metadata
        self.number_of_blocks = number_of_blocks
        self.block_size = block_size
        self.square_side = self.block_size * self.number_of_blocks
        self.screen = ''
        self.clock = 0

        # data to be written into boxes
        self.data_list = []
        self.law_dict = {}

    def setData(self, data):
        """
            Sets the data to be displayed on the board.
            :param data: The data to be displayed on the board.
            data contains a list of tuples. Each tuple contains the data of a single block (coordinates: tuple, color: tuple, value: str).
        """
        self.data_list = data
        return

    def getData(self):
        return self.data_list

    def setColors(self, colors: list):
        """
            Sets the colors for each cage on the board.
            colors is list of tuple, each tuple is (r, g, b)
        """
        self.colors = colors
        return

    def getColors(self):
        return self.colors

    def paintColorOnly(self, coordinates: tuple, color: tuple) -> None:

        # x, y are the coordinates of the rectangle: starts at the top left corner (0, 0)
        # x is the row number, y is the column number
        y, x = coordinates[0] - 1, coordinates[1] - 1
        Y, X = y * self.block_size, x * self.block_size

        # create the rectangle
        rect = pygame.Rect(Y, X, self.block_size, self.block_size)
        # draw the rectangle
        pygame.draw.rect(self.screen, color, rect)

        return

    def drawGrid(self):

        # draw laws
        self.drawLaws()

        # draw text
        if self.data_list:
            for coordinates, value in self.data_list:

                # x, y are the coordinates of the rectangle: starts at the top left corner (0, 0)
                # x is the row number, y is the column number
                y, x = coordinates[0] - 1, coordinates[1] - 1
                Y, X = y * self.block_size, x * self.block_size

                self.addText(text=value,
                             size=30,
                             coordinates=(Y + self.block_size / 2, X + self.block_size / 2))

        return

    def drawLaws(self):

        color_index = 0
        # for each cage
        # self.law_dict result of Create_Law_Positions()
        for cage_cells, law in self.law_dict.items():
            # ((2, 2), (3, 2)): '3 -'
            # for each cell in cage
            for index, cell in enumerate(cage_cells):
                # x, y are the coordinates of the rectangle: starts at the top left corner (0, 0)
                # x is the row number, y is the column number
                # print(cell)
                y, x = cell[0] - 1, cell[1] - 1
                Y, X = y * self.block_size, x * self.block_size

                # painting color
                self.paintColorOnly(cell, self.colors[color_index])

                # adding law text
                if index == 0:
                    self.addText(law, 15, (Y + 20, X + 10))

            color_index += 1

        return

    # def drawRect(self, coordinates: tuple, color: tuple, value='', corner_law='') -> None:
    #     """
    #         Draws a rectangle on the screen.
    #         :param coordinates: The coordinates of the rectangle. Coordinates start at top left (1, 1)
    #         :param color: The color of the rectangle.
    #         :param value: The value to be displayed on the rectangle.
    #         :param corner_law: The corner_law to be displayed on the border rectangle.

    #     """

    #     # x, y are the coordinates of the rectangle: starts at the top left corner (0, 0)
    #     # x is the row number, y is the column number
    #     y, x = coordinates[0] - 1, coordinates[1] - 1
    #     Y, X = y * self.block_size, x * self.block_size

    #     self.paintColorOnly(coordinates, color)

    #     # # Add text and adjusting its position
    #     self.addText(value,
    #                  30,
    #                  (Y + self.block_size / 2, X + self.block_size / 2))
    #     self.addText(corner_law, 15, (Y + 10, X+10))

    #     return

    def addText(self, text: str, size: int, coordinates: tuple) -> None:
        # Add text and adjusting its coordinates
        font = pygame.font.SysFont("comicsansms", size)
        text_widget = font.render(text, True, (0, 0, 0))
        text_widget_rect = text_widget.get_rect()
        text_widget_rect.center = coordinates

        self.screen.blit(text_widget, text_widget_rect)
        return

    def display(self):
        pygame.quit()
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.square_side, self.square_side))
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))
        # self.drawGrid()
        # pygame.display.update()
        # try:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             return
        # except:
        #     pygame.quit()
        #     return

        while True:
            self.drawGrid()
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
            except:
                pygame.quit()
                return

            pygame.display.update()


if __name__ == "__main__":
    board = Board(6, 80)

    solver = eval('''{((1,1),(1,2)):(5,6),((3,1),(2,1)):(3,6),((3,2),(2,2)):(4,1),((4,1),(4,2)):(4,5),((6,1),(6,2),(6,3),(5,1)): (2,3,1,1),((5,3),(5,2)):(6,2),((2,3),(2,4),(1,3),(1,4)):(5,4,4,3),((3,3),(4,3)):(2,3),((5,4),(6,4)):(5,6),((2,5),(1,5)):(3,2),((3,4),(3,5)):(1,6),((4,4),(4,5),(5,5)):(2,1,4),((1,6),(2,6),(3,6)):(1,2,5),((4,6),(5,6)):(6,3),((6,6),(6,5)):(4,5)}''')

    laws_example = \
        "(((1, 1), (1, 2)), '+', 11)\n"\
        "(((2, 1), (3, 1)), '/', 2)\n"\
        "(((2, 2), (3, 2)), '-', 3)\n"\
        "(((4, 1), (4, 2)), '*', 20)\n"\
        "(((5, 1), (6, 1), (6, 2), (6, 3)), '*', 6)\n"\
        "(((5, 2), (5, 3)), '/', 3)\n"\
        "(((1, 3), (1, 4), (2, 3), (2, 4)), '*', 240)\n"\
        "(((3, 3), (4, 3)), '*', 6)\n"\
        "(((5, 4), (6, 4)), '*', 30)\n"\
        "(((1, 5), (2, 5)), '*', 6)\n"\
        "(((3, 4), (3, 5)), '*', 6)\n"\
        "(((4, 4), (4, 5), (5, 5)), '+', 7)\n"\
        "(((1, 6), (2, 6), (3, 6)), '+', 8)\n"\
        "(((4, 6), (5, 6)), '/', 2)\n"\
        "(((6, 5), (6, 6)), '+', 9)\n"

    laws_dict = helpers.Create_Law_Positions(laws_example)

    board.setColors(helpers.Generate_Random_Colors(len(laws_dict)))

    board.law_dict = laws_dict
    
    # cells = helpers.Convert_Cages(solver)

    # board.setData(cells)
    board.display()
    
    cells = helpers.Convert_Cages(solver)

    board.setData(cells)
    board.display()



    # board.setData([

    #     # 4x4 board

    #     # ((0, 0), (0, 255, 150), "1"),
    #     # ((1, 0), (150, 255, 150), "4"),
    #     # ((2, 0), (0, 18, 150), "7"),
    #     # ((3, 0), (158, 255, 12), "7"),
    #     # ((0, 1), (255, 0, 150), "2"),
    #     # ((1, 1), (0, 255, 150), "M"),
    #     # ((2, 1), (0, 255, 150), "O"),
    #     # ((3, 1), (0, 255, 150), "O"),
    #     # ((0, 2), (0, 255, 150), "F"),
    #     # ((1, 2), (255, 255, 150), "T"),
    #     # ((2, 2), (0, 255, 150), "Y"),
    #     # ((3, 2), (0, 255, 150), "Y"),
    #     # ((0, 3), (0, 255, 150), "K"),
    #     # ((1, 3), (0, 255, 150), "N"),
    #     # ((2, 3), (0, 255, 150), "K"),
    #     # ((3, 3), (0, 255, 0), "N"),

    #     # 3x3 board
    #     ((1, 1), (12, 0, 150), "X"),
    #     ((2, 1), (150, 255, 150), '4'),
    #     ((3, 1), (0, 18, 150), "7"),
    #     ((4, 1), (158, 255, 12), "7"),
    #     ((1, 2), (255, 0, 150), "2"),
    #     ((2, 2), (0, 255, 150), "M"),
    #     ((3, 2), (0, 255, 150), "O"),
    #     ((4, 2), (0, 255, 150), "O"),
    #     ((1, 3), (0, 255, 150), "F"),
    #     ((2, 3), (255, 255, 150), "T"),
    #     ((3, 3), (0, 255, 150), "Y"),
    #     ((4, 3), (0, 255, 150), "Y"),

    # ])

    # board.display()

    # Drawing kenken borders

    # # Draw the top border
    # pygame.draw.line(self.screen, (0, 0, 0), (Y, X), (Y + self.block_size, X))

    # # Draw the bottom border
    # pygame.draw.line(self.screen, (0, 0, 0), (Y, X + self.block_size), (Y + self.block_size, X + self.block_size))

    # # Draw the left border
    # pygame.draw.line(self.screen, (0, 0, 0), (Y, X), (Y, X + self.block_size))

    # # Draw the right border
    # pygame.draw.line(self.screen, (0, 0, 0), (Y + self.block_size, X), (Y + self.block_size, X + self.block_size))
