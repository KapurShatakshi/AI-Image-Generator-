"""
AI Text-to-Image Generator – FastAPI backend.
Run with:
    uvicorn backend.app:app --reload
"""
from io import BytesIO
from base64 import b64encode
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import spacy

from .config import get_settings

settings = get_settings()
nlp = spacy.blank("en")

if settings.model_provider.lower() == "stability":
    from diffusers import StableDiffusionPipeline
    import torch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipe = StableDiffusionPipeline.from_pretrained(
        settings.sd_model, torch_dtype=torch.float16 if device.type == "cuda" else torch.float32
    ).to(device)
    def generate_image(prompt: str, n: int = 1) -> list[bytes]:
        images = pipe(prompt, num_images_per_prompt=n).images
        return [img.convert("RGB").tobytes("jpeg", "RGB") for img in images]
else:
    import openai
    openai.api_key = settings.openai_api_key
    def generate_image(prompt: str, n: int = 1) -> list[bytes]:
        resp = openai.images.generate(prompt=prompt, n=n, size="512x512", response_format="b64_json")
        return [img['b64_json'] for img in resp.data]

class PromptRequest(BaseModel):
    prompt: str = Field(..., example="A cyberpunk cat reading a newspaper at dawn")
    num_images: int = Field(1, ge=1, le=4)

class ImageResponse(BaseModel):
    images: list[str]

app = FastAPI(
    title="AI Text-to-Image Generator",
    description="Generate images from text prompts using DALL·E or Stable Diffusion",
    version="1.0.0",
)

@app.post("/generate", response_model=ImageResponse)
def generate(req: PromptRequest):
    doc = nlp(req.prompt.strip())
    clean_prompt = " ".join(tok.text for tok in doc)
    try:
        raws = generate_image(clean_prompt, n=req.num_images)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    b64_images = [b64encode(img).decode("utf-8") if isinstance(img, (bytes, bytearray)) else img for img in raws]
    return ImageResponse(images=b64_images)