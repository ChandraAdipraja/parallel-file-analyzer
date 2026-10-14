## NAMA     : CHANDRA ADIPRAJA
## NPM      : 247006111194
## KELAS    : G

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from time import perf_counter

from analyzer import analyze_text


NPM = 247006111194

MAX_FILES = 1940
DEFAULT_THREADS = 4
DEFAULT_PROCESSES = 3
DEFAULT_FILES = 1940

DATA_DIR = Path("data")
RESULTS_FILE = Path("results.csv")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Benchmark Parallel File Analyzer"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=DEFAULT_THREADS,
        help="Jumlah thread yang digunakan"
    )

    parser.add_argument(
        "--processes",
        type=int,
        default=DEFAULT_PROCESSES,
        help="Jumlah process yang digunakan"
    )

    parser.add_argument(
        "--files",
        type=int,
        default=DEFAULT_FILES,
        help="Jumlah file yang dianalisis"
    )

    args = parser.parse_args()

    if args.threads < 1:
        raise ValueError("Jumlah thread harus minimal 1.")

    if args.processes < 1:
        raise ValueError("Jumlah process harus minimal 1.")

    if args.files < 1 or args.files > MAX_FILES:
        raise ValueError(
            f"Jumlah file harus berada pada rentang 1 sampai {MAX_FILES}."
        )

    return args


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def aggregate_results(results):
    total = {
        "characters": 0,
        "words": 0,
        "lines": 0,
        "vowels": 0,
        "digits": 0,
        "symbols": 0,
    }

    for result in results:
        for key in total:
            total[key] += result[key]

    return total


def run_serial(files):
    results = []

    start_time = perf_counter()

    for file_path in files:
        text = read_file(file_path)
        result = analyze_text(text)
        results.append(result)

    elapsed_time = perf_counter() - start_time

    return results, elapsed_time


def run_parallel(files, threads, processes):
    start_time = perf_counter()

    with ThreadPoolExecutor(max_workers=threads) as thread_pool:
        texts = list(thread_pool.map(read_file, files))

    with ProcessPoolExecutor(max_workers=processes) as process_pool:
        results = list(process_pool.map(analyze_text, texts))

    elapsed_time = perf_counter() - start_time

    return results, elapsed_time


def save_result_to_csv(
    threads,
    processes,
    total_files,
    serial_time,
    parallel_time,
    serial_throughput,
    parallel_throughput,
    speedup,
    efficiency
):
    file_exists = RESULTS_FILE.exists()

    with open(
        RESULTS_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "threads",
                "processes",
                "files",
                "serial_time",
                "parallel_time",
                "serial_throughput",
                "parallel_throughput",
                "speedup",
                "efficiency"
            ])

        writer.writerow([
            threads,
            processes,
            total_files,
            f"{serial_time:.4f}",
            f"{parallel_time:.4f}",
            f"{serial_throughput:.2f}",
            f"{parallel_throughput:.2f}",
            f"{speedup:.2f}",
            f"{efficiency:.2f}"
        ])


def main():
    args = parse_arguments()

    threads = args.threads
    processes = args.processes
    total_files = args.files

    all_files = sorted(DATA_DIR.glob("*.txt"))

    if len(all_files) < total_files:
        raise ValueError(
            f"Dataset tidak mencukupi.\n"
            f"File tersedia  : {len(all_files)}\n"
            f"File dibutuhkan: {total_files}"
        )

    files = all_files[:total_files]

    print("=" * 60)
    print("              PARALLEL FILE ANALYZER")
    print("                 PERFORMANCE TEST")
    print("=" * 60)

    print(f"NPM               : {NPM}")
    print(f"Jumlah file       : {total_files}")
    print(f"Jumlah thread     : {threads}")
    print(f"Jumlah process    : {processes}")
    print(f"Total worker      : {threads + processes}")

    print("=" * 60)
    print()

    print("Menjalankan pemrosesan serial...")

    serial_results, serial_time = run_serial(files)

    print("Pemrosesan serial selesai.")
    print()

    print("Menjalankan pemrosesan hybrid parallel...")

    parallel_results, parallel_time = run_parallel(
        files,
        threads,
        processes
    )

    print("Pemrosesan parallel selesai.")
    print()

    serial_total = aggregate_results(serial_results)
    parallel_total = aggregate_results(parallel_results)

    if serial_total != parallel_total:
        raise RuntimeError(
            "Hasil serial dan parallel tidak sama!"
        )

    serial_throughput = total_files / serial_time
    parallel_throughput = total_files / parallel_time

    speedup = serial_time / parallel_time

    total_workers = threads + processes

    efficiency = (
        speedup / total_workers
    ) * 100

    print("=" * 60)
    print("                    HASIL ANALISIS")
    print("=" * 60)

    print(f"Total karakter    : {parallel_total['characters']:,}")
    print(f"Total kata        : {parallel_total['words']:,}")
    print(f"Total baris       : {parallel_total['lines']:,}")
    print(f"Total vokal       : {parallel_total['vowels']:,}")
    print(f"Total angka       : {parallel_total['digits']:,}")
    print(f"Total simbol      : {parallel_total['symbols']:,}")

    print()
    print("=" * 60)
    print("                  HASIL PERFORMANCE")
    print("=" * 60)

    print(f"Waktu serial       : {serial_time:.4f} detik")
    print(f"Waktu parallel     : {parallel_time:.4f} detik")

    print()

    print(
        f"Throughput serial  : "
        f"{serial_throughput:.2f} file/detik"
    )

    print(
        f"Throughput parallel: "
        f"{parallel_throughput:.2f} file/detik"
    )

    print()

    print(f"Speedup            : {speedup:.2f}x")
    print(f"Efisiensi hybrid   : {efficiency:.2f}%")

    print()

    save_result_to_csv(
        threads,
        processes,
        total_files,
        serial_time,
        parallel_time,
        serial_throughput,
        parallel_throughput,
        speedup,
        efficiency
    )

    print("=" * 60)
    print("Validasi hasil     : BERHASIL")
    print("Hasil serial dan parallel sama.")
    print()
    print(f"Hasil disimpan     : {RESULTS_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()