"""
Putting everything in here for now. Until things get more...complicated.
Thankfully I'm already starting to write in a modular manner,
so it won't be that hard to just cut-paste
out the bits I need into other .py files as needed.
"""

import arcade

# Game window constants.
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
WINDOW_TITLE = "Adventure"

# Window position shortcuts.
CENTER_X, CENTER_Y = (WINDOW_WIDTH/2), (WINDOW_HEIGHT/2)


class Avatar:

    SPEED = 5

    def __init__(self):
        self.avatar = arcade.Sprite("assets/sprites/squares/yellow.png")
        self.avatar.center_x, self.avatar.center_y = CENTER_X, CENTER_Y
        self.avatar.change_x, self.avatar.change_y = 0, 0

    def draw(self):
        self.avatar.draw()

    def move(self, key):
        if key == arcade.key.UP:
            self.avatar.change_y = Avatar.SPEED
        if key == arcade.key.DOWN:
            self.avatar.change_y = -Avatar.SPEED
        if key == arcade.key.LEFT:
            self.avatar.change_x = -Avatar.SPEED
        if key == arcade.key.RIGHT:
            self.avatar.change_x = Avatar.SPEED

    def stop_moving(self, direction):
        if direction == "VERTICAL":
            self.avatar.change_y = 0
        elif direction == "HORIZONTAL":
            self.avatar.change_x = 0

    def update_position(self):
        self.avatar.center_x += self.avatar.change_x
        self.avatar.center_y += self.avatar.change_y


class Adventure(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.color.COOL_GREY)  # The Floor Color.

        # Game Elements
        self.avatar = None
        self.player = None
        self.walls = None

        self.map = None
        self.map_exits = {
            """For each loaded map, load in which exits lead to which next map.
            If None, there is no exit."""
            'top': "",
            'bottom': "",
            'left': "",
            'right': ""
        }

        # Simple physics engine will be loaded to prevent ghosting through walls.
        self.physics_engine = None

    def setup(self):

        # I call it the avatar because it sounds cool. It's the play.
        self.avatar = Avatar()
        self.player = arcade.SpriteList()
        self.player.append(self.avatar.avatar)

        # Load in the map.
        active_map = "assets/maps/yellow_castle.tmx"
        self.walls = arcade.SpriteList()
        self.map = arcade.tilemap.read_tmx(active_map)
        self.walls = arcade.tilemap.process_layer(self.map, "walls",
                                                  use_spatial_hash=True)

        self.physics_engine = arcade.PhysicsEngineSimple(self.avatar.avatar,
                                                         self.walls)

    def on_key_press(self, key, _):
        self.avatar.move(key)

    def on_key_release(self, key, _):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.avatar.stop_moving("VERTICAL")
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.avatar.stop_moving("HORIZONTAL")

    def on_draw(self):
        arcade.start_render()

        self.walls.draw()
        self.avatar.draw()

    # Logic
    def should_game_change_map(self):
        if self.avatar.avatar.center_y == WINDOW_HEIGHT:  # Top of the screen.
            try:
                self.map_exits['top'] = self.map.properties['exit_top']
            except ValueError:
                print("You need to implement an exit, idiot.")
                return

            new_active_map = f"assets/maps/{self.map_exits['top']}.tmx"
            self.map = arcade.read_tmx(new_active_map)
            self.walls = arcade.process_layer(self.map, "walls",
                                              use_spatial_hash=True)
            self.physics_engine.walls = self.walls

            self.avatar.avatar.center_y = 10

        elif self.avatar.avatar.center_y == 0:  # Bottom of the screen.
            try:
                self.map_exits['bottom'] = self.map.properties['exit_bottom']
            except ValueError:
                print("You need to implement an exit, idiot.")
                return

            new_active_map = f"assets/maps/{self.map_exits['bottom']}.tmx"
            self.map = arcade.read_tmx(new_active_map)
            self.walls = arcade.process_layer(self.map, "walls",
                                              use_spatial_hash=True)
            self.physics_engine.walls = self.walls

            self.avatar.avatar.center_y = WINDOW_HEIGHT - 10

    def on_update(self, delta):
        """
        Game logic goes here. Make checks and such.
        """
        self.avatar.update_position()
        self.physics_engine.update()
        self.should_game_change_map()


def main():
    game = Adventure()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()