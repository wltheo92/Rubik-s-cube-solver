from button import *
import pygame
from solver import *

# A renderer for a calculated solution
class GuideRenderer:
        def __init__(self, x, y, cubeModel, moveCallback):
                self.x = x
                self.y = y 
                self.cubeModel = cubeModel
                # Callback to use when moving the cube
                self.moveCallback = moveCallback

                # buttons
                self.toggle = Button(x, y, 100, 50, "Guide", self.enable, 'guide')
                self.solveButton = Button(x, y+150, 140, 50, "Solve Next", self.solveNext, 'next')

                # Enable by default
                self.enable()

                # Set up the solution environment
                self.moves = None
                self.refreshSolution()

                # Incorrect moves count to know when to reset the solution
                self.incorrect = 0

        # Solves the next move
        def solveNext(self):
                move = self.nextMove()
                if move:
                        self.moveCallback(str(move))

        # Returns a list of event listeners to send events to
        def getListeners(self):
                return [self.toggle, self.solveButton]

        # Enables the renderer
        def enable(self):
                # Change the button
                self.toggle.text = "Hide"
                self.enabled = True
                self.toggle.action = self.disable
                self.toggle.image_file = 'hide'
                self.toggle.image = pygame.image.load(f'images//{self.toggle.image_file}({self.toggle.suffix}).jpg')
                
                # Make sure the solution is up to date
                self.refreshSolution()

        def disable(self):
                # change the button
                self.enabled = False
                self.toggle.text = "Guide"
                self.toggle.action = self.enable
                self.toggle.image_file = 'guide'
                self.toggle.image = pygame.image.load(f'images//{self.toggle.image_file}({self.toggle.suffix}).jpg')

        # Retrieves the next move of the solution
        def nextMove(self):
                # By default have no key
                key = None
                # Just retrieve th efirst key in order
                for key in self.moves:
                        break
                if key == None: return None
                # Get the first move of the next section
                return self.moves[key][0][0]
        
        # Adds a move in front of the move list
        def prependMove(self, move):
                nextMove = self.nextMove()

                # If there is no moves, create a new section called AUF
                if len(self.moves) == 0:
                        self.moves["auf"] = [[]]

                # Get the first key
                for key in self.moves:
                        break

                # Check if the new move can combine with the next move
                if nextMove and nextMove.face == move.face:
                        if nextMove.double:
                                nextMove.double = False
                                nextMove.invert = move.invert
                        elif nextMove.invert == move.invert:
                                nextMove.double = True
                                nextMove.invert = False
                else:
                        # Prepend the move 
                        self.moves[key][0].insert(0, move)

        
        # Removes the next move from the solution
        def popNextMove(self):
                # Remove the next move
                for key in self.moves: break

                # Remove the first move
                self.moves[key][0] = self.moves[key][0][1:]

                # Check if the subsection is done, clear and move to the next subsection
                while len(self.moves[key]) != 0 and len(self.moves[key][0]) == 0:
                        self.moves[key] = self.moves[key][1:]

                # Check if the section is done, clear and move to the next section
                while key in self.moves and len(self.moves[key]) == 0:
                        del self.moves[key]
                        for key in self.moves: break

        # Gets a new solution from the solver
        def refreshSolution(self):
                self.moves = generate_solution(self.cubeModel)

        # Updates the current solution based on a move by the user
        def updateSolution(self, move):
                nextMove = self.nextMove()

                # If it's an expected move, remove it
                if nextMove == move:
                        self.popNextMove()
                        return
                # If it's a move that is counter to the expected move, make it a double
                elif nextMove != None and nextMove.double and nextMove.face == move.face:
                        nextMove.double = False
                        nextMove.invert = move.invert
                else:
                        # If it's solved, we're done
                        if isSolved(self.cubeModel):
                                self.moves = {}
                                return
                        # If we make an incorrect move
                        if self.incorrect < 5:
                                # Keep track of how many incorect moves
                                self.incorrect += 1
                                # Invert the incoming move (so we can add the counter to the solution)
                                move.invert = not move.invert
                                # Add the counter move to the solution
                                self.prependMove(move)
                        else:
                                # If too many are wrong, just start over
                                self.refreshSolution()
                                self.incorrect = 0

        # Draws the renderer
        def draw(self, win):
                self.toggle.draw(win)

                if not self.enabled: return
                
                # If it's solved, change the text to "solved"
                if len(self.moves) == 0:
                        key = "Solved"
                        value = ""
                else:
                        # Otherwise, populate the values with the next subsection
                        for key, value in self.moves.items():
                                value = value[0]
                                break
                        # Only draw the solve button if there is a next move
                        self.solveButton.draw(win)

                font = pygame.font.SysFont('Arial', 20)

                # Render section name
                text_surf = font.render(key, True, (0, 0, 0))
                win.blit(text_surf, (self.x+5, self.y+ self.toggle.height + 10))
                # Render the solution
                value = " ".join(map(str, value))
                if len(value) <= 25:
                        text_surf = font.render(value, True, (0, 0, 0))
                        win.blit(text_surf, (self.x+5,
							 self.y + self.toggle.height + 35))
                else:
                        end_no = 25
                        if value[24] != ' ' and value[25] != ' ': end_no = 24
                        text_surf1 = font.render(value[:end_no].strip(), True, (0, 0, 0))
                        text_surf2 = font.render(value[end_no:].strip(), True, (0, 0, 0))
                        win.blit(text_surf1, (self.x+5,
							 self.y + self.toggle.height + 35))
                        win.blit(text_surf2, (self.x+5,
							 self.y + self.toggle.height + 55))
                
                if value != '':
                        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x, self.y + self.toggle.height + 9, 203, 75), 2, 3)
