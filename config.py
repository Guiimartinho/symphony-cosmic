# config.py

# -- Application Settings --
# Defines how often to fetch new data from NASA, in seconds.
UPDATE_INTERVAL_SECONDS: int = 300  # 5 minutes

# -- Audio Settings --
# Standard sample rate for audio processing.
SAMPLERATE: int = 44100
# Default master amplitude (volume) to prevent clipping.
MASTER_AMPLITUDE: float = 0.4

# -- NASA API Settings --
# Base URL for the DONKI (Database Of Notifications, Knowledge, Information) API.
NASA_API_BASE_URL: str = "https://api.nasa.gov/DONKI"

# -- Sonification Mapping Parameters --

# Solar Wind Speed to Frequency Mapping
# Realistic range of solar wind speed in km/s.
SOLAR_WIND_SPEED_MIN: float = 300.0
SOLAR_WIND_SPEED_MAX: float = 1000.0
# Audible frequency range in Hz to map the wind speed to.
SOLAR_WIND_FREQ_MIN: float = 60.0  # Deep bass
SOLAR_WIND_FREQ_MAX: float = 1200.0 # High mid-range
# Power for non-linear mapping. >1 gives more sensitivity to high speeds.
SOLAR_WIND_FREQ_POWER: float = 1.5

# Geomagnetic Storm (KpIndex) to Noise Intensity Mapping
# KpIndex is an integer from 0 to 9.
KP_INDEX_MAX: int = 9
# Noise intensity will be mapped from 0.0 to this max value.
KP_NOISE_MAX_INTENSITY: float = 0.35