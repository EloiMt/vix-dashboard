#!/bin/bash

# Fichiers
DATA_FILE="$HOME/vix_data.csv"
REPORT_FILE="$HOME/daily_report.txt"

# Récupérer la date du dernier enregistrement
TODAY=$(tail -n 1 "$DATA_FILE" | cut -d',' -f1 | cut -d'T' -f1)

# Extraire les lignes du jour
lines_today=$(grep "$TODAY" "$DATA_FILE")

# Si aucune donnée pour aujourd'hui, on quitte
if [ -z "$lines_today" ]; then
    echo "[$(date)] Aucune donnée pour aujourd'hui." > "$REPORT_FILE"
    exit 0
fi

# Extraire les valeurs VIX (2e colonne)
vix_values=$(echo "$lines_today" | cut -d ',' -f2)

# Calcul des statistiques
open=$(echo "$vix_values" | head -n 1)
close=$(echo "$vix_values" | tail -n 1)
min=$(echo "$vix_values" | sort -n | head -n 1)
max=$(echo "$vix_values" | sort -n | tail -n 1)

# Variation en %
change=$(awk "BEGIN {printf \"%.2f\", (($close - $open) / $open) * 100}")

# Moyenne et écart-type (volatilité)
read mean stddev <<< $(echo "$vix_values" | awk '{sum+=$1; sumsq+=$1*$1} END {mean=sum/NR; stddev=sqrt(sumsq/NR - mean^2); printf "%.2f %.2f", mean, stddev}')

# Médiane
median=$(echo "$vix_values" | sort -n | awk '{a[i++]=$1} END {if (i%2==1) print a[int(i/2)]; else print (a[i/2-1]+a[i/2])/2}')

# Nombre d'observations
count=$(echo "$vix_values" | wc -l)

# Écriture du rapport
{
    echo "📈 Date: $TODAY"
    echo "🔸 Open: $open"
    echo "🔸 Close: $close"
    echo "🔸 High: $max"
    echo "🔸 Low: $min"
    echo "📉 Change: $change %"
    echo "📊 Mean: $mean"
    echo "📊 Median: $median"
    echo "📊 Data points: $count"
    echo "📈 Volatility (σ): $stddev"
} > "$REPORT_FILE"

