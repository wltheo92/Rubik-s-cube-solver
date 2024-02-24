
import pygame
###############
# Button class
class Button:
    def __init__(self, x, y, width, height, text, action, image_file):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.colourAccent = (180, 180, 180)
        self.image_file = image_file
        self.suffix = 1
        self.image = pygame.image.load(f'images//{self.image_file}({self.suffix}).jpg')

    # Mouse over event handler
    def mouse_over(self, pos):
        # Change the colour accent so the button changes colour with movement
        if self.is_over(pos):
            self.colourAccent = (150, 150, 150)
            self.suffix = 2
        else:
            self.colourAccent = (180, 180, 180)
            self.suffix = 1
        self.image = pygame.image.load(f'images//{self.image_file}({self.suffix}).jpg')

    def draw(self, win):
        # Draw the accent colour as the main colour so it responds to movement
        pygame.draw.rect(win, (100, 100, 100, 10), pygame.Rect(self.x+2, self.y+2, self.width, self.height),0,5)
        pygame.draw.rect(win, self.colourAccent, pygame.Rect(self.x, self.y, self.width, self.height),0,5)
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height), 2, 5)
        font = pygame.font.SysFont('Arial', 20)
        if self.text:
            text_surf = font.render(self.text, True, (0, 0, 0))
            win.blit(self.image, (self.x+5, self.y+5))
            win.blit(text_surf, (self.x + 40 + (self.width - 45 - text_surf.get_width()) // 2,
                             self.y + (self.height - text_surf.get_height()) // 2))
        else:
            win.blit(self.image, (self.x + (self.width - self.image.get_width()) // 2,
                            self.y + (self.height - self.image.get_height()) // 2))

    # Checks if a position is within the button
    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height
