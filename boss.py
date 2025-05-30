import pygame
import random
import math

class Boss:
    def __init__(self, screen_width, screen_height, hp_multiplier=1.0):
        # Position and size
        self.width = 60  # 80から60に縮小
        self.height = 60  # 80から60に縮小
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
        self.max_hp = int(200 * hp_multiplier)  # 難易度に応じてHP調整
        self.hp = self.max_hp
        self.shoot_timer = 0
        self.shoot_delay = 30  # Shoot every 30 frames
        
        # Phase tracking
        self.phase = 1  # Start at phase 1
        self.phase_thresholds = [0.7, 0.4, 0.2]  # Phase changes at 70%, 40%, and 20% HP
        self.current_phase_index = 0
        
        # Appearance
        self.color = (200, 0, 0)  # Dark red
        self.hit_effect = 0  # For flashing when hit
        self.core_rotation = 0  # For rotating core
        
        # Special attack patterns for different phases
        self.phase_patterns = {
            1: ["normal", "circle", "zigzag", "charge"],
            2: ["circle", "zigzag", "charge", "spiral"],
            3: ["zigzag", "charge", "spiral", "burst"],
            4: ["charge", "spiral", "burst", "laser"]
        }
        
        # Special attack variables
        self.spiral_angle = 0
        self.burst_timer = 0
        self.laser_charging = 0
        self.laser_firing = 0
    
    def update(self):
        # Update hit effect (flashing when hit)
        if self.hit_effect > 0:
            self.hit_effect -= 1
        
        # Update core rotation
        self.core_rotation = (self.core_rotation + 2) % 360
        
        # Check for phase change
        self._check_phase()
        
        # Update pattern timer and change pattern
        self.pattern_timer += 1
        if self.pattern_timer > 300:  # Change pattern every 5 seconds (300 frames)
            self.pattern_timer = 0
            self.current_pattern = random.choice(self.phase_patterns[self.phase])
            # Reset pattern-specific variables
            self.circle_angle = 0
            self.move_timer = 0
            self.spiral_angle = 0
            self.burst_timer = 0
            self.laser_charging = 0
            self.laser_firing = 0
        
        # Apply current movement pattern
        if self.current_pattern == "normal":
            self._normal_movement()
        elif self.current_pattern == "circle":
            self._circle_movement()
        elif self.current_pattern == "zigzag":
            self._zigzag_movement()
        elif self.current_pattern == "charge":
            self._charge_movement()
        elif self.current_pattern == "spiral":
            self._spiral_movement()
        elif self.current_pattern == "burst":
            self._burst_movement()
        elif self.current_pattern == "laser":
            self._laser_movement()
        
        # Keep boss on screen
        self._stay_on_screen()
    
    def _check_phase(self):
        # Calculate current HP percentage
        hp_percent = self.hp / self.max_hp
        
        # Check if we need to advance to next phase
        if (self.current_phase_index < len(self.phase_thresholds) and 
            hp_percent <= self.phase_thresholds[self.current_phase_index]):
            self.phase += 1
            self.current_phase_index += 1
            # Increase speed with each phase
            self.speed += 0.5
            # Force pattern change
            self.pattern_timer = 290  # Almost time for a new pattern
    
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
        circle_speed = 0.02 + (self.phase - 1) * 0.005  # Faster circles in later phases
        self.circle_angle += circle_speed
        self.x = self.circle_center_x + math.cos(self.circle_angle) * self.circle_radius
        self.y = self.circle_center_y + math.sin(self.circle_angle) * self.circle_radius
    
    def _zigzag_movement(self):
        # Zigzag movement
        zigzag_speed = self.speed * (1 + (self.phase - 1) * 0.2)  # Faster zigzags in later phases
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
        self.x += self.direction_x * zigzag_speed
        self.y += self.direction_y * (zigzag_speed * 1.5)  # Faster vertical movement
    
    def _charge_movement(self):
        # Charge toward the left side then return
        charge_speed = self.speed * (1 + (self.phase - 1) * 0.3)  # Faster charges in later phases
        self.move_timer += 1
        
        if self.move_timer < 60:  # Prepare phase
            # Move slowly up and down
            self.y += math.sin(self.move_timer * 0.1) * 2
        elif self.move_timer < 90:  # Charge phase
            self.x -= charge_speed * 3  # Fast movement to the left
        else:  # Return phase
            if self.x < self.screen_width - 150:
                self.x += charge_speed * 2  # Return to the right side
            else:
                # Reset pattern when returned
                self.pattern_timer = 290  # Almost time for a new pattern
    
    def _spiral_movement(self):
        # Phase 2+: Spiral outward then inward
        self.spiral_angle += 0.05
        spiral_radius = 50 + 30 * math.sin(self.spiral_angle * 0.2)
        
        # Move in a spiral pattern
        self.x = self.screen_width - 150 + math.cos(self.spiral_angle) * spiral_radius
        self.y = self.screen_height // 2 + math.sin(self.spiral_angle) * spiral_radius
    
    def _burst_movement(self):
        # Phase 3+: Quick bursts in random directions
        self.burst_timer += 1
        
        if self.burst_timer % 60 < 10:  # Burst for 10 frames every 60 frames
            # Random burst direction
            if self.burst_timer % 60 == 0:
                self.direction_x = random.uniform(-1, 1)
                self.direction_y = random.uniform(-1, 1)
                # Normalize
                magnitude = math.sqrt(self.direction_x**2 + self.direction_y**2)
                if magnitude > 0:
                    self.direction_x /= magnitude
                    self.direction_y /= magnitude
            
            # Move quickly in burst direction
            burst_speed = self.speed * 4
            self.x += self.direction_x * burst_speed
            self.y += self.direction_y * burst_speed
        else:
            # Slow movement between bursts
            self._normal_movement()
    
    def _laser_movement(self):
        # Phase 4: Charge and fire a powerful laser
        if self.laser_charging < 90:  # Charging phase (1.5 seconds)
            self.laser_charging += 1
            # Move to center vertically during charging
            target_y = self.screen_height // 2 - self.height // 2
            if abs(self.y - target_y) > 2:
                if self.y < target_y:
                    self.y += 2
                else:
                    self.y -= 2
            # Slight horizontal movement
            self.x += math.sin(self.laser_charging * 0.1) * 1
        elif self.laser_firing < 60:  # Firing phase (1 second)
            self.laser_firing += 1
            # Stay relatively still during firing
            self.x += random.uniform(-0.5, 0.5)  # Just a little shake
        else:
            # Reset after firing
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
        
        # Adjust shoot delay based on phase
        phase_shoot_delay = max(15, self.shoot_delay - (self.phase - 1) * 4)  # 10から15に増加、減少幅も5から4に調整
        
        if self.shoot_timer >= phase_shoot_delay:
            self.shoot_timer = 0
            should_shoot = True
            
            # Different shooting patterns based on current movement pattern and phase
            if self.current_pattern == "normal":
                # Single bullet (all phases)
                bullet_data.append({
                    'x': self.x, 
                    'y': self.y + self.height // 2,
                    'speed_x': -7,
                    'speed_y': 0
                })
                
                # Additional bullets in later phases
                if self.phase >= 2:
                    bullet_data.append({
                        'x': self.x, 
                        'y': self.y + self.height // 2,
                        'speed_x': -7,
                        'speed_y': -1
                    })
                    bullet_data.append({
                        'x': self.x, 
                        'y': self.y + self.height // 2,
                        'speed_x': -7,
                        'speed_y': 1
                    })
                
            elif self.current_pattern == "circle":
                # Spread shot (3-5 bullets depending on phase)
                num_bullets = 3 + min(2, self.phase - 1)
                spread = 0.6  # Total spread angle in radians
                
                for i in range(num_bullets):
                    angle = -spread/2 + spread * i / (num_bullets - 1)
                    bullet_data.append({
                        'x': self.x, 
                        'y': self.y + self.height // 2,
                        'speed_x': -7 * math.cos(angle),
                        'speed_y': -7 * math.sin(angle)
                    })
                
            elif self.current_pattern == "zigzag":
                # Two bullets, up and down (all phases)
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
                
                # Additional bullets in later phases
                if self.phase >= 3:
                    bullet_data.append({
                        'x': self.x, 
                        'y': self.y + self.height // 2,
                        'speed_x': -7,
                        'speed_y': 0
                    })
                
            elif self.current_pattern == "charge":
                # Rapid fire during charge
                if self.move_timer >= 60 and self.move_timer < 90:
                    # Faster shooting during charge
                    if random.random() < 0.25:  # 0.3から0.25に減少
                        bullet_data.append({
                            'x': self.x, 
                            'y': self.y + random.randint(0, self.height),
                            'speed_x': -8,
                            'speed_y': random.uniform(-1, 1)
                        })
                        
                        # Additional bullets in phase 4
                        if self.phase >= 4 and random.random() < 0.4:  # 0.5から0.4に減少
                            bullet_data.append({
                                'x': self.x, 
                                'y': self.y + random.randint(0, self.height),
                                'speed_x': -8,
                                'speed_y': random.uniform(-2, 2)
                            })
            
            elif self.current_pattern == "spiral":
                # Phase 2+: Spiral bullets
                for i in range(self.phase):  # More bullets in later phases
                    angle = self.spiral_angle + i * (2 * math.pi / self.phase)
                    bullet_data.append({
                        'x': self.x + self.width // 2, 
                        'y': self.y + self.height // 2,
                        'speed_x': -5 * math.cos(angle),
                        'speed_y': -5 * math.sin(angle)
                    })
            
            elif self.current_pattern == "burst":
                # Phase 3+: Burst of bullets in all directions
                if self.burst_timer % 60 < 10 and self.burst_timer % 6 == 0:  # 5から6に増加
                    num_bullets = 8  # 8 directions
                    for i in range(num_bullets):
                        angle = i * (2 * math.pi / num_bullets)
                        bullet_data.append({
                            'x': self.x + self.width // 2, 
                            'y': self.y + self.height // 2,
                            'speed_x': -6 * math.cos(angle),
                            'speed_y': -6 * math.sin(angle)
                        })
            
            elif self.current_pattern == "laser":
                # Phase 4: Powerful laser attack
                if self.laser_charging >= 60 and self.laser_charging < 90 and self.laser_charging % 10 == 0:
                    # Warning shots during charging
                    bullet_data.append({
                        'x': self.x, 
                        'y': self.y + self.height // 2,
                        'speed_x': -10,
                        'speed_y': 0
                    })
                elif self.laser_firing > 0 and self.laser_firing < 60 and self.laser_firing % 4 == 0:  # 3から4に増加
                    # Rapid laser fire
                    bullet_data.append({
                        'x': self.x, 
                        'y': self.y + self.height // 2,
                        'speed_x': -12,
                        'speed_y': random.uniform(-0.5, 0.5)  # Slight spread
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
        
        # Draw boss core (rotating)
        core_radius = self.width // 4
        core_color = self._get_phase_color()
        pygame.draw.circle(screen, core_color, (center_x, center_y), core_radius)
        
        # Draw rotating energy lines in core
        for i in range(4):
            angle = math.radians(self.core_rotation + i * 90)
            line_length = core_radius - 5
            x1 = center_x + math.cos(angle) * line_length
            y1 = center_y + math.sin(angle) * line_length
            x2 = center_x - math.cos(angle) * line_length
            y2 = center_y - math.sin(angle) * line_length
            pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
        
        # Draw boss details (eyes)
        eye_radius = self.width // 10
        eye_color = (255, 255, 0)  # Yellow eyes
        
        # Eyes change based on phase
        if self.phase >= 3:
            eye_color = (255, 0, 0)  # Red eyes in later phases
        
        pygame.draw.circle(screen, eye_color, 
                          (center_x - core_radius // 2, center_y - core_radius // 2), 
                          eye_radius)
        pygame.draw.circle(screen, eye_color, 
                          (center_x - core_radius // 2, center_y + core_radius // 2), 
                          eye_radius)
        
        # Draw special effects based on current pattern
        if self.current_pattern == "laser" and self.laser_charging >= 30:
            # Draw charging effect
            charge_radius = (self.laser_charging - 30) / 2
            charge_color = (255, 100, 100, 128)
            
            # Create a surface with alpha
            charge_surface = pygame.Surface((charge_radius * 2, charge_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(charge_surface, charge_color, (charge_radius, charge_radius), charge_radius)
            
            # Position charge effect
            charge_x = self.x - charge_radius
            charge_y = self.y + self.height // 2 - charge_radius
            screen.blit(charge_surface, (charge_x, charge_y))
            
            # Draw laser beam when firing
            if self.laser_firing > 0:
                beam_height = 20 + 10 * math.sin(self.laser_firing * 0.2)
                beam_length = self.x
                pygame.draw.rect(screen, (255, 50, 50), 
                                (0, self.y + self.height // 2 - beam_height // 2, 
                                 beam_length, beam_height))
                
                # Draw beam core (brighter)
                core_height = beam_height // 2
                pygame.draw.rect(screen, (255, 200, 200), 
                                (0, self.y + self.height // 2 - core_height // 2, 
                                 beam_length, core_height))
        
        # Draw HP bar
        self.draw_hp_bar(screen)
    
    def _get_phase_color(self):
        # Core color changes with phase
        if self.phase == 1:
            return (255, 100, 0)  # Orange
        elif self.phase == 2:
            return (255, 50, 50)  # Red
        elif self.phase == 3:
            return (200, 0, 200)  # Purple
        else:
            return (255, 0, 0)  # Bright red
    
    def draw_hp_bar(self, screen):
        # Draw HP bar background
        bar_width = 200
        bar_height = 20
        bar_x = self.screen_width - bar_width - 20
        bar_y = 20
        
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Draw HP bar fill
        fill_width = int((self.hp / self.max_hp) * bar_width)
        
        # Color changes based on HP percentage and phase
        hp_percent = self.hp / self.max_hp
        if hp_percent > 0.7:
            fill_color = (0, 255, 0)  # Green
        elif hp_percent > 0.4:
            fill_color = (255, 255, 0)  # Yellow
        elif hp_percent > 0.2:
            fill_color = (255, 150, 0)  # Orange
        else:
            fill_color = (255, 0, 0)  # Red
            
        pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Draw phase indicators
        for i, threshold in enumerate(self.phase_thresholds):
            marker_x = bar_x + int(threshold * bar_width)
            pygame.draw.line(screen, (255, 255, 255), 
                            (marker_x, bar_y), (marker_x, bar_y + bar_height), 2)
        
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw text
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"BOSS: {self.hp}/{self.max_hp} (Phase {self.phase})", True, (255, 255, 255))
        screen.blit(text, (bar_x + 10, bar_y + 2))
