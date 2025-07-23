# main.py (The Full Cosmic Orchestra Conductor)

import os
import time
import logging
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from typing import Dict, Any, List

import config
# --- MUDANÇA: Importa de ambos os clientes ---
from nasa_client import fetch_nasa_data
from sidc_client import fetch_sunspot_data

# ... (Todas as classes de Instrumentos e a classe CosmicOrchestra permanecem exatamente as mesmas) ...
class CME_Melody:
    def __init__(self):
        self.scale_notes_hz: List[float] = [
            65.41, 73.42, 77.78, 87.31, 98.00, 103.83, 116.54, 130.81, 146.83, 
            155.56, 174.61, 196.00, 207.65, 233.08, 261.63, 293.66, 311.13, 
            349.23, 392.00, 415.30, 466.16 ]
        self.melody_sequence: List[float] = [110.0] * config.CME_MELODY_LENGTH
        self.current_step: int = 0
        self.last_step_time: float = 0
        self.note_frame_count: int = 0
    def update(self, data: Dict[str, Any]):
        speed_series = data.get('cme_speed_series', [])
        if not speed_series:
            self.melody_sequence = [self.scale_notes_hz[0]] * config.CME_MELODY_LENGTH
            return
        new_melody = []
        for speed in speed_series:
            norm_speed = (speed - config.CME_SPEED_MIN) / (config.CME_SPEED_MAX - config.CME_SPEED_MIN)
            norm_speed = np.clip(norm_speed, 0, 1)
            note_index = int(norm_speed * (len(self.scale_notes_hz) - 1))
            new_melody.append(self.scale_notes_hz[note_index])
        while len(new_melody) < config.CME_MELODY_LENGTH: new_melody.extend(new_melody)
        self.melody_sequence = new_melody[:config.CME_MELODY_LENGTH]
    def process(self, t: np.ndarray, frames: int, samplerate: int) -> np.ndarray:
        if time.time() - self.last_step_time > config.CME_NOTE_DURATION_SECONDS:
            self.current_step = (self.current_step + 1) % len(self.melody_sequence)
            self.last_step_time = time.time()
            self.note_frame_count = 0
        current_frequency = self.melody_sequence[self.current_step]
        t_note = (np.arange(self.note_frame_count, self.note_frame_count + frames)) / samplerate
        attack = 0.01
        decay = config.CME_NOTE_DURATION_SECONDS - attack
        env = np.exp(-t_note / decay)
        if int(attack * samplerate) > 0:
            env[:int(attack * samplerate)] = np.linspace(0, 1, int(attack * samplerate))
        self.note_frame_count += frames
        return np.sin(2 * np.pi * current_frequency * t_note) * env * 0.7
class GST_Noise:
    def __init__(self): self.intensity = 0.0
    def update(self, data: Dict[str, Any]):
        kp_index = data.get('max_kp_index', 0)
        self.intensity = (kp_index / config.KP_INDEX_MAX) * config.KP_NOISE_MAX_INTENSITY
    def process(self, t: np.ndarray, frames: int, samplerate: int) -> np.ndarray:
        return np.random.uniform(-1, 1, size=frames) * self.intensity
class Sunspot_Drone:
    def __init__(self): self.frequency = config.SUNSPOT_FREQ_MIN
    def update(self, data: Dict[str, Any]):
        sunspots = data.get('sunspot_number', 0)
        norm_sunspots = min(sunspots, config.SUNSPOT_NUMBER_MAX) / config.SUNSPOT_NUMBER_MAX
        self.frequency = config.SUNSPOT_FREQ_MIN + norm_sunspots * (config.SUNSPOT_FREQ_MAX - config.SUNSPOT_FREQ_MIN)
    def process(self, t: np.ndarray, frames: int, samplerate: int) -> np.ndarray:
        return np.sin(2 * np.pi * self.frequency * t) * 0.6
class Pulsar_Rhythm:
    def __init__(self):
        self.last_tick_time = 0
        click_duration = config.PULSAR_CLICK_DECAY * 5
        t_click = np.arange(int(click_duration * config.SAMPLERATE)) / config.SAMPLERATE
        click_env = np.exp(-t_click / config.PULSAR_CLICK_DECAY)
        self.click_wave = np.sin(2 * np.pi * config.PULSAR_CLICK_FREQ * t_click) * click_env * 0.5
    def update(self, data: Dict[str, Any]): pass
    def process(self, t: np.ndarray, frames: int, samplerate: int) -> np.ndarray:
        output = np.zeros(frames)
        time_to_next_tick = (self.last_tick_time + config.PULSAR_PERIOD_SECONDS) - time.time()
        if time_to_next_tick < (frames / samplerate):
            start_frame = max(0, int(time_to_next_tick * samplerate))
            if start_frame < frames:
                end_frame = start_frame + len(self.click_wave)
                frames_to_write = min(len(self.click_wave), frames - start_frame)
                output[start_frame:end_frame] += self.click_wave[:frames_to_write]
            self.last_tick_time += config.PULSAR_PERIOD_SECONDS
        if time.time() - self.last_tick_time > config.PULSAR_PERIOD_SECONDS * 2:
            self.last_tick_time = time.time()
        return output
class Flare_Accent:
    def __init__(self):
        self.is_playing = False; self.gong_start_time = 0; self.intensity = 0; self.last_flare_id = None
    def update(self, data: Dict[str, Any]):
        flare = data.get('latest_flare')
        if flare and flare.get('flrID') != self.last_flare_id:
            self.last_flare_id = flare['flrID']
            self.is_playing = True; self.gong_start_time = time.time()
            class_type = flare.get('classType', 'C')[0]
            if 'X' in class_type: self.intensity = 1.0
            elif 'M' in class_type: self.intensity = 0.7
            else: self.intensity = 0.4
            logging.info(f"!!! TRIGGERING FLARE GONG (Class: {class_type}) !!!")
    def process(self, t: np.ndarray, frames: int, samplerate: int) -> np.ndarray:
        if not self.is_playing: return np.zeros(frames)
        time_since_start = time.time() - self.gong_start_time
        if time_since_start > config.FLARE_GONG_DURATION_SECONDS:
            self.is_playing = False; return np.zeros(frames)
        t_gong = (t - t[0]) + time_since_start
        env = np.exp(-t_gong / (config.FLARE_GONG_DURATION_SECONDS / 4))
        freq = config.FLARE_GONG_BASE_FREQ
        gong = (np.sin(2 * np.pi * freq * t_gong) +
                0.5 * np.sin(2 * np.pi * freq * 1.51 * t_gong) +
                0.3 * np.sin(2 * np.pi * freq * 2.75 * t_gong))
        return gong * env * self.intensity
class CosmicOrchestra:
    def __init__(self):
        self.instruments = [CME_Melody(), GST_Noise(), Sunspot_Drone(), Pulsar_Rhythm(), Flare_Accent()]
        self.frame_count: int = 0
    def update_all(self, data: Dict[str, Any]):
        logging.info("Updating all instruments with new data...")
        for instrument in self.instruments: instrument.update(data)
    def audio_callback(self, outdata: np.ndarray, frames: int, time_info, status):
        if status: logging.warning(f"Audio stream status: {status}")
        t = (np.arange(frames) + self.frame_count) / config.SAMPLERATE
        final_signal = np.zeros(frames)
        for instrument in self.instruments: final_signal += instrument.process(t, frames, config.SAMPLERATE)
        final_signal *= config.MASTER_AMPLITUDE
        final_signal = np.clip(final_signal, -1.0, 1.0)
        outdata[:] = final_signal.astype(np.float32).reshape(-1, 1)
        self.frame_count += frames

# --- Main Conductor ---
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Initializing The Full Cosmic Orchestra...")
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    if not api_key or "SUA_CHAVE" in api_key:
        logging.critical("CRITICAL: NASA_API_KEY not found or not set. Exiting.")
        return

    orchestra = CosmicOrchestra()

    try:
        logging.info("Starting audio stream...")
        with sd.OutputStream(callback=orchestra.audio_callback, samplerate=config.SAMPLERATE, channels=1, dtype='float32'):
            while True:
                logging.info("Fetching cosmic event data...")
                
                # --- MUDANÇA: Busca os dados de ambas as fontes ---
                nasa_data = fetch_nasa_data(api_key)
                sunspot_data = fetch_sunspot_data()

                # --- MUDANÇA: Junta os dados em um único dicionário ---
                master_data = nasa_data.copy()
                master_data.update(sunspot_data)

                if master_data:
                    orchestra.update_all(master_data)
                
                logging.info(f"Next update in {config.UPDATE_INTERVAL_SECONDS / 60:.0f} minutes.")
                time.sleep(config.UPDATE_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logging.info("Symphony interrupted by user. Shutting down.")
    except Exception as e:
        logging.error(f"A critical error has stopped the orchestra: {e}", exc_info=True)

if __name__ == "__main__":
    main()