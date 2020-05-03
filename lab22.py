# Морозов-Леонов О.С., ІО-71, № заліковки: 7117
# #  n w    N
# 17 8 1200 1024
# Додаткове завдання: порівняти час виконання ДФТ та ФФт

import random as r
import math
import matplotlib.pyplot as plt
import datetime

n = 17
w_max = 1200
N = 1024  # N змінюється від 64 до 1024 з кроком 64

w_real = [[math.cos(2 * math.pi * i * j / N) for j in range(N)] for i in range(N)]
w_imag = [[math.sin(2 * math.pi * i * j / N) for j in range(N)] for i in range(N)]


def graph(N):
    x = [0] * N

    for i in range(n):
        A = r.randrange(2)
        W = r.randrange(w_max)
        f = r.randrange(1e9)
        for t in range(N):
            x[t] += A * math.sin(W * t + f)
    return x


def fft(x: list):
    N = len(x)
    fftt = [[0] * 2 for i in range(N)]
    for i in range(N // 2):
        array1 = [0] * 2
        array2 = [0] * 2
        for j in range(N // 2):
            cos = math.cos(4 * math.pi * i * j / N)
            sin = math.sin(4 * math.pi * i * j / N)
            array1[0] += x[2 * j + 1] * cos # real
            array1[1] += x[2 * j + 1] * sin # imag
            array2[0] += x[2 * j] * cos # real
            array2[1] += x[2 * j] * sin # imag
        cos = math.cos(2 * math.pi * i / N)
        sin = math.sin(2 * math.pi * i / N)
        fftt[i][0] = array2[0] + array1[0] * cos - array1[1] * sin # real
        fftt[i][1] = array2[1] + array1[0] * sin + array1[1] * cos # imag
        fftt[i + N // 2][0] = array2[0] - (array1[0] * cos - array1[1] * sin) # real
        fftt[i + N // 2][1] = array2[1] - (array1[0] * sin + array1[1] * cos) # imag
    return fftt


def dft(x: list):
    N = len(x)
    dftt = [[sum(w_real[p][k] * x[k] for k in range(N)), sum(w_imag[p][k] * x[k] for k in range(N))] for p in range(N)]
    return dftt


def timings(N_min, N_max, N_step):
    arg_data = [arg for arg in range(N_min, N_max+1, N_step)]
    X = graph(N)
    dft_times = []
    fft_times = []
    for arg in arg_data:
        time = datetime.datetime.now()
        dft(X[:arg])
        time = datetime.datetime.now() - time
        dft_times.append(time.total_seconds() * 1e6 + time.microseconds)

        time = datetime.datetime.now()
        fft(X[:arg])
        time = datetime.datetime.now() - time
        fft_times.append(time.total_seconds() * 1e6 + time.microseconds)
    return arg_data, dft_times, fft_times


x_data, dft_times, fft_times = timings(64, 1024, 64)
plt.plot(x_data, dft_times)
#plt.legend(["DFT"])
plt.plot(x_data, fft_times)
plt.legend(["DFT", "FFT"])
plt.show()

exit(0)

X = graph()
fftt = fft(X)

data_fft = [math.sqrt(fftt[i][0] ** 2 + fftt[i][1] ** 2) for i in range(N)]

plt.plot([i for i in range(N)], X)
plt.show()
plt.plot([i for i in range(N)], data_fft)
plt.show()