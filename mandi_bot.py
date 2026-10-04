"""Purvanchal Mandi Bhav Bot — Live sarkari rate, NO API KEY needed.
Base: https://mandi-api.onrender.com (UP supported)
Setup: sirf BOT_TOKEN chahiye (GitHub Secrets me).
"""
import os
import requests
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YAHAN_APNA_BOT_TOKEN_DALO")
CHANNEL = os.environ.get("CHANNEL", "@purvanchal_mandi_bhav")

BASE = "https://mandi-api.onrender.com"
STATE = "Uttar Pradesh"

# Poori sabzi + fal + anaaj list — API me English naam se
WANTED = [
    "Potato", "Onion", "Tomato", "Green Chilli", "Brinjal", "Cauliflower",
    "Cabbage", "Okra", "Carrot", "Peas", "Bottle Gourd", "Bitter Gourd",
    "Pumpkin", "Cucumber", "Radish", "Spinach", "Ginger", "Garlic",
    "Lemon", "Coriander", "Banana", "Apple", "Mango", "Papaya",
    "Wheat", "Paddy", "Mustard", "Gram", "Masoor", "Sugarcane",
]

HINDI = {
    "Potato": "🥔 Aalu", "Onion": "🧅 Pyaaz", "Tomato": "🍅 Tamatar",
    "Green Chilli": "🌶️ Hari Mirch", "Brinjal": "🍆 Baingan",
    "Cauliflower": "🥦 Phool Gobhi", "Cabbage": "🥬 Patta Gobhi",
    "Okra": "🫛 Bhindi", "Carrot": "🥕 Gajar", "Peas": "🫛 Matar",
    "Bottle Gourd": "🥒 Lauki", "Bitter Gourd": "🥒 Karela",
    "Pumpkin": "🎃 Kaddu", "Cucumber": "🥒 Kheera", "Radish": "🥗 Mooli",
    "Spinach": "🥬 Palak", "Ginger": "🫚 Adrak", "Garlic": "🧄 Lahsun",
    "Lemon": "🍋 Nimbu", "Coriander": "🌿 Dhaniya",
    "Banana": "🍌 Kela", "Apple": "🍎 Seb", "Mango": "🥭 Aam", "Papaya": "🍈 Papita",
    "Wheat": "🌾 Gehun", "Paddy": "🌾 Dhan", "Mustard": "🌻 Sarso",
    "Gram": "🫘 Chana", "Masoor": "🫘 Masoor", "Sugarcane": "🎋 Ganna",
}

VEG = set(list(HINDI.keys())[:24])
GRAIN = {"Wheat", "Paddy", "Mustard", "Gram", "Masoor", "Sugarcane"}


def fetch_live_rates():
    rows = []
    for comm in WANTED:
        try:
            r = requests.get(f"{BASE}/v1/prices",
                             params={"state": STATE, "commodity": comm, "market": "Varanasi"},
                             timeout=20)
            done = False
            if r.ok:
                data = r.json()
                items = data if isinstance(data, list) else data.get("data", data.get("prices", []))
                if items:
                    rows.append(items[0] if isinstance(items, list) else items)
                    done = True
            if not done:
                r2 = requests.get(f"{BASE}/v1/prices",
                                  params={"state": STATE, "commodity": comm}, timeout=20)
                if r2.ok:
                    data = r2.json()
                    items = data if isinstance(data, list) else data.get("data", data.get("prices", []))
                    if isinstance(items, list) and items:
                        pick = next((x for x in items
                                     if "varanasi" in str(x.get("market", "")).lower()), items[0])
                        rows.append(pick)
        except Exception as e:
            print(f"{comm} fail:", e)
    return rows if rows else None


def price_of(rec):
    for k in ("modal_price", "modal", "price", "modal_price_rs", "min_price"):
        if rec.get(k):
            return rec[k]
    return "?"


def fmt(rec):
    comm = rec.get("commodity", "")
    return f"{HINDI.get(comm, '• ' + comm)} — ₹{price_of(rec)}/q"


def build_message(rows):
    dt = datetime.now().strftime("%d %B, %A")
    head = (
        "🌾 *PURVANCHAL MANDI BHAV* 🌾\n"
        f"📍 Pahadiya Mandi, Varanasi\n"
        f"📅 {dt} | ⏰ Subah 4:00 Baje\n"
        "━━━━━━━━━━━━━━━\n"
    )
    tail = (
        "━━━━━━━━━━━━━━━\n"
        "✅ Sarkari mandi rate\n\n"
        "📢 *Apne 2 kisan bhaiyo ko jodo!*\n"
        "👉 @purvanchal_mandi_bhav\n"
        "Roz subah 4 baje sabse pehle bhav pao 🙏\n\n"
        "💬 Rate par charcha ke liye Discuss dabao 👇"
    )
    if not rows:
        body = (
            "\n🥬 *SABZI BHAV (₹/quintal)*\n"
            "🥔 Aalu — ₹1200-1400/q\n🧅 Pyaaz — ₹750-1130/q\n🍅 Tamatar — ₹1500-2000/q\n"
            "🫛 Bhindi — ₹1800-2200/q\n🍆 Baingan — ₹1200-1600/q\n🥦 Phool Gobhi — ₹1000-1400/q\n"
            "🥬 Patta Gobhi — ₹800-1200/q\n🥕 Gajar — ₹1500-2000/q\n🫛 Matar — ₹2500-3200/q\n"
            "🥒 Lauki — ₹800-1200/q\n🥒 Karela — ₹1500-2000/q\n🎃 Kaddu — ₹600-1000/q\n"
            "🥒 Kheera — ₹1000-1500/q\n🥗 Mooli — ₹800-1200/q\n🥬 Palak — ₹1000-1500/q\n"
            "🫚 Adrak — ₹2500-3500/q\n🧄 Lahsun — ₹4000-6000/q\n🍋 Nimbu — ₹2000-3000/q\n"
            "🌿 Dhaniya — ₹1500-2500/q\n🌶️ Hari Mirch — ₹1400-1510/q\n"
            "\n🍌 *FAL BHAV*\n🍌 Kela — ₹1500-2500/q\n🍎 Seb — ₹5000-8000/q\n🍈 Papita — ₹1200-2000/q\n"
            "\n🌾 *ANAAJ BHAV*\n🌾 Gehun — ₹2365-2475/q\n🌾 Dhan — ₹2200-2600/q\n"
            "🌻 Sarso — ₹5500-6200/q\n🫘 Chana — ₹5500-6500/q\n"
        )
        return head + body + "\n" + tail
    veg, fruit, grain = [], [], []
    for rec in rows:
        c = rec.get("commodity", "")
        if c in GRAIN:
            grain.append("• " + fmt(rec))
        elif c in ("Banana", "Apple", "Mango", "Papaya"):
            fruit.append("• " + fmt(rec))
        else:
            veg.append("• " + fmt(rec))
    body = ""
    if veg:
        body += "\n🥬 *SABZI BHAV (₹/quintal)*\n" + "\n".join(veg) + "\n"
    if fruit:
        body += "\n🍌 *FAL BHAV*\n" + "\n".join(fruit) + "\n"
    if grain:
        body += "\n🌾 *ANAAJ BHAV*\n" + "\n".join(grain) + "\n"
    return head + body + "\n" + tail


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown"}, timeout=30)
    print(r.text[:500])
    return r.ok


if __name__ == "__main__":
    rows = fetch_live_rates()
    print("Live rows:", len(rows) if rows else 0, "(fallback)" if not rows else "")
    msg = build_message(rows)
    print(msg)
    if "YAHAN" in BOT_TOKEN:
        print("\n⚠️ BOT_TOKEN dalo, tabhi Telegram par jayega.")
    else:
        send(msg)
