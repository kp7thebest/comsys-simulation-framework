import numpy as np
from scipy.signal import hilbert


def txmod(mod_type, m_t, fc, t, kf=1):  # t is now the third argument, fc is fourth
    A=1, 
    if mod_type == "DSB-SC":
        x_t = m_t * np.cos(2 * np.pi * fc * t)
        return x_t
    elif mod_type == "AM":
        # Assuming A here is the DC offset for AM
        x_t = (m_t + A) * np.cos(2 * np.pi * fc * t)
        return x_t
    elif mod_type == "USSB":
        m_h = np.imag(hilbert(m_t))
        x_t = m_t * np.cos(2 * np.pi * fc * t) - m_h * np.sin(2 * np.pi * fc * t)
        return x_t
    elif mod_type == "LSSB":
        m_h = np.imag(hilbert(m_t))
        x_t = m_t * np.cos(2 * np.pi * fc * t) + m_h * np.sin(2 * np.pi * fc * t)
        return x_t
    elif mod_type == "FM":
        # Use the passed A for carrier amplitude, use passed kf for frequency sensitivity
        integral_of_m_t = np.cumsum(m_t) * (t[1] - t[0])
        # The equation for FM uses the carrier amplitude A and frequency deviation constant kf.
        x_t = A * np.cos(2 * np.pi * fc * t + 2 * np.pi * kf * integral_of_m_t)
        return x_t
    elif mod_type == "polar":
        # bits: array of 0/1, t: time vector
        pulse_width = 1  # 1 sample per bit for simplicity
        x_t = np.where(m_t == 1, 1, -1)  # 1 for bit 1, -1 for bit 0
        return x_t
