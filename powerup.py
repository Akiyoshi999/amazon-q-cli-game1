import pygame
import random
import math

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15  # 20から15に縮小
        self.height = 15  # 20から15に縮小
        self.speed = 2
        
        # Randomly select powerup type
        self.types = ["multi_shot", "diagonal_shot", "speed_up", "shield"]
        self.type = random.choice(self.types)
        
        # Set color based on type
        self.colors = {
            "multi_shot": (255, 255, 0),     # Yellow
            "diagonal_shot": (0, 255, 255),  # Cyan
            "speed_up": (0, 255, 0),         # Green
            "shield": (100, 100, 255)        # Blue
        }
        self.color = self.colors[self.type]
        
        # Animation
        self.pulse_value = 0
        self.pulse_direction = 1
        self.rotation = 0
    
    def update(self):
        # Move left
        self.x -= self.speed
        
        # Animate
        self.pulse_value += 0.05 * self.pulse_direction
        if self.pulse_value >= 1.0:
            self.pulse_value = 1.0
            self.pulse_direction = -1
        elif self.pulse_value <= 0.0:
            self.pulse_value = 0.0
            self.pulse_direction = 1
        
        # Rotate
        self.rotation += 2
        if self.rotation >= 360:
            self.rotation = 0
    
    def draw(self, screen):
        # Calculate pulse effect
        pulse = 5 * self.pulse_value
        
        # Draw base shape (rotating)
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        if self.type == "multi_shot":
            # Draw star shape for multi-shot
            points = []
            for i in range(5):
                # Outer points (star tips)
                angle = math.radians(self.rotation + i * 72)
                x = center_x + math.cos(angle) * (self.width // 2 + pulse)
                y = center_y + math.sin(angle) * (self.height // 2 + pulse)
                points.append((x, y))
                
                # Inner points
                angle = math.radians(self.rotation + i * 72 + 36)
                x = center_x + math.cos(angle) * (self.width // 4)
                y = center_y + math.sin(angle) * (self.height // 4)
                points.append((x, y))
            
            pygame.draw.polygon(screen, self.color, points)
            
        elif self.type == "diagonal_shot":
            # Draw X shape for diagonal shot
            thickness = 4
            length = self.width // 2 + pulse
            
            # Rotate points
            angle1 = math.radians(self.rotation)
            angle2 = math.radians(self.rotation + 90)
            
            # First diagonal line
            x1 = center_x + math.cos(angle1) * length
            y1 = center_y + math.sin(angle1) * length
            x2 = center_x + math.cos(angle1 + math.pi) * length
            y2 = center_y + math.sin(angle1 + math.pi) * length
            
            # Second diagonal line
            x3 = center_x + math.cos(angle2) * length
            y3 = center_y + math.sin(angle2) * length
            x4 = center_x + math.cos(angle2 + math.pi) * length
            y4 = center_y + math.sin(angle2 + math.pi) * length
            
            pygame.draw.line(screen, self.color, (x1, y1), (x2, y2), thickness)
            pygame.draw.line(screen, self.color, (x3, y3), (x4, y4), thickness)
            
        elif self.type == "speed_up":
            # Draw arrow shape for speed up
            points = []
            
            # Arrow head
            angle = math.radians(self.rotation)
            x = center_x + math.cos(angle) * (self.width // 2 + pulse)
            y = center_y + math.sin(angle) * (self.height // 2 + pulse)
            points.append((x, y))
            
            # Arrow wings
            angle1 = math.radians(self.rotation + 140)
            angle2 = math.radians(self.rotation - 140)
            
            x1 = center_x + math.cos(angle1) * (self.width // 2)
            y1 = center_y + math.sin(angle1) * (self.height // 2)
            points.append((x1, y1))
            
            # Arrow middle indent
            x2 = center_x + math.cos(angle) * (self.width // 4)
            y2 = center_y + math.sin(angle) * (self.height // 4)
            points.append((x2, y2))
            
            x3 = center_x + math.cos(angle2) * (self.width // 2)
            y3 = center_y + math.sin(angle2) * (self.height // 2)
            points.append((x3, y3))
            
            pygame.draw.polygon(screen, self.color, points)
            
        elif self.type == "shield":
            # Draw shield shape
            radius = self.width // 2 + pulse
            pygame.draw.circle(screen, self.color, (center_x, center_y), radius, 3)
            
            # Draw cross inside
            line_length = radius * 0.7
            angle = math.radians(self.rotation)
            
            for i in range(2):
                angle_i = angle + i * math.pi/2
                x1 = center_x + math.cos(angle_i) * line_length
                y1 = center_y + math.sin(angle_i) * line_length
                x2 = center_x + math.cos(angle_i + math.pi) * line_length
                y2 = center_y + math.sin(angle_i + math.pi) * line_length
                pygame.draw.line(screen, self.color, (x1, y1), (x2, y2), 2)
        
        # Draw letter inside
        font = pygame.font.SysFont(None, 15)
        letters = {
            "multi_shot": "M",
            "diagonal_shot": "D",
            "speed_up": "S",
            "shield": "P"  # P for Protection
        }
        text = font.render(letters[self.type], True, (0, 0, 0))
        text_rect = text.get_rect(center=(center_x, center_y))
        screen.blit(text, text_rect)
    
    def apply_effect(self, player):
        """Apply powerup effect to player"""
        if self.type == "multi_shot":
            player.powerups["multi_shot"] = 500  # Active for 500 frames (about 8 seconds)
            return "Multi-Shot activated!"
            
        elif self.type == "diagonal_shot":
            player.powerups["diagonal_shot"] = 500
            return "Diagonal-Shot activated!"
            
        elif self.type == "speed_up":
            player.speed += 2
            player.powerups["speed_up"] = 600  # 10 seconds
            return "Speed Boost activated!"
            
        elif self.type == "shield":
            player.powerups["shield"] = 300  # 5 seconds
            return "Shield activated!"
            
        return "Power-Up collected!"
