# Instructions for agents populating this Name Trainer

Your job: fill this repo so the app teaches a **specific group of people**. When
you're done, opening `index.html` should show real faces, names, and bios for that
group. You only ever edit **`people.js`** and add image files to **`faces/`** — do
not touch `index.html`.

## What "done" looks like

1. `people.js` exports `window.PEOPLE` — one `{ name, img, bio }` object per person.
2. Every `img` path exists in `faces/` and shows the right person.
3. `window.TRAINER_TITLE` is set to the group's name.
4. `index.html` opens with no missing images and no console errors.

## Step 1 — Get the list of people

The human will point you at a source (a roster, an Airtable/Notion/Google Sheet, a
conference page, a CSV…). Extract, for each person:
- **name** (full display name)
- **bio material**: what they work on / study, role, and affiliation. 1–3 sentences
  is ideal. This is what **Bios mode** grades against, so make it substantive but
  concise. Strip junk/boilerplate.
- a **LinkedIn URL or other photo source** if available.

## Step 2 — Get a photo for each person

Save each photo as `faces/<slug>.jpg` where `<slug>` is the name lowercased with
every run of non-alphanumeric characters replaced by `_`
(`"Wyatt O'Brien" → wyatt_o_brien`). Square-ish images look best (the app crops to a
circle). 200–1000px is plenty.

Ways to get photos, roughly in order of preference:
- **LinkedIn (if the human is logged in via a browser-automation tool).** Open each
  profile and grab the profile photo. A robust trick: from a `linkedin.com` page,
  load each profile in a **same-origin iframe**, find the `img` whose `src` matches
  `profile-displayphoto|profile-framedphoto` with `naturalWidth > 80`, then
  `fetch()` that src and save the bytes. Two gotchas learned the hard way:
  - LinkedIn's CSP blocks `fetch`/iframes to `localhost`, and Chrome blocks
    multiple auto-downloads. To get bytes out of the page, stream them via a
    `window.open(...)` popup + `postMessage` to a tiny local receiver, or any
    channel that isn't blocked by the page's CSP.
  - A profile with **no photo** returns LinkedIn's default ghost avatar (often a
    small, identical-for-everyone file ~9–10 KB). Detect duplicates by hash and
    treat those as "no photo".
  - For people **not in the sheet's links**, LinkedIn people-search by name, then
    **disambiguate using their known affiliation/role** before accepting a face —
    never attach a guessed face, since a wrong face teaches a wrong association.
- **Other sources:** personal/academic site, GitHub avatar, conference speaker page,
  org "team" page. Verify identity before using.
- **Fallback avatar** when no real photo can be confidently found:
  `python3 scripts/make_avatars.py "Full Name"` → writes `faces/<slug>.png`.
  Use the `.png` path in `people.js`.

## Step 3 — Write `people.js`

```js
window.TRAINER_TITLE = "Acme 2026 Cohort";
window.PEOPLE = [
  { name: "Jane Doe", img: "faces/jane_doe.jpg",
    bio: "PhD student at MIT on mechanistic interpretability; previously SWE at Stripe." },
  { name: "John Smith", img: "faces/john_smith.png",   // png = generated avatar
    bio: "Policy researcher at the Institute for X, focused on AI governance." },
];
```

Rules:
- Keep strings **ASCII-safe** or properly escaped. In particular, real-world bios
  sometimes contain `U+2028`/`U+2029` line separators that are valid JSON but break
  inline JS — strip or escape them. (If you build this from Python,
  `json.dumps(s, ensure_ascii=True)` is the safe way to emit each string.)
- Every person should have a non-empty `bio` (Bios mode only quizzes people who do).

## Step 4 — Verify

- Open `index.html`; flip the top-left toggle to confirm both modes work.
- Good check for photo correctness: build a labelled contact-sheet montage of all
  `faces/` images (e.g. with Pillow) and eyeball that each face matches its name and
  nothing is broken.
- Report which people got real photos vs. generated avatars, and why (no photo on
  profile / couldn't confidently identify / no source).

## Notes

- The Bios-mode grader calls OpenRouter from the browser with the user's key
  (default model `openai/gpt-5.4-nano`). You don't need a key to populate data — it's
  only needed at quiz time, entered by the user.
- Don't commit anyone's API key.
