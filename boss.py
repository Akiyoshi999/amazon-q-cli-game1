import pygame
import random
import math

class Boss:
    def __init__(self, screen_width, screen_height):
        # Position and size
        self.width = 80
        self.height = 80
        self.x = screen_width - self.width - 50  # Position on the right side
        self.y = screen_height // 2 - self.height // 2
        
        # Movement
        self.speed = 3
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.move_timer = 0
        self.move_delay = 60  # Change direction every 60 frames
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        
        # Special movement patterns
        self.pattern_timer = 0
        self.current_pattern = "normal"
        self.patterns = ["normal", "circle", "zigzag", "charge"]
        self.circle_angle = 0
        self.circle_radius = 100
        self.circle_center_x = screen_width - 150
        self.circle_center_y = screen_height // 2
        
        # Stats
        self.max_hp = 100
        self.hp = self.max_hp
        self.shoot_timer = 0
        self.shoot_delay = 30  # Shoot every 30 frames
        
        # Appearance
        self.color = (200, 0, 0)  # Dark red
        self.hit_effect = 0  # For flashing when hit
    
    def update(self):
        # Update hit effect (flashing when hit)
        if self.hit_effect > 0:
            self.hit_effect -= 1
        
        # Update pattern timer and change pattern
        self.pattern_timer += 1
        if self.pattern_timer > 300:  # Change pattern every 5 seconds (300 frames)
            self.pattern_timer = 0
            self.current_pattern = random.choice(self.patterns)
            # Reset pattern-specific variables
            self.circle_angle = 0
            self.move_timer = 0
        
        # Apply current movement pattern
        if self.current_pattern == "normal":
            self._normal_movement()
        elif self.current_pattern == "circle":
            self._circle_movement()
        elif self.current_pattern == "zigzag":
            self._zigzag_movement()
        elif self.current_pattern == "charge":
            self._charge_movement()
        
        # Keep boss on screen
        self._stay_on_screen()
    
    def _normal_movement(self):
        # Random movement with occasional direction changes
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self.direction_x = random.choice([-1, 0, 1])
            self.direction_y = random.choice([-1, 0, 1])
            
            # Ensure boss doesn't stay still
            if self.direction_x == 0 and self.direction_y == 0:
                self.direction_y = random.choice([-1, 1])
        
        # Move boss
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
    
    def _circle_movement(self):
        # Move in a circular pattern
        self.circle_angle += 0.02
        self.x = self.circle_center_x + math.cos(self.circle_angle) * self.circle_radius
        self.y = self.circle_center_y + math.sin(self.circle_angle) * self.circle_radius
    
    def _zigzag_movement(self):
        # Zigzag movement
        self.move_timer += 1
        if self.move_timer >= 20:  # Change vertical direction more frequently
            self.move_timer = 0
            self.direction_y *= -1
        
        # Move horizontally back and forth
        if self.x > self.screen_width - 150:
            self.direction_x = -1
        elif self.x < self.screen_width - 250:
            self.direction_x = 1
        
        # Apply movement
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * (self.speed * 1.5)  # Faster vertical movement
    
    def _charge_movement(self):
        # Charge toward the left side then return
        self.move_timer += 1
        
        if self.move_timer < 60:  # Prepare phase
            # Move slowly up and down
            self.y += math.sin(self.move_timer * 0.1) * 2
        elif self.move_timer < 90:  # Charge phase
            self.x -= self.speed * 3  # Fast movement to the left
        else:  # Return phase
            if self.x < self.screen_width - 150:
                self.x += self.speed * 2  # Return to the right side
            else:
                # Reset pattern when returned
                self.pattern_timer = 290  # Almost time for a new pattern
    
    def _stay_on_screen(self):
        # Keep boss on screen
        min_x = self.screen_width // 2  # Don't go beyond the middle of the screen
        max_x = self.screen_width - self.width - 20
        min_y = 20
        max_y = self.screen_height - self.height - 20
        
        self.x = max(min_x, min(self.x, max_x))
        self.y = max(min_y, min(self.y, max_y))
    
    def shoot(self):
        # Determine if it's time to shoot
        self.shoot_timer += 1
        should_shoot = False
        bullet_data = []
        
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            should_shoot = True
            
            # Different shooting patterns based on current movement pattern
            if self.current_pattern == "normal":
                # Single bullet
                bullet_data.append({
                    'x': self.x, 
                    'y': self.y + self.height // 2,
                    'speed_x': -7,
                    'speed_y': 0
                })
            elif self.current_pattern == "circle":
                # Spread shot (3 bullets)
                for angle in [-0.2, 0, 0.2]:
                    bullet_data.append({
                        'x': self.x, 
                        'y': self.y + self.height // 2,
                        'speed_x': -7 * math.cos(angle),
                        'speed_y': -7 * math.sin(angle)
                    })
            elif self.current_pattern == "zigzag":
                # Two bullets, up and down
                bullet_data.append({
                    'x': self.x, 
                    'y': self.y + self.height // 4,
                    'speed_x': -6,
                    'speed_y': -2
                })
                bullet_data.append({
                    'x': self.x, 
                    'y': self.y + 3 * self.height // 4,
                    'speed_x': -6,
                    'speed_y': 2
                })
            elif self.current_pattern == "charge":
                # Rapid fire during charge
                if self.move_timer >= 60 and self.move_timer < 90:
                    # Faster shooting during charge
                    if random.random() < 0.3:  # 30% chance each frame
                        bullet_data.append({
                            'x': self.x, 
                            'y': self.y + random.randint(0, self.height),
                            'speed_x': -8,
                            'speed_y': random.uniform(-1, 1)
                        })
        
        return should_shoot, bullet_data
    
    def take_damage(self, damage=10):
        self.hp -= damage
        self.hit_effect = 5  # Set flash effect for 5 frames
        return self.hp <= 0  # Return True if boss is defeated
    
    def draw(self, screen):
        # Determine color based on hit effect
        color = self.color
        if self.hit_effect > 0:
            color = (255, 200, 200)  # Flash white when hit
        
        # Draw boss body (octagon shape for more complex appearance)
        points = []
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        for i in range(8):
            angle = math.pi / 4 * i
            radius = self.width // 2
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            points.append((x, y))
        
        pygame.draw.polygon(screen, color, points)
        
        # Draw boss core
        core_radius = self.width // 4
        pygame.draw.circle(screen, (255, 100, 0), (center_x, center_y), core_radius)
        
        # Draw boss details (eyes)
        eye_radius = self.width // 10
        pygame.draw.circle(screen, (255, 255, 0), 
                          (center_x - core_radius // 2, center_y - core_radius // 2), 
                          eye_radius)
        pygame.draw.circle(screen, (255, 255, 0), 
                          (center_x - core_radius // 2, center_y + core_radius // 2), 
                          eye_radius)
        
        # Draw HP bar
        self.draw_hp_bar(screen)
    
    def draw_hp_bar(self, screen):
        # Draw HP bar background
        bar_width = 200
        bar_height = 20
        bar_x = self.screen_width - bar_width - 20
        bar_y = 20
        
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Draw HP bar fill
        fill_width = int((self.hp / self.max_hp) * bar_width)
        
        # Color changes based on HP percentage
        if self.hp > self.max_hp * 0.6:
            fill_color = (0, 255, 0)  # Green
        elif self.hp > self.max_hp * 0.3:
            fill_color = (255, 255, 0)  # Yellow
        else:
            fill_color = (255, 0, 0)  # Red
            
        pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw text
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"BOSS: {self.hp}/{self.max_hp}", True, (255, 255, 255))
        screen.blit(text, (bar_x + 10, bar_y + 2))
