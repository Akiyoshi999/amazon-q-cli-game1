import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 5
        self.color = (0, 255, 0)  # Green
    
    def update(self, keys, screen_width, screen_height):
        # Move up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        # Move down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        
        # Keep player on screen
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))
    
    def draw(self, screen):
        # Draw player ship (triangle shape)
        points = [
            (self.x, self.y + self.height // 2),  # Nose
            (self.x + self.width, self.y),        # Top
            (self.x + self.width, self.y + self.height)  # Bottom
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # Draw cockpit
        cockpit_x = self.x + self.width - 15
        cockpit_y = self.y + self.height // 2 - 5
        pygame.draw.rect(screen, (100, 100, 255), (cockpit_x, cockpit_y, 10, 10))
