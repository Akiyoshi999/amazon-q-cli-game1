import pygame
import math

class Bullet:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.width = 8  # 弾の幅
        self.height = 4  # 弾の高さ
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = (255, 255, 0)  # Yellow
        
        # ミサイルの向きを計算（速度ベクトルから角度を求める）
        if speed_x != 0 or speed_y != 0:
            self.angle = math.atan2(speed_y, speed_x)
        else:
            self.angle = 0
        
        # 煙のエフェクト用
        self.smoke_particles = []
        self.smoke_timer = 0
    
    def update(self):
        # 位置の更新
        self.x += self.speed_x
        self.y += self.speed_y
        
        # 煙のエフェクト更新
        self.smoke_timer += 1
        if self.smoke_timer >= 2:  # 2フレームごとに煙を追加
            self.smoke_timer = 0
            # 弾の後ろに煙を追加
            angle = self.angle + math.pi  # 逆方向
            offset_x = math.cos(angle) * (self.width / 2)
            offset_y = math.sin(angle) * (self.width / 2)
            
            self.smoke_particles.append({
                'x': self.x + offset_x,
                'y': self.y + offset_y,
                'size': 2,
                'life': 10  # 煙の寿命（フレーム数）
            })
        
        # 煙のパーティクルを更新
        for particle in self.smoke_particles[:]:
            particle['life'] -= 1
            particle['size'] -= 0.2
            
            # 寿命が尽きたパーティクルを削除
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.smoke_particles.remove(particle)
    
    def draw(self, screen, color=None):
        if color is None:
            color = self.color
        
        # 煙のパーティクルを描画
        for particle in self.smoke_particles:
            alpha = int(255 * (particle['life'] / 10))
            smoke_color = (200, 200, 200, alpha)  # 灰色の煙
            
            # 透明度のある円を描画するための準備
            smoke_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surface, smoke_color, 
                              (int(particle['size']), int(particle['size'])), 
                              int(particle['size']))
            
            # 煙を描画
            screen.blit(smoke_surface, 
                       (int(particle['x'] - particle['size']), 
                        int(particle['y'] - particle['size'])))
        
        # ミサイル本体を描画
        # 回転した座標を計算
        cos_angle = math.cos(self.angle)
        sin_angle = math.sin(self.angle)
        
        # ミサイルの形状を定義（先端、胴体、後部）
        points = [
            (self.x + self.width * cos_angle, self.y + self.width * sin_angle),  # 先端
            (self.x + (self.width/2) * cos_angle - (self.height/2) * sin_angle, 
             self.y + (self.width/2) * sin_angle + (self.height/2) * cos_angle),  # 胴体上部
            (self.x - (self.width/2) * cos_angle - (self.height/2) * sin_angle, 
             self.y - (self.width/2) * sin_angle + (self.height/2) * cos_angle),  # 後部上部
            (self.x - (self.width/2) * cos_angle + (self.height/2) * sin_angle, 
             self.y - (self.width/2) * sin_angle - (self.height/2) * cos_angle),  # 後部下部
            (self.x + (self.width/2) * cos_angle + (self.height/2) * sin_angle, 
             self.y + (self.width/2) * sin_angle - (self.height/2) * cos_angle),  # 胴体下部
        ]
        
        # ミサイル本体を描画
        pygame.draw.polygon(screen, color, points)
        
        # ミサイルの後部に炎を描画（プレイヤーの弾のみ）
        if color == self.color:  # プレイヤーの弾の場合
            flame_color = (255, 100, 0)  # オレンジ色の炎
            flame_points = [
                (self.x - (self.width/2) * cos_angle - (self.height/2) * sin_angle, 
                 self.y - (self.width/2) * sin_angle + (self.height/2) * cos_angle),  # 後部上部
                (self.x - (self.width/2) * cos_angle + (self.height/2) * sin_angle, 
                 self.y - (self.width/2) * sin_angle - (self.height/2) * cos_angle),  # 後部下部
                (self.x - self.width * cos_angle, self.y - self.width * sin_angle),  # 炎の先端
            ]
            pygame.draw.polygon(screen, flame_color, flame_points)
            
            # 内側の炎（より明るい色）
            inner_flame_color = (255, 200, 0)  # 黄色っぽい炎
            inner_flame_points = [
                (self.x - (self.width/2) * cos_angle - (self.height/4) * sin_angle, 
                 self.y - (self.width/2) * sin_angle + (self.height/4) * cos_angle),
                (self.x - (self.width/2) * cos_angle + (self.height/4) * sin_angle, 
                 self.y - (self.width/2) * sin_angle - (self.height/4) * cos_angle),
                (self.x - (self.width*0.8) * cos_angle, self.y - (self.width*0.8) * sin_angle),
            ]
            pygame.draw.polygon(screen, inner_flame_color, inner_flame_points)
