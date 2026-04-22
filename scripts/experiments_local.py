import subprocess
import threading
import time
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import psutil

# ==============================
# Monitoring Utilities
# ==============================


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

    print(f"\nMonitoring processes matching: '{process_name}'\n", flush=True)

    # CPU warm-up
    for p in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        if process_name in safe_cmdline(p.info):
            try:
                p.cpu_percent(None)
            except psutil.NoSuchProcess:
                pass

    while not stop_event.is_set():
        procs = [
            p
            for p in psutil.process_iter(attrs=["pid", "name", "cmdline"])
            if process_name in safe_cmdline(p.info)
        ]

        total_rss = 0
        total_cpu = 0
        pids = []

        for p in procs:
            try:
                mem = p.memory_info()
                total_rss += mem.rss
                total_cpu += p.cpu_percent(None)
                pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass

        records.append(
            {
                "timestamp": datetime.now(),
                "pids": ",".join(map(str, pids)),
                "n_procs": len(pids),
                "rss_mb": total_rss / 1024**2,
                "cpu_percent": total_cpu,
            }
        )

        print(
            f"[{records[-1]['timestamp']:%H:%M:%S}] "
            f"procs={len(pids)} "
            f"RSS={records[-1]['rss_mb']:.1f} MB "
            f"CPU={records[-1]['cpu_percent']:.1f}%",
            flush=True,
        )

        time.sleep(interval)

    return pd.DataFrame(records)


# ==============================
# Pipeline Runner
# ==============================


def run_pipeline_with_monitor(command, run_name, output_dir):
    stop_event = threading.Event()
    monitor_data = {}

    def monitor_wrapper():
        df = monitor_process(
            process_name="ollama",
            interval=30,
            stop_event=stop_event,
        )
        monitor_data["df"] = df

    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor_wrapper)
    monitor_thread.start()

    # Run pipeline
    process = subprocess.Popen(command, shell=True)
    process.wait()

    # Stop monitor
    stop_event.set()
    monitor_thread.join()

    print(f"\nPipeline finished for {run_name}. Monitor stopped.")

    # Save results
    df = monitor_data.get("df", pd.DataFrame())

    if not df.empty:
        csv_path = f"{output_dir}/{run_name}.csv"
        plot_path = f"{output_dir}/{run_name}.png"

        df.set_index("timestamp", inplace=True)
        df.to_csv(csv_path)

        ax = df["rss_mb"].plot(
            title=f"Memory Usage (RSS) - {run_name}",
            figsize=(10, 5),
        )
        ax.set_ylabel("Memory (MB)")
        ax.set_xlabel("Time")

        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

        print(f"Saved monitoring CSV to {csv_path}")
        print(f"Saved monitoring plot to {plot_path}")
    else:
        print("No monitoring data collected.")


# ==============================
# Personalization Pipeline Loop
# ==============================


def run_personalization(base_route: str):
    stories = [
        "caballero.md",
        "calendario.md",
        "cuaderno.md",
        "mensaje.md",
        "rana.md",
        "yi.md",
    ]

    profiles = [
        "boy.md",
        "girl.md",
    ]

    for profile in profiles:
        for story in stories:
            story_path = f"{base_route}/stories/{story}"
            preferences_path = f"{base_route}/profiles/{profile}"

            run_name = f"{profile[:-3]}_{story[:-3]}"

            command = (
                f"uv run scripts/main.py "
                f"--story_path {story_path} "
                f"--preferences_path {preferences_path} "
                f"--pipelines PERSONALIZATION "
                f"--output_path outputs/personalization/{run_name}.md "
                f"--verbose"
            )

            print(f"\nRunning command: {command}\n")

            run_pipeline_with_monitor(
                command, run_name, output_dir="outputs/personalization/monitoring"
            )

            print("Sleeping 5 minutes for next run...\n")
            time.sleep(300)

def run_questions(base_route: str):
    stories = [
        "caballero.md",
        "calendario.md",
        "cuaderno.md",
        "mensaje.md",
        "rana.md",
        "yi.md",
    ]

    for story in stories:
        story_path = f"{base_route}/stories/{story}"
        run_name = f"questions_{story[:-3]}"

        command = (
            f"uv run src/main.py "
            f"--story_path {story_path} "
            f"--preferences_path {base_route}/profiles/girl.md "
            f"--pipelines QUESTIONS "
            f"--output_path outputs/questions/{story[:-3]}.md "
            f"--verbose"
        )

        print(f"\nRunning command: {command}\n")

        run_pipeline_with_monitor(
            command, run_name, output_dir="outputs/questions/monitoring"
        )

        print("Sleeping 5 minutes for next run...\n")
        time.sleep(300)


# ==============================
# MAIN
# ==============================


def main():
    base_route = "data"

    run_personalization(base_route)
    run_questions(base_route)

if __name__ == "__main__":
    main()
