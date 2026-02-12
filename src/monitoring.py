import time
from datetime import datetime

import matplotlib.pyplot as plt
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
    process_name="Inferencer",
    interval=1,
    duration=None,
):
    records = []
    start_time = time.time()

    print(f"Monitoring processes matching: '{process_name}'", flush=True)
    print("Press Ctrl+C to stop...\n", flush=True)

    try:
        # Initial CPU warm-up
        for p in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
            if process_name in safe_cmdline(p.info):
                try:
                    p.cpu_percent(None)
                except psutil.NoSuchProcess:
                    pass

        while True:
            procs = [
                p for p in psutil.process_iter(attrs=["pid", "name", "cmdline"])
                if process_name in safe_cmdline(p.info)
            ]

            if not procs:
                time.sleep(interval)
                continue

            total_rss = 0
            total_vms = 0
            total_cpu = 0
            total_mem_percent = 0
            pids = []

            for p in procs:
                try:
                    mem = p.memory_info()
                    total_rss += mem.rss
                    total_vms += mem.vms
                    total_cpu += p.cpu_percent(None)
                    total_mem_percent += p.memory_percent()
                    pids.append(p.pid)
                except psutil.NoSuchProcess:
                    pass

            records.append({
                "timestamp": datetime.now(),
                "pids": ",".join(map(str, pids)),
                "n_procs": len(pids),
                "rss_mb": total_rss / 1024 ** 2,
                "vms_mb": total_vms / 1024 ** 2,
                "cpu_percent": total_cpu,
                "mem_percent": total_mem_percent,
            })

            print(
                f"[{records[-1]['timestamp']:%H:%M:%S}] "
                f"procs={len(pids)} "
                f"RSS={records[-1]['rss_mb']:.1f} MB "
                f"CPU={records[-1]['cpu_percent']:.1f}%",
                flush=True,
            )

            slept = 0
            while slept < interval:
                time.sleep(0.1)
                slept += 0.1

            if duration and (time.time() - start_time) > duration:
                break

    except KeyboardInterrupt:
        print("\nStopped by user (Ctrl+C)", flush=True)

    return pd.DataFrame(records)


def main():
    df = monitor_process(
        process_name="ollama",
        interval=1,
    )

    if df.empty:
        print("No data collected.")
        return

    df.set_index("timestamp", inplace=True)

    output_file = "monitoring.csv"
    df.to_csv(output_file)
    print(f"Saved data to {output_file}")

    ax = df["rss_mb"].plot(
        title="Monitoring Total Resident Memory (RSS) Over Time",
        figsize=(10, 5),
    )
    ax.set_ylabel("Memory (MB)")
    ax.set_xlabel("Time")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
