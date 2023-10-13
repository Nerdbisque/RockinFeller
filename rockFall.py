import arcade
import arcade.gui
import random

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "RockinFeller"


class qButton(arcade.gui.UIFlatButton):
    def on_click(self, even: arcade.gui.UIOnClickEvent):
        arcade.exit()

class Coin(arcade.Sprite):
    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        self.center_y -= 1
        if self.top < 0:
            self.reset_pos()

class MainView(arcade.View):

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.FOREST_GREEN)
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start", width=200)
        self.v_box.add(start_button.with_space_around(bottom=15))

        @start_button.event("on_click")
        def on_click_switch_button(event):
            # Passing the main view into menu view as an argument.
            game_view = Game(self)
            self.window.show_view(game_view)

        quit_button = qButton(text="Quit", width=200)
        self.v_box.add(quit_button)
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        
    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.FOREST_GREEN])
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

        
class Game(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_sprite_list = None
        self.coin_sprite_list = None

        self.player_sprite = None
        self.score = 0

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        self.player_sprite_list = arcade.SpriteList()
        self.coin_sprite_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite_list.append(self.player_sprite)

        for i in range(COIN_COUNT):
            coin = Coin(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_sprite_list.append(coin)

    def on_draw(self):
        self.clear()
        self.coin_sprite_list.draw()
        self.player_sprite_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        self.coin_sprite_list.update()

        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_sprite_list)
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.FOREST_GREEN])
        self.manager.enable()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()

if __name__ == "__main__":
    main()