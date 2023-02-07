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
import math
import random


class Herbivores(pygame.sprite.Sprite):
    def __init__(self, window_size, x, y, radius, speed):
        super().__init__()
        """Cell's Info"""
        self.window_size: list = window_size
        # Radius & Energy
        if radius <= 9:
            radius = 10
        # elif radius >= 51:
        #     radius = 50
        self.radius: int = radius
        self.energy: int = 400 / (self.radius ** 4)
        # Speed
        if speed <= 7:
            speed = 8
        elif speed >= 21:
            speed = 20
        self.speed: int = speed
        self.colour: list = [0, self.energy, 0] # Cell's colour

        """About Move"""
        self.x, self.y = x, y
        self.destination: list = [random.randint(self.radius, self.window_size[0] - self.radius), random.randint(self.radius, self.window_size[1] - self.radius)]

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def get_energy(self):
        self.energy += 0.5
        self.colour[1] = self.energy

    def move(self, FPS):
        angle: float = math.atan2(self.destination[1] - self.rect.y, self.destination[0] - self.rect.x)
        self.rect.x += round(math.cos(angle) * FPS / self.speed)
        self.rect.y += round(math.sin(angle) * FPS / self.speed)
        if abs(self.destination[0] - self.rect.x) <= 5 and abs(self.destination[1] - self.rect.y) <= 5:
            self.destination: list = [random.randint(self.radius, self.window_size[0] - self.radius), random.randint(self.radius, self.window_size[1] - self.radius)]

    def update(self, FPS):
        self.move(FPS)
        self.get_energy()
        """Show Herbivores"""
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)


class Predator(pygame.sprite.Sprite):
    def __init__(self, radius, colour):
        super().__init__()
        self.radius: int = radius
        self.energy: int = round(radius**2 * math.pi) # Energy according to size
        self.speed: int = 5 # If speed is high -> Energy lost fast
        self.colour: list = colour # Cell's colour
        self.x, self.y = random.randint(10, 500), random.randint(10, 500)
        """Show Predator"""
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)


class Ground:
    def __init__(self):
        self.window_size: list = [1280, 720]
        self.add_group()
        self.main()

    def add_group(self):
        """Add Entity to Group"""
        self.herbivores_group = pygame.sprite.Group()
        self.predator_group = pygame.sprite.Group()
        self.common_group = pygame.sprite.Group()

        for i in range(2):
            radius: int = random.randint(10, 30)
            herbivores = Herbivores(
                                    self.window_size, 
                                    random.randint(radius, self.window_size[0] - radius), # X
                                    random.randint(radius, self.window_size[1] - radius), # Y
                                    radius, # Radius
                                    random.randint(10, 20) # Speed
                                    )
            self.herbivores_group.add(herbivores)
            self.common_group.add(herbivores)

        for j in range(0):
            predator = Predator(20, [220, 0, 0])
            self.predator_group.add(predator)
            self.common_group.add(predator)

    def divid_herbivores(self):
        for herbivores in self.herbivores_group:
            if herbivores.energy >= 240 - 800 / herbivores.radius:
                herbivores.energy = 400 / (herbivores.radius ** 4)
                """Heredity"""
                new_herbivores_radius = herbivores.radius + random.randrange(-7, 7)

                new_herbivores_speed = herbivores.speed + random.randrange(-2, 2)

                new_herbivores = Herbivores(
                                            self.window_size, 
                                            herbivores.rect.x, # X
                                            herbivores.rect.y, # Y
                                            new_herbivores_radius, # Radius
                                            new_herbivores_speed # Speed
                                            )
                self.herbivores_group.add(new_herbivores)
                self.common_group.add(new_herbivores)
    
    def main(self):
        pygame.init()
        pygame.display.set_caption("Environment Test")
        screen = pygame.display.set_mode(self.window_size) # Set up the screen
        clock = pygame.time.Clock()

        running: bool = True
        while running:
            FPS = clock.tick(60)
            """Event Process"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # If press X button -> Quit
                    running = False
            
            self.divid_herbivores()

            screen.fill((100, 100, 100)) # Fill the background with white
            self.common_group.draw(screen)
            """Show FPS"""
            font = pygame.font.Font(None, 30)
            fps_text = font.render(f"FPS : {round(clock.get_fps())}", True, [0, 255, 0])
            fps_text_Rect = fps_text.get_rect()
            fps_text_Rect.center = (self.window_size[0] - 60, 30)
            
            entity_number_text = font.render(f"Entity : {len(self.common_group)}", True, [255, 255, 255])
            entity_number_text_Rect = entity_number_text.get_rect()
            entity_number_text_Rect.center = (self.window_size[0] - 200, 30)
            
            screen.blit(entity_number_text, entity_number_text_Rect) # Show FPS
            screen.blit(fps_text, fps_text_Rect) # Show FPS

            self.common_group.update(FPS) # Update all entity
            pygame.display.update() # Update the screen

        pygame.quit() # Quit the program


if __name__=="__main__":
    Ground()