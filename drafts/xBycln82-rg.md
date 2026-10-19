::summary
Pixel Experience on the MI 11X gives you a clean Pixel-style Android build with the Google apps already inside, so there is no separate GApps zip to flash. This guide covers the full install on alioth — MI 11X, POCO F3 and Redmi K40 — plus an honest look at the launcher, camera and battery once it boots.

::body
You want your MI 11X to stop feeling like MIUI and start feeling like a Pixel. No clutter launcher, no twenty toggles buried in a menu, no apps you never asked for. Pixel Experience is usually the ROM people get pointed to first, and on alioth it is a genuinely different phone once it boots.

This article is two things at once. First the install, in the order that actually works, because alioth is fussy about a few steps. Then the honest part — what you are left with after the setup wizard, and whether it still deserves to be your daily ROM.

## What you need before you touch anything

- An unlocked bootloader. There is no path around this, and unlocking wipes your data the moment it happens.
- A custom recovery already running on the phone. OrangeFox and TWRP both do the job here.
- The Pixel Experience zip built for alioth. This exact build, not one for another Xiaomi device.
- No GApps package. Pixel Experience includes the Google apps already, and stacking a second set on top causes problems.
- Firmware that matches what the build expects. If you are coming from a much newer MIUI base, slow down and check.
- A full backup of your internal storage, plus a battery above 60%.

## Step 1 — back up before anything else

Boot into recovery and copy everything you care about to a PC or a drive. Photos, downloads, chat backups, the lot. You are going to wipe data later, and after that there is no getting it back. I have watched people skip this because the ROM "usually works" and then spend the evening trying to recover files from a phone that will not boot.

## Step 2 — copy the ROM zip into internal storage

Put the zip in the phone's internal storage, not on your PC. You will not have a working cable connection once you are in recovery on every setup, and hunting for a file that lives on the wrong machine is a silly way to lose ten minutes.

## Step 3 — wipe data, cache and Dalvik

In recovery, wipe data, cache and Dalvik. This is a clean flash and it is the right call when the ROM sits on a new base. Do not skip it because you are upgrading from an older Pixel Experience build — the data format step later matters more than you think.

## Step 4 — flash the ROM zip and let it finish

Flash the zip and then keep your hands off the phone. The recovery will print progress and then go quiet for a bit at the end. That pause is normal. Do not tap reboot the second the bar looks stuck.

## Step 5 — format data if the ROM asks for it

Pixel Experience builds on this hardware often want a data format after the flash. If the installer asks, do it. Skipping it is the single most common reason people end up in a bootloop staring at the boot animation for twenty minutes.

## Step 6 — reboot and wait out the first boot

The first boot on alioth is slow. Give it several minutes before you start worrying. When the setup wizard finally appears, sign in and let the phone settle.

## Step 7 — give it a day before you judge battery

Do not decide the ROM drains too fast in the first three hours. The phone is indexing, restoring and downloading. Use it normally for a full day, then look at the numbers.

## What it looks like once it boots

The launcher is the Pixel launcher, and that is the whole point. At a glance, clean app drawer, no MIUI folder soup. The settings app looks like a Pixel settings app. Notifications behave normally. If the thing that bothered you about MIUI was how much of it there was, this is the fix.

## What actually changed

- **The feel.** Lighter, less busy, and faster to navigate once your apps are installed.
- **The camera.** Expect the stock camera experience, not a Xiaomi camera improvement. The hardware does not change because the ROM did. On alioth the camera is usable but it is not where this ROM wins.
- **Battery.** Roughly in line with other clean Android builds on this chipset. It is not a magic upgrade, and anyone promising one is selling something.
- **Google apps.** Already inside. Sign in and go.

## Where people get stuck

- **Flashing an alioth build on a phone that is not alioth.** It will not boot. The MI 11X, POCO F3 and Redmi K40 share hardware — a build for anything else does not.
- **Skipping the data format.** Bootloop. Every time.
- **Adding a GApps zip on top.** The ROM already includes Google apps. A second package fights with the first one and you get crashes, not extra features.
- **Using a recovery that is too old for the zip.** If the flash fails at the start, update your recovery before you blame the ROM.

## Who should install it

If you want a Pixel-style experience without buying a Pixel, this is the ROM to try. If you need MIUI's camera processing or you rely on Xiaomi-specific features, stay where you are. And if you have never flashed anything before, follow every step slowly rather than skipping the boring ones — the boring ones are the ones that save you.

One last note. If the driver side of flashing is what usually stops you, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks, so you are not hunting through Device Manager at midnight. It is free, and the link is in the downloads section.

::faq
Q: Does Pixel Experience include Google apps?
A: Yes, they are built into the ROM. Do not flash a separate GApps package on top — it fights with the ones already there and causes crashes rather than adding anything useful.

Q: Will the camera get better after flashing Pixel Experience?
A: No. The sensor and the hardware do not change because the software did. You get a clean camera app on the same hardware, which on the MI 11X is usable but not a reason to flash this ROM.

Q: Which devices does this alioth build work on?
A: The MI 11X, POCO F3 and Redmi K40 all share the alioth platform, so the same zip covers all three. A build for any other device will flash and then fail to boot.

Q: Do I need to format data after flashing?
A: If the installer asks you to, yes. Skipping the data format is the most common cause of a bootloop on a clean flash, especially when you are coming from a different ROM or a different Android base.

Q: Is Pixel Experience still worth installing on the MI 11X?
A: If you want the Pixel look and a clean Android build, yes — it is a solid daily driver on this hardware. What it is not is a performance or camera upgrade. Flash it for the experience, not for a benchmark.
