## NAMA     : CHANDRA ADIPRAJA
## NPM      : 247006111194
## KELAS    : G

import random
import string
from pathlib import Path

NPM = 247006111194
RANDOM_SEED = NPM

TOTAL_FILES = 1940
OUTPUT_DIR = Path("data")

TARGET_FILE_SIZE = 20 * 1024


WORDS = [
    "parallel",
    "computing",
    "file",
    "analyzer",
    "python",
    "thread",
    "process",
    "data",
    "analysis",
    "system",
    "performance",
    "algorithm",
    "program",
    "computer",
    "network",
    "information",
    "technology",
    "software",
    "hardware",
    "execution",
]

DIGITS = string.digits

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"

def generate_line():

    word_count = random.randint(15, 30)

    parts = []

    for _ in range(word_count):
        choice = random.randint(1, 10)

        if choice <= 7:
            # Kata
            parts.append(random.choice(WORDS))

        elif choice <= 9:
            # Angka
            parts.append(
                "".join(
                    random.choice(DIGITS)
                    for _ in range(random.randint(1, 6))
                )
            )

        else:
            # Simbol
            parts.append(random.choice(SYMBOLS))

    return " ".join(parts)

def generate_file(file_number):

    lines = []
    current_size = 0

    while current_size < TARGET_FILE_SIZE:
        line = generate_line()

        lines.append(line)

        current_size += len(line.encode("utf-8")) + 1

    file_path = OUTPUT_DIR / f"file_{file_number:04d}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

def main():
    random.seed(RANDOM_SEED)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=== Parallel File Analyzer ===")
    print(f"NPM          : {NPM}")
    print(f"Random Seed  : {RANDOM_SEED}")
    print(f"Jumlah file  : {TOTAL_FILES}")
    print("Target ukuran: ±20 KB/file")
    print(f"Output       : {OUTPUT_DIR}")
    print()

    for file_number in range(1, TOTAL_FILES + 1):
        generate_file(file_number)

    print("Dataset berhasil dibuat.")
    print(f"Total file: {TOTAL_FILES}")


if __name__ == "__main__":
    main()