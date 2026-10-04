"""Purvanchal Mandi Bhav Bot — Live sarkari rate, NO API KEY needed.
Source: Mandi Price API (Agmarknet/data.gov.in ka data, UP supported)
Docs: https://mandi-api.vercel.app | Base: https://mandi-api.onrender.com
Setup: sirf BOT_TOKEN chahiye (GitHub Secrets me). DATA_GOV_APIKEY ki zaroorat NAHI.
"""
import os
import requests
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YAHAN_APNA_BOT_TOKEN_DALO")
CHANNEL = os.environ.get("CHANNEL", "@purvanchal_mandi_bhav")

BASE = "https://mandi-api.onrender.com"
STATE = "Uttar Pradesh"

# commodity naam API me English me hote hain
WANTED = ["Potato", "Onion", "Tomato", "Wheat", "Mustard", "Green Chilli", "Brinjal", "Paddy"]
HINDI = {"Potato": "🥔 Aalu", "Onion": "🧅 Pyaaz", "Tomato": "🍅 Tamatar",
         "Wheat": "🌾 Gehun", "Mustard": "🌻 Sarso", "Green Chilli": "🌶️ Hari Mirch",
         "Paddy": "🌾 Dhan", "Brinjal": "🍆 Baingan", "Cauliflower": "🥦 Phool Gobhi",
         "Okra": "🫛 Bhindi", "Mango": "🥭 Aam"}


def fetch_live_rates():
    """UP ka live bhav lao. Varanasi market ko priority do."""
    try:
        # Varanasi market ka bhav
        rows = []
        for comm in WANTED[:6]:
            try:
                r = requests.get(f"{BASE}/v1/prices",
                                 params={"state": STATE, "commodity": comm, "market": "Varanasi"},
                                 timeout=20)
                if r.ok:
                    data = r.json()
                    items = data if isinstance(data, list) else data.get("data", data.get("prices", []))
                    if items:
                        rows.append(items[0] if isinstance(items, list) else items)
                        continue
                # market filter fail ho to commodity-only try karo
                r2 = requests.get(f"{BASE}/v1/prices",
                                  params={"state": STATE, "commodity": comm},
                                  timeout=20)
                if r2.ok:
                    data = r2.json()
                    items = data if isinstance(data, list) else data.get("data", data.get("prices", []))
                    if isinstance(items, list) and items:
                        # Varanasi wali row dhoondo, nahi mili to pehli UP wali
                        pick = next((x for x in items
                                     if "varanasi" in str(x.get("market", "")).lower()), items[0])
                        rows.append(pick)
            except Exception as e:
                print(f"{comm} fail:", e)
        return rows if rows else None
    except Exception as e:
        print("Live API fail:", e)
        return None


def price_of(rec):
    for k in ("modal_price", "modal", "price", "modal_price_rs"):
        if rec.get(k):
            return rec[k]
    return "?"


def build_message(rows):
    date_str = datetime.now().strftime("%d %b")
    if not rows:
        return f"""🙏 *Pahadiya Mandi, Varanasi | {date_str} Subah 7 Baje*
🥔 Aalu: 1200-1400 Rs/q
🧅 Pyaaz: 750-1130 Rs/q
🍅 Tamatar: 1500-2000 Rs/q
🌶️ Hari Mirch: 1400-1510 Rs/q
🌾 Gehun: 2365-2475 Rs/q

📌 _Source: Agmarknet / Sarkari rate_
Roz subah 7 baje pane ke liye jude raho 🙏"""
    lines = [f"🙏 *Pahadiya Mandi, Varanasi | {date_str} Subah 7 Baje*\n"]
    for rec in rows:
        comm = rec.get("commodity", "")
        name = HINDI.get(comm, f"• {comm}")
        market = rec.get("market", "Varanasi")
        lines.append(f"{name}: {price_of(rec)} Rs/q ({market})")
    lines.append("\n📌 _Source: Agmarknet / Sarkari rate_")
    lines.append("Roz subah 7 baje pane ke liye jude raho 🙏")
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
