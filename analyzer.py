### NAMA     : CHANDRA ADIPRAJA
### NPM      : 247006111194
### KELAS    : G
import re


def analyze_text(text):

    # Jumlah seluruh karakter, termasuk spasi dan newline
    characters = len(text)

    # Menghitung kata yang terdiri dari karakter alfabet
    words = len(re.findall(r"[A-Za-z]+", text))

    # Menghitung jumlah baris
    lines = len(text.splitlines())

    # Menghitung jumlah vokal
    vowels = sum(
        1 for char in text.lower()
        if char in "aeiou"
    )

    # Menghitung jumlah angka
    digits = sum(
        1 for char in text
        if char.isdigit()
    )

    # Menghitung jumlah simbol
    symbols = sum(
        1 for char in text
        if not char.isalnum() and not char.isspace()
    )

    return {
        "characters": characters,
        "words": words,
        "lines": lines,
        "vowels": vowels,
        "digits": digits,
        "symbols": symbols,
    }


if __name__ == "__main__":
    sample_text = """Python parallel computing 123 File analyzer @ data"""

    result = analyze_text(sample_text)

    print("=== HASIL ANALISIS ===")
    print(f"Karakter : {result['characters']}")
    print(f"Kata     : {result['words']}")
    print(f"Baris    : {result['lines']}")
    print(f"Vokal    : {result['vowels']}")
    print(f"Angka    : {result['digits']}")
    print(f"Simbol   : {result['symbols']}")