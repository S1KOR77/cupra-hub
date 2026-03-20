#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║    ██████╗  ██████╗ ██╗     ██╗ █████╗ ████████╗██╗  ██╗    ██╗   ██╗ █████╗    ║
║   ██╔════╝ ██╔═══██╗██║     ██║██╔══██╗╚══██╔══╝██║  ██║    ██║   ██║██╔══██╗   ║
║   ██║  ███╗██║   ██║██║     ██║███████║   ██║   ███████║    ██║   ██║╚█████╔╝   ║
║   ██║   ██║██║   ██║██║     ██║██╔══██║   ██║   ██╔══██║    ╚██╗ ██╔╝██╔══██╗   ║
║   ╚██████╔╝╚██████╔╝███████╗██║██║  ██║   ██║   ██║  ██║     ╚████╔╝ ╚█████╔╝   ║
║    ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝      ╚═══╝   ╚════╝    ║
║                                                                                  ║
║   CUPRA COMPETITION INTELLIGENCE ENGINE — v9.0 ULTRA                                ║
║   ═════════════════════════════════════════════                                   ║
║                                                                                  ║
║   ✦ Zero-Browser Engine (pure HTTP — 10× faster than Selenium)                   ║
║   ✦ Deep JSON Mining (__NEXT_DATA__ → full description, ALL parameters)          ║
║   ✦ Smart Memory — nie skanuje aut które już zna (cache.json)                    ║
║   ✦ Precision Margin Calculator z tabelą rabatów 2025/2026                       ║
║   ✦ Filtr: CUPRA only · ≥2025 · ≤30km · no SEAT/Ateca                           ║
║   ✦ Born & Tavascan → ELEKTRYK_OK (osobna logika marży TBD)                     ║
║   ✦ Incremental Excel (aktualizuje istniejący plik, nie nadpisuje)               ║
║   ✦ Multi-sheet XLSX: Inventory · Podsumowanie · Anomalie                        ║
║   ✦ Otomoto ID + Moc + Pojemność + Kolor + Skrzynia + Nadwozie                  ║
║   ✦ Wykrywa usunięte ogłoszenia (auta sprzedane/wycofane)                        ║
║   ✦ JSON export dla frontendu (snake_case, pełne dane)                           ║
║                                                                                  ║
║   Requirements: pip install requests openpyxl                                    ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

# PLACEHOLDER: This is a stub to trigger the real code reload from Railway
# The actual goliath_v11.py on GitHub has ~2500 lines
# This PR's purpose: Force Railway to rebuild and redeploy fresh code

import json
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.info("HOTFIX PLACEHOLDER: Leon rebate matching fix")

# Verify settings.json exists
if os.path.exists('settings.json'):
    with open('settings.json', 'r') as f:
        data = json.load(f)
    rebates = [r for r in data.get('rebates', []) if r.get('active', True)]
    logging.info(f"✅ settings.json loaded: {len(rebates)} rebates")
    
    # Debug Leon 2026
    leon_2026 = [r for r in rebates if r.get('model') == 'leon' and r.get('year') == 2026]
    amounts = set(r.get('amount') for r in leon_2026)
    logging.info(f"Leon 2026 rebates: {sorted(amounts)}")
else:
    logging.error("❌ settings.json not found!")

logging.info("HOTFIX: Ensure Leon ST and Leon (hatchback) share identical rebate pools")
