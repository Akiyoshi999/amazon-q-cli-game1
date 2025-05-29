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
            
            # --- 通常BGM ---
            # よりメロディックで穏やかな通常BGM
            
            # ベースリズム (穏やかなビート)
            beat_freq = 3  # beats per second (少し遅め)
            beat = 0.3 * np.sin(2 * np.pi * beat_freq * t)
            beat = beat * (beat > 0)  # Keep only positive parts
            
            # ベースライン (明るいパターン)
            bass_notes = [220, 262, 196, 175]  # A3, C4, G3, F3
            bass_pattern_duration = 4.0  # seconds per pattern
            bass = np.zeros_like(t)
            
            for i in range(int(duration / bass_pattern_duration)):
                start_idx = int(i * bass_pattern_duration * sample_rate)
                for j, note in enumerate(bass_notes):
                    note_start = start_idx + int(j * bass_pattern_duration / len(bass_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * bass_pattern_duration / len(bass_notes) * sample_rate), len(t))
                    if note_start < len(t) and note_end > note_start:
                        note_t = t[note_start:note_end] - t[note_start]
                        bass[note_start:note_end] += 0.25 * np.sin(2 * np.pi * note * note_t)
            
            # メロディ (明るく軽快なメロディ)
            melody_notes = [392, 440, 494, 523, 494, 440, 392, 349]  # G4, A4, B4, C5, B4, A4, G4, F4
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
                            melody[note_start:note_end] += 0.2 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # 高音部の装飾 (アルペジオ風)
            high_notes = [659, 587, 523, 494, 523, 587, 659, 784]  # E5, D5, C5, B4, C5, D5, E5, G5
            high_pattern_duration = 4.0
            high_melody = np.zeros_like(t)
            
            for i in range(int(duration / high_pattern_duration)):
                start_idx = int(i * high_pattern_duration * sample_rate)
                for j, note in enumerate(high_notes):
                    note_start = start_idx + int(j * high_pattern_duration / len(high_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * high_pattern_duration / len(high_notes) * sample_rate), len(t))
                    if note_start < len(t) and note_end > note_start:
                        note_t = t[note_start:note_end] - t[note_start]
                        if len(note_t) > 0:
                            # 短い音符のエンベロープ
                            envelope = np.exp(-10 * (note_t - 0.2 * (note_t[-1] - note_t[0])) ** 2 / max(0.0001, (note_t[-1] - note_t[0])) ** 2)
                            high_melody[note_start:note_end] += 0.15 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # トラックを結合
            bgm = beat + bass + melody + high_melody
            
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
            self.sounds['bgm'].set_volume(0.4)
            
            # --- ボス戦BGM ---
            # より激しく緊迫感のあるボス戦BGM
            
            # 速いビート
            boss_beat_freq = 5  # 速いビート
            boss_beat = 0.5 * np.sin(2 * np.pi * boss_beat_freq * t)
            boss_beat = boss_beat * (boss_beat > 0)
            
            # 低音で不気味なベースライン
            boss_bass_notes = [147, 165, 147, 131]  # D3, E3, D3, C3 (低めの音)
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
            
            # ドラマチックなメロディ
            boss_melody_notes = [392, 370, 392, 466, 440, 392, 349, 330]  # G4, F#4, G4, A#4, A4, G4, F4, E4
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
            
            # 緊迫感を出す高音の効果音
            boss_fx_notes = [587, 554, 587, 622, 587, 554, 523, 494]  # D5, C#5, D5, D#5, D5, C#5, C5, B4
            boss_fx = np.zeros_like(t)
            
            # 不規則なリズムで高音を鳴らす
            fx_pattern = [0.5, 0.7, 1.2, 1.5, 2.3, 2.5, 3.1, 3.6, 4.2, 4.4, 5.0, 5.5, 6.1, 6.3, 7.0, 7.5, 8.2, 8.4, 9.0, 9.5]
            for time_point in fx_pattern:
                if time_point < duration:
                    idx = int(time_point * sample_rate)
                    note_idx = int(time_point) % len(boss_fx_notes)
                    note = boss_fx_notes[note_idx]
                    
                    # 短い効果音
                    note_duration = 0.1
                    end_idx = min(idx + int(note_duration * sample_rate), len(t))
                    if idx < len(t):
                        note_t = np.arange(end_idx - idx) / sample_rate
                        envelope = np.exp(-15 * note_t)
                        boss_fx[idx:end_idx] += 0.25 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # ボスBGMのトラックを結合
            boss_bgm = boss_beat + boss_bass + boss_melody + boss_fx
            
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
