import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 45
        self.height = 35
        self.speed = 5
        self.color = (0, 255, 0)  # Green
        self.engine_color = (255, 100, 0)  # Orange for engine
        self.detail_color = (0, 200, 255)  # Cyan for details
        
        # Engine animation
        self.engine_flicker = 0
        
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
        
        # Update engine animation
        self.engine_flicker = (self.engine_flicker + 1) % 10
    
    def draw(self, screen):
        # Draw engine flames (animated)
        flame_length = 15 + (5 if self.engine_flicker < 5 else 0)
        flame_points = [
            (self.x - flame_length, self.y + self.height // 2),  # Tip
            (self.x, self.y + self.height // 3),                 # Top
            (self.x, self.y + 2 * self.height // 3)              # Bottom
        ]
        pygame.draw.polygon(screen, self.engine_color, flame_points)
        
        # Inner flame (brighter)
        inner_flame_length = flame_length // 2
        inner_flame_points = [
            (self.x - inner_flame_length, self.y + self.height // 2),  # Tip
            (self.x, self.y + self.height // 2 - 5),                   # Top
            (self.x, self.y + self.height // 2 + 5)                    # Bottom
        ]
        pygame.draw.polygon(screen, (255, 255, 0), inner_flame_points)
        
        # Draw main ship body (sleek aerodynamic shape)
        ship_points = [
            (self.x, self.y + self.height // 2),                  # Nose
            (self.x + self.width // 3, self.y),                   # Top front
            (self.x + 2 * self.width // 3, self.y),               # Top middle
            (self.x + self.width, self.y + self.height // 4),     # Top rear
            (self.x + self.width, self.y + 3 * self.height // 4), # Bottom rear
            (self.x + 2 * self.width // 3, self.y + self.height), # Bottom middle
            (self.x + self.width // 3, self.y + self.height)      # Bottom front
        ]
        pygame.draw.polygon(screen, self.color, ship_points)
        
        # Draw wing details
        wing_top = [
            (self.x + self.width // 3, self.y),
            (self.x + self.width // 2, self.y - 10),
            (self.x + 2 * self.width // 3, self.y)
        ]
        pygame.draw.polygon(screen, self.detail_color, wing_top)
        
        wing_bottom = [
            (self.x + self.width // 3, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height + 10),
            (self.x + 2 * self.width // 3, self.y + self.height)
        ]
        pygame.draw.polygon(screen, self.detail_color, wing_bottom)
        
        # Draw cockpit (glass dome)
        cockpit_x = self.x + 2 * self.width // 3
        cockpit_y = self.y + self.height // 2 - 8
        cockpit_width = 15
        cockpit_height = 16
        
        # Cockpit base
        pygame.draw.ellipse(screen, (100, 100, 150), 
                           (cockpit_x, cockpit_y, cockpit_width, cockpit_height))
        
        # Cockpit glass reflection
        pygame.draw.ellipse(screen, (150, 200, 255), 
                           (cockpit_x + 2, cockpit_y + 2, cockpit_width - 4, cockpit_height // 2 - 2))
        
        # Draw thruster nozzles
        pygame.draw.rect(screen, (100, 100, 100), 
                        (self.x + self.width - 5, self.y + self.height // 4 - 2, 8, 4))
        pygame.draw.rect(screen, (100, 100, 100), 
                        (self.x + self.width - 5, self.y + 3 * self.height // 4 - 2, 8, 4))
        
        # Draw shield if active
        if self.powerups["shield"] > 0:
            # Draw shield bubble
            shield_radius = max(self.width, self.height) + 10
            shield_color = (100, 100, 255, 128)  # Blue with transparency
            
            # Create a surface with alpha
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            
            # Draw shield with pulsing effect
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 0.3 + 0.7
            shield_alpha = int(128 * pulse)
            
            # Outer shield
            pygame.draw.circle(shield_surface, (100, 100, 255, shield_alpha), 
                              (shield_radius, shield_radius), shield_radius)
            
            # Inner shield (brighter)
            pygame.draw.circle(shield_surface, (150, 150, 255, shield_alpha), 
                              (shield_radius, shield_radius), shield_radius - 5, 3)
            
            # Shield energy ripples
            ripple_radius = (pygame.time.get_ticks() // 100) % shield_radius
            pygame.draw.circle(shield_surface, (200, 200, 255, shield_alpha // 2), 
                              (shield_radius, shield_radius), ripple_radius, 2)
            
            # Position shield around player
            shield_x = self.x + self.width // 2 - shield_radius
            shield_y = self.y + self.height // 2 - shield_radius
            screen.blit(shield_surface, (shield_x, shield_y))
        
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
