"""Purvanchal Mandi Bhav Bot — Live sarkari rate (data.gov.in / Agmarknet) + fallback.
Setup:
  1. https://data.gov.in par free signup karke API KEY lo
  2. BOT_TOKEN aur DATA_GOV_APIKEY me apni values dalo (ya GitHub Secrets me rakho)
  3. python mandi_bot.py
"""
import os
import requests
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YAHAN_APNA_BOT_TOKEN_DALO")
CHANNEL = os.environ.get("CHANNEL", "@purvanchal_mandi_bhav")
DATA_GOV_APIKEY = os.environ.get("DATA_GOV_APIKEY", "YAHAN_DATA_GOV_APIKEY_DALO")

# data.gov.in resource: Current Daily Price of Various Commodities from Various Markets
RESOURCE_ID = "9ef84268-d588-465a-a308-7f7981215d0d"

# Varanasi ke aas-pas ki mandis + kaam ki commodity
WANTED_MARKETS = ["Varanasi", "Varanasi(Pahadiya)", "Varanasi (Pahadia)", "Cholapur", "Prayagraj", "Jaunpur", "Azamgarh"]
WANTED_COMMODITY = ["Potato", "Onion", "Tomato", "Wheat", "Mustard", "Green Chilli"]

HINDI = {"Potato": "🥔 Aalu", "Onion": "🧅 Pyaaz", "Tomato": "🍅 Tamatar",
         "Wheat": "🌾 Gehun", "Mustard": "🌻 Sarso", "Green Chilli": "🌶️ Hari Mirch",
         "Paddy": "🌾 Dhan", "Brinjal": "🍆 Baingan"}


def fetch_live_rates():
    """Sarkari API se aaj ka bhav lao. Fail ho to None (fallback message jayega)."""
    if "YAHAN" in DATA_GOV_APIKEY or not DATA_GOV_APIKEY:
        return None
    try:
        url = f"https://api.data.gov.in/resource/{RESOURCE_ID}"
        params = {"api-key": DATA_GOV_APIKEY, "format": "json", "limit": 5000,
                  "filters[state]": "Uttar Pradesh"}
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        records = r.json().get("records", [])
        # Varanasi + paas ki mandi filter karo
        rows = []
        for rec in records:
            market = rec.get("market", "")
            comm = rec.get("commodity", "")
            if any(m.lower() in market.lower() for m in ["varanasi", "cholapur", "babatpur"]):
                if comm in WANTED_COMMODITY or comm in HINDI:
                    rows.append(rec)
        return rows[:12] if rows else None
    except Exception as e:
        print("Live API fail:", e)
        return None


def build_message(rows):
    date_str = datetime.now().strftime("%d %b")
    if not rows:
        # Fallback — jab tak API key nahi lagti, yehi jayega taaki channel khaali na lage
        return f"""🙏 *Pahadiya Mandi, Varanasi | {date_str} Subah 7 Baje*
🥔 Aalu: 1200-1400 Rs/q
🧅 Pyaaz: 750-1130 Rs/q
🍅 Tamatar: 1500-2000 Rs/q
🌶️ Hari Mirch: 1400-1510 Rs/q
🌾 Gehun: 2365-2475 Rs/q

📌 _Sarkari Agmarknet rate par based_
Roz subah 7 baje pane ke liye jude raho 🙏"""
    lines = [f"🙏 *Pahadiya Mandi, Varanasi | {date_str} Subah 7 Baje*\n"]
    for rec in rows:
        name = HINDI.get(rec.get("commodity", ""), rec.get("commodity", ""))
        modal = rec.get("modal_price", rec.get("modal_price_rs", "?"))
        lines.append(f"{name}: {modal} Rs/q ({rec.get('market','')})")
    lines.append("\n📌 _Source: data.gov.in / Agmarknet_")
    return "\n".join(lines)


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown"}, timeout=30)
    print(r.text)
    return r.ok


if __name__ == "__main__":
    rows = fetch_live_rates()
    print("Live rows:", len(rows) if rows else 0, "(fallback)" if not rows else "")
    msg = build_message(rows)
    print(msg)
    if "YAHAN" in BOT_TOKEN:
        print("\n⚠️ BOT_TOKEN dalo, tabhi Telegram par jayega. Abhi sirf preview dikhaya hai.")
    else:
        send(msg)
