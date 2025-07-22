# main.py (Version with two instruments: GST and CME)

import os
import time
import logging
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from typing import Dict, Any

from nasa_client import fetch_live_data

# --- Global Settings ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
SAMPLERATE = 44100
UPDATE_INTERVAL = 300
MASTER_AMPLITUDE = 0.4

class CosmicOrchestra:
    """ Manages the sonic state based on cosmic data. """
    def __init__(self):
        self.frequency: float = 110.0
        self.noise_intensity: float = 0.0
        self.frame_count: int = 0
    
    def update_sonics(self, data: Dict[str, Any]):
        """ Maps CME speed to frequency and Kp index to noise. """
        # --- Instrument 1: CME Speed maps to Frequency ---
        cme_speed = data.get('fastest_cme_speed', 0)
        
        if cme_speed == 0:
            self.frequency = 110.0  # Calm note (A2)
        else:
            # Map speed (300 to 2000 km/s) to frequency (110 to 1200 Hz)
            # This is a direct, faithful mapping.
            norm_speed = (cme_speed - 300) / (2000 - 300)
            norm_speed = np.clip(norm_speed, 0, 1) # Ensure value is between 0 and 1
            self.frequency = 110 + norm_speed * 1090
        
        # --- Instrument 2: Kp Index maps to Noise ---
        max_kp = data.get('max_kp_index', 0)
        self.noise_intensity = (max_kp / 9.0) * 0.3
        
        logging.info(f"Sonics updated: CME Speed {cme_speed} km/s => Frequency={self.frequency:.2f} Hz | KpIndex {max_kp} => Noise={self.noise_intensity:.2f}")

    def audio_callback(self, outdata: np.ndarray, frames: int, time_info, status):
        """ The audio engine callback, generates sound continuously. """
        if status:
            logging.warning(f"Audio stream status: {status}")

        t = (np.arange(frames) + self.frame_count) / SAMPLERATE
        self.frame_count += frames

        main_wave = 0.7 * np.sin(2 * np.pi * self.frequency * t)
        harmonic = 0.3 * np.sin(2 * np.pi * (self.frequency * 2) * t)
        tone = main_wave + harmonic
        noise = np.random.uniform(-1, 1, size=frames) * self.noise_intensity
        final_signal = (tone + noise) * MASTER_AMPLITUDE
        final_signal = np.clip(final_signal, -1.0, 1.0)
        
        outdata[:] = final_signal.astype(np.float32).reshape(-1, 1)

def main():
    """ Initializes and runs the Cosmic Orchestra application. """
    logging.info("Initializing 2-Instrument Cosmic Orchestra...")
    
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    if not api_key or "SUA_CHAVE" in api_key:
        logging.critical("CRITICAL: NASA_API_KEY not found or not set in .env file. Exiting.")
        return

    orchestra = CosmicOrchestra()

    try:
        logging.info("Starting audio stream. The symphony begins...")
        with sd.OutputStream(callback=orchestra.audio_callback, samplerate=SAMPLERATE, channels=1, dtype='float32'):
            while True:
                logging.info("Fetching cosmic data for all instruments...")
                nasa_data = fetch_live_data(api_key)
                
                if nasa_data:
                    orchestra.update_sonics(nasa_data)
                else:
                    logging.warning("No data received, defaulting to calm state.")
                    orchestra.update_sonics({})
                
                logging.info(f"Next update in {UPDATE_INTERVAL / 60:.0f} minutes.")
                time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        logging.info("Symphony interrupted by user. Shutting down.")
    except Exception as e:
        logging.error(f"A critical error has stopped the orchestra: {e}", exc_info=True)

if __name__ == "__main__":
    main()