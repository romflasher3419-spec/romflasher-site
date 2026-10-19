# Writer guide — Rom Flasher website articles

You are writing **one article** for each assigned video. The site is the written
half of the Rom Flasher YouTube channel. Goal: a page someone finds on Google,
reads top to bottom, and finishes with the job done.

**Language: English only.** No Hindi, no Hinglish, no Devanagari characters.

---

## Your task, exactly

1. Read `content/<videoId>.json`. It already has the title, device, ROM, the real
   links and the view count. Do not invent links and do not change them.
2. Write a draft file: `drafts/<videoId>.md`
3. Run: `python set_article.py "--id=<videoId>" "--file=drafts/<videoId>.md"`
4. If it prints warnings, fix the draft and run it again. Done only when it
   prints `[OK]`.

Work from this folder: `C:\Users\vrohi\romflasher-site`
Python is at `C:\Python315\python.exe`.

---

## Draft format — exactly these three sections

```
::summary
Two or three sentences that answer the search query immediately.

::body
## A real heading
A paragraph.

- a bullet
- another bullet

::faq
Q: A question a real person would type into Google.
A: A direct answer, two or three sentences.

Q: Another question.
A: Another direct answer.
```

Rules the checker enforces:

| part | length | count |
|---|---|---|
| summary | 80–600 characters | 1 |
| body | 1800–12000 characters | 1 |
| faq | — | 2–6 pairs (use 4–5) |

Aim for a body around **4,000–6,000 characters**. That is the sweet spot.

---

## Voice — the part that matters

Write like a friend who has already done this job and is telling you what to
watch out for. Not a manual. Not a spec sheet.

**Do:**
- Open with the situation the reader is actually in
  ("You flashed the ROM, it booted, and now the camera app crashes.")
- Say what breaks and why. Name the exact file, folder or menu.
- Use "you" and "I". Short sentences. One idea per line.
- Admit where something is fiddly or slow. That builds trust.
- Give one small reassurance where people panic.

**Do not:**
- No hype. No "ultimate", "insane", "game changer", "in 2026!".
- No filler like "In conclusion", "It is important to note that".
- No invented numbers, no made-up benchmarks, no fake version numbers.
- No promise that a method is safe or official when it is not.

---

## Hard bans (the checker rejects these)

Never write any of these, in any form:

- subscribe / bell / "hit like" / like this video / thumbs up
- comment below / let me know in the comments / share this video
- watch more / stay tuned / "2k subscribers"
- unlock code / paid app / premium app / locked app

The app is **free**. Say "the free Rom Flasher tool", never a price or a code.

---

## Structure that works

1. **Hook** (2–4 sentences) — the exact problem, in the reader's words.
2. **What you need** — a short bullet list, before any steps.
3. **The steps** — `## Step 1 —`, `## Step 2` … numbered headings.
4. **Where people get stuck** — 3 bullets of real failure modes.
4. **One honest paragraph** — what is annoying, or what changed in a recent build.
5. **FAQ** — 4–5 questions, real search phrasing.

Vary it. Some videos are a review, not a tutorial — then the structure becomes
what it looks like, what changed, what is broken, who should install it.

---

## Facts

Use only:
- the title and description in `content/<id>.json`
- the original description inside the batch file
  (`C:\Users\vrohi\.romflasher\batches\*.txt`)
- general, safe Android knowledge (fastboot, recovery, unlocking wipes data,
  vbmeta, boot images, OTA, Play Integrity)

If you do not know an exact number or file name, describe the step without it.
Never guess a filename into a step the reader will follow.

---

## Model to copy

`drafts/-n5Kb8536xs.md` is the approved sample. Read it once before you start.
Match that feel: warm, specific, no fluff, ends with something useful.

---

## Checklist before you say "done"

- [ ] `python set_article.py "--id=<id>" "--file=drafts/<id>.md"` printed `[OK]`
- [ ] English only, zero Devanagari
- [ ] No banned words anywhere
- [ ] Links untouched (they come from the JSON — the draft never changes them)
- [ ] The steps match the device and ROM in the title
- [ ] Nothing invented that a reader would act on
