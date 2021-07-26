"""This file defines the player."""
import arcade

# Player constants.
SIZE = {"x": 20, "y": 20}
SPEED = 5


class Player:
    def make_avatar(self):
        return arcade.create_rectangle_filled(self.x, self.y,
                                              SIZE["x"], SIZE["y"],
                                              self.color)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = arcade.color.YELLOW
        self.avatar = self.make_avatar()

    def update_color(self, color):
        self.color = color
        # Used to keep color of player the same as the map.
        self.avatar = self.make_avatar()

    def move(self, direction):
        if direction == "UP":
            self.y += SPEED
        elif direction == "DOWN":
            self.y -= SPEED
        elif direction == "LEFT":
            self.x -= SPEED
        elif direction == "RIGHT":
            self.x += SPEED

        self.avatar = self.make_avatar()