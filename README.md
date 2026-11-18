# The World in One Page — 17 November 2026

Entry for the make.fun bounty **"Sum up 17 November's world news in one image"**
(`news-image-20261117`, $250, 50 places paid).

A newspaper front page for Tuesday 17 November 2026, drawn programmatically
with Python PIL (`render_image.py`) so every headline is exact and legible:

- **Lead:** Ukraine strikes the Crimea bridge — span collapses; Russia hits
  Kyiv bridges in reply.
- **Diplomacy:** Trump in Asia — Manila for ASEAN, then Shenzhen for APEC;
  trilateral nuclear talks with Xi and Putin set for Nov 19.
- **Middle East:** Hormuz on edge — Iran drones at the US radar in Bahrain
  intercepted; tankers hit mines; a third US carrier arrives.
- **Asia-Pacific:** Japan scrambles jets as suspected Russian aircraft
  violate its airspace.
- **Gaza:** UK sanctions Israeli settlement firms; West urges Israel to open
  Gaza aid crossings.
- **Yemen:** Houthis advance; government forces pull back to defend Aden.
- **Also:** Europe plans a Rwanda return hub for rejected asylum seekers;
  ULA Vulcan rocket fails, 40 Amazon satellites lost.

Sources: BBC, Reuters, AP, Just Security.

## How it works

`main.py` (Python 3.13, standard library only) copies `entry.png` — the
1024×1024 PNG rendered by `render_image.py` — to `/output/entry.png`.
The same bytes on every run; no network.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT. See `LICENSE`.
