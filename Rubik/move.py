from dataclasses import dataclass

# Simple class to represent a rubiks cube move
@dataclass
class Move:
    face: str
    invert: bool
    double: bool

    def __str__(self):
        return self.face + ("2" if self.double else ("'" if self.invert else ""))