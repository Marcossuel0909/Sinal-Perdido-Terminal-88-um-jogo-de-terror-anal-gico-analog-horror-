# audio.py
import pygame
import numpy as np

# Inicializa o mixer do Pygame para áudio
pygame.mixer.init(frequency=44100, size=-16, channels=1)

def gerar_onda_senoidal(freq, duracao, volume=0.2):
    """Gera um tom puro de áudio (bip/sinal)."""
    amostras = int(44100 * duracao)
    t = np.linspace(0, duracao, amostras, False)
    onda = np.sin(2 * np.pi * freq * t) * 32767 * volume
    audio = onda.astype(np.int16)
    return pygame.mixer.Sound(audio.tobytes())

def gerar_ruido_branco(duracao, volume=0.1):
    """Gera áudio de estática de rádio."""
    amostras = int(44100 * duracao)
    ruido = np.random.uniform(-1, 1, amostras) * 32767 * volume
    audio = ruido.astype(np.int16)
    return pygame.mixer.Sound(audio.tobytes())

# --- EFEITOS PRONTOS PARA USO ---

def tocar_clique_tecla():
    """Som curto de clique ao digitar."""
    som = gerar_onda_senoidal(800, 0.015, volume=0.1)
    som.play()

def tocar_estatica_radio():
    """Som de ruído/estática de rádio ao sintonizar."""
    som = gerar_ruido_branco(0.3, volume=0.15)
    som.play()

def tocar_bip_morse():
    """Som de bip em Morse ao capturar sinal ou descriptografar."""
    som = gerar_onda_senoidal(1000, 0.1, volume=0.2)
    som.play()