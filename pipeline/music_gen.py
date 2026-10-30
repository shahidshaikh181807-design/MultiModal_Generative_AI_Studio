import os
import numpy as np
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import scipy.io.wavfile as wavfile

# Musical scales (MIDI note numbers)
SCALES = {
    "C Major (Energetic & Uplifting)": [60, 62, 64, 65, 67, 69, 71, 72, 74, 76],
    "A Minor (Emotional & Melancholic)": [57, 60, 62, 64, 65, 67, 69, 72, 74, 76],
    "D Dorian (Cinematic & Sci-Fi)": [50, 52, 53, 55, 57, 59, 60, 62, 65, 67],
    "Pentatonic Blues (Soulful & Expressive)": [60, 63, 65, 66, 67, 70, 72, 75]
}

def midi_to_freq(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69.0) / 12.0))

def generate_4bar_melody(scale_name="C Major (Energetic & Uplifting)", tempo=120, latent_seed=42, output_midi_path="outputs/sample_melody.mid"):
    """
    Generates a structured 4-bar melody (MusicVAE / Latent Sequence style).
    Each bar has 4 beats (16 beats total, 4/4 meter).
    """
    os.makedirs(os.path.dirname(output_midi_path), exist_ok=True)
    np.random.seed(latent_seed)
    
    scale = SCALES.get(scale_name, SCALES["C Major (Energetic & Uplifting)"])
    
    # MusicVAE latent interpolation style:
    # A 4-dimensional latent trajectory: Bar 1 Theme, Bar 2 Variation, Bar 3 Climax, Bar 4 Resolution
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Set tempo (microseconds per beat)
    tempo_val = mido.bpm2tempo(tempo)
    track.append(MetaMessage('set_tempo', tempo=tempo_val, time=0))
    track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    track.append(MetaMessage('track_name', name='MusicVAE_4Bar_Melody', time=0))
    
    ticks_per_beat = mid.ticks_per_beat # Default 480
    events = [] # list of (pitch, start_time_beats, duration_beats, velocity)
    
    # 4 bars, each 4 beats
    for bar in range(4):
        bar_start = bar * 4.0
        # Latent motif drift
        if bar == 0: # Exposition (Root focus)
            base_idx = 0
            steps = [0.0, 1.0, 2.0, 3.0]
            durations = [1.0, 0.5, 0.5, 2.0]
        elif bar == 1: # Development (Step up)
            base_idx = 2
            steps = [0.0, 0.75, 1.5, 2.5, 3.0]
            durations = [0.75, 0.75, 1.0, 0.5, 1.0]
        elif bar == 2: # Climax (High register)
            base_idx = 4
            steps = [0.0, 0.5, 1.0, 2.0, 3.0]
            durations = [0.5, 0.5, 1.0, 1.0, 1.0]
        else: # Cadence & Resolution
            base_idx = 1
            steps = [0.0, 1.0, 2.0]
            durations = [1.0, 1.0, 2.0]
            
        for s, d in zip(steps, durations):
            # Sample from scale with latent bias
            jitter = np.random.choice([-1, 0, 1, 2], p=[0.15, 0.5, 0.25, 0.1])
            idx = int(np.clip(base_idx + jitter, 0, len(scale) - 1))
            pitch = scale[idx]
            velocity = int(np.random.randint(80, 115))
            start_time = bar_start + s
            events.append((pitch, start_time, d, velocity))
            
    # Sort events by start time
    events.sort(key=lambda x: x[1])
    
    # Write to MIDI Track
    current_tick = 0
    midi_timeline = [] # (tick, 'on'/'off', pitch, vel)
    for pitch, start_b, dur_b, vel in events:
        start_tick = int(start_b * ticks_per_beat)
        end_tick = int((start_b + dur_b * 0.9) * ticks_per_beat)
        midi_timeline.append((start_tick, 'on', pitch, vel))
        midi_timeline.append((end_tick, 'off', pitch, 0))
        
    midi_timeline.sort(key=lambda x: x[0])
    
    last_tick = 0
    for tick, event_type, pitch, vel in midi_timeline:
        delta = max(0, tick - last_tick)
        if event_type == 'on':
            track.append(Message('note_on', note=pitch, velocity=vel, time=delta))
        else:
            track.append(Message('note_off', note=pitch, velocity=vel, time=delta))
        last_tick = tick
        
    track.append(MetaMessage('end_of_track', time=ticks_per_beat))
    mid.save(output_midi_path)
    return events, output_midi_path

def synthesize_midi_to_wav(events, tempo=120, output_wav_path="outputs/sample_melody.wav", sample_rate=44100):
    """
    Synthesizes MIDI notes into rich polyphonic audio with harmonic overtone synthesis
    and ADSR envelope (Attack, Decay, Sustain, Release) + stereo warm acoustics.
    """
    os.makedirs(os.path.dirname(output_wav_path), exist_ok=True)
    seconds_per_beat = 60.0 / tempo
    total_beats = 17.0 # 4 bars + 1 beat ring out
    total_samples = int(total_beats * seconds_per_beat * sample_rate)
    audio = np.zeros(total_samples, dtype=np.float32)
    
    for pitch, start_b, dur_b, vel in events:
        freq = midi_to_freq(pitch)
        start_sec = start_b * seconds_per_beat
        dur_sec = dur_b * seconds_per_beat
        
        start_sample = int(start_sec * sample_rate)
        note_samples = int(dur_sec * sample_rate)
        if start_sample + note_samples > total_samples:
            note_samples = total_samples - start_sample
            
        t = np.linspace(0, dur_sec, note_samples, endpoint=False)
        
        # Additive synthesis with warm acoustic piano/marimba timbre (fundamental + 3 harmonics)
        waveform = (
            1.0 * np.sin(2 * np.pi * freq * t) +
            0.45 * np.sin(2 * np.pi * 2 * freq * t) +
            0.20 * np.sin(2 * np.pi * 3 * freq * t) +
            0.08 * np.sin(2 * np.pi * 4 * freq * t)
        )
        
        # ADSR Envelope
        attack = int(0.02 * sample_rate)
        decay = int(0.08 * sample_rate)
        release = int(0.06 * sample_rate)
        sustain_level = 0.7
        
        env = np.ones(note_samples, dtype=np.float32) * sustain_level
        if note_samples > attack:
            env[:attack] = np.linspace(0, 1.0, attack)
        if note_samples > attack + decay:
            env[attack:attack+decay] = np.linspace(1.0, sustain_level, decay)
        if note_samples > release:
            env[-release:] = np.linspace(sustain_level, 0.0, release)
            
        note_signal = waveform * env * (vel / 127.0) * 0.35
        audio[start_sample:start_sample + note_samples] += note_signal
        
    # Apply soft-clipping / normalization
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.88
        
    # Convert to 16-bit PCM WAV
    audio_int16 = (audio * 32767).astype(np.int16)
    wavfile.write(output_wav_path, sample_rate, audio_int16)
    return output_wav_path
