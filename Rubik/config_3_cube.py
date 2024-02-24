
# Constants
WINDOW_SIZE = 800
ROTATE_SPEED = 0.1
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
CUBE_SIZE = 30
CUBE_GAP = 2
CUBE_2D_START_X = (WINDOW_SIZE - (12 * CUBE_SIZE + 11 * CUBE_GAP)) // 2
CUBE_2D_Y_OFFSET = 150
CUBE_2D_START_Y = WINDOW_SIZE - (9 * CUBE_SIZE + 8 * CUBE_GAP) - CUBE_2D_Y_OFFSET
row_col = 3
surface_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 0, 255)]
# Cube surfaces definition
cube_surfaces = [
    [0, 1, 2, 3],    # Front face
    [1, 5, 6, 2],    # Right face
    [5, 4, 7, 6],    # Back face
    [4, 0, 3, 7],    # Left face
    [4, 5, 1, 0],    # Bottom face
    [3, 2, 6, 7]     # Top face
]
