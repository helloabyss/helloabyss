"""Consistent online backup of the app database.

Case data and documents inside the database are already encrypted with DATA_KEY, so a
backup file is safe to store off-site. Keep DATA_KEY somewhere separate from the backups:
without it they can't be read, and with both together they can.

Usage:  python3 scripts/backup.py /data/cfads.db /backups [--keep 30]
Schedule daily (cron) and copy /backups to off-site storage (S3, Backblaze, etc.).
"""

import argparse
import os
import sqlite3
from datetime import datetime

p = argparse.ArgumentParser()
p.add_argument("database")
p.add_argument("out_dir")
p.add_argument("--keep", type=int, default=30)
a = p.parse_args()
os.makedirs(a.out_dir, exist_ok=True)
dest = os.path.join(a.out_dir, f"cfads-{datetime.now():%Y%m%d-%H%M%S}.db")
with sqlite3.connect(a.database) as src, sqlite3.connect(dest) as dst:
    src.backup(dst)
old = sorted(f for f in os.listdir(a.out_dir) if f.startswith("cfads-") and f.endswith(".db"))
for f in old[:-a.keep]:
    os.remove(os.path.join(a.out_dir, f))
print(dest)
