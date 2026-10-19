::summary
Lunaris AOSP v3.12 on the POCO X7 Pro (rodin) is an unofficial Android 16 build, and this page covers AnTuTu, Geekbench 6, a CPU throttle run and four games. Benchmarks give you a baseline. The throttle and sustained gaming runs are the part that tells you what it is really like to use.

::body
You found Lunaris AOSP v3.12 for the POCO X7 Pro and you want to know one thing before you flash it: does it stay good once the phone is warm, or does it only look good on a cool benchmark run. That is the question the numbers below actually answer.

This is an unofficial Lunaris AOSP build for rodin, on Android 16. It was built 19 September 2026 with a security patch from 17 September 2026. Everything here came off the device on the day, in one session, with no figures borrowed from anywhere else.

## What was tested

- AnTuTu — one clean overall run
- Geekbench 6 — CPU first, then GPU
- CPU throttle and stability — the part most reviews skip entirely
- PUBG Mobile — frame behaviour and heat over a match
- Call of Duty Mobile — sustained load on a heavier title
- Asphalt Legends Unite — GPU-heavy, in shorter bursts
- Free Fire MAX — the lighter, longer session
- Stability after the tests, not just during them

## How to read the scores

AnTuTu and Geekbench 6 give you a baseline for what Lunaris AOSP v3.12 can do on this hardware. That is their job. They are a ceiling, not a promise.

What people get wrong is treating the peak number as the daily number. You will basically never see peak performance in a real match, because by the time you are deep into a game the phone is warm, other apps are running, and the screen has been on for a while.

The CPU throttle run is the fix for that. It loads the chip continuously and shows how much of the peak survives once things heat up. Watch whether the drop is a gentle slope or a cliff. A slope means an hour of play feels consistent. A cliff means the first ten minutes feel great and then everything gets uncomfortable.

## What the games showed

The four games are there to cover the whole load range, not to give you one headline frame number.

- **PUBG Mobile** — the middle of the curve, and the best all-round test of how a match feels.
- **COD Mobile** — the heavier option, and the one that pushes heat fastest.
- **Asphalt Legends Unite** — GPU-focused, shorter bursts rather than a long grind.
- **Free Fire MAX** — the light end, where you can play a long session without the phone working hard.

Heat is the thread running through all four. A cool phone always performs better than a warm one, on this ROM or any other. So treat the results as a range, and judge the long sessions, because that is what you will actually do.

## The build details

- ROM: Lunaris AOSP v3.12, unofficial
- Device: POCO X7 Pro, codename rodin
- Android: 16
- Build date: 19 September 2026
- Security patch: 17 September 2026
- Credits: @rakmoparte and the Lunaris AOSP Team

It is a clean AOSP base, which is the appeal. No extra layer stacked on top of another layer, no folder of toggles you open once and forget. If you want a phone that behaves like plain Android, this is the shape of ROM you want.

## Who should install it

If you are on a POCO X7 Pro and you want Android 16 without the stock layer on top, this is a fair pick. It is a sensible choice for someone who prefers a tidy system over a feature-packed one.

If you want the extras that HyperOS gives you — the camera app, the specific gestures, the ecosystem pieces — you will miss them. An AOSP build is not a HyperOS replacement. It is a different phone experience entirely.

## Before you flash

- Unlocked bootloader, or nothing else here works.
- A full backup with your files copied off the device. Flashing wipes internal storage.
- A PC with ADB and fastboot working, plus the driver installed so the phone is seen in fastboot mode.
- The build is unofficial, so read the thread and the maintainer notes before you start. Things change between releases.

One thing worth knowing: the first boot on a fresh Android 16 install takes a few minutes. Sit with the logo instead of assuming the worst.

If the driver setup is the part that stops you, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is on this page.

::faq
Q: Is Lunaris AOSP v3.12 official for the POCO X7 Pro?
A: No. It is an unofficial Lunaris AOSP build for rodin, credited to @rakmoparte and the Lunaris AOSP Team. That is normal for many device builds, but it means you should read the maintainer notes before flashing.

Q: Do benchmark scores translate into daily use?
A: They are a ceiling, not a promise. The CPU throttle run and the long gaming sessions are the realistic part, because they show what is left once the phone is warm.

Q: Is Lunaris AOSP good for gaming?
A: It handles games in a normal range for this hardware, and the lighter titles hold a long session well. Heavy titles depend on how long you play and how hot the phone gets, which is true on any build.

Q: What Android version is Lunaris AOSP v3.12?
A: It is Android 16. This build was compiled on 19 September 2026 with a security patch dated 17 September 2026, so it is current for its release.

Q: Will flashing Lunaris AOSP wipe my phone?
A: Yes. Moving to a custom ROM formats internal storage, so copy everything you care about off the device first and expect the setup wizard on first boot.
