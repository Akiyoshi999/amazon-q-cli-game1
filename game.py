import pygame
import random
import math
from player import Player
from enemy import Enemy
from bullet import Bullet
from boss import Boss

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Horizontal Shooter")
        
        # Game objects
        self.player = Player(50, height // 2)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        
        # Game state
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_delay = 60  # Frames between enemy spawns
        
        # Boss state
        self.boss = None
        self.boss_spawn_score = 200  # Spawn boss after this score
        self.boss_defeated = False
        
        # Load background
        self.bg_color = (0, 0, 50)  # Dark blue background
        
        # Load fonts
        self.font = pygame.font.SysFont(None, 36)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over:
                # Fire bullet
                bullet = Bullet(self.player.x + self.player.width, 
                               self.player.y + self.player.height // 2, 
                               10, 0)  # Horizontal bullet
                self.player_bullets.append(bullet)
            elif event.key == pygame.K_r and self.game_over:
                # Restart game
                self.__init__(self.width, self.height)
    
    def update(self):
        if self.game_over:
            return
            
        # Update player
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.width, self.height)
        
        # Check if boss should spawn
        if self.score >= self.boss_spawn_score and self.boss is None and not self.boss_defeated:
            self.boss = Boss(self.width, self.height)
            # Stop spawning regular enemies when boss appears
            self.enemies = []
        
        # Spawn regular enemies (only if boss is not present)
        if self.boss is None:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_timer = 0
                y = random.randint(50, self.height - 50)
                enemy = Enemy(self.width, y)
                self.enemies.append(enemy)
                
                # Increase difficulty over time
                if self.spawn_delay > 20:
                    self.spawn_delay -= 1
        
        # Update boss
        if self.boss is not None:
            self.boss.update()
            
            # Boss shooting
            should_shoot, bullet_data = self.boss.shoot()
            if should_shoot:
                for data in bullet_data:
                    bullet = Bullet(data['x'], data['y'], data['speed_x'], data['speed_y'])
                    self.enemy_bullets.append(bullet)
            
            # Check collision with player
            if self.check_collision(self.boss, self.player):
                self.game_over = True
        
        # Update regular enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Remove enemies that are off-screen
            if enemy.x < -enemy.width:
                self.enemies.remove(enemy)
                
            # Enemy shoots randomly
            if random.random() < 0.01:  # 1% chance per frame
                bullet = Bullet(enemy.x, enemy.y + enemy.height // 2, -5, 0)
                self.enemy_bullets.append(bullet)
                
            # Check collision with player
            if self.check_collision(enemy, self.player):
                self.game_over = True
        
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet.update()
            
            # Remove bullets that are off-screen
            if bullet.x > self.width:
                self.player_bullets.remove(bullet)
                continue
            
            # Check collision with boss
            if self.boss is not None and self.check_collision(bullet, self.boss):
                self.player_bullets.remove(bullet)
                boss_defeated = self.boss.take_damage(10)
                if boss_defeated:
                    self.boss = None
                    self.boss_defeated = True
                    self.score += 100  # Extra points for defeating boss
                break
                
            # Check collision with regular enemies
            for enemy in self.enemies[:]:
                if self.check_collision(bullet, enemy):
                    self.player_bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            
            # Remove bullets that are off-screen
            if bullet.x < 0:
                self.enemy_bullets.remove(bullet)
                continue
                
            # Check collision with player
            if self.check_collision(bullet, self.player):
                self.enemy_bullets.remove(bullet)
                self.game_over = True
    
    def render(self):
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw boss
        if self.boss is not None:
            self.boss.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw bullets
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
            
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen, (255, 0, 0))  # Red for enemy bullets
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Draw boss approaching message
        if self.boss_spawn_score - self.score <= 50 and self.boss is None and not self.boss_defeated:
            warning_text = self.font.render("WARNING: Boss approaching!", True, (255, 50, 50))
            text_rect = warning_text.get_rect(center=(self.width // 2, 50))
            self.screen.blit(warning_text, text_rect)
        
        # Draw boss defeated message
        if self.boss_defeated and self.score >= self.boss_spawn_score + 100:
            victory_text = self.font.render("Boss Defeated!", True, (50, 255, 50))
            text_rect = victory_text.get_rect(center=(self.width // 2, 50))
            self.screen.blit(victory_text, text_rect)
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to restart", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, text_rect)
        
        # Update display
        pygame.display.flip()
    
    def check_collision(self, obj1, obj2):
        # Simple rectangle collision
        return (obj1.x < obj2.x + obj2.width and
                obj1.x + obj1.width > obj2.x and
                obj1.y < obj2.y + obj2.height and
                obj1.y + obj1.height > obj2.y)
