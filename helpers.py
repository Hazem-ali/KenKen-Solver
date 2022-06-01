# Helper functions for the gui

def Generate_Random_Colors(num_colors, color_type='rgb'):
    """ Generate random colors in HEX or RGB ( default ) """
    import random
    # transparency = 150  # alpha: 150 is 50% transparent

    hex_colors = ["#"+''.join
                  ([random.choice('3456789ABCDEF')for _ in range(6)])
                  for _ in range(num_colors)]

    rgb_colors = [(int(hex_colors[i][1:3], 16),
                   int(hex_colors[i][3:5], 16),
                   int(hex_colors[i][5:7], 16))
                  for i in range(num_colors)]

    if color_type == 'hex':
        return hex_colors
    return rgb_colors


def Cage_To_Cells(cage_positions: tuple, cage_values) -> list:
    """
    Convert one cage to a list of tuples, eact tuple has a coordinate and a corresponding value
    """
    cells = []
    # print(cage_positions[0])
    # print(cage_values)

    # if type(cage_values) == type(tuple()):

    # then it is solver dict
    # {((1, 2), (1, 3)): (5,6)}
    for i in range(len(cage_positions)):
        # print(i)
        cell = (cage_positions[i], str(cage_values[i]))
        cells.append(cell)

    # else:
    #     # then it is for laws dict
    #     # {((1, 1), (1, 2)): '11 +'}
    #     for i in range(len(cage_positions)):
    #         cell = tuple()
    #         if i == 0:
    #             cell = (cage_positions[i], str(cage_values))
    #         else:
    #             cell = (cage_positions[i], '')
    #         cells.append(cell)

    return cells


def Convert_Cages(cages: dict) -> list:
    """
    Convert a dictionary of cages with values to a list of cells
    """
    cells = []

    for cage_positions, cage_values in cages.items():
        
        cage_cells = Cage_To_Cells(cage_positions, cage_values)
        cells.extend(cage_cells)
        
    return cells


def Create_Law_Positions(data: str) -> dict:
    # create a dict with first position and combination of operation and result
    # example = \
    #     "(((1, 1), (1, 2)), '+', 11)\n"\
    #     "(((2, 1), (3, 1)), '/', 2)\n"\
    #     "(((2, 2), (3, 2)), '-', 3)\n"\
    #     "(((4, 1), (4, 2)), '*', 20)\n"\
    #     "(((5, 1), (6, 1), (6, 2), (6, 3)), '*', 6)\n"\
    #     "(((5, 2), (5, 3)), '/', 3)\n"\
    #     "(((1, 3), (1, 4), (2, 3), (2, 4)), '*', 240)\n"\
    #     "(((3, 3), (4, 3)), '*', 6)\n"\
    #     "(((5, 4), (6, 4)), '*', 30)\n"\
    #     "(((1, 5), (2, 5)), '*', 6)\n"\
    #     "(((3, 4), (3, 5)), '*', 6)\n"\
    #     "(((4, 4), (4, 5), (5, 5)), '+', 7)\n"\
    #     "(((1, 6), (2, 6), (3, 6)), '+', 8)\n"\
    #     "(((4, 6), (5, 6)), '/', 2)\n"\
    #     "(((6, 5), (6, 6)), '+', 9)\n"

    myData = data.splitlines()

    result = {}

    for item in myData:
        extracted = eval(item)
        result[extracted[0]] = f"{extracted[2]} {extracted[1]}"

    return result
