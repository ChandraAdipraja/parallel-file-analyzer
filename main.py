## NAMA     : CHANDRA ADIPRAJA
## NPM      : 247006111194
## KELAS    : G

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from time import perf_counter

from analyzer import analyze_text

NPM = 247006111194

TOTAL_FILES = 1940
THREADS = 4
PROCESSES = 3

DATA_DIR = Path("data")

def read_file(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text

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

def main():
    files = sorted(DATA_DIR.glob("*.txt"))

    if len(files) != TOTAL_FILES:
        raise ValueError(
            f"Jumlah file tidak sesuai. "
            f"Ditemukan {len(files)} file, "
            f"seharusnya {TOTAL_FILES} file."
        )

    print("========================================")
    print("       PARALLEL FILE ANALYZER")
    print("========================================")
    print(f"NPM              : {NPM}")
    print(f"Jumlah file      : {TOTAL_FILES}")
    print(f"Jumlah thread    : {THREADS}")
    print(f"Jumlah process   : {PROCESSES}")
    print("========================================")
    print()

    start_time = perf_counter()

    with ThreadPoolExecutor(
        max_workers=THREADS
    ) as thread_pool:

        texts = list(
            thread_pool.map(
                read_file,
                files
            )
        )

    with ProcessPoolExecutor(
        max_workers=PROCESSES
    ) as process_pool:

        results = list(
            process_pool.map(
                analyze_text,
                texts
            )
        )

    total = aggregate_results(results)

    end_time = perf_counter()
    elapsed_time = end_time - start_time

    throughput = TOTAL_FILES / elapsed_time

    print("HASIL ANALISIS")
    print("----------------------------------------")
    print(f"Total karakter : {total['characters']:,}")
    print(f"Total kata     : {total['words']:,}")
    print(f"Total baris    : {total['lines']:,}")
    print(f"Total vokal    : {total['vowels']:,}")
    print(f"Total angka    : {total['digits']:,}")
    print(f"Total simbol   : {total['symbols']:,}")
    print()

    print("PERFORMA")
    print("----------------------------------------")
    print(f"Waktu total    : {elapsed_time:.4f} detik")
    print(f"Throughput     : {throughput:.2f} file/detik")
    print()


if __name__ == "__main__":
    main()