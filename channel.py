#channel.py
import numpy as np

def channel(t, channel_type, Bandwidth, a, td=0):

    if channel_type == "distortionless":
        h = np.zeros_like(t)
        idx = np.argmin(np.abs(t - td))
        h[idx] = 1  
        h = a * h   
        return h

    elif channel_type == "bandlimited":
        h = (2 * a *Bandwidth) * np.sinc(2 * Bandwidth * t)
        return h    
    
