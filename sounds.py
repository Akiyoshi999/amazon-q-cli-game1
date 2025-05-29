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
            duration = 10.0  # 10 seconds loop (shorter for testing)
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Base rhythm
            beat_freq = 4  # beats per second
            beat = 0.4 * np.sin(2 * np.pi * beat_freq * t)
            beat = beat * (beat > 0)  # Keep only positive parts
            
            # Bass line
            bass_notes = [220, 220, 165, 196]  # A3, A3, E3, G3
            bass_pattern_duration = 4.0  # seconds per pattern
            bass = np.zeros_like(t)
            
            for i in range(int(duration / bass_pattern_duration)):
                start_idx = int(i * bass_pattern_duration * sample_rate)
                for j, note in enumerate(bass_notes):
                    note_start = start_idx + int(j * bass_pattern_duration / len(bass_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * bass_pattern_duration / len(bass_notes) * sample_rate), len(t))
                    if note_start < len(t) and note_end > note_start:
                        note_t = t[note_start:note_end] - t[note_start]
                        bass[note_start:note_end] += 0.3 * np.sin(2 * np.pi * note * note_t)
            
            # Melody
            melody_notes = [440, 494, 523, 587, 659, 587, 523, 494]  # Simple scale up and down
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
                            envelope = np.exp(-5 * (note_t - 0.5 * (note_t[-1] - note_t[0])) ** 2 / max(0.0001, (note_t[-1] - note_t[0])) ** 2)
                            melody[note_start:note_end] += 0.2 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # Combine tracks
            bgm = beat + bass + melody
            
            # Normalize
            max_val = np.max(np.abs(bgm))
            if max_val > 0:
                bgm = bgm / max_val
            
            # Convert to stereo
            bgm_stereo = np.column_stack((bgm, bgm))
            
            # Convert to 16-bit PCM
            bgm_stereo = (bgm_stereo * 32767).astype(np.int16)
            
            # Create sound object
            self.sounds['bgm'] = pygame.sndarray.make_sound(bgm_stereo)
            self.sounds['bgm'].set_volume(0.4)
            
            # Create boss music
            boss_beat_freq = 5  # Faster beat
            boss_beat = 0.5 * np.sin(2 * np.pi * boss_beat_freq * t)
            boss_beat = boss_beat * (boss_beat > 0)
            
            # More intense bass line
            boss_bass_notes = [165, 196, 165, 147]  # Lower, more ominous
            boss_bass = np.zeros_like(t)
            
            for i in range(int(duration / bass_pattern_duration)):
                start_idx = int(i * bass_pattern_duration * sample_rate)
                for j, note in enumerate(boss_bass_notes):
                    note_start = start_idx + int(j * bass_pattern_duration / len(boss_bass_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * bass_pattern_duration / len(boss_bass_notes) * sample_rate), len(t))
                    if note_start < len(t):
                        note_t = t[note_start:note_end] - t[note_start]
                        boss_bass[note_start:note_end] += 0.4 * np.sin(2 * np.pi * note * note_t)
            
            # More dramatic melody
            boss_melody_notes = [523, 494, 523, 587, 523, 494, 440, 392]
            boss_melody = np.zeros_like(t)
            
            for i in range(int(duration / melody_pattern_duration)):
                start_idx = int(i * melody_pattern_duration * sample_rate)
                for j, note in enumerate(boss_melody_notes):
                    note_start = start_idx + int(j * melody_pattern_duration / len(boss_melody_notes) * sample_rate)
                    note_end = min(start_idx + int((j + 1) * melody_pattern_duration / len(boss_melody_notes) * sample_rate), len(t))
                    if note_start < len(t) and note_end > note_start:
                        note_t = t[note_start:note_end] - t[note_start]
                        if len(note_t) > 0:
                            envelope = np.exp(-5 * (note_t - 0.5 * (note_t[-1] - note_t[0])) ** 2 / max(0.0001, (note_t[-1] - note_t[0])) ** 2)
                            boss_melody[note_start:note_end] += 0.3 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # Combine boss tracks
            boss_bgm = boss_beat + boss_bass + boss_melody
            
            # Add some distortion for intensity
            boss_bgm = np.tanh(boss_bgm * 1.5) * 0.8
            
            # Normalize
            max_val = np.max(np.abs(boss_bgm))
            if max_val > 0:
                boss_bgm = boss_bgm / max_val
            
            # Convert to stereo
            boss_bgm_stereo = np.column_stack((boss_bgm, boss_bgm))
            
            # Convert to 16-bit PCM
            boss_bgm_stereo = (boss_bgm_stereo * 32767).astype(np.int16)
            
            # Create sound object
            self.sounds['boss_bgm'] = pygame.sndarray.make_sound(boss_bgm_stereo)
            self.sounds['boss_bgm'].set_volume(0.4)
            
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
