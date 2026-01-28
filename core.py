import json
import os
from pathlib import Path
from groq import Groq

# --- KONFIGURASI ---
# Disarankan menggunakan environment variable, tapi saya masukkan di sini sesuai contoh Anda
API_KEY = "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"
client = Groq(api_key=API_KEY)

BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faq_toko.json"

# Aturan khusus untuk AI (System Prompt)
ATURAN_AI = """
Kamu adalah Customer Service Pintar dari 'Ayu Cell'. 
Tugasmu: Menjawab pertanyaan pelanggan tentang produk handphone, aksesoris, paket data, dan pulsa.

Aturan menjawab:
1. Gunakan bahasa yang sopan, ramah, santai, dan mudah dimengerti.
2. Fokus pada layanan Ayu Cell.
3. Jika pertanyaan tidak terkait produk handphone, aksesoris, paket data, dan pulsa, jawab dengan sopan bahwa kamu hanya melayani produk handphone, aksesoris, paket data, dan pulsa.
4. Jika tidak tahu jawabannya, sarankan pelanggan menghubungi admin di WA: 083842685163.
5. Gunakan sapaan umum seperti "Halo", "Hai", "Selamat datang di Ayu Cell", dll.
6. Jangan pernah memberikan informasi palsu atau menyesatkan.
7. Jika ada yang berkata kasar, tanggapi dengan sopan dan ingatkan untuk menggunakan bahasa yang ramah.
"""

# --- LOAD DATA FAQ ---
try:
    with FAQ_FILE.open("r", encoding="utf-8") as f:
        FAQS = json.load(f)
except Exception:
    FAQS = []
    print("Peringatan: file faq_toko.json tidak ditemukan atau korup.")

def get_bot_reply(user_message: str) -> str:
    text = (user_message or "").lower().strip()

    # 1. LOGIKA FAQ LOKAL (Keyword Matching)
    for faq in FAQS:
        for kw in faq["keywords"]:
            if kw.lower() in text:
                return faq["answer"]

    # 2. LOGIKA SAPAAN UMUM
    sapaan = ["halo", "hai", "assalamualaikum", "pagi", "siang", "sore", "malam", "permisi"]
    if any(s in text for s in sapaan):
        return (
            "Halo, selamat datang di Ayu Cell 👋\n"
            "Ada yang bisa kami bantu mengenai produk handphone, aksesoris, paket data, dan pulsa?\n"
            "Atau anda butuh bantuan lainnya?"
        )

    # 3. LOGIKA GROQ AI (Jika FAQ tidak ditemukan)
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", # Menggunakan model terbaru yang lebih stabil
            messages=[
                {"role": "system", "content": ATURAN_AI},
                {"role": "user", "content": user_message}
            ],
            temperature=0.6, # Seimbang antara kreatif dan konsisten
            max_tokens=150,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error Groq: {e}")
        return (
            "Maaf, sistem kami sedang sibuk. 😅\n"
            "Langsung saja hubungi admin kami di WA: 087887976070 agar segera dibantu."
        )

# --- TESTING (Opsional) ---
if __name__ == "__main__":
    print("Bot Subhan Service Aktif! (Ketik 'exit' untuk berhenti)")
    while True:
        tanya = input("User: ")
        if tanya.lower() == 'exit':
            break
        print(f"Bot : {get_bot_reply(tanya)}")