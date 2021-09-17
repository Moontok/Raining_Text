import pygame as pg
from random import randint, choice, randrange

def main():
    pg.init()

    width, height = 1920, 1080
    chars = "CSforAR"
    base_font_size = 50
    font_color = (0, 255, 255)
    speed = 40

    screen = pg.display.set_mode((width, height))
    display_surface = pg.Surface((width, height))
    display_surface.set_alpha(10)

    clock = pg.time.Clock()

    drops = list()

    for x in range(0, width, base_font_size):
        drop = Drop(x, height, chars, base_font_size, font_color)
        drops.append(drop)

    while True:
        screen.blit(display_surface, (0, 0))
        display_surface.fill(pg.Color("black"))

        for drop in drops:
            if drop.is_alive():
                drop.increment_y()
            else:
                drop.respawn()
            drop.draw(screen)            

        pg.time.delay(speed)

        pg.display.update()

        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()


class Drop:
    """Outlines a drop of text that falls down the screen."""

    def __init__(self, x, y, letters, font_size, font_color):
        self.size = randint(1, font_size + 1)
        self.font_color = font_color
        self.letters = letters
        self.rendered_letters = self.generate_rendered_letters()
        self.letter_count = randint(0, len(letters))
        self.x = x
        self.y = randrange(0, y + 1, font_size)
        self.screen_height = y
        self.life_remaining = randrange(len(letters), y, font_size)

    def generate_rendered_letters(self) -> list:
        """Create the rendered letters and return them."""

        random_text_tails = [
            "/\/\/\/\/\/", 
            "()()()()()(", 
            "|||||||||||"
        ]

        letters = f"{self.letters}{choice(random_text_tails)}"
        font = pg.font.SysFont("Console", self.size)
        font.set_bold(True)
        self.font_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        rendered_letters = list()
        for letter in letters:
            rendered_letters.append(font.render(letter, True, self.font_color))
        return rendered_letters

    def increment_y(self) -> None:
        self.y += self.size
        self.life_remaining -= 1

    def is_alive(self) -> bool:
        return self.life_remaining > 0 and self.y < self.screen_height
    
    def get_next_letter(self) -> str:
        letter = self.rendered_letters[self.letter_count % len(self.rendered_letters)]
        self.letter_count += 1
        
        return letter  
        
    def draw(self, screen):        
        screen.blit(self.get_next_letter(), (self.x, self.y))

    def respawn(self) -> None:
        self.rendered_letters = self.generate_rendered_letters()
        self.y = randint(0, self.screen_height + 1)
        self.life_remaining = randrange(len(self.rendered_letters), self.screen_height, self.size)

if __name__ == "__main__":
    main()