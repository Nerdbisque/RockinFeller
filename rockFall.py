import arcade
import arcade.gui

class qButton(arcade.gui.UIFlatButton):
    def on_click(self, even: arcade.gui.UIOnClickEvent):
        arcade.exit()

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "UIFlatButton Example", resizable=True)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.FOREST_GREEN)
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

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
        
window = MyWindow()
arcade.run()