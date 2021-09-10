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
        self.background = arcade.load_texture('assets/wide.png')

        button_normal = arcade.load_texture('assets/Q1.png')
        hovered_texture = arcade.load_texture('assets/Q2.png')
        pressed_texture = arcade.load_texture('assets/Q1.png')
        button = arcade.gui.UIImageButton(
            center_x= 620,
            center_y= 380,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
        )
        self.ui_manager.add_ui_element(button)

        button_normal1 = arcade.load_texture('assets/Start1.png')
        hovered_texture1 = arcade.load_texture('assets/Start2.png')
        pressed_texture1 = arcade.load_texture('assets/Start1.png')
        button2 = arcade.gui.UIImageButton(
            center_x= 620,
            center_y= 460,
            normal_texture=button_normal1,
            hover_texture=hovered_texture1,
            press_texture=pressed_texture1,
        )
        self.ui_manager.add_ui_element(button2)

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
