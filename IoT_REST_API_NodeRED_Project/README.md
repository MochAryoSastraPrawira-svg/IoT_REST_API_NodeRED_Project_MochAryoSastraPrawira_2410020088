# Praktikum REST API Node-RED untuk Sistem IoT

Sistem monitoring dan kontrol IoT berbasis **MQTT (Mosquitto)**, **Node-RED Backend**, **SQLite**, **WebSocket**, dan **Custom Web Dashboard (Chart.js)**.

## Fitur Utama & Pengembangan
1. **Endpoint `PUT /api/threshold`**: Mengatur batas suhu (*threshold*) dan memicu peringatan otomatis via MQTT (`iot/alert`) serta notifikasi visual di dashboard ketika suhu melewati batas.
2. **Grafik Real-Time (Chart.js)**: Visualisasi tren suhu (°C) dan kelembaban (%) secara langsung.
3. **Autentikasi API Key (`X-API-Key`)**: Validasi header `X-API-Key: RAHASIABANGAT123` pada seluruh endpoint REST API (`/api/*`).
4. **Komunikasi Real-Time WebSocket (`/ws/iot`)**: Push update data sensor dari Node-RED ke browser secara instan tanpa *polling* HTTP.
5. **Penyimpanan Riwayat ke SQLite (`iot_monitoring.db`)**: Menyimpan data sensor secara persisten ke database SQLite dan menampilkan 50 riwayat terakhir melalui `GET /api/history`.

## Struktur File
- `simulasi_esp32.py` — Simulator perangkat ESP32 (MQTT Publisher data sensor & Subscriber kontrol/alert).
- `flows_iot_nodered.json` — Konfigurasi flow Node-RED siap import.
- `dashboard.html` — Antarmuka web monitoring & kontrol real-time.
- `requirements.txt` — Daftar dependensi Python.
- `.gitignore` — Mengecualikan file database lokal (`*.db`) dan cache Python saat push ke GitHub.

## Cara Menjalankan
1. **Install Dependensi:**
   - Python: `pip install -r requirements.txt`
   - Node-RED: `npm install node-red-node-sqlite` (di folder `~/.node-red` atau via *Manage Palette*).
2. **Jalankan MQTT Broker (Terminal 1):**
   ```bash
   mosquitto -v
   ```
3. **Jalankan Node-RED (Terminal 2):**
   ```bash
   node-red
   ```
   Buka `http://localhost:1880`, klik **Menu $ightarrow$ Import**, pilih file `flows_iot_nodered.json`, lalu klik **Deploy**.
4. **Jalankan Simulator ESP32 (Terminal 3):**
   ```bash
   python simulasi_esp32.py
   ```
5. **Buka Dashboard:**
   Buka file `dashboard.html` di browser modern.

## Pengujian Endpoint (`curl`)
```bash
# GET Suhu Terakhir
curl -H "X-API-Key: RAHASIABANGAT123" http://localhost:1880/api/suhu

# GET History dari SQLite
curl -H "X-API-Key: RAHASIABANGAT123" http://localhost:1880/api/history

# PUT Update Threshold Suhu
curl -X PUT http://localhost:1880/api/threshold \
  -H "Content-Type: application/json" \
  -H "X-API-Key: RAHASIABANGAT123" \
  -d '{"threshold": 28.5}'

# POST Kontrol Perangkat
curl -X POST http://localhost:1880/api/kontrol \
  -H "Content-Type: application/json" \
  -H "X-API-Key: RAHASIABANGAT123" \
  -d '{"device":"lamp","action":"on"}'
```
