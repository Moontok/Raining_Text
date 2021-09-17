import arcade
import random


def main():
    screen_width = 1280
    screen_height = 720
    screen_title = "CSforAR Matrix Rain"
    window = Matrix(screen_width, screen_height, screen_title)
    # window.set_vsync(True)
    arcade.run()


class Matrix(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)

        self.width: int = width
        self.height: int = height
        self.screen_title: str = title
        self.font_size = 15
        self.letters = "CSforAR "
        self.font_color = (0, 255, 0)
        self.bg_color = (0, 0, 0, 25)
        self.cover = arcade.create_rectangle_filled(self.width // 2, self.height // 2, self.width, self.height, self.bg_color)
        self.drops = self.create_drops(self.width // self.font_size)
        
        arcade.set_background_color(self.bg_color)

    def on_update(self, delta_time):
        """ Update loop for each frame. """        

        for drop in self.drops:
            if drop.is_alive():
                drop.increment_y(self.font_size)
            else:
                drop.respawn(self.height)

    def on_draw(self):
        """ Render the screen."""

        self.cover.draw()

        for drop in self.drops:
            arcade.draw_text(drop.get_next_letter(), drop.get_x(), drop.get_y(), self.font_color, drop.get_size())

    def create_drops(self, number_to_create: int) -> list:

        drops = list()

        for x in range(number_to_create):
            drop = Drop(x, self.height, self.letters, self.font_size)
            drops.append(drop)

        return drops


class Drop:
    def __init__(self, x, y, letters, font_size):
        self.letters = letters
        self.letter_count = 0
        self.x = x * font_size
        self.y = random.randrange(0, y + 1, font_size)
        self.font_size = font_size
        # self.size = random.rndint(5, self.font_size)
        self.size = self.font_size
        self.life_remaining = random.randrange(len(letters), y, font_size)

    def increment_y(self, value) -> None:
        self.y -= self.size
        self.life_remaining -= 1

    def is_alive(self) -> bool:
        return self.life_remaining > 0 and self.y > 0

    def get_life(self) -> int:
        return self.life_remaining

    def get_x(self) -> int:
        return self.x

    def set_x(self, value) -> None:
        self.x = value

    def get_y(self) -> int:
        return self.y

    def get_size(self) -> int:
        return self.size
    
    def get_next_letter(self) -> str:
        letter = self.letters[self.letter_count % len(self.letters)]
        self.letter_count += 1
        
        return letter
    
    def respawn(self, value) -> None:
        # self.size = random.randint(1, self.font_size)
        self.y = random.randrange(0, value + 1, self.font_size)
        self.life_remaining = random.randrange(len(self.letters), value, self.font_size)


if __name__ == "__main__":
    main()