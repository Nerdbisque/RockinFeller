import random
import arcade
import arcade.gui

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ROCK = .30
MOVEMENT_SPEED = 7
ROCK_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "RockinFeller"

class Player(arcade.Sprite):

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start", width=200)
        self.v_box.add(start_button.with_space_around(bottom=15))

        start_button.on_click = self.on_click_start

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.FOREST_GREEN)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_click_start(self, event):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


# class GameOverView(arcade.View):

    # def __init__(self):
        # super().__init__()
        # self.texture = arcade.load_texture("")

        # arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    # def on_draw(self):
        # self.clear()
        # self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

class GameView(arcade.View):

    def __init__(self):
            # Call the parent class initializer
        super().__init__()
            # Variables that will hold sprite lists
        self.player_sprite_list = None
        self.rock_sprite_list = None

            # Set up the player info
        self.player_sprite = None
        self.score = 0

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.collision_sound = arcade.Sound(":resources:sounds/upgrade3.wav")
        arcade.set_background_color(arcade.color.FOREST_GREEN)

    def setup(self):
            # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.rock_sprite_list = arcade.SpriteList()
        self.score = 0
            # Set up the player
            # Character image from kenney.nl
        self.player_sprite = Player(":resources:images/space_shooter/playerShip1_blue.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite_list.append(self.player_sprite)
            # Create the rocks
        for i in range(ROCK_COUNT):
                # Create the rock instance
                # Rock image from kenney.nl
            rock = Rock(":resources:images/space_shooter/meteorGrey_med1.png", SPRITE_SCALING_ROCK)
                # Position the rock
            rock.center_x = random.randrange(SCREEN_WIDTH)
            rock.center_y = random.randrange(SCREEN_HEIGHT)
                # Add the rock to the lists
            self.rock_sprite_list.append(rock)

    def on_draw(self):
        self.clear()
        self.rock_sprite_list.draw()
        self.player_sprite_list.draw()
            # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update_player_speed(self):
            # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_update(self, delta_time):
            # Call update on all sprites (The sprites don't do much in this
            # example though.)
        self.rock_sprite_list.update()
        self.player_sprite_list.update()
            # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.rock_sprite_list)
            # Loop through each colliding sprite, remove it, and add to the score.
        for rock in hit_list:
            rock.remove_from_sprite_lists()
            self.collision_sound.play(0.1, 0, False, 1)
            self.score += 1
    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()

class Rock(arcade.Sprite):

    def reset_pos(self):
            # Reset the rock to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
            # Move the rock
        self.center_y -= 1
            # See if the rock has fallen off the bottom of the screen.
        if self.top < 0:
            self.reset_pos()
def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()