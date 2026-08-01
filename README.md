Arch, ya — venv aja Bos, paling aman biar sistem Python-nya gak keutak-atik:

```bash
cd ~/fbi-secret/minimax
python -m venv venv
source venv/bin/activate
pip install ollama python-dotenv
```

Habis itu tiap mau jalanin scriptnya, `source venv/bin/activate` dulu, baru:

```bash
python vibe_agent.py
```

Kalau males `activate` tiap kali, bisa langsung panggil binary di dalam venv-nya tanpa activate:

```bash
./venv/bin/python vibe_agent.py
```

Alternatif kalau emang cuma mau pakai sekali-sekali dan gak mau ribet venv, bisa juga:

```bash
pip install --break-system-packages ollama python-dotenv
```

Tapi ini nembus proteksi PEP 668 yang emang sengaja dipasang biar package pip gak bentrok sama package `pacman`-nya Arch — kalau nanti ada breakage di system Python, jangan kaget, Bos. Venv tetep pilihan yang lebih waras buat kasus kayak gini.
