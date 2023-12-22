#!/bin/bash

# Sprawdzenie liczby argumentów
if [ $# -ne 2 ]; then
    echo "Użycie: $0 plik_tekstowy.txt prefix"
    exit 1
fi

# Argumenty
input_file="$1"
prefix="$2"

# Pętla odczytująca adresy URL z pliku i pobierająca pliki
index=1
while IFS= read -r url; do
    filename="${url##*/}"
    wget "$url" -O "${prefix}_${index}_${filename}"
    ((index++))
done < "$input_file"