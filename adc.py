#adc.py
import numpy as np

def adc(adc_type,m_t,fs,N,t):
    
    if adc_type == "PCM":

        samples = m_t
        levels = 2 ** N
        m_min, m_max = samples.min(), samples.max()

        
        m_min = float(m_min)
        m_max = float(m_max)

        q_step = (m_max - m_min) / (levels - 1)
        quantized_indices = np.round((samples - m_min) / q_step).astype(int)
        quantized_indices = np.clip(quantized_indices, 0, levels - 1)

        b = ''.join([format(qi, f'0{N}b') for qi in quantized_indices])

    if adc_type == "DM":

        raise NotImplementedError("Delta Modulation ADC not implemented yet.")
    
    return b