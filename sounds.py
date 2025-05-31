import pygame
import os
import numpy as np

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Sound effects dictionary
        self.sounds = {}
        
        # Music state
        self.current_music = None
        
        # Create simple sounds directly in memory
        self._create_sounds()
    
    def _create_sounds(self):
        """Create simple sound effects directly in memory"""
        try:
            # Shoot sound (short beep)
            sample_rate = 22050
            
            # Shoot sound
            duration = 0.1
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            shoot_sound = np.sin(2 * np.pi * 440 * t) * 0.5
            shoot_sound = np.column_stack((shoot_sound, shoot_sound))
            shoot_sound = (shoot_sound * 32767).astype(np.int16)
            self.sounds['shoot'] = pygame.sndarray.make_sound(shoot_sound)
            self.sounds['shoot'].set_volume(0.3)
            
            # Explosion sound
            duration = 0.5
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            noise = np.random.uniform(-1, 1, len(t))
            decay = np.exp(-5 * t)
            explosion_sound = noise * decay
            explosion_sound = np.column_stack((explosion_sound, explosion_sound))
            explosion_sound = (explosion_sound * 32767).astype(np.int16)
            self.sounds['explosion'] = pygame.sndarray.make_sound(explosion_sound)
            self.sounds['explosion'].set_volume(0.5)
            
            # Powerup sound
            duration = 0.3
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            freq = np.linspace(300, 1200, len(t))
            powerup_sound = np.sin(2 * np.pi * freq * t / sample_rate * 1000)
            powerup_sound = np.column_stack((powerup_sound, powerup_sound))
            powerup_sound = (powerup_sound * 32767).astype(np.int16)
            self.sounds['powerup'] = pygame.sndarray.make_sound(powerup_sound)
            self.sounds['powerup'].set_volume(0.7)
            
            # Boss hit sound
            duration = 0.2
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            freq = np.linspace(200, 50, len(t))
            boss_hit = np.sin(2 * np.pi * freq * t / sample_rate * 500) * np.exp(-10 * t)
            boss_hit = np.column_stack((boss_hit, boss_hit))
            boss_hit = (boss_hit * 32767).astype(np.int16)
            self.sounds['boss_hit'] = pygame.sndarray.make_sound(boss_hit)
            self.sounds['boss_hit'].set_volume(0.4)
            
            # Boss appear sound
            duration = 1.0
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            boss_appear = np.sin(2 * np.pi * 150 * t) * 0.5 + np.sin(2 * np.pi * 153 * t) * 0.5
            boss_appear = boss_appear * np.exp(-2 * t)
            boss_appear = np.column_stack((boss_appear, boss_appear))
            boss_appear = (boss_appear * 32767).astype(np.int16)
            self.sounds['boss_appear'] = pygame.sndarray.make_sound(boss_appear)
            self.sounds['boss_appear'].set_volume(0.8)
            
            # Boss defeat sound
            duration = 1.5
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            noise = np.random.uniform(-1, 1, len(t)) * np.exp(-8 * t)
            fanfare = np.zeros_like(t)
            fanfare_idx = int(sample_rate * 0.3)  # Start fanfare after explosion
            if fanfare_idx < len(t):
                fanfare[fanfare_idx:] = np.sin(2 * np.pi * 440 * t[:len(t)-fanfare_idx]) * 0.7
            boss_defeat = noise + fanfare
            boss_defeat = np.column_stack((boss_defeat, boss_defeat))
            boss_defeat = (boss_defeat * 32767).astype(np.int16)
            self.sounds['boss_defeat'] = pygame.sndarray.make_sound(boss_defeat)
            self.sounds['boss_defeat'].set_volume(0.8)
            
            # Create BGM
            self._create_bgm()
            
        except Exception as e:
            print(f"Error creating sounds: {e}")
    
    def _create_bgm(self):
        """Create background music directly in memory"""
        try:
            sample_rate = 22050
            duration = 10.0  # 10 seconds loop
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # --- 通常BGM (より明るく爽快な曲調に変更) ---
            
            # ベースリズム (よりテンポアップ)
            beat_freq = 4.5  # beats per second (4から4.5に増加)
            beat = 0.3 * np.sin(2 * np.pi * beat_freq * t)
            beat = beat * (beat > 0)  # Keep only positive parts
            
            # ベースライン (より明るい音階を使用)
            bass_notes = [262, 330, 392, 349]  # C4, E4, G4, F4 (明るい長調)
            bass_pattern_duration = 4.0  # seconds per pattern
            bass = np.zeros_like(t)
            
            for i in range(int(duration / bass_pattern_duration)):
                start_idx = int(i * bass_pattern_duration * sample_rate)
                for j, note in enumerate(bass_notes):
                    note_start = start_idx + int(j * bass_pattern_duration / len(bass_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * bass_pattern_duration / len(bass_notes) * sample_rate), len(t))
                    if note_start < len(t) and note_end > note_start:
                        note_t = t[note_start:note_end] - t[note_start]
                        bass[note_start:note_end] += 0.3 * np.sin(2 * np.pi * note * note_t)  # 0.25から0.3に増加
            
            # メロディ (より明るく軽快なメロディ)
            melody_notes = [523, 587, 659, 698, 784, 698, 659, 587]  # C5, D5, E5, F5, G5, F5, E5, D5
            melody_pattern_duration = 8.0  # seconds per pattern
            melody = np.zeros_like(t)
            
            for i in range(int(duration / melody_pattern_duration)):
                start_idx = int(i * melody_pattern_duration * sample_rate)
                for j, note in enumerate(melody_notes):
                    note_start = start_idx + int(j * melody_pattern_duration / len(melody_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * melody_pattern_duration / len(melody_notes) * sample_rate), len(t))
                    if note_start < len(t) and note_end > note_start:
                        note_t = t[note_start:note_end] - t[note_start]
                        if len(note_t) > 0:
                            envelope = np.exp(-3 * (note_t - 0.5 * (note_t[-1] - note_t[0])) ** 2 / max(0.0001, (note_t[-1] - note_t[0])) ** 2)
                            melody[note_start:note_end] += 0.25 * np.sin(2 * np.pi * note * note_t) * envelope  # 0.2から0.25に増加
            
            # 高音部の装飾 (より明るいアルペジオ)
            high_notes = [784, 880, 988, 1047, 1175, 1047, 988, 880]  # G5, A5, B5, C6, D6, C6, B5, A5
            high_pattern_duration = 4.0
            high_melody = np.zeros_like(t)
            
            # 高音部の装飾をより多く
            for i in range(int(duration / high_pattern_duration)):
                start_idx = int(i * high_pattern_duration * sample_rate)
                for j, note in enumerate(high_notes):
                    note_start = start_idx + int(j * high_pattern_duration / len(high_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * high_pattern_duration / len(high_notes) * sample_rate), len(t))
                    if note_start < len(t) and note_end > note_start:
                        note_t = t[note_start:note_end] - t[note_start]
                        if len(note_t) > 0:
                            # 短い音符のエンベロープ
                            envelope = np.exp(-8 * (note_t - 0.2 * (note_t[-1] - note_t[0])) ** 2 / max(0.0001, (note_t[-1] - note_t[0])) ** 2)
                            high_melody[note_start:note_end] += 0.2 * np.sin(2 * np.pi * note * note_t) * envelope  # 0.15から0.2に増加
            
            # 明るい効果音を追加
            bright_fx = np.zeros_like(t)
            fx_pattern = [0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75, 8.25, 8.75, 9.25, 9.75]
            for time_point in fx_pattern:
                if time_point < duration:
                    idx = int(time_point * sample_rate)
                    # 明るい効果音の音符
                    fx_notes = [1047, 1175, 1319, 1397]  # C6, D6, E6, F6
                    note = fx_notes[int(time_point * 2) % len(fx_notes)]
                    
                    # 短い効果音
                    note_duration = 0.1
                    end_idx = min(idx + int(note_duration * sample_rate), len(t))
                    if idx < len(t):
                        note_t = np.arange(end_idx - idx) / sample_rate
                        envelope = np.exp(-12 * note_t)
                        bright_fx[idx:end_idx] += 0.15 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # トラックを結合
            bgm = beat + bass + melody + high_melody + bright_fx
            
            # 正規化
            max_val = np.max(np.abs(bgm))
            if max_val > 0:
                bgm = bgm / max_val
            
            # ステレオに変換
            bgm_stereo = np.column_stack((bgm, bgm))
            
            # 16-bit PCMに変換
            bgm_stereo = (bgm_stereo * 32767).astype(np.int16)
            
            # サウンドオブジェクトを作成
            self.sounds['bgm'] = pygame.sndarray.make_sound(bgm_stereo)
            self.sounds['bgm'].set_volume(0.45)  # 0.4から0.45に増加
            
            # --- ボス戦BGM (より盛り上がる感じに変更) ---
            
            # 速いビート (よりテンポアップ)
            boss_beat_freq = 6  # 速いビート (5から6に増加)
            boss_beat = 0.5 * np.sin(2 * np.pi * boss_beat_freq * t)
            boss_beat = boss_beat * (boss_beat > 0)
            
            # 力強いベースライン
            boss_bass_notes = [196, 233, 196, 175]  # G3, A#3, G3, F3
            boss_bass = np.zeros_like(t)
            
            for i in range(int(duration / bass_pattern_duration)):
                start_idx = int(i * bass_pattern_duration * sample_rate)
                for j, note in enumerate(boss_bass_notes):
                    note_start = start_idx + int(j * bass_pattern_duration / len(boss_bass_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * bass_pattern_duration / len(boss_bass_notes) * sample_rate), len(t))
                    if note_start < len(t):
                        note_t = t[note_start:note_end] - t[note_start]
                        # より強いベース音
                        boss_bass[note_start:note_end] += 0.45 * np.sin(2 * np.pi * note * note_t)
            
            # 盛り上がるメロディ
            boss_melody_notes = [392, 466, 523, 622, 587, 523, 466, 392]  # G4, A#4, C5, D#5, D5, C5, A#4, G4
            boss_melody = np.zeros_like(t)
            
            for i in range(int(duration / melody_pattern_duration)):
                start_idx = int(i * melody_pattern_duration * sample_rate)
                for j, note in enumerate(boss_melody_notes):
                    note_start = start_idx + int(j * melody_pattern_duration / len(boss_melody_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * melody_pattern_duration / len(boss_melody_notes) * sample_rate), len(t))
                    if note_start < len(t) and note_end > note_start:
                        note_t = t[note_start:note_end] - t[note_start]
                        if len(note_t) > 0:
                            # より強いアタックのエンベロープ
                            envelope = np.exp(-4 * (note_t - 0.3 * (note_t[-1] - note_t[0])) ** 2 / max(0.0001, (note_t[-1] - note_t[0])) ** 2)
                            boss_melody[note_start:note_end] += 0.35 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # 高音部の効果音 (より派手に)
            boss_fx_notes = [784, 740, 784, 831, 784, 740, 698, 659]  # G5, F#5, G5, G#5, G5, F#5, F5, E5
            boss_fx = np.zeros_like(t)
            
            # 不規則なリズムで高音を鳴らす (より多く)
            fx_pattern = [0.3, 0.5, 0.7, 1.0, 1.2, 1.5, 1.8, 2.0, 2.3, 2.5, 2.8, 3.0, 3.3, 3.5, 3.8, 4.0,
                         4.3, 4.5, 4.8, 5.0, 5.3, 5.5, 5.8, 6.0, 6.3, 6.5, 6.8, 7.0, 7.3, 7.5, 7.8, 8.0,
                         8.3, 8.5, 8.8, 9.0, 9.3, 9.5, 9.8]
            for time_point in fx_pattern:
                if time_point < duration:
                    idx = int(time_point * sample_rate)
                    note_idx = int(time_point * 4) % len(boss_fx_notes)
                    note = boss_fx_notes[note_idx]
                    
                    # 短い効果音
                    note_duration = 0.1
                    end_idx = min(idx + int(note_duration * sample_rate), len(t))
                    if idx < len(t):
                        note_t = np.arange(end_idx - idx) / sample_rate
                        envelope = np.exp(-15 * note_t)
                        boss_fx[idx:end_idx] += 0.25 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # ドラム風の効果音を追加
            drum_pattern = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5]
            drum_sound = np.zeros_like(t)
            for time_point in drum_pattern:
                if time_point < duration:
                    idx = int(time_point * sample_rate)
                    # ドラム音の長さ
                    drum_duration = 0.05
                    end_idx = min(idx + int(drum_duration * sample_rate), len(t))
                    if idx < len(t):
                        # ノイズベースのドラム音
                        drum_t = np.arange(end_idx - idx) / sample_rate
                        noise = np.random.uniform(-1, 1, len(drum_t))
                        envelope = np.exp(-30 * drum_t)
                        drum_sound[idx:end_idx] += 0.4 * noise * envelope
            
            # ボスBGMのトラックを結合
            boss_bgm = boss_beat + boss_bass + boss_melody + boss_fx + drum_sound
            
            # 歪みを加えて迫力を出す
            boss_bgm = np.tanh(boss_bgm * 1.8) * 0.8
            
            # 正規化
            max_val = np.max(np.abs(boss_bgm))
            if max_val > 0:
                boss_bgm = boss_bgm / max_val
            
            # ステレオに変換
            boss_bgm_stereo = np.column_stack((boss_bgm, boss_bgm))
            
            # 16-bit PCMに変換
            boss_bgm_stereo = (boss_bgm_stereo * 32767).astype(np.int16)
            
            # サウンドオブジェクトを作成
            self.sounds['boss_bgm'] = pygame.sndarray.make_sound(boss_bgm_stereo)
            self.sounds['boss_bgm'].set_volume(0.5)  # ボス戦はやや大きめの音量
            
        except Exception as e:
            print(f"Error creating BGM: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound effect once"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def play_music(self, music_name):
        """Play background music in a loop"""
        if self.current_music == music_name:
            return  # Already playing this music
            
        try:
            if music_name in self.sounds:
                # Stop any currently playing music
                pygame.mixer.stop()
                
                # Play the new music in a loop
                self.sounds[music_name].play(-1)  # -1 means loop indefinitely
                self.current_music = music_name
            else:
                print(f"Music not found: {music_name}")
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        """Stop the currently playing music"""
        try:
            pygame.mixer.stop()
            self.current_music = None
        except Exception as e:
            print(f"Error stopping music: {e}")
