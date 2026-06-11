# Name Trainer

A tiny, single-file web app for learning the **names** and **what-they-do** of a
group of people (a team, cohort, club, conference, etc.). Open it in a browser —
no build step, no server.

![two modes: Names and Bios](#)

## Two modes (toggle in the top-left)

- **Names** — study each face + name, then drill yourself by typing names.
- **Bios** — you're shown a face + name and type what you remember about what the
  person does. A cheap model grades it ✓/✗ via [OpenRouter](https://openrouter.ai).
  Paste an API key in the box at the bottom of Bios mode (stored only in your
  browser's localStorage). Default model: `openai/gpt-5.4-nano`.

## Run it

Just open `index.html` in any browser (double-click it, or `file://…`).
It loads your data from **`people.js`** and photos from **`faces/`**.

## Make it yours

This repo ships with three sample people so it runs out of the box. To use it for
your own group, replace `people.js` and the images in `faces/`. The fastest way is
to **point a coding agent at this repo** — see [`AGENTS.md`](AGENTS.md), which tells
the agent exactly what to produce.

### Data format (`people.js`)

```js
window.TRAINER_TITLE = "My Cohort";          // optional heading
window.PEOPLE = [
  { name: "Jane Doe",
    img:  "faces/jane_doe.jpg",
    bio:  "PhD student at MIT working on mechanistic interpretability." },
  // …one object per person
];
```

- `img` can be a `.jpg` photo or a `.png` fallback avatar — both render the same.
- Convention: filename = the name lowercased with non-alphanumerics turned to `_`
  (e.g. `Jane Doe` → `faces/jane_doe.jpg`).

### Fallback avatars

For anyone you can't find a photo of, generate a clean initials avatar:

```bash
uv pip install pillow         # or: pip install pillow
python3 scripts/make_avatars.py "Jane Doe" "John Smith"
```

## License

MIT — see [LICENSE](LICENSE).
