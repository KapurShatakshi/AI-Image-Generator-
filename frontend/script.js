const form = document.getElementById("promptForm");
const gallery = document.getElementById("gallery");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  gallery.innerHTML = "⏳ Generating...";
  const prompt = document.getElementById("promptInput").value.trim();
  const num = parseInt(document.getElementById("countSelect").value, 10);
  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, num_images: num }),
    });
    const data = await res.json();
    if (!res.ok) throw Error(data.detail || "Generation failed");
    gallery.innerHTML = "";
    data.images.forEach((b64) => {
      const img = document.createElement("img");
      img.src = `data:image/jpeg;base64,${b64}`;
      gallery.appendChild(img);
    });
  } catch (err) {
    gallery.innerHTML = `<p style="color:red">${err.message}</p>`;
  }
});
