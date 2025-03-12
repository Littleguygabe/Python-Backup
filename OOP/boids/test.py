import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Boid class
class Boid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Bounce off walls
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity[1] = -self.velocity[1]


# Function to calculate distance between two boids
def distance(boid1, boid2):
    x1, y1 = boid1.rect.center
    x2, y2 = boid2.rect.center
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# Function to update boid velocities based on flocking behavior
def update_boids(boids):
    for boid in boids:
        alignment = [0, 0]
        cohesion = [0, 0]
        separation = [0, 0]
        count = 0

        for other_boid in boids:
            if boid != other_boid:
                dist = distance(boid, other_boid)
                if dist < 50:
                    count += 1
                    alignment[0] += other_boid.velocity[0]
                    alignment[1] += other_boid.velocity[1]
                    cohesion[0] += other_boid.rect.x
                    cohesion[1] += other_boid.rect.y
                    separation[0] += (boid.rect.x - other_boid.rect.x) / dist
                    separation[1] += (boid.rect.y - other_boid.rect.y) / dist

        if count > 0:
            alignment[0] /= count
            alignment[1] /= count
            cohesion[0] /= count
            cohesion[1] /= count
            separation[0] /= count
            separation[1] /= count

        boid.velocity[0] += alignment[0] + (cohesion[0] - boid.rect.x) / 100 + separation[0]
        boid.velocity[1] += alignment[1] + (cohesion[1] - boid.rect.y) / 100 + separation[1]


# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(30)]
    all_sprites.add(boids)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_boids(boids)
        all_sprites.update()

        screen.fill(BLACK)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
