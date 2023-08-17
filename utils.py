import os, sys
import matplotlib.pyplot as plt
import numpy as np

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def plot_leads(signals, fs, leads=range(12), labels=[''], peaks=None, figsize=(8,4)):
    t = np.linspace(0, signals[0].shape[0]/fs-1, signals[0].shape[0])
    fig, axes = plt.subplots(len(leads), 1, figsize=figsize)
    for ind, l in enumerate(leads):
        for s, signal_ in enumerate(signals):
            axes[ind].plot(t, signal_[:, l], label=labels[s])
        if peaks is not None:
            for key, value in peaks.items():
                peaks_i = value[:, l]
                axes[ind].plot(t[peaks_i], signal_[peaks_i, l], 'o', label=key)
    fig.supylabel('ECG (mV)')
    fig.supxlabel('Time (seconds)')
                      
    plt.legend(loc='upper right')
    plt.show()