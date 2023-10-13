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

class initialize(arcade.gui.UIFlatButton):
    def on_click(self, even: arcade.gui.UIOnClickEvent):
        arcade.exit()
        #window = MyGame()
        #window.setup()
        # arcade.run()

class Coin(arcade.Sprite):
    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        self.center_y -= 1
        if self.top < 0:
            self.reset_pos()

class MyWindow(arcade.Window):

    def __init__(self):
        super().__init__(800, 600, "UIFlatButton Example", resizable=True)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.FOREST_GREEN)
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = initialize(text="Start", width=200)
        self.v_box.add(start_button)

        quit_button = qButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        start_button.on_click = self.on_click_start
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        print("Start:", event)

    def on_draw(self):
        self.clear()
        self.manager.draw()

        
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

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

window = MyWindow()
arcade.run()