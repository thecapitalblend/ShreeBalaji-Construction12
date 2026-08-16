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

### 🆕 Accurate To-Scale 2D Layout Generator
AI text-to-image tools (Midjourney/DALL-E/etc.) room dimensions ka real
math check nahi karte — labels aur actual drawn size mismatch ho sakta hai.
Isliye app me ek **code-based layout engine** (`layout_engine.py`) bhi hai
jo matplotlib se ek EXACT to-scale drawing banata hai:
- Rooms ko horizontal "rows" (strips) me arrange kiya jata hai.
- Har row ki height aur har cell ki width ko *ratios* se normalize karke
  actual feet me convert kiya jata hai — is wajah se sum hamesha
  plot ke width/length ke *exactly* barabar hota hai (guaranteed, no drift).
- Room list editable hai (Streamlit table) — apna khud ka layout bana sakte hain.
- Self-check panel dikhata hai ki dimensions match kar rahe hain ya nahi.

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
