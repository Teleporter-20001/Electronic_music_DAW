from app.backend.Models.Instruments.DecaySine import DecaySine
import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def test_decaysine():
    num = 1000
    freq = 440
    inst = DecaySine()
    time = np.linspace(0, 100, num)
    phase = 2 * np.pi * freq * time
    value = inst.generate(phase, time=time)
    plt.plot(time, value)
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.show()
