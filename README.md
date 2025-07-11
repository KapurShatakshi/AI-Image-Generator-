# AI Text-to-Image Generator 🖼️✨

Generate stunning images from natural-language prompts using state-of-the-art generative AI  
(DALL·E 3 or Stable Diffusion 2-1).

## ✨ Features
* 📜 Clean NLP pre-processing for better prompts  
* 🔌 Pluggable back-ends: OpenAI / local Stable Diffusion (🤗 Diffusers)  
* ⚡️ FastAPI async API (`POST /generate`)  
* 🖥️ Zero-build frontend – just open `frontend/index.html`  

## 🏃‍♂️ Quick Start

```bash
git clone https://github.com/KapurShatakshi/ai-text-to-image.git
cd ai-text-to-image/backend
cp .env  .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

Then open another terminal:

```bash
cd frontend
python -m http.server 8000
```

Visit <http://localhost:8000> and create some magic! ✨