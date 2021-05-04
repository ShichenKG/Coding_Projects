import arcade, os

import arcade.gui
from arcade.gui import UIFlatButton, UIGhostFlatButton, UIManager
from arcade.gui.ui_style import UIStyle

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = 'Doors.stu'

# Title Screen for the Game
class Title(arcade.View):
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

        #Background image will be stored here
        self.background = None

    # Setting up what the player can see
    def setup(self):
        # Adds the image to the background
        self.background = arcade.load_texture('wide.png')

        button_normal = arcade.load_texture('quit1.png')
        hovered_texture = arcade.load_texture('quit2.png')
        pressed_texture = arcade.load_texture('quit3.png')
        button = arcade.gui.UIImageButton(
            center_x=left_column_x,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
        )
        self.ui_manager.add_ui_element(button)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

def TitleScreen():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,title='Doors')
    window.show_view(Title())
    arcade.run()

TitleScreen()