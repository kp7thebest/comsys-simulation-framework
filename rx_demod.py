#rx_demod
import numpy as np  
from scipy.signal import hilbert
from filter_sinc import filter_sinc
from convo_out import convo_out
from scipy.signal import convolve

def rx_demod(demod_type, x_t, fc, fs, t):
    
    if demod_type == "SD":  
        amplitude = 1
        c_t = amplitude * np.cos(2 * np.pi * fc * t)
        y_t = x_t * c_t
        B = 5000
        g_t = filter_sinc(B, fs)
        m_hat_t = convolve(y_t, g_t, mode='same')
    
    elif demod_type == "ED":  
        m_hat_t = np.abs(hilbert(x_t)) - 1 
    
    elif demod_type == 'EDFM':
        analytic_signal = hilbert(x_t)
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        dt = t[1] - t[0]
        m_hat_t = np.diff(instantaneous_phase) / (2 * np.pi * dt)
        m_hat_t = np.concatenate(([m_hat_t[0]], m_hat_t))
        m_hat_t = m_hat_t - np.mean(m_hat_t)
        m_hat_t = m_hat_t / np.max(np.abs(m_hat_t))     

    return m_hat_t
