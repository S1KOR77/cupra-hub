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

import json
import logging
import os

def load_rebates():
    """Wczytaj rabaty i konfigurację z settings.json."""
    settings_file = "settings.json"
    if not os.path.exists(settings_file):
        logging.warning(f"  🚨 Brak {settings_file} — scrapuje bez rabatów!")
        return [], {}, {}
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        rebates = [r for r in data.get("rebates", []) if r.get("active", True)]
        margin_cfg = data.get("margin_config", {})
        dealer_pcts = data.get("dealer_percentages", {})
        
        # DEBUG: Log Leon entry loading
        leon_2025 = [r for r in rebates if r.get("model") == "leon" and r.get("year") == 2025]
        leon_2026 = [r for r in rebates if r.get("model") == "leon" and r.get("year") == 2026]
        
        logging.info(f"  ✅ Wczytane {len(rebates)} aktywnych rabatów z {settings_file}")
        logging.info(f"    Leon 2025: {len(leon_2025)} rebates ({sorted(set(r.get('amount') for r in leon_2025))})")
        logging.info(f"    Leon 2026: {len(leon_2026)} rebates ({sorted(set(r.get('amount') for r in leon_2026))})")
        
        return rebates, margin_cfg, dealer_pcts
    except Exception as e:
        logging.warning(f"  🚨 Błąd wczytywania {settings_file}: {e}")
        return [], {}, {}

REBATES_LIST, MARGIN_CFG, DEALER_PCTS = load_rebates()
logging.basicConfig(level=logging.INFO, format="%(message)s")
load_rebates()
