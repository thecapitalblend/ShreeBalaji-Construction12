# 🏠 Vastu AI Architect — Expert Prompt Generator

Streamlit app jo aapke plot ke **dimensions** lekar 5 alag expert-level
AI prompts generate karta hai:

1. **2D Floor Plan** — Vastu-compliant room zoning ke saath
2. **3D Elevation / Render** — photorealistic exterior render prompt
3. **Structure (Column & Beam)** — IS 456 / IS 1893 based structural brief
4. **Rebar / Sariya Detailing** — bar diameter, spacing, shear/strength basis
5. **Home / Bangla / Villa Concept** — luxury bungalow/villa full brief

Har prompt India-specific Vastu texts (Mayamatam, Vishwakarma Prakash, etc.)
aur Structural IS Codes (IS 456, IS 875, IS 1893, IS 13920, SP 34) ka
reference leta hai.

### 🆕 Structurally-Aligned To-Scale 2D Layout Engine (v2)
AI text-to-image tools (Midjourney/DALL-E/etc.) room dimensions ka real
math check nahi karte, aur ek naive "row-slicing" approach bhi galat
nikla (columns row-to-row align nahi karte, bilkul jaisa ek real 30x50
bungalow plan me dekha gaya tha — Master Bedroom/Kitchen boundary ek
jagah, Pooja/Dining boundary kahi aur).

Isliye `layout_engine.py` me ab ek **shared structural grid engine** hai:
- Poore plot ke liye EK hi set of x-lines (West→East) aur y-lines
  (North→South) hoti hai. Har room in SAME lines se banta hai — isliye
  koi bhi do adjacent room ki common wall/column line hamesha ek grid-line
  par hogi (column continuity **mathematically guaranteed**, koi drift
  possible nahi).
- Har room ka width/height ek **Max Beam Span** limit (default 15 ft,
  editable) ke against check hota hai — exceed karne par warning milti
  hai ("intermediate column ya deeper beam chahiye").
- Column markers (C1 = perimeter, C2 = interior junction) automatically
  un exact points par draw hote hain jaha rooms milte hain — real column
  schedule jaisa.
- Default template ek corrected 30'x50' North-facing bungalow hai jisme
  entrance/parking North side par hai (facing se match), aur Vastu zoning
  (Pooja NE, Kitchen SE, Master Bedroom SW) sahi hai.
- Self-check panel dikhata hai: alignment PASS/FAIL + span warnings.

> ⚠️ Ye tool sirf AI-prompts / conceptual to-scale sketch banata hai —
> actual construction ke liye licensed Architect / Structural Engineer se
> verify zaroor karvayein.

---

## 🚀 Local Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Browser me `http://localhost:8501` khul jayega.

---

## 📦 GitHub Par Upload Kaise Karein

1. GitHub par naya repository banayein (e.g. `vastu-ai-generator`).
2. Is folder ke saare files (`app.py`, `prompts.py`, `requirements.txt`,
   `README.md`) us repo me upload/push kar dein:

```bash
git init
git add .
git commit -m "Initial commit: Vastu AI Architect prompt generator"
git branch -M main
git remote add origin https://github.com/<your-username>/vastu-ai-generator.git
git push -u origin main
```

---

## ☁️ Streamlit Cloud Par Deploy Kaise Karein (Free)

1. [streamlit.io/cloud](https://share.streamlit.io) par GitHub account se
   login karein.
2. "New app" par click karein.
3. Apna GitHub repo select karein (`vastu-ai-generator`).
4. Main file path: `app.py`.
5. "Deploy" par click karein — kuch minute me aapka app live ho jayega
   ek public URL par jise aap kahin bhi share kar sakte hain.

---

## 🛠️ Tech Stack

- Python 3.9+
- Streamlit (UI)
- Pure Python string templates (no external API key required)

## 📁 File Structure

```
vastu-ai-generator/
├── app.py             # Streamlit UI + 5 expert prompt templates + to-scale layout UI
├── layout_engine.py   # Code-based exact-math 2D layout generator (matplotlib)
├── requirements.txt   # dependencies
└── README.md          # ye file
```
