import pygame as pg
import random as rm

def main():
    pg.init()

    width, height = 1920, 1080
    chars = "CSforAR"
    base_font_size = 50
    font_color = (0, 255, 255)
    bg_color = pg.Color("black")
    # Lower is faster
    speed = 40

    main_screen: pg.Surface = pg.display.set_mode((width, height))
    main_screen.fill(bg_color)
    alpha_cover = pg.Surface((width, height))
    alpha_cover.set_alpha(10)

    clock: pg.Clock = pg.time.Clock()

    drops: list[Drop] = list()

    # Create a Drop for each column (x) on the screen.
    # Columns are determined by base font size and screen width
    for x in range(0, width, base_font_size - base_font_size // 2):
        drop = Drop(x, height, chars, base_font_size, font_color)
        drops.append(drop)

    while True:
        main_screen.blit(alpha_cover, (0, 0))

        for drop in drops:
            if drop.is_alive():
                drop.increment_y()
            else:
                drop.respawn()
            drop.draw(main_screen)            

        pg.time.delay(speed)

        pg.display.update()

        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()


class Drop:
    """Outlines a drop of text that falls down the screen."""

    def __init__(self, x: int, y: int, letters: str, font_size: int, font_color: tuple):
        self.base_size = font_size
        self.size = rm.randint(1, font_size)
        self.step = rm.randint(1, font_size) // 3 + 1
        self.font_color = font_color
        self.letters = letters
        self.rendered_letters = self.generate_rendered_letters()
        self.letter_count = rm.randint(0, len(letters))
        self.x = x
        self.y = rm.randrange(0, y + 1)
        self.screen_height = y
        self.life_remaining = rm.randrange(len(letters), y, font_size)

    def generate_rendered_letters(self) -> list[pg.Surface]:
        """Create a list of the rendered letters to a Surface and return them."""
        
        normal_font = pg.font.SysFont("Console", self.size)
        glyph_font = pg.font.Font("fonts\\alien_glyphs.ttf", self.size)
        # self.font_color = (rm.randint(0, 255), rm.randint(0, 255), rm.randint(0, 255)) 
        aslphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        random_text_tails = [
            "/\/\/\/\/\/", 
            "()()()()()(", 
            "|||||||||||",
            "^-|^-|^-|^-",
            "<><><><><><",
            "+|+|+|+|+|+"
        ]
        letter = [rm.choice(self.letters) for _ in range(10)]

        letters = f"{self.letters}{rm.choice(random_text_tails)}"

        rendered_letters: list[pg.Surface] = list()

        for letter in self.letters:
            rendered_letters.append(normal_font.render(letter, True, self.font_color))
        for _ in range(3, 8):
            rendered_letters.append(glyph_font.render(rm.choice(aslphabet), True, self.font_color))
        for letter in rm.choice(random_text_tails):
            rendered_letters.append(normal_font.render(letter, True, self.font_color))
        
        return rendered_letters

    def increment_y(self) -> None:
        """Increments the drop towards the bottom of the screen and
        decrements the remaining life of the drop.
        """

        self.y += self.step
        self.life_remaining -= 1


    def is_alive(self) -> bool:
        """Return True if the drop should still be rendered. """

        return self.life_remaining > 0 and self.y < self.screen_height
    

    def get_next_rendered_letter(self) -> pg.Surface:
        """Return the next rendred letter Surface to display by the drop."""

        letter = self.rendered_letters[self.letter_count % len(self.rendered_letters)]
        self.letter_count += 1
        
        return letter
        

    def draw(self, screen: pg.Surface) -> None:
        """Draw the rendered letter Surface to the main screen.""" 

        screen.blit(self.get_next_rendered_letter(), (self.x, self.y))


    def respawn(self) -> None:
        """Respawns the drop to a new vertical location, size, and life remaining."""
        
        self.size = rm.randint(1, self.base_size)
        self.step = rm.randint(1, self.base_size) // 3 + 1

        self.rendered_letters: list[pg.Surface] = self.generate_rendered_letters()

        self.y = rm.randint(0, self.screen_height + 1)
        self.life_remaining = rm.randrange(len(self.rendered_letters), self.screen_height, self.size)


if __name__ == "__main__":
    main()