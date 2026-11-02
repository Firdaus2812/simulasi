# Simulasi respons transien kontrol P dan PI pada model motor DC (dual axis solar tracker)
# Model (sub-bab 2.2.10, persamaan 2.4): G(s) = K / [s(s + a)]
# Nilai K dan a di bawah adalah NILAI ILUSTRASI (parameter motor belum diidentifikasi).
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

K, a = 30.0, 5.0            # K = Kt/(Ra*J), a = (Ra*b + Kt*Ke)/(Ra*J)
Kp, Ki = 2.0, 5.0           # parameter pengendali (contoh)
t = np.linspace(0, 6, 3000)

def lingkar_tertutup(num_c, den_c):
    """T(s) = C*G / (1 + C*G)  (persamaan 3.1) dengan C = num_c/den_c."""
    num_L = np.polymul(num_c, [K])
    den_L = np.polymul(den_c, [1, a, 0])
    den_T = np.polyadd(den_L, np.pad(num_L, (len(den_L)-len(num_L), 0)))
    return signal.TransferFunction(num_L, den_T)

def metrik(y):
    """Parameter respons transien (persamaan 2.8 - 2.11), nilai akhir = 1."""
    tr = t[np.argmax(y >= 0.9)] - t[np.argmax(y >= 0.1)]
    kp = np.argmax(y); tp = t[kp]; Mp = max(0.0, (y[kp]-1)*100)
    luar = np.where(np.abs(y-1) > 0.02)[0]
    ts = t[luar[-1]+1] if len(luar) else 0.0
    return tr, tp, Mp, ts

sistem = {"Kontrol P":  lingkar_tertutup([Kp], [1]),
          "Kontrol PI": lingkar_tertutup([Kp, Ki], [1, 0])}

# Pemeriksaan analitis untuk kontrol P (persamaan 3.2)
wn = np.sqrt(K*Kp); zeta = a/(2*np.sqrt(K*Kp))
print(f"Kontrol P: wn = {wn:.3f} rad/s, zeta = {zeta:.3f} -> underdamped")
print(f"           Mp teori = {100*np.exp(-np.pi*zeta/np.sqrt(1-zeta**2)):.1f} %\n")

fig, ax = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for axis, (nama, sys) in zip(ax, sistem.items()):
    _, y = signal.step(sys, T=t)
    tr, tp, Mp, ts = metrik(y)
    print(f"{nama}: tr={tr:.2f} s, tp={tp:.2f} s, Mp={Mp:.1f} %, ts(2%)={ts:.2f} s, y(akhir)={y[-1]:.3f}")
    axis.plot(t, y, lw=2); axis.axhline(1, color="k", ls="--", lw=.8)
    axis.set_title(f"Output {nama}"); axis.set_xlabel("Waktu (s)"); axis.grid(alpha=.3)
ax[0].set_ylabel("Posisi (ternormalisasi)")
plt.tight_layout(); plt.savefig("Output_P_dan_PI.png", dpi=200)
