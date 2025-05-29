import pygame
import os

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Sound effects dictionary
        self.sounds = {}
        
        # Load sound effects
        self._load_sounds()
        
        # Music state
        self.current_music = None
    
    def _load_sounds(self):
        # Create sounds directory if it doesn't exist
        sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        if not os.path.exists(sounds_dir):
            os.makedirs(sounds_dir)
        
        # Generate simple sound effects using pygame
        self._generate_sound_effects()
        
        # Load sound effects
        try:
            self.sounds['shoot'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'shoot.wav'))
            self.sounds['explosion'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'explosion.wav'))
            self.sounds['powerup'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'powerup.wav'))
            self.sounds['boss_hit'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'boss_hit.wav'))
            self.sounds['boss_appear'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'boss_appear.wav'))
            self.sounds['boss_defeat'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'boss_defeat.wav'))
            
            # Set volumes
            self.sounds['shoot'].set_volume(0.3)
            self.sounds['explosion'].set_volume(0.5)
            self.sounds['powerup'].set_volume(0.7)
            self.sounds['boss_hit'].set_volume(0.4)
            self.sounds['boss_appear'].set_volume(0.8)
            self.sounds['boss_defeat'].set_volume(0.8)
        except Exception as e:
            print(f"Error loading sounds: {e}")
    
    def _generate_sound_effects(self):
        """Generate simple sound effects using pygame.sndarray"""
        sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        
        try:
            import numpy as np
            
            # Shoot sound (short beep)
            sample_rate = 22050
            duration = 0.1  # seconds
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            shoot_sound = np.sin(2 * np.pi * 440 * t) * 0.5
            shoot_sound = (shoot_sound * 32767).astype(np.int16)
            pygame.sndarray.make_sound(shoot_sound).save(os.path.join(sounds_dir, 'shoot.wav'))
            
            # Explosion sound (noise with decay)
            duration = 0.5
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            noise = np.random.uniform(-1, 1, len(t))
            decay = np.exp(-5 * t)
            explosion_sound = noise * decay
            explosion_sound = (explosion_sound * 32767).astype(np.int16)
            pygame.sndarray.make_sound(explosion_sound).save(os.path.join(sounds_dir, 'explosion.wav'))
            
            # Powerup sound (ascending tone)
            duration = 0.3
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            freq = np.linspace(300, 1200, len(t))
            powerup_sound = np.sin(2 * np.pi * freq * t / sample_rate * 1000)
            powerup_sound = (powerup_sound * 32767).astype(np.int16)
            pygame.sndarray.make_sound(powerup_sound).save(os.path.join(sounds_dir, 'powerup.wav'))
            
            # Boss hit sound (low thud)
            duration = 0.2
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            freq = np.linspace(200, 50, len(t))
            boss_hit = np.sin(2 * np.pi * freq * t / sample_rate * 500) * np.exp(-10 * t)
            boss_hit = (boss_hit * 32767).astype(np.int16)
            pygame.sndarray.make_sound(boss_hit).save(os.path.join(sounds_dir, 'boss_hit.wav'))
            
            # Boss appear sound (ominous tone)
            duration = 1.0
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            boss_appear = np.sin(2 * np.pi * 150 * t) * 0.5 + np.sin(2 * np.pi * 153 * t) * 0.5
            boss_appear = boss_appear * np.exp(-2 * t)
            boss_appear = (boss_appear * 32767).astype(np.int16)
            pygame.sndarray.make_sound(boss_appear).save(os.path.join(sounds_dir, 'boss_appear.wav'))
            
            # Boss defeat sound (explosion followed by fanfare)
            duration = 1.5
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            noise = np.random.uniform(-1, 1, len(t)) * np.exp(-8 * t)
            fanfare = np.zeros_like(t)
            fanfare_idx = int(sample_rate * 0.3)  # Start fanfare after explosion
            fanfare[fanfare_idx:] = np.sin(2 * np.pi * 440 * t[:-fanfare_idx]) * 0.7
            boss_defeat = noise + fanfare
            boss_defeat = (boss_defeat * 32767).astype(np.int16)
            pygame.sndarray.make_sound(boss_defeat).save(os.path.join(sounds_dir, 'boss_defeat.wav'))
            
            # Generate simple BGM
            self._generate_bgm(sounds_dir)
            
        except ImportError:
            print("NumPy not available, skipping sound generation")
        except Exception as e:
            print(f"Error generating sounds: {e}")
    
    def _generate_bgm(self, sounds_dir):
        """Generate simple background music"""
        try:
            import numpy as np
            
            sample_rate = 22050
            duration = 30.0  # 30 seconds loop
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Base rhythm (simple beat)
            beat_freq = 4  # beats per second
            beat = 0.4 * np.sin(2 * np.pi * beat_freq * t)
            beat = beat * (beat > 0)  # Keep only positive parts
            
            # Bass line (repeating pattern)
            bass_notes = [220, 220, 165, 196]  # A3, A3, E3, G3
            bass_pattern_duration = 4.0  # seconds per pattern
            bass = np.zeros_like(t)
            
            for i in range(int(duration / bass_pattern_duration)):
                start_idx = int(i * bass_pattern_duration * sample_rate)
                for j, note in enumerate(bass_notes):
                    note_start = start_idx + int(j * bass_pattern_duration / len(bass_notes) * sample_rate)
                    note_end = start_idx + int((j + 1) * bass_pattern_duration / len(bass_notes) * sample_rate)
                    note_t = t[note_start:note_end] - t[note_start]
                    bass[note_start:note_end] += 0.3 * np.sin(2 * np.pi * note * note_t)
            
            # Melody (simple repeating melody)
            melody_notes = [440, 494, 523, 587, 659, 587, 523, 494]  # Simple scale up and down
            melody_pattern_duration = 8.0  # seconds per pattern
            melody = np.zeros_like(t)
            
            for i in range(int(duration / melody_pattern_duration)):
                start_idx = int(i * melody_pattern_duration * sample_rate)
                for j, note in enumerate(melody_notes):
                    note_start = start_idx + int(j * melody_pattern_duration / len(melody_notes) * sample_rate)
                    note_end = start_idx + int((j + 1) * melody_pattern_duration / len(melody_notes) * sample_rate)
                    note_t = t[note_start:note_end] - t[note_start]
                    # Add envelope to each note
                    envelope = np.exp(-5 * (note_t - 0.5 * (note_t[-1] - note_t[0])) ** 2 / (note_t[-1] - note_t[0]) ** 2)
                    melody[note_start:note_end] += 0.2 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # Combine tracks
            bgm = beat + bass + melody
            
            # Normalize
            bgm = bgm / np.max(np.abs(bgm))
            
            # Convert to 16-bit PCM
            bgm = (bgm * 32767).astype(np.int16)
            
            # Save as WAV
            pygame.sndarray.make_sound(bgm).save(os.path.join(sounds_dir, 'bgm.wav'))
            
            # Create boss music (more intense)
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
                    note_end = start_idx + int((j + 1) * bass_pattern_duration / len(boss_bass_notes) * sample_rate)
                    note_t = t[note_start:note_end] - t[note_start]
                    boss_bass[note_start:note_end] += 0.4 * np.sin(2 * np.pi * note * note_t)
            
            # More dramatic melody
            boss_melody_notes = [523, 494, 523, 587, 523, 494, 440, 392]
            boss_melody = np.zeros_like(t)
            
            for i in range(int(duration / melody_pattern_duration)):
                start_idx = int(i * melody_pattern_duration * sample_rate)
                for j, note in enumerate(boss_melody_notes):
                    note_start = start_idx + int(j * melody_pattern_duration / len(boss_melody_notes) * sample_rate)
                    note_end = start_idx + int((j + 1) * melody_pattern_duration / len(boss_melody_notes) * sample_rate)
                    note_t = t[note_start:note_end] - t[note_start]
                    envelope = np.exp(-5 * (note_t - 0.5 * (note_t[-1] - note_t[0])) ** 2 / (note_t[-1] - note_t[0]) ** 2)
                    boss_melody[note_start:note_end] += 0.3 * np.sin(2 * np.pi * note * note_t) * envelope
            
            # Combine boss tracks
            boss_bgm = boss_beat + boss_bass + boss_melody
            
            # Add some distortion for intensity
            boss_bgm = np.tanh(boss_bgm * 1.5) * 0.8
            
            # Normalize
            boss_bgm = boss_bgm / np.max(np.abs(boss_bgm))
            
            # Convert to 16-bit PCM
            boss_bgm = (boss_bgm * 32767).astype(np.int16)
            
            # Save as WAV
            pygame.sndarray.make_sound(boss_bgm).save(os.path.join(sounds_dir, 'boss_bgm.wav'))
            
        except Exception as e:
            print(f"Error generating BGM: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound effect once"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_name):
        """Play background music in a loop"""
        if self.current_music == music_name:
            return  # Already playing this music
            
        try:
            sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
            music_file = os.path.join(sounds_dir, f'{music_name}.wav')
            
            if os.path.exists(music_file):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(0.4)  # Lower volume for background music
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_music = music_name
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()
        self.current_music = None
