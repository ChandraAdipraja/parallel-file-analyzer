### NAMA     : CHANDRA ADIPRAJA
### NPM      : 247006111194
### KELAS    : G

import csv
from pathlib import Path

import matplotlib.pyplot as plt


RESULTS_FILE = Path("results.csv")
OUTPUT_DIR = Path("grafik")


def load_results():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"{RESULTS_FILE} tidak ditemukan. "
            "Jalankan benchmark.py terlebih dahulu."
        )

    results = []

    with open(
        RESULTS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            results.append({
                "threads": int(row["threads"]),
                "processes": int(row["processes"]),
                "files": int(row["files"]),
                "parallel_time": float(row["parallel_time"]),
                "speedup": float(row["speedup"]),
            })

    return results


def plot_time_vs_threads(results):
    threads = [row["threads"] for row in results]
    times = [row["parallel_time"] for row in results]

    labels = [
        f"{row['threads']}T\n"
        f"{row['processes']}P - "
        f"{row['files']} file"
        for row in results
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(
        range(len(results)),
        times,
        marker="o"
    )

    plt.xticks(
        range(len(results)),
        labels
    )

    plt.xlabel("Konfigurasi Thread")
    plt.ylabel("Waktu Parallel (detik)")
    plt.title("Waktu vs Jumlah Thread")

    plt.grid(True)
    plt.tight_layout()

    output = OUTPUT_DIR / "waktu_vs_thread.png"

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Grafik dibuat: {output}")


def plot_time_vs_processes(results):
    processes = [row["processes"] for row in results]
    times = [row["parallel_time"] for row in results]

    labels = [
        f"{row['processes']}P\n"
        f"{row['threads']}T - "
        f"{row['files']} file"
        for row in results
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(
        range(len(results)),
        times,
        marker="o"
    )

    plt.xticks(
        range(len(results)),
        labels
    )

    plt.xlabel("Konfigurasi Process")
    plt.ylabel("Waktu Parallel (detik)")
    plt.title("Waktu vs Jumlah Process")

    plt.grid(True)
    plt.tight_layout()

    output = OUTPUT_DIR / "waktu_vs_process.png"

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Grafik dibuat: {output}")


def plot_speedup(results):
    labels = [
        f"{row['threads']}T-"
        f"{row['processes']}P-"
        f"{row['files']}"
        for row in results
    ]

    speedups = [
        row["speedup"]
        for row in results
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(
        range(len(results)),
        speedups,
        marker="o"
    )

    plt.xticks(
        range(len(results)),
        labels
    )

    plt.xlabel("Konfigurasi")
    plt.ylabel("Speedup (x)")
    plt.title("Speedup vs Konfigurasi")

    plt.grid(True)
    plt.tight_layout()

    output = OUTPUT_DIR / "speedup_vs_konfigurasi.png"

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Grafik dibuat: {output}")


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    results = load_results()

    if not results:
        raise ValueError(
            "results.csv tidak memiliki data eksperimen."
        )

    print("=" * 50)
    print("          GENERATE GRAFIK")
    print("=" * 50)

    print(f"Jumlah eksperimen: {len(results)}")
    print()

    plot_time_vs_threads(results)
    plot_time_vs_processes(results)
    plot_speedup(results)

    print()
    print("Semua grafik berhasil dibuat.")


if __name__ == "__main__":
    main()