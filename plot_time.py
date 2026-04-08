#plot_time
import matplotlib.pyplot as plt


def plot_time(t, m_t,title="Add Title", fig=1):
    plt.figure(fig)
    plt.plot(t, m_t)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Signal Amplitude")
    plt.grid(True)