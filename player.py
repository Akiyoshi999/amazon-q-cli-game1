import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 5
        self.color = (0, 255, 0)  # Green
        
        # Powerups
        self.powerups = {
            "multi_shot": 0,     # Multiple bullets at once
            "diagonal_shot": 0,  # Diagonal bullets
            "speed_up": 0,       # Increased speed
            "shield": 0          # Temporary invulnerability
        }
        
        # Powerup message
        self.powerup_message = ""
        self.message_timer = 0
    
    def update(self, keys, screen_width, screen_height):
        # Update powerup timers
        for powerup in self.powerups:
            if self.powerups[powerup] > 0:
                self.powerups[powerup] -= 1
                
                # Reset speed when speed powerup expires
                if powerup == "speed_up" and self.powerups[powerup] == 0:
                    self.speed = 5
        
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
        
        # Calculate speed based on powerups
        current_speed = self.speed
        
        # Move up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= current_speed
        # Move down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += current_speed
        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= current_speed
        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += current_speed
        
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
        
        # Draw shield if active
        if self.powerups["shield"] > 0:
            # Draw shield bubble
            shield_radius = max(self.width, self.height) + 5
            shield_color = (100, 100, 255, 128)  # Blue with transparency
            
            # Create a surface with alpha
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, shield_color, (shield_radius, shield_radius), shield_radius)
            
            # Draw shield with pulsing effect
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 0.3 + 0.7
            shield_surface.set_alpha(int(128 * pulse))
            
            # Position shield around player
            shield_x = self.x + self.width // 2 - shield_radius
            shield_y = self.y + self.height // 2 - shield_radius
            screen.blit(shield_surface, (shield_x, shield_y))
        
        # Draw player ship
        pygame.draw.polygon(screen, self.color, points)
        
        # Draw cockpit
        cockpit_x = self.x + self.width - 15
        cockpit_y = self.y + self.height // 2 - 5
        pygame.draw.rect(screen, (100, 100, 255), (cockpit_x, cockpit_y, 10, 10))
        
        # Draw powerup indicators
        self._draw_powerup_indicators(screen)
        
        # Draw powerup message
        if self.message_timer > 0:
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.powerup_message, True, (255, 255, 255))
            screen.blit(text, (self.x, self.y - 20))
    
    def _draw_powerup_indicators(self, screen):
        # Draw small indicators for active powerups
        indicator_size = 5
        indicator_y = self.y - 10
        
        # Multi-shot indicator
        if self.powerups["multi_shot"] > 0:
            pygame.draw.rect(screen, (255, 255, 0), 
                            (self.x, indicator_y, indicator_size, indicator_size))
        
        # Diagonal-shot indicator
        if self.powerups["diagonal_shot"] > 0:
            pygame.draw.rect(screen, (0, 255, 255), 
                            (self.x + indicator_size + 2, indicator_y, indicator_size, indicator_size))
        
        # Speed-up indicator
        if self.powerups["speed_up"] > 0:
            pygame.draw.rect(screen, (0, 255, 0), 
                            (self.x + (indicator_size + 2) * 2, indicator_y, indicator_size, indicator_size))
        
        # Shield indicator is visible as the shield itself
    
    def set_powerup_message(self, message):
        """Set a message to display above the player"""
        self.powerup_message = message
        self.message_timer = 120  # Display for 2 seconds (120 frames)
    
    def fire_bullets(self):
        """Return a list of bullets based on current powerups"""
        bullets = []
        
        # Base bullet
        bullets.append({
            'x': self.x + self.width,
            'y': self.y + self.height // 2,
            'speed_x': 10,
            'speed_y': 0
        })
        
        # Multi-shot powerup (3 bullets in a row)
        if self.powerups["multi_shot"] > 0:
            bullets.append({
                'x': self.x + self.width,
                'y': self.y + self.height // 4,  # Higher
                'speed_x': 10,
                'speed_y': 0
            })
            bullets.append({
                'x': self.x + self.width,
                'y': self.y + 3 * self.height // 4,  # Lower
                'speed_x': 10,
                'speed_y': 0
            })
        
        # Diagonal-shot powerup
        if self.powerups["diagonal_shot"] > 0:
            bullets.append({
                'x': self.x + self.width,
                'y': self.y + self.height // 2,
                'speed_x': 8,
                'speed_y': -5  # Up-diagonal
            })
            bullets.append({
                'x': self.x + self.width,
                'y': self.y + self.height // 2,
                'speed_x': 8,
                'speed_y': 5   # Down-diagonal
            })
        
        return bullets
    
    def has_shield(self):
        """Check if shield is active"""
        return self.powerups["shield"] > 0
