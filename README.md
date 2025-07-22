# Cosmic Symphony

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

*A real-time generative music application that transforms live space weather data into an ever-changing auditory experience.*

## The Vision

The "Cosmic Symphony" is not just a program, but a digital orchestra where the musicians are celestial phenomena. The core idea is to create a direct, faithful translation of the raw forces of our solar system into sound. Instead of pre-composed music, the symphony is generated in real-time, conducted by the sun's activity and its effect on Earth.

Every data stream—be it the speed of a solar flare, the intensity of a geomagnetic storm, or the impact of a cosmic ray—becomes a unique instrument or a voice in the choir. The result is a soundscape that is constantly evolving, reflecting the quiet, minimalist periods of solar calm as well as the chaotic, dense crescendos of a major solar storm. It's a way to listen to the cosmos.

## Current State & Features

This project has successfully moved from concept to a functional, modular application. The current implementation features:

* **A Two-Instrument Orchestra:** The symphony is currently performed by two main instruments, driven by separate data feeds:
    1.  **Coronal Mass Ejections (CME):** The speed of the fastest recently detected CME directly controls the fundamental **frequency (pitch)** of the main harmonic tone. Faster CMEs result in higher, more intense notes.
    2.  **Geomagnetic Storms (GST):** The maximum observed Kp-index (a measure of storm intensity) controls the amount of **atmospheric noise** mixed into the sound, representing the disturbance in Earth's magnetosphere.

* **Real-time Data Fetching:** The application connects directly to NASA's DONKI (Database Of Notifications, Knowledge, Information) API to source its data.

* **Continuous Audio Stream:** Using the `sounddevice` library, the application generates a continuous, non-repeating stream of audio that changes as new data is fetched.

* **Professional & Modular Architecture:** The code is structured professionally with concerns separated into different modules:
    * `config.py`: For all application settings and parameters.
    * `nasa_client.py`: A dedicated module for all communication with the NASA API.
    * `main.py`: The main conductor, using classes to manage the orchestra and its state without global variables.
    * **Dependency Management:** Uses a `requirements.txt` file for easy setup.
    * **Secure API Key Handling:** Uses a `.env` file to keep credentials safe and out of the source code.

## How to Set Up and Run

### 1. Prerequisites
* Python 3.10 or 3.11
* A NASA API Key

### 2. Installation

```bash
# Clone the repository (example)
# git clone [https://github.com/Guiimartinho/symphony-cosmic.git](https://github.com/Guiimartinho/symphony-cosmic.git)
# cd cosmic-symphony

# Create and activate a Python virtual environment
# On Windows (PowerShell):
# python -m venv .venv
# .\.venv\Scripts\activate
#
# On macOS/Linux:
# python -m venv .venv
# source .venv/bin/activate

# Create a requirements.txt file (if you haven't already)
pip freeze > requirements.txt

# Install all dependencies
pip install -r requirements.txt
```
### 3. Configuration
Create a file named `.env` in the root of the project directory. Add your NASA API key to it like this:
```bash
NASA_API_KEY=YourActualApiKeyGoesHere
```

### 4. Running the Symphony
Simply run the main script from your terminal:
```bash
python main.py
```

The application will start, fetch the initial data, and begin playing the sound. It will automatically fetch new data every 5 minutes (as defined in config.py) and update the sound accordingly. Press Ctrl+C to stop the symphony gracefully.


## Project Roadmap (Future Instruments)

The current two-instrument orchestra is just the beginning. The modular architecture makes it easy to add new musicians:

* **Pulsar Rhythm Section:** Use the ATNF Pulsar Catalogue to add a steady, precise rhythmic background based on pulsar rotation periods.
* **Cosmic Ray Percussion:** Use data from observatories like Pierre Auger to trigger sharp, percussive sounds for high-energy cosmic ray events.
* **Solar Flare Cymbals:** Map the intensity (C, M, X class) of solar flares to bright, cymbal-like crashes.
* **Sunspot Bass Drone:** Use the daily sunspot number to control a very low-frequency drone that slowly evolves over days.

## Acknowledgments

This project is made possible by the publicly available data from [NASA's Space Weather Database Of Notifications, Knowledge, Information (DONKI)](https://ccmc.gsfc.nasa.gov/donki/).