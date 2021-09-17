import pygame
import random

def main():
    pygame.init()

    width, height = 1920, 1080
    chars = "CSforAR"
    base_font_size = 50
    font_color = (0, 255, 255)
    speed = 1

    screen = pygame.display.set_mode((width, height))
    display_surface = pygame.Surface((width, height))
    display_surface.set_alpha(10)

    clock = pygame.time.Clock()

    drops = list()

    for x in range(0, width, base_font_size):
        drop = Drop(x, height, chars, base_font_size, font_color)
        drops.append(drop)

    while True:
        screen.blit(display_surface, (0, 0))
        display_surface.fill(pygame.Color('black'))

        for drop in drops:
            if drop.is_alive():
                drop.increment_y()
            else:
                drop.respawn()
            drop.draw(screen)            

        pygame.time.delay(speed)

        pygame.display.update()

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


class Drop:
    def __init__(self, x, y, letters, font_size, font_color):
        self.font_size = font_size
        self.size = font_size
        self.font_color = font_color
        self.letters = letters
        self.rendered_letters = self.generate_letters()
        self.letter_count = random.randint(0, len(letters))
        self.x = x
        self.y = random.randrange(0, y + 1, font_size)
        self.screen_height = y
        self.life_remaining = random.randrange(len(letters), y, font_size)

    def generate_letters(self) -> list:
        random_char = ["/\/\/\/\/\/", "()()()()()(", "|||||||||||"]
        letters = f"{self.letters}{random.choice(random_char)}"
        self.size = random.randint(1, self.font_size + 1)
        font = pygame.font.SysFont('Console', self.size)
        font.set_bold(True)
        # self.font_color = (random.randint(0,255), random.randint(0,255), random.randint(0,125))
        rendered_letters = list()
        for letter in letters:
            rendered_letters.append(font.render(letter, True, self.font_color))
        return rendered_letters

    def increment_y(self) -> None:
        self.y += self.size
        # self.y += self.font_size
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
        self.rendered_letters = self.generate_letters()
        self.y = random.randint(0, self.screen_height + 1)
        self.life_remaining = random.randrange(len(self.rendered_letters), self.screen_height, self.font_size)

if __name__ == "__main__":
    main()