# Import necessary modules
import pygame
import sys

# Define some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# Initialize Pygame
pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Top-Down RPG")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state objects
        self.player = Player(self)

    def new(self):
        """Start a new game and initialize game objects."""
        self.all_sprites = pygame.sprite.Group()

        # Add player sprite to the group
        self.all_sprites.add(self.player)

    def run(self):
        """Run the game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        """Update game state."""
        self.all_sprites.update()

    def events(self):
        """Handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        """Draw the game screen."""
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        """Quit the game."""
        pygame.quit()
        sys.exit()

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))  # Red player
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = 5

    def update(self):
        """Update player position based on input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.velocity

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    