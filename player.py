import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 25
        self.speed = 5
        self.color = (0, 255, 255)
        self.shield_active = False
        self.shield_timer = 0
        self.shield_duration = 300  # フレーム数（約5秒）
        self.max_hp = 2
        self.hp = self.max_hp
        self.hit_effect_timer = 0
        self.hit_effect_duration = 30  # 0.5秒間
        self.hitbox_radius = 3  # 当たり判定の半径
        self.powerups = {
            "multi_shot": 0,
            "diagonal_shot": 0,
            "speed_up": 0,
            "shield": 0
        }

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # 画面外に出ないように制限
        self.x = max(self.width // 2, min(self.x, 800 - self.width // 2))
        self.y = max(self.height // 2, min(self.y, 600 - self.height // 2))

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = self.shield_duration

    def update(self, keys=None, width=None, height=None):
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
        
        if self.hit_effect_timer > 0:
            self.hit_effect_timer -= 1
            
        # パワーアップの時間を減らす
        for powerup_type in self.powerups:
            if self.powerups[powerup_type] > 0:
                self.powerups[powerup_type] -= 1
                
                # シールドの場合は特別処理
                if powerup_type == "shield" and self.powerups[powerup_type] > 0:
                    self.shield_active = True
                
                # スピードアップの効果が切れたら元に戻す
                if powerup_type == "speed_up" and self.powerups[powerup_type] == 0:
                    self.speed = 5  # 元のスピードに戻す
            
        # キー入力による移動処理（引数が提供されている場合）
        if keys is not None:
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1
            
            self.move(dx, dy)

    def draw(self, screen):
        # 自機の描画（より洗練されたデザイン）
        # 基本的な船体
        ship_color = (0, 255, 255)  # 通常色
        
        # ダメージエフェクト（赤く点滅）
        if self.hit_effect_timer > 0 and self.hit_effect_timer % 6 < 3:
            ship_color = (255, 100, 100)  # ダメージ時は赤く
        
        # 船体の描画
        points = [
            (self.x + self.width // 2, self.y),
            (self.x - self.width // 2, self.y - self.height // 3),
            (self.x - self.width // 2 + 10, self.y),
            (self.x - self.width // 2, self.y + self.height // 3)
        ]
        pygame.draw.polygon(screen, ship_color, points)
        
        # エンジン炎
        flame_length = 10 + (pygame.time.get_ticks() % 10) // 5 * 5  # アニメーション効果
        pygame.draw.polygon(screen, (255, 165, 0), [
            (self.x - self.width // 2, self.y - self.height // 6),
            (self.x - self.width // 2 - flame_length, self.y),
            (self.x - self.width // 2, self.y + self.height // 6)
        ])
        
        # 翼の詳細
        pygame.draw.line(screen, (0, 200, 200), 
                        (self.x - self.width // 4, self.y - self.height // 3),
                        (self.x + self.width // 4, self.y - self.height // 6), 2)
        pygame.draw.line(screen, (0, 200, 200), 
                        (self.x - self.width // 4, self.y + self.height // 3),
                        (self.x + self.width // 4, self.y + self.height // 6), 2)
        
        # コックピット
        pygame.draw.circle(screen, (200, 200, 255), 
                        (self.x + self.width // 6, self.y), self.height // 5)
        pygame.draw.circle(screen, (255, 255, 255), 
                        (self.x + self.width // 6 + 2, self.y - 2), self.height // 10)
        
        # シールドエフェクト
        if self.shield_active:
            shield_radius = self.width + 5 + math.sin(pygame.time.get_ticks() / 100) * 3
            pygame.draw.circle(screen, (100, 100, 255, 128), (self.x, self.y), shield_radius, 2)
            # エネルギー波紋
            wave_offset = (pygame.time.get_ticks() % 30) / 30
            for i in range(3):
                wave_radius = shield_radius - 10 + i * 7 + wave_offset * 7
                if wave_radius < shield_radius:
                    pygame.draw.circle(screen, (150, 150, 255, 100), (self.x, self.y), wave_radius, 1)
        
        # 当たり判定の赤い点
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 3)
        
        # HPバーの描画
        self.draw_hp_bar(screen)

    def draw_hp_bar(self, screen):
        # HPバーの背景
        bar_width = 40
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.height - 10
        
        # 背景（グレー）
        pygame.draw.rect(screen, (70, 70, 70), (bar_x, bar_y, bar_width, bar_height))
        
        # HPに応じたバーの長さ
        hp_ratio = self.hp / self.max_hp
        current_bar_width = int(bar_width * hp_ratio)
        
        # HPに応じた色（満タン時は緑、半分以下は赤）
        if hp_ratio > 0.5:
            bar_color = (0, 255, 0)  # 緑
        else:
            bar_color = (255, 0, 0)  # 赤
        
        # HPバー
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, current_bar_width, bar_height))
        
        # 枠線
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 1)

    def get_hitbox_center(self):
        # 当たり判定は中心点のみ
        return (self.x, self.y)
        
    def take_damage(self):
        if not self.shield_active:
            self.hp -= 1
            self.hit_effect_timer = self.hit_effect_duration
            # HPが0になった場合のみゲームオーバーを返す
            return self.hp <= 0
        return False
    def has_shield(self):
        return self.shield_active
        
    def fire_bullets(self):
        # 基本的な弾のデータを返す
        bullet_data = []
        
        # マルチショットが有効な場合
        if self.powerups["multi_shot"] > 0:
            # 中央の弾
            bullet_data.append({
                'x': self.x + self.width // 2,
                'y': self.y,
                'speed_x': 10,
                'speed_y': 0
            })
            
            # 上下の弾
            bullet_data.append({
                'x': self.x + self.width // 2,
                'y': self.y - 10,
                'speed_x': 10,
                'speed_y': 0
            })
            
            bullet_data.append({
                'x': self.x + self.width // 2,
                'y': self.y + 10,
                'speed_x': 10,
                'speed_y': 0
            })
        
        # 斜め発射が有効な場合
        elif self.powerups["diagonal_shot"] > 0:
            # 中央の弾
            bullet_data.append({
                'x': self.x + self.width // 2,
                'y': self.y,
                'speed_x': 10,
                'speed_y': 0
            })
            
            # 斜め上下の弾
            bullet_data.append({
                'x': self.x + self.width // 2,
                'y': self.y,
                'speed_x': 9,
                'speed_y': -3
            })
            
            bullet_data.append({
                'x': self.x + self.width // 2,
                'y': self.y,
                'speed_x': 9,
                'speed_y': 3
            })
        
        # 通常の弾
        else:
            bullet_data.append({
                'x': self.x + self.width // 2,
                'y': self.y,
                'speed_x': 10,
                'speed_y': 0
            })
        
        return bullet_data
        
    def set_powerup_message(self, message):
        # パワーアップメッセージを設定（必要に応じて実装）
        pass
