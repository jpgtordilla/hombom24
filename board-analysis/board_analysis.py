import matplotlib.pyplot as plt
import numpy as np


class BoardAnalysis:
    def __init__(self):
        pass

    def txt_to_ndarray(self, path):
        """Converts a text file to a two-dimensional numpy array"""
        return np.loadtxt(path, dtype=int)  # get HOM data text file, converts to a 2D np.ndarray

    def plot_magnitude_phase_both_cav(self, path):
        """Plots the magnitude and phase plots for Cavity 1 and 2."""
        pulse_data = self.txt_to_ndarray(path)
        fft_size = 1024  # size of the Fast Fourier Transform
        start = 408  # starting index in pulse_data
        stop = start + fft_size  # end index in pulse_data

        # CAVITY 1
        cap = 20  # index of the Cavity 1 data in pulse_data
        cplx0 = pulse_data[cap] + pulse_data[cap + 100] * 1j  # create an array of complex numbers
        cplx_m0 = abs(cplx0)  # array of magnitude
        cplx_p0 = np.angle(cplx0, deg=True)  # array of phase

        # CAVITY 2
        # cap + 300 is the index of Cavity 2 data
        cplx1 = pulse_data[cap + 300] + pulse_data[cap + 200] * 1j
        cplx_m1 = abs(cplx1)
        cplx_p1 = np.angle(cplx1, deg=True)

        size = 2 ** 12  # size of time domain signal
        time_bin = 1.0E+6 / 245.76E+6  # Units of us, time interval for each sample (245.76 MHz)
        time_steps = np.linspace(0, time_bin * (size - 1),
                                 num=size)  # array of time values from 0 to the total time duration
        fig, axs = plt.subplots(2)
        plt.rcParams['figure.dpi'] = 500  # 500 dots per inch resolution
        lw = 0.8  # set line width
        axs[0].plot(time_steps[start:stop], cplx_m0[start:stop], linewidth=lw)  # plot magnitude of signal
        axs[0].plot(time_steps[start:stop], cplx_m1[start:stop], linewidth=lw)
        axs[1].plot(time_steps[start:stop], cplx_p0[start:stop], linewidth=lw)
        axs[1].plot(time_steps[start:stop], cplx_p1[start:stop], linewidth=lw)
        axs[0].legend(['Cavity 1', 'Cavity 2'], loc='upper right', prop={'size': 8})
        axs[1].legend(['Cavity 1', 'Cavity 2'], loc='upper right', prop={'size': 8})
        axs[1].set_xlabel("Time (us)")
        axs[0].set_ylabel("Magnitude")
        axs[1].set_ylabel("Phase(Deg)")
        axs[0].grid()
        axs[1].grid()
        plt.show()
        return

    def plot_fft_psd(self, path):
        pulse_data = self.txt_to_ndarray(path)
        fft_size = 1024  # size of the Fast Fourier Transform
        start = 408  # starting index in pulse_data
        stop = start + fft_size  # end index in pulse_data

        # CAVITY 1
        cap = 20  # index of the Cavity 1 data in pulse_data
        cplx0 = pulse_data[cap] + pulse_data[cap + 100] * 1j  # create an array of complex numbers

        # CAVITY 2
        # cap + 300 is the index of Cavity 2 data
        cplx1 = pulse_data[cap + 300] + pulse_data[cap + 200] * 1j

        # FFT and windowing
        Fs = 245.76 * 1e6  # sampling frequency: 245.76 MHz
        iq0 = cplx0[start:stop]  # slice of the complex numbers, to be plotted
        iq1 = cplx1[start:stop]
        freq = np.fft.fftfreq(n=iq1.size, d=1 / Fs)  # compute array of discrete frequencies
        n = len(iq0)  # equal to "fft_size" and the length of the complex numbers array
        f = Fs * np.arange(n) / n - Fs / 2  # frequency array centered at 0
        window = np.blackman(fft_size)  # create a Blackman window (reduce spectral leakage)

        # CAVITY 1
        Y = np.fft.fft(iq0 * window)  # compute the Fast Fourier transform of Cavity 1 signal
        Y_abs = np.abs(Y)  # compute array of magnitudes of the FFT result
        p = np.int_(np.size(Y_abs))  # get the length of the magnitude array
        Y_rd = np.concatenate((Y_abs[np.int_(p / 2):p], Y_abs[0:np.int_(p / 2)]), axis=None)  # FFT shift
        P2log0 = 20 * np.log10(Y_rd / np.max(Y_abs))  # computer the log-scaled power spectrum

        # CAVITY 2
        Y = np.fft.fft(iq1 * window)  # compute the Fast Fourier transform of Cavity 2 signal
        Y_abs = np.abs(Y)
        p = np.int_(np.size(Y_abs))
        Y_rd = np.concatenate((Y_abs[np.int_(p / 2):p], Y_abs[0:np.int_(p / 2)]), axis=None)
        P2log1 = 20 * np.log10(Y_rd / np.max(Y_abs))

        axs = plt.subplots(1)
        plt.rcParams['figure.dpi'] = 500
        plt.plot(f / 1e6, P2log0, '.-')
        plt.plot(f / 1e6, P2log1, '.-')
        plt.legend(['Cavity 1', 'Cavity 2'], loc='lower right')
        plt.grid()
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Power (dB)")
        plt.show()