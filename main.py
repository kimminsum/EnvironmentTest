"""
Title : Nature Environment Test
L Common System
  Energy System : if energy is 0 -> dead
  Reproduction Standard : Over Specific Energy -> Reproduction

L Predator : Predation on herbivores, Predation when carnivores double in size
  Reproduction : Speed, Detection range

L Herbivores : Energy rises over time
  Reproduction : Energy Rise Rate, Size
"""
import pygame
import math
import random


class Predator(pygame.sprite.Sprite):
    def __init__(self, window_size, x, y, radius, speed):
        super().__init__()
        self.window_size: list = window_size
        """Cell's Info"""
        # Radius & Energy
        if radius <= 9:
            radius = 10
        self.radius: int = radius
        self.energy: int = 500 / (self.radius ** 4) + 50
        # Speed
        if speed <= 7:
            speed = 8
        elif speed >= 21:
            speed = 20
        self.speed: int = speed
        self.colour: list = [self.energy, 0, 0] # Cell's colour
        """About Move"""
        self.x, self.y = x, y
        self.destination: list = [random.randint(self.radius, self.window_size[0] - self.radius), random.randint(self.radius, self.window_size[1] - self.radius)]

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def move(self, FPS):
        angle: float = math.atan2(self.destination[1] - self.rect.y, self.destination[0] - self.rect.x)
        self.rect.x += round(math.cos(angle) * FPS / self.speed)
        self.rect.y += round(math.sin(angle) * FPS / self.speed)
        if abs(self.destination[0] - self.rect.x) <= 5 and abs(self.destination[1] - self.rect.y) <= 5:
            self.destination: list = [random.randint(self.radius, self.window_size[0] - self.radius), random.randint(self.radius, self.window_size[1] - self.radius)]

    def update(self, FPS):
        self.move(FPS)
        """Show Predator"""
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (self.radius, self.radius), self.radius)


class Herbivores(pygame.sprite.Sprite):
    def __init__(self, window_size, x, y, radius, speed):
        super().__init__()
        self.window_size: list = window_size
        """Cell's Info"""
        # Radius & Energy
        if radius <= 9:
            radius = 10
        self.radius: int = radius
        self.energy: int = 400 / (self.radius ** 4) + 50
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




class Ground:
    def __init__(self):
        self.window_size: list = [1280, 720]
        self.add_group()
        self.main()

    def add_group(self):
        self.herbivores_group = pygame.sprite.Group()
        self.predator_group = pygame.sprite.Group()
        self.common_group = pygame.sprite.Group()
        """Add Entity to Group"""
        for j in range(10): # Predator
            radius: int = random.randint(10, 30)
            predator = Predator(
                                    self.window_size, 
                                    random.randint(radius, self.window_size[0] - radius), # X
                                    random.randint(radius, self.window_size[1] - radius), # Y
                                    radius, # Radius
                                    random.randint(10, 20) # Speed
                                    )
            self.predator_group.add(predator)
            self.common_group.add(predator)

        for i in range(2): # Herbivores
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

    def show_info(self, screen, clock):
        font = pygame.font.Font(None, 25) # Font Style : None , Font Size : 30
        # FPS
        fps_text = font.render(f"FPS : {round(clock.get_fps())}", True, [0, 255, 0])
        fps_text_Rect = fps_text.get_rect()
        fps_text_Rect.center = (self.window_size[0] - 60, 30)
        # Predator
        predator_number_text = font.render(f"Predator : {len(self.predator_group)}", True, [255, 0, 0])
        predator_number_text_Rect = predator_number_text.get_rect()
        predator_number_text_Rect.center = (83, 60)
        # Herbivores
        herbivores_number_text = font.render(f"Herbivores : {len(self.herbivores_group)}", True, [0, 255, 0])
        herbivores_number_text_Rect = herbivores_number_text.get_rect()
        herbivores_number_text_Rect.center = (90, 30)
        # All Entity
        entity_number_text = font.render(f"Entity : {len(self.common_group)}", True, [255, 255, 255])
        entity_number_text_Rect = entity_number_text.get_rect()
        entity_number_text_Rect.center = (73, 90)

        screen.blit(fps_text, fps_text_Rect) # Show FPS
        screen.blit(predator_number_text, predator_number_text_Rect) # Show Predator
        screen.blit(herbivores_number_text, herbivores_number_text_Rect) # Show Herbivores
        screen.blit(entity_number_text, entity_number_text_Rect) # Show FPS

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

            """Show Entity"""
            screen.fill((100, 100, 100)) # Fill the background with white
            self.common_group.draw(screen)
            self.show_info(screen, clock) # Show Infomaition about cells
            self.common_group.update(FPS) # Update all entity
            pygame.display.update() # Update the screen

        pygame.quit() # Quit the program


if __name__=="__main__":
    Ground()