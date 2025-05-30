import pygame

class Bullet:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.width = 8  # 6から8に拡大
        self.height = 4  # 3から4に拡大
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = (255, 255, 0)  # Yellow
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
    
    def draw(self, screen, color=None):
        if color is None:
            color = self.color
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
