import pygame
import random
import math
from player import Player
from enemy import Enemy
from bullet import Bullet
from boss import Boss
from powerup import PowerUp
from sounds import SoundManager

class Game:
    def __init__(self, width, height, difficulty="normal"):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Horizontal Shooter")
        
        # 難易度設定
        self.difficulty = difficulty
        self._apply_difficulty_settings()
        
        # Game objects
        self.player = Player(50, height // 2)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.powerups = []
        
        # Game state
        self.score = 0
        self.game_over = False
        self.game_cleared = False
        self.spawn_timer = 0
        self.spawn_delay = self.base_spawn_delay  # 難易度に応じて設定
        
        # Powerup spawn settings
        self.powerup_timer = 0
        self.powerup_delay = self.base_powerup_delay  # 難易度に応じて設定
        
        # Boss state
        self.boss = None
        self.boss_spawn_score = 200  # Spawn boss after this score
        self.boss_defeated = False
        
        # Sound manager
        try:
            self.sound_manager = SoundManager()
            # Don't try to play music right away, wait until sounds are generated
        except Exception as e:
            print(f"Error initializing sound manager: {e}")
            self.sound_manager = None
        
        # Load background
        self.bg_color = (0, 0, 50)  # Dark blue background
        
        # Load fonts
        self.font = pygame.font.SysFont(None, 36)
    
    def _apply_difficulty_settings(self):
        """難易度に応じたゲーム設定を適用"""
        if self.difficulty == "easy":
            self.enemy_shoot_chance = 0.005  # 敵の発射確率
            self.base_spawn_delay = 80  # 敵の出現間隔
            self.base_powerup_delay = 240  # パワーアップの出現間隔
            self.boss_hp_multiplier = 0.7  # ボスのHP倍率
            self.player_damage_multiplier = 1.5  # プレイヤーの与えるダメージ倍率
        elif self.difficulty == "normal":
            self.enemy_shoot_chance = 0.007
            self.base_spawn_delay = 60
            self.base_powerup_delay = 300
            self.boss_hp_multiplier = 1.0
            self.player_damage_multiplier = 1.0
        elif self.difficulty == "hard":
            self.enemy_shoot_chance = 0.01
            self.base_spawn_delay = 45
            self.base_powerup_delay = 360
            self.boss_hp_multiplier = 1.3
            self.player_damage_multiplier = 0.8
        else:
            # デフォルトはnormal
            self.difficulty = "normal"
            self.enemy_shoot_chance = 0.007
            self.base_spawn_delay = 60
            self.base_powerup_delay = 300
            self.boss_hp_multiplier = 1.0
            self.player_damage_multiplier = 1.0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over and not self.game_cleared:
                # Fire bullet
                bullet_data = self.player.fire_bullets()
                for data in bullet_data:
                    bullet = Bullet(data['x'], data['y'], data['speed_x'], data['speed_y'])
                    self.player_bullets.append(bullet)
                
                # Play sound
                if self.sound_manager:
                    try:
                        self.sound_manager.play_sound('shoot')
                    except Exception as e:
                        pass  # Silently ignore sound errors
                
            elif event.key == pygame.K_r and (self.game_over or self.game_cleared):
                # Restart game with same difficulty
                self.__init__(self.width, self.height, self.difficulty)
    
    def update(self):
        if self.game_over or self.game_cleared:
            return
            
        # Update player
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.width, self.height)
        
        # Start BGM if not already playing
        if self.sound_manager and not self.sound_manager.current_music:
            try:
                self.sound_manager.play_music('bgm')
            except Exception:
                pass
        
        # Check if boss should spawn
        if self.score >= self.boss_spawn_score and self.boss is None and not self.boss_defeated:
            self.boss = Boss(self.width, self.height, self.boss_hp_multiplier)
            # Stop spawning regular enemies when boss appears
            self.enemies = []
            # Play boss appear sound
            if self.sound_manager:
                try:
                    self.sound_manager.play_sound('boss_appear')
                    self.sound_manager.play_music('boss_bgm')
                except Exception:
                    pass  # Silently ignore sound errors
        
        # Spawn powerups
        self.powerup_timer += 1
        if self.powerup_timer >= self.powerup_delay:
            self.powerup_timer = 0
            # Only spawn powerups during regular gameplay (not during boss fight)
            if self.boss is None:
                x = self.width
                y = random.randint(50, self.height - 50)
                powerup = PowerUp(x, y)
                self.powerups.append(powerup)
        
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
        
        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            
            # Remove powerups that are off-screen
            if powerup.x < -powerup.width:
                self.powerups.remove(powerup)
                continue
                
            # Check collision with player
            if self.check_collision(powerup, self.player):
                message = powerup.apply_effect(self.player)
                self.player.set_powerup_message(message)
                self.powerups.remove(powerup)
                if self.sound_manager:
                    try:
                        self.sound_manager.play_sound('powerup')
                    except Exception:
                        pass
        
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
            if self.check_collision(self.boss, self.player) and not self.player.has_shield():
                self.game_over = True
                if self.sound_manager:
                    try:
                        self.sound_manager.play_sound('explosion')
                    except Exception:
                        pass
        
        # Update regular enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Remove enemies that are off-screen
            if enemy.x < -enemy.width:
                self.enemies.remove(enemy)
                continue
                
            # Enemy shoots randomly - 難易度に応じた確率で発射
            if random.random() < self.enemy_shoot_chance:
                bullet = Bullet(enemy.x, enemy.y + enemy.height // 2, -5, 0)
                self.enemy_bullets.append(bullet)
                
            # Check collision with player
            if self.check_collision(enemy, self.player) and not self.player.has_shield():
                self.game_over = True
                if self.sound_manager:
                    try:
                        self.sound_manager.play_sound('explosion')
                    except Exception:
                        pass
        
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
                # 難易度に応じたダメージを与える
                boss_defeated = self.boss.take_damage(10 * self.player_damage_multiplier)
                if self.sound_manager:
                    try:
                        self.sound_manager.play_sound('boss_hit')
                    except Exception:
                        pass
                
                if boss_defeated:
                    self.boss = None
                    self.boss_defeated = True
                    self.game_cleared = True  # ゲームクリア状態に設定
                    self.score += 100  # Extra points for defeating boss
                    if self.sound_manager:
                        try:
                            self.sound_manager.play_sound('boss_defeat')
                            self.sound_manager.play_music('bgm')  # Return to normal music
                        except Exception:
                            pass
                break
                
            # Check collision with regular enemies
            for enemy in self.enemies[:]:
                if self.check_collision(bullet, enemy):
                    self.player_bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    if self.sound_manager:
                        try:
                            self.sound_manager.play_sound('explosion')
                        except Exception:
                            pass
                    
                    # Chance to spawn powerup when enemy is destroyed
                    if random.random() < 0.1:  # 10% chance
                        powerup = PowerUp(enemy.x, enemy.y)
                        self.powerups.append(powerup)
                    
                    break
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            
            # Remove bullets that are off-screen
            if bullet.x < 0:
                self.enemy_bullets.remove(bullet)
                continue
                
            # Check collision with player
            if self.check_collision(bullet, self.player) and not self.player.has_shield():
                self.enemy_bullets.remove(bullet)
                self.game_over = True
                if self.sound_manager:
                    try:
                        self.sound_manager.play_sound('explosion')
                    except Exception:
                        pass
    
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
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw bullets
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
            
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen, (255, 0, 0))  # Red for enemy bullets
        
        # Draw score and difficulty
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        difficulty_text = self.font.render(f"Difficulty: {self.difficulty.capitalize()}", True, (255, 255, 255))
        self.screen.blit(difficulty_text, (10, 40))
        
        # Draw powerup status
        self._draw_powerup_status()
        
        # Draw boss approaching message
        if self.boss_spawn_score - self.score <= 50 and self.boss is None and not self.boss_defeated:
            warning_text = self.font.render("WARNING: Boss approaching!", True, (255, 50, 50))
            text_rect = warning_text.get_rect(center=(self.width // 2, 50))
            self.screen.blit(warning_text, text_rect)
        
        # Draw game cleared message
        if self.game_cleared:
            victory_text = self.font.render("GAME CLEARED!", True, (50, 255, 50))
            text_rect = victory_text.get_rect(center=(self.width // 2, self.height // 2 - 40))
            self.screen.blit(victory_text, text_rect)
            
            score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(score_text, score_rect)
            
            restart_text = self.font.render("Press R to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
        
        # Draw game over message
        elif self.game_over:
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press R to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
            self.screen.blit(restart_text, restart_rect)
        
        # Update display
        pygame.display.flip()
    
    def _draw_powerup_status(self):
        # Draw powerup status at the bottom of the screen
        status_y = self.height - 30
        font = pygame.font.SysFont(None, 24)
        
        # Multi-shot status
        if self.player.powerups["multi_shot"] > 0:
            text = font.render(f"Multi-Shot: {self.player.powerups['multi_shot'] // 60}s", True, (255, 255, 0))
            self.screen.blit(text, (10, status_y))
        
        # Diagonal-shot status
        if self.player.powerups["diagonal_shot"] > 0:
            text = font.render(f"Diag-Shot: {self.player.powerups['diagonal_shot'] // 60}s", True, (0, 255, 255))
            self.screen.blit(text, (150, status_y))
        
        # Speed-up status
        if self.player.powerups["speed_up"] > 0:
            text = font.render(f"Speed-Up: {self.player.powerups['speed_up'] // 60}s", True, (0, 255, 0))
            self.screen.blit(text, (290, status_y))
        
        # Shield status
        if self.player.powerups["shield"] > 0:
            text = font.render(f"Shield: {self.player.powerups['shield'] // 60}s", True, (100, 100, 255))
            self.screen.blit(text, (430, status_y))
    
    def check_collision(self, obj1, obj2):
        # Simple rectangle collision
        return (obj1.x < obj2.x + obj2.width and
                obj1.x + obj1.width > obj2.x and
                obj1.y < obj2.y + obj2.height and
                obj1.y + obj1.height > obj2.y)
