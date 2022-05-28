"""board.py"""
from typing import List, Tuple, Optional, Dict
import pygame
import helpers

COLORTYPE = Tuple[float, float, float]
class Board:
    """
        KenKen Board
    """
    def __init__(
        self: object,
        number_of_blocks: int,
        block_size: Optional[int]=50):
        """
            Initializes the board.
            :param number_of_blocks (int): The number of blocks in the board.
            :param block_size (int): The size of the blocks.
        """
        # drawing metadata
        self.number_of_blocks = number_of_blocks
        self.block_size = block_size
        self.square_side = self.block_size * self.number_of_blocks
        self.screen = ''
        self.clock = 0

        self.colors = None

        # data to be written into boxes
        self.data_list = []
        self.law_dict = {}

    def setData(
        self: object,
        data: List[
            Tuple[
                Tuple[int, int],
                Optional[COLORTYPE],
                str]]):
        """
            Sets the data to be displayed on the board.
            :param data: The data to be displayed on the board.
                data contains a list of tuples. Each tuple contains the data of a single block
                (coordinates: tuple, color: tuple, value: str).
        """
        self.data_list = data

    def getData(
        self: object) \
            -> List[
                Tuple[
                    Tuple[int, int],
                    COLORTYPE,
                    str]]:
        """
            Returns the data of the board.
            :return: The data of the board.
        """
        return self.data_list

    def setColors(
        self:object,
        colors: List[COLORTYPE]):
        """
            Sets the colors for each cage on the board.
            colors is list of tuple, each tuple is (r, g, b)
        """
        self.colors = colors
        return

    def getColors(
        self: object)\
            -> List[COLORTYPE]:
        """
            Returns the colors of the cages.
        """
        return self.colors

    def setLaws(
        self: object,
        laws: Dict[Tuple[Tuple[int, int]], str]):
        """
            Sets the laws for each cage on the board.
            laws is a dictionary of tuples, each tuple is (x, y, value)
        """
        self.law_dict = laws

    def getLaws(
        self: object)\
            -> Dict[Tuple[Tuple[int, int]], str]:
        """
            Returns the laws of the board.
        """
        return self.law_dict

    def paint_color_only(
        self: object,
        coordinates: Tuple[int, int],
        color: COLORTYPE) -> None:
        """
            Paints a square with a given color.
            :param coordinates: The coordinates of the square.
            :param color: The color of the square.
        """
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(
                (coordinates[0]-1) * self.block_size,
                (coordinates[1]-1) * self.block_size,
                self.block_size,
                self.block_size))



        # x, y are the coordinates of the rectangle: starts at the top left corner (0, 0)
        # x is the row number, y is the column number
        # y, x = coordinates[0] - 1, coordinates[1] - 1
        # Y, X = y * self.block_size, x * self.block_size

        # # create the rectangle
        # rect = pygame.Rect(Y, X, self.block_size, self.block_size)
        # # draw the rectangle
        # pygame.draw.rect(self.screen, color, rect)

    def drawGrid(
        self: object):
        """
            Draws the grid on the screen.
        """

        # draw laws
        self.drawLaws()

        # draw text
        if self.data_list:
            for coordinates, value in self.data_list:
                self.addText(
                    text=value,
                    size=15,
                    coordinates= (
                        (coordinates[0] -1) * self.block_size + self.block_size // 2,
                        (coordinates[1] -1) * self.block_size + self.block_size // 2)
                        )

                # x, y are the coordinates of the rectangle: starts at the top left corner (0, 0)
                # x is the row number, y is the column number
                # y, x = coordinates[0] - 1, coordinates[1] - 1
                # Y, X = y * self.block_size, x * self.block_size

                # self.addText(text=value,
                #              size=30,
                #              coordinates=(Y + self.block_size / 2, X + self.block_size / 2))

    def drawLaws(
        self: object):
        """
            Draws the laws on the screen.
        """
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
                self.paint_color_only(cell, self.colors[color_index])

                # adding law text
                if index == 0:
                    self.addText(law, 15, (Y + 20, X + 10))

            color_index += 1

    # def drawRect(self, coordinates: tuple, color: tuple, value='', corner_law=''):
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

    #     self.paint_color_only(coordinates, color)

    #     # # Add text and adjusting its position
    #     self.addText(value,
    #                  30,
    #                  (Y + self.block_size / 2, X + self.block_size / 2))
    #     self.addText(corner_law, 15, (Y + 10, X+10))

    def addText(
        self:object,
        text: str,
        size: int,
        coordinates: Tuple[int, int],
        text_color: COLORTYPE = (0, 0, 0)):
        """
            Adds text to the screen.
            :param text: The text to be displayed.
            :param size: The size of the text.
            :param coordinates: The coordinates of the text.
        """
        # Add text and adjusting its coordinates
        font = pygame.font.SysFont("comicsansms", size)
        text_widget = font.render(text, True, text_color)
        text_widget_rect = text_widget.get_rect()
        text_widget_rect.center = coordinates

        self.screen.blit(text_widget, text_widget_rect)

    def display(
        self: object):

        pygame.quit()
        pygame.init()
        pygame.display.set_caption("KenKen")
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

    # *random generated from repo
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
    # laws_example is the random generated laws that we need to solve
    # this (((6, 5), (6, 6)), '+', 9) we convert it into dict {((6, 5),
    # (6, 6)): "9 +"} using Create_Law_Positions function

    # * solved from repo
    solver = eval('''{((1,1),(1,2)):(5,6),((3,1),(2,1)):(3,6),((3,2),(2,2)):(4,1)\
        ,((4,1),(4,2)):(4,5),((6,1),(6,2),(6,3),(5,1)): (2,3,1,1),((5,3),(5,2)):(6,2)\
        ,((2,3),(2,4),(1,3),(1,4)):(5,4,4,3),((3,3),(4,3)):(2,3),((5,4),(6,4)):(5,6)\
        ,((2,5),(1,5)):(3,2),((3,4),(3,5)):(1,6),((4,4),(4,5),(5,5)):(2,1,4),\
        ((1,6),(2,6),(3,6)):(1,2,5),((4,6),(5,6)):(6,3),((6,6),(6,5)):(4,5)}''')
    # solver is a dict that contains positions and their corresponding values

    # * wrapper function to get cage values and cage cells
    laws_dict = helpers.Create_Law_Positions(laws_example)
    # {((1, 1), (1, 2)): '11 +',...}

    board.setColors(helpers.Generate_Random_Colors(len(laws_dict)))

    board.setLaws(laws_dict)
    # print(board.getLaws())

    # Display laws without values
    board.display()

    # Display laws with values

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
