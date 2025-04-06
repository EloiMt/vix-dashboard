#!/bin/bash

# Récupère les données depuis CBOE
json=$(curl -s -A "Mozilla/5.0" "https://www.cboe.com/indices/data/?symbol=VIX&timeline=1M")

# Vérifie si jq a bien pu lire le JSON
if [[ -z "$json" || "$json" == *"error"* ]]; then
    echo "[$(date "+%Y-%m-%d %H:%M:%S")] Erreur lors de la récupération des données." >> ~/vix_log.txt
    exit 1
fi

# Extraction du dernier point
last_entry=$(echo "$json" | jq '.data[-1]')

timestamp=$(echo "$last_entry" | jq -r '.[0]')
open=$(echo "$last_entry" | jq -r '.[1]')
high=$(echo "$last_entry" | jq -r '.[2]')
low=$(echo "$last_entry" | jq -r '.[3]')
close=$(echo "$last_entry" | jq -r '.[4]')

# Calcul du changement en pourcentage
change=$(awk "BEGIN {printf \"%.2f\", (($close - $open)/$open)*100}")

# Calcul d'une "volatilité simple" = high - low
volatility=$(awk "BEGIN {printf \"%.2f\", ($high - $low)}")

# Enregistrement CSV (timestamp, close)
echo "$timestamp,$close" >> ~/vix_data.csv

# Log de scraping
echo "[$(date "+%Y-%m-%d %H:%M:%S")] VIX scrappé : $close" >> ~/vix_log.txt

# Rapport texte
report_path=~/daily_report.txt
{
    echo "📈 Daily VIX Report for ${timestamp:0:10}"
    echo ""
    echo "📌 Open:      $open"
    echo "📌 Close:     $close"
    echo "📌 High:      $high"
    echo "📌 Low:       $low"
    echo "📉 Change:    $change %"
    echo "📊 Volatility (σ): $volatility"
} > "$report_path"

