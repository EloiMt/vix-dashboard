Ce projet permet de visualiser l'évolution du VIX en temps réel via un dashboard en Dash/Plotly.

## Fonctionnalités
Scraping du VIX depuis Yahoo Finance
Mise à jour automatique toutes les 5 minutes
Rapport quotidien à 20h
Dashboard web

## Auteurs
Eloi Martin	
Ahmed Mili 
---

## 🔧 Features

- 🔁 **Scrapes VIX** every 5 minutes (from Yahoo Finance)
- 📈 **Interactive dashboard** displaying the VIX evolution
- 📝 **Daily report generation** (max, min, average values…)
- 🔄 **Continuous updates** via `cron`
- 📂 **Comprehensive logging** of all processes

---

## 🚀 Technologies Used

- Python (Pandas, Dash, Plotly)
- Bash scripting (for automation)
- Cron (for task scheduling)
- Linux (Ubuntu EC2 environment)
- GitHub (version control and collaboration)

---

## 📌 Manual Launch

```bash
python3 dashboard.py
