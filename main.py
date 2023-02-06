"""
Title : Nature Environment Test
L Common System
  Energy System : if energy is 0 -> dead
  Reproduction Standard : Over Specific Energy -> Reproduction

L Herbivores : Energy rises over time
  Reproduction : Energy Rise Rate, Size

L Carnivores : Predation on herbivores, Predation when carnivores double in size
  Reproduction : Speed, Detection range
"""
import pygame


class Carnivores(pygame.sprite.Sprite):
    def __init__(self, radius, colour):
        super().__init__()
        self.radius = radius
        self.colour = colour
        self.x, self.y = 10, 10
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        self.image = pygame.Surface((self.radius *2, self.radius *2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)


class Predator(pygame.sprite.Sprite):
    def __init__(self, radius, colour):
        super().__init__()
        self.radius = radius
        self.colour = colour
        self.x, self.y = 10, 50
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        self.image = pygame.Surface((self.radius *2, self.radius *2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)

class Ground:
    def __init__(self):
        self.add_group()


    def add_group(self):
        self.carnivores_group = pygame.sprite.Group()
        self.predator_group = pygame.sprite.Group()
        self.common_group = pygame.sprite.Group()

        for i in range(1):
            carnivores = Carnivores(10, [255, 0, 0])
            self.carnivores_group.add(carnivores)
            self.common_group.add(carnivores)

        for j in range(1):
            predator = Predator(20, [0, 255, 0])
            self.predator_group.add(predator)
            self.common_group.add(predator)

    def main(self):
        pygame.init()
        pygame.display.set_caption("Environment Test")
        screen = pygame.display.set_mode([500, 500]) # Set up the screen

        running : bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # If press X button -> Quit
                    running = False

            screen.fill((255, 255, 255)) # Fill the background with white
            self.common_group.draw(screen)
            self.common_group.update()
            pygame.display.update() # Update the screen

        pygame.quit() # Over the program


if __name__=="__main__":
    ground = Ground()
    ground.main()