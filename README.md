# Simulasi Kontrol P dan PI pada Model Motor DC

Simulasi pendukung sub-bab 3.1.1 skripsi *PID control on ESP32-based Dual Axis Solar Tracker*.

- `Simulasi.slx` : model Simulink (MATLAB R20xx, ganti dengan versimu)
- `simulasi_pid_tracker.py` : simulasi yang sama dalam Python

Model motor: G(s) = 30 / (s² + 5s). Parameter ilustrasi: K = 30, a = 5, Kp = 2, Ki = 5.
Nilai ini bukan hasil identifikasi motor sebenarnya.

Hasil: kontrol P overshoot 34,3 %, kontrol PI overshoot 72,2 %.
