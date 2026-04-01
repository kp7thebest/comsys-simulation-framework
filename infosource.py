#infosource.py

import numpy as np
import matplotlib.pyplot as plt
import random
import sounddevice as sd
from scipy.io import wavfile
import os

fs_hz = 8000
duration_s = 1.0
amplitude = 0.8


def infosource(signal_type,f,fs,amp,T):

    def _tone(fs_hz, duration_s, freqs, amp):
    #t = np.arange(0, duration_s, 1.0/fs_hz, dtype=np.float64)
        start_time = 0
        stop_time = 1
        t = np.linspace((start_time+T), (stop_time+T), int(fs * (stop_time - start_time)) + 1)
        sig = np.zeros_like(t)
        for f in freqs:
            sig += np.sin(2*np.pi*f*t)
        # Normalize by number of tones to control amplitude
        sig = amp * sig / max(1, len(freqs))
        return t, sig

    

    if signal_type == "sine":
        start_time = 0
        stop_time = 1
        t = np.linspace((start_time+T), (stop_time+T), int(fs * (stop_time - start_time)) + 1)
        m_t = amp * np.sin(2 * np.pi * f * t)
             

    elif signal_type == 'multitone':
        f_1=f
        f_2 = 2 * f_1
        f_max = max(f_1, f_2)
        fs = 10 * f_max
        start_time = 0
        stop_time = 1
        A_1 = 1
        A_2 = 1
        t = np.linspace(start_time+T, stop_time+T, int(fs * (stop_time - start_time)) + 1)

        m_t = A_1 * np.sin(2 * np.pi * f_1 * t) + A_2 * np.sin(2 * np.pi * f_2 * t)
       
    elif signal_type == "sinc":
        
        start_time = -10
        stop_time = 10
        t = np.linspace(start_time+T, stop_time+T, int(fs * (stop_time - start_time)) + 1)
        m_t =  2 * f * np.sinc(2 * f* (t-T))
        

    elif signal_type == "real_time_song":
        wav_path = "waving.wav"
        if not os.path.exists(wav_path):
            raise FileNotFoundError(f"'{wav_path}' not found. CWD={os.getcwd()}")
        sample_rate, data = wavfile.read(wav_path)
        # Normalize integer PCM to float32 in [-1, 1]
        if np.issubdtype(data.dtype, np.integer):
            data = data.astype(np.float32) / np.iinfo(data.dtype).max
        else:
            data = data.astype(np.float32)
        # Convert stereo to mono by averaging channels
        if m_T.ndim > 1:
            m_T = m_T[:, 0]
            
    elif signal_type =="dialtone":
        
        t, m_t = _tone(fs_hz, duration_s, [350.0, 440.0], amplitude)

    elif signal_type == "charname":
        name = "Karthik Periasamy"
        bits = []
        for c in name:
            ascii_val = ord(c)
            # Convert to 8-bit binary and extend to bits list
            bits.extend([int(b) for b in format(ascii_val, '08b')])
        bits = np.array(bits)
        t = np.arange(len(bits))
        m_t = bits  # For compatibility, but main output is bits
        return bits, t

       
    else:
        raise ValueError("Unsupported signal type: choose 'sine' or 'sinc'.")

    return m_t, t


# infosource.py
# Generates time-domain sources. Every generator returns (t, m_t).
"""
import numpy as np

def _tone(fs_hz, duration_s, freqs, amp):
    t = np.arange(0, duration_s, 1.0/fs_hz, dtype=np.float64)
    sig = np.zeros_like(t)
    for f in freqs:
        sig += np.sin(2*np.pi*f*t)
    # Normalize by number of tones to control amplitude
    sig = amp * sig / max(1, len(freqs))
    return t, sig

def _cadenced_pair(fs_hz, total_s, on_s, off_s, freqs, amp):
    
    t = np.arange(0, total_s, 1.0/fs_hz, dtype=np.float64)
    period = on_s + off_s
    # Indicator: 1 during ON, 0 during OFF
    phase = (t % period) < on_s
    base = np.zeros_like(t)
    for f in freqs:
        base += np.sin(2*np.pi*f*t)
    base /= max(1, len(freqs))
    return t, amp * base * phase.astype(float)

def infosource(signal_type="sine",
               fs_hz=8000,
               duration_s=1.0,
               amplitude=0.8,
               **kwargs):
    
    Returns:
        t (np.ndarray): time vector [s]
        m_t (np.ndarray): source signal
    Supported signal_type:
      "sine" (freq)
      "sinc" (bandwidth B)
      "multitone" (freqs=[...])
      "square" (freq)
      "noise"
      "dialtone"  (350+440 Hz continuous)
      "busytone"  (480+620 Hz, 0.5s ON / 0.5s OFF)
      "ringtone"  (440+480 Hz, 2s ON / 4s OFF)
    
    t = np.arange(0, duration_s, 1.0/fs_hz, dtype=np.float64)

    if signal_type == "sine":
        f0 = float(kwargs.get("freq", 440.0))
        m_t = amplitude * np.sin(2*np.pi*f0*t)

    elif signal_type == "sinc":
        # Bandlimited pulse: g(t) = 2B sinc(2B t)
        B = float(kwargs.get("B", 800.0))
        m_t = amplitude * (2*B) * np.sinc(2*B*t)

    elif signal_type == "multitone":
        freqs = kwargs.get("freqs", [350.0, 440.0])
        t, m_t = _tone(fs_hz, duration_s, freqs, amplitude)

    elif signal_type == "square":
        f0 = float(kwargs.get("freq", 5.0))
        duty = float(kwargs.get("duty", 0.5))
        m_t = amplitude * ( ( (t*f0) % 1.0 ) < duty ).astype(float)*2 - amplitude

    elif signal_type == "noise":
        rng = np.random.default_rng(kwargs.get("seed", None))
        m_t = amplitude * rng.standard_normal(t.shape)

    # Telephone tones (ITU-like)
    elif signal_type == "dialtone":
        # Continuous: 350 + 440 Hz
        t, m_t = _tone(fs_hz, duration_s, [350.0, 440.0], amplitude)

    elif signal_type == "busytone":
        # 480 + 620 Hz; 0.5 s ON / 0.5 s OFF cadence
        t, m_t = _cadenced_pair(fs_hz, duration_s, 0.5, 0.5, [480.0, 620.0], amplitude)

    elif signal_type == "ringtone":
        # 440 + 480 Hz; 2 s ON / 4 s OFF cadence
        t, m_t = _cadenced_pair(fs_hz, duration_s, 2.0, 4.0, [440.0, 480.0], amplitude)

    else:
        raise ValueError(f"Unsupported signal_type: {signal_type}")

    return t, m_t.astype(np.float64)
"""