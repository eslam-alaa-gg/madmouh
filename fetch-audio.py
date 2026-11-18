from pathlib import Path
from urllib.request import urlopen
import json

audio_url = "https://sadakah-58j1.vercel.app/surah-ya-sin.mp3"
metadata_url = "https://sadakah-58j1.vercel.app/assets/audio/quran/metadata.json"

try:
    audio_bytes = urlopen(audio_url, timeout=120).read()
    metadata = json.loads(urlopen(metadata_url, timeout=30).read().decode("utf-8"))

    audio_dir = Path("assets/audio/quran")
    surah_dir = audio_dir / "surah"
    surah_dir.mkdir(parents=True, exist_ok=True)
    (surah_dir / "surah-ya-sin.mp3").write_bytes(audio_bytes)

    for item in metadata.get("audio", []):
        item["src"] = "assets/audio/quran/surah/surah-ya-sin.mp3"
        item["reader"] = "قارئ القرآن الكريم"

    audio_dir.mkdir(parents=True, exist_ok=True)
    (audio_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    page = Path("index.html")
    html = page.read_text(encoding="utf-8")
    html = html.replace(audio_url, "assets/audio/quran/surah/surah-ya-sin.mp3")
    page.write_text(html, encoding="utf-8")
    print("Quran audio bundled locally:", len(audio_bytes), "bytes")
except Exception as error:
    print("Audio bundle unavailable; keeping remote audio fallback:", error)
