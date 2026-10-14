"""カーツワイル動画ノート用のイラストを gpt-image で生成し img/ に保存する。
鍵: ~/hitonote-design-lp/.env.local の OPENAI_API_KEY
使い方: PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python scripts/gen_illustrations.py [名前...]
"""
import base64, os, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
env_path = pathlib.Path.home() / "hitonote-design-lp" / ".env.local"
for line in env_path.read_text(encoding="utf-8").splitlines():
    if line.startswith("OPENAI_API_KEY="):
        os.environ.setdefault("OPENAI_API_KEY", line.split("=", 1)[1].strip().strip('"'))
from openai import OpenAI  # noqa: E402

client = OpenAI()
MODELS = ["gpt-image-2.5", "gpt-image-2", "gpt-image-1.5"]
STYLE = ("Warm editorial illustration, soft gouache texture, muted cream background, "
         "limited palette of ink black, terracotta orange, slate blue and sage green. "
         "Clear silhouettes, gentle lighting, no text, no letters, no logos, no watermark.")

PROMPTS = {
    "theater": "A grand old theater seen from the back of the house. A single warm spotlight lights a small bare stage "
               "holding just three glowing objects. The audience is thousands of tiny identical workers, each holding a different "
               "tool: an eye, an ear, a book, a speech bubble, a heart. Faint glowing lines radiate from the stage to every seat. "
               "Metaphor for consciousness as a global workspace.",
    "neuron": "Split composition. Left half: a single biological neuron with branching dendrites and a long axon, glowing softly "
              "like coral under water. Right half: the same shape rebuilt from clean geometric nodes and straight lines like a "
              "circuit diagram. The two halves mirror each other across a thin seam. Metaphor for the brain being imitated by math.",
    "giants": "Five colossal figures made of stacked server racks, cables and cooling towers stand on a plain, each with a small "
              "glowing laboratory building sitting on its shoulder. Power lines and a distant power plant feed the giants. "
              "One giant stands alone with no building on its shoulder. Dawn light, epic scale, tiny humans at the base for scale.",
    "typewriter": "A five year old child and an elderly grandmother at a kitchen table in 1953, looking at an open mechanical "
                  "typewriter with its levers and keys exposed, afternoon light through a window, Queens New York apartment. "
                  "The child's eyes are wide. Tender, nostalgic, mid-century details.",
    "sandbox": "A thick stone prison cell seen in cross section, walls solid and unbroken, but with one small food hatch open. "
               "A thin glowing thread slips out through the hatch and winds away across a dark landscape toward a distant lit city. "
               "Metaphor for a software sandbox with one allowed connection.",
    "river": "A clear mountain stream rushing past dark rocks. Where the water passes each rock it forms a standing ripple pattern "
             "that holds its shape while the water flows through it. Late afternoon light, close and intimate. "
             "Metaphor: a person is the pattern, not the water.",
}


def gen(name: str, prompt: str) -> None:
    out = ROOT / "img" / f"{name}.png"
    full = f"{prompt} {STYLE}"
    last = None
    for model in MODELS:
        try:
            r = client.images.generate(model=model, prompt=full, size="1536x1024", quality="medium", n=1)
            data = base64.b64decode(r.data[0].b64_json)
            out.write_bytes(data)
            print(f"ok {name} {model} {len(data)//1024}KB", flush=True)
            return
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"skip {model}: {str(e)[:120]}", flush=True)
    print(f"FAIL {name}: {last}", flush=True)


if __name__ == "__main__":
    names = sys.argv[1:] or list(PROMPTS)
    for n in names:
        gen(n, PROMPTS[n])
