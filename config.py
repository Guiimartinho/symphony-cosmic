# config.py

# -- Application Settings --
# Defines how often to fetch new data from NASA, in seconds.
UPDATE_INTERVAL_SECONDS: int = 300  # 5 minutes

# -- Audio Settings --
# Standard sample rate for audio processing.
SAMPLERATE: int = 44100
# Default master amplitude (volume) to prevent clipping.
MASTER_AMPLITUDE: float = 0.3

# -- Data Source URLs --
NASA_API_BASE_URL: str = "https://api.nasa.gov/DONKI"
# Correct, official, and stable URL for the daily total sunspot number data file:
SIDC_SUNSPOT_URL: str = "https://www.sidc.be/silso/DATA/SN_d_tot_V2.0.txt"

# -- Sonification Mapping Parameters --

# CME Melody Instrument
CME_SPEED_MIN: float = 300.0
CME_SPEED_MAX: float = 2000.0
CME_MELODY_LENGTH: int = 16
CME_NOTE_DURATION_SECONDS: float = 0.5

# GST Noise Instrument
KP_INDEX_MAX: int = 9
KP_NOISE_MAX_INTENSITY: float = 0.15

# Sunspot Drone Instrument
SUNSPOT_NUMBER_MAX: int = 250 # A high value for a busy solar cycle
SUNSPOT_FREQ_MIN: float = 30.0 # Deep, subsonic bass
SUNSPOT_FREQ_MAX: float = 80.0 # Palpable low bass

# Pulsar Rhythm Instrument
# Period in seconds for the Vela Pulsar (~11.2 pulses per second)
PULSAR_PERIOD_SECONDS: float = 0.08933
PULSAR_CLICK_FREQ: float = 1200.0 # Frequency of the percussive click
PULSAR_CLICK_DECAY: float = 0.05   # How fast the click sound fades

# Solar Flare Accent Instrument
FLARE_GONG_DURATION_SECONDS: float = 8.0
FLARE_Gong_BASE_FREQ: float = 120.0