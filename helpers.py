# Helper functions for the gui

def Generate_Random_Colors(num_colors, color_type='rgb'):
    """ Generate random colors in HEX or RGB ( default ) """
    import random
    # transparency = 150  # alpha: 150 is 50% transparent

    hex_colors = ["#"+''.join
                  ([random.choice('0123456789ABCDEF')for _ in range(6)])
                  for _ in range(num_colors)]

    rgb_colors = [(int(hex_colors[i][1:3], 16),
                   int(hex_colors[i][3:5], 16),
                   int(hex_colors[i][5:7], 16))
                  for i in range(num_colors)]

    if color_type == 'hex':
        return hex_colors
    return rgb_colors


def Cage_To_Cells(cage_positions: tuple, cage_values: tuple, color: tuple) -> list:
    """
    Convert one cage to a list of cells
    """
    cells = []

    for i in range(len(cage_positions)):
        cell = (cage_positions[i], color, str(cage_values[i]))
        cells.append(cell)

    return cells


def Convert_Cages(cages: dict) -> list:
    """
    Convert a dictionary of cages to a list of cells
    """
    cells = []
    no_of_cages = len(cages)
    color_list = Generate_Random_Colors(no_of_cages)

    color_index = 0
    for cage_positions, cage_values in cages.items():
        cage_cells = Cage_To_Cells(
            cage_positions, cage_values, color_list[color_index])
        cells.extend(cage_cells)
        color_index += 1
    return cells
