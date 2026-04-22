import time
from datetime import datetime

import pandas as pd
import psutil


def safe_cmdline(pinfo):
    cmd = pinfo.get("cmdline")
    if isinstance(cmd, list):
        return " ".join(cmd)
    if isinstance(cmd, str):
        return cmd
    return ""


def monitor_process(
    process_name="ollama",
    interval=5,
    stop_event=None,
):
    records = []

    print(f"Monitoring processes matching: '{process_name}'", flush=True)

    # CPU warm-up
    for p in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        if process_name in safe_cmdline(p.info):
            try:
                p.cpu_percent(None)
            except psutil.NoSuchProcess:
                pass

    while not stop_event.is_set():
        procs = [
            p for p in psutil.process_iter(attrs=["pid", "name", "cmdline"])
            if process_name in safe_cmdline(p.info)
        ]

        total_rss = total_cpu = 0
        pids = []

        for p in procs:
            try:
                mem = p.memory_info()
                total_rss += mem.rss
                total_cpu += p.cpu_percent(None)
                pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass

        records.append({
            "timestamp": datetime.now(),
            "pids": ",".join(map(str, pids)),
            "n_procs": len(pids),
            "rss_mb": total_rss / 1024 ** 2,
            "cpu_percent": total_cpu,
        })

        print(
            f"[{records[-1]['timestamp']:%H:%M:%S}] "
            f"procs={len(pids)} "
            f"RSS={records[-1]['rss_mb']:.1f} MB "
            f"CPU={records[-1]['cpu_percent']:.1f}%",
            flush=True,
        )

        time.sleep(interval)

    return pd.DataFrame(records)
