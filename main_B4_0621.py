#main.py
from plot_time import plot_time
from infosource import infosource
from plot_time import plot_time
from infosource import infosource
from spectrum_signal import spectrum_signal
from filter_sinc import filter_sinc
from convo_out import convo_out
from txmod import txmod
import matplotlib.pyplot as plt
import numpy as np
import random
from rx_demod import rx_demod

plt.ion()


def main():
    # parameters
    fc = 100.0
    amp = 1.0
    f = 10.0

    # Request the real-time song (infosource builds t using WAV sample rate)
    placeholder_fs = 8000
    m_t, t = infosource("real_time_song", f, placeholder_fs, amp, 0)

    # derive actual sampling rate from returned time vector
    if len(t) >= 2:
        fs = 1.0 / (t[1] - t[0])
    else:
        fs = float(placeholder_fs)
    print(f"Using sample rate fs = {fs:.1f} Hz (derived from infosource)")

    # Time-domain original
    plot_time(t, m_t, 'message-td', fig=1)
    # Frequency-domain original (use spectrum_signal which returns freq_axis, M_f)
    freq_axis_orig, M_f_orig = spectrum_signal(m_t, fs, 'message-fd', fig=2)

    # Modulate (FM) and plot
    kf = 1.0
    x_t = txmod("FM", m_t, fc, t, kf)
    plot_time(t, x_t, 'modulated-td', fig=3)
    freq_axis_mod, M_f_mod = spectrum_signal(x_t, fs, 'modulated-fd', fig=4)

    # Demodulate
    # use a lowpass cutoff to smooth numerical differentiation noise (Hz)
    lp_cut = min(4000.0, 0.45 * (0.5 * fs))
    m_hat_t = rx_demod("EDFM", x_t, fc, fs, t, kf=kf, lp_cutoff_hz=lp_cut)

    # Ensure same length for plotting / MSE
    m_orig = np.asarray(m_t)
    m_hat = np.asarray(m_hat_t)
    L = min(len(m_orig), len(m_hat))
    m_orig = m_orig[:L]
    m_hat = m_hat[:L]
    t_plot = t[:L]

    # Plot demodulated
    plot_time(t_plot, m_hat, 'demodulated-td', fig=5)
    freq_axis_demod, M_f_demod = spectrum_signal(m_hat, fs, 'demodulated-fd', fig=6)

    # Quick accuracy check (compare against centered original since txmod zero-centers before FM)
    m_orig_centered = m_orig - np.mean(m_orig)
    mse = np.mean((m_orig_centered - m_hat) ** 2)
    print(f"MSE (orig vs demod): {mse:.6e}")

    # Overlay for visual comparison
    plt.figure(7)
    plt.plot(t_plot, m_orig_centered, label='original (centered)', alpha=0.8)
    plt.plot(t_plot, m_hat, label='demodulated', alpha=0.7)
    plt.title('Original vs Demodulated')
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)



if __name__ == "__main__":
    main()
    plt.show(block=True)
if __name__ == "__main__":
  main()
  plt.show(block=True)
