"""Start point for game..."""
import arcade
from player import Player

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720  # Start out with a 720p style screen.
WINDOW_TITLE = "Adventure"


class AdventureWindow(arcade.Window):

    # Initial Setup.
    def __init__(self, w, h, title):
        super().__init__(w, h, title)
        arcade.set_background_color(arcade.color.COOL_GREY)
        self.player = None
        self.direction = None

    def setup(self):
        self.player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    # Draw code, game logic processing.
    def on_draw(self):
        arcade.start_render()
        self.player.avatar.draw()

    def on_update(self, delta_time):
        if self.direction is None:
            pass  # Do literally nothing.
        elif self.direction == "UP":
            self.player.move("UP")
        elif self.direction == "DOWN":
            self.player.move("DOWN")
        elif self.direction == "LEFT":
            self.player.move("LEFT")
        elif self.direction == "RIGHT":
            self.player.move("RIGHT")

    # Input responses.
    def on_key_press(self, key, modifiers):
        # Movement, and pick-up/dropping of item. Very simple.
        if key == arcade.key.UP:
            self.direction = "UP"
        elif key == arcade.key.DOWN:
            self.direction = "DOWN"
        elif key == arcade.key.LEFT:
            self.direction = "LEFT"
        elif key == arcade.key.RIGHT:
            self.direction = "RIGHT"

    def on_key_release(self, key, modifiers):
        # Would suck if releasing a key didn't stop moving the player avatar.
        if key == arcade.key.UP:
            self.direction = None
        elif key == arcade.key.DOWN:
            self.direction = None
        elif key == arcade.key.LEFT:
            self.direction = None
        elif key == arcade.key.RIGHT:
            self.direction = None


def main():
    game = AdventureWindow(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()