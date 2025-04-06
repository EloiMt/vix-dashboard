#!/bin/bash

DATA_FILE="$HOME/vix_data.csv"
REPORT_FILE="$HOME/daily_report.txt"
TODAY=$(date "+%Y-%m-%d")

# Extraire les lignes du jour
lines_today=$(grep "$TODAY" "$DATA_FILE")

# Si aucune donnée, on quitte
if [ -z "$lines_today" ]; then
    echo "[$(date)] Aucune donnée pour aujourd'hui." > "$REPORT_FILE"
    exit 0
fi

# Extraire les valeurs
vix_values=$(echo "$lines_today" | cut -d ',' -f2)

open=$(echo "$vix_values" | head -n 1)
close=$(echo "$vix_values" | tail -n 1)
min=$(echo "$vix_values" | sort -n | head -n 1)
max=$(echo "$vix_values" | sort -n | tail -n 1)
change=$(awk "BEGIN {printf \"%.2f\", (($close - $open) / $open) * 100}")

# Moyenne et volatilité
read mean stddev <<< $(echo "$vix_values" | awk '{sum+=$1; sumsq+=$1*$1;} END {mean=sum/NR; stddev=sqrt(sumsq/NR - mean^2); print mean, stddev}')

# Médiane
median=$(echo "$vix_values" | sort -n | awk '{a[i++]=$1;} END {print a[int(i/2)]}')

# Nombre d'observations
count=$(echo "$vix_values" | wc -l)

# Écrire le rapport
echo "📈 Daily VIX Report for $TODAY" > "$REPORT_FILE"
echo "🔸 Open: $open" >> "$REPORT_FILE"
echo "🔸 Close: $close" >> "$REPORT_FILE"
echo "🔸 High: $max" >> "$REPORT_FILE"
echo "🔸 Low: $min" >> "$REPORT_FILE"
echo "📉 Change: $change %" >> "$REPORT_FILE"
echo "📊 Mean: $mean" >> "$REPORT_FILE"
echo "📊 Median: $median" >> "$REPORT_FILE"
echo "📊 Data points: $count" >> "$REPORT_FILE"
echo "📈 Volatility (σ): $stddev" >> "$REPORT_FILE"
