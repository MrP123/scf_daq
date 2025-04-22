import numpy as np
import matplotlib.pyplot as plt
from sdypy_sep005.sep005 import assert_sep005
import pywt

from data_converter import measurement_dict_to_sep005

class PlottingWrapper():
    """
    Wraps around the recorded data from LDAQ and provides some convenient plotting utilities as methods
    """

    def __init__(self, full_data: dict):
        try:
            # data is already SEP005 compliant -> do nothing
            assert_sep005(full_data)
        except:
            # otherwise convert to SEP005 representation
            full_data = measurement_dict_to_sep005(full_data)
        finally:
            self.full_data = full_data

    def plot_raw_data(self) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots()
        time = self.full_data["time"]
        data = self.full_data["data"]

        ax.plot(time, data)
        ax.legend(self.full_data["channel_name"], loc="upper right")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")

        return fig, ax
        
    def plot_channel(self, channel: int = 0) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots()
        time = self.full_data["time"]
        data = self.full_data["data"]

        ax.plot(time, data[:, channel])
        ax.legend([self.full_data["channel_name"][channel]], loc="upper right") #wrap in additional list so that str is not unrolled
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")

        return fig, ax
    
    def plot_between_times(self, start_time: float, end_time: float) -> tuple[plt.Figure, plt.Axes]:
        times = np.array([start_time, end_time])
        indices = (times * self.full_data["fs"]).astype(int)
        start, end = indices[0], indices[1]

        time = self.full_data["time"]
        data = self.full_data["data"]

        fig, ax = plt.subplots()
        ax.plot(time[start:end], data[start:end, :])
        ax.legend(self.full_data["channel_name"], loc="upper right")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")
        
        return fig, ax
    
    def plot_wavelet_decomp(self, start_time: float, end_time: float, channel: int = 0) -> tuple[plt.Figure, list[plt.Axes]]:
        times = np.array([start_time, end_time])
        indices = (times * self.full_data["fs"]).astype(int)
        start, end = indices[0], indices[1]

        time = self.full_data["time"]
        data = self.full_data["data"]

        ch_data = data[:, channel]
        coeffs = pywt.wavedec(ch_data, 'db2', level=5)
        #cA5, cD5, cD4, cD3, cD2, cD1 = coeffs

        fig, axs = plt.subplots(6, 1)
        axs: list[plt.Axes]

        for i, c in enumerate(coeffs):
            start_t_wavelet = int(start / len(time) * len(c))
            end_t_wavelet = int(end / len(time) * len(c))

            loc_time = np.linspace(time[0], time[-1], c.shape[0])
            axs[i].plot(loc_time[start_t_wavelet:end_t_wavelet], c[start_t_wavelet:end_t_wavelet])

        axs[-1].set_xlabel("Time (s)")
        axs[len(axs)//2].set_ylabel("Voltage (V)")

        return fig, axs