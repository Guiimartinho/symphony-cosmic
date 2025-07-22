# test_sound.py
import sounddevice as sd
import numpy as np

print("--- Testando a saída de áudio com a biblioteca 'sounddevice' ---")

try:
    # Parâmetros do som
    samplerate = 44100  # Taxa de amostragem padrão (CD)
    frequency = 440.0   # Frequência da nota Lá (A4)
    duration = 2.0      # Duração em segundos

    # Gera a onda senoidal
    t = np.linspace(0., duration, int(samplerate * duration), endpoint=False)
    amplitude = 0.5
    waveform = amplitude * np.sin(2. * np.pi * frequency * t)

    # Toca o som no dispositivo de saída padrão
    print("Tocando um tom de 440 Hz por 2 segundos... Você deve ouvir um som agora.")
    sd.play(waveform, samplerate)
    
    # Espera o som terminar
    sd.wait()

    print("Teste concluído com sucesso!")

except Exception as e:
    print(f"\nOcorreu um erro durante o teste de áudio: {e}")
    print("Isso pode indicar um problema mais profundo com os drivers de áudio do seu sistema.")