::summary
Nusantara Project 4.7 Selarong is the official alioth build on an Android 12L base, and it stays close to clean Android with only the switches you actually use. This guide walks through the whole flash on the MI 11X, POCO F3 or Redmi K40, and covers what to prepare before you touch the bootloader.

::body
You have heard the name Nusantara on a forum thread, you have downloaded the zip, and now you are staring at a phone that still runs MIUI. This build is 4.7, the Selarong release, sitting on the Android 12L base. It is the official Nusantara drop for the alioth platform, so the MI 11X, POCO F3 and Redmi K40 all take the same file.

The reason people keep coming back to this ROM is simple. It stays close to clean Android and does not bury you in toggles. Every switch it adds is one you might actually flip once a week. That makes it a good pick if the big feature-stuffed ROMs feel like too much.

## What you need before you start

- An unlocked bootloader. Nothing here works until that is done, and unlocking wipes your data.
- A custom recovery already running. OrangeFox or TWRP both handle this zip.
- The Nusantara 4.7 Selarong zip built for alioth. Not another device's build, no matter how similar the name sounds.
- Firmware that matches the base this build expects. This is the step people rush and regret.
- A full backup of internal storage and a battery above 60%.

That firmware point deserves one more sentence. If you are jumping down from a much newer MIUI base, check before you flash. A mismatched firmware base does not fail loudly during the flash. It fails later, as random crashes and a camera that refuses to open.

## Step 1 — put the zip in internal storage

Download the ROM zip and leave it in the phone's internal storage. Do not park it on your PC and assume you will reconnect in time. Once you are in recovery, the cable connection may not be there when you need it.

## Step 2 — boot into recovery and take a backup

Before anything else, take a full backup. System and data. This is the step that turns a bad flash into a twenty-minute inconvenience instead of a lost evening.

## Step 3 — wipe data, cache and Dalvik

Clean flash is the safe route here. A new Android base under an old data set is asking for trouble, and wiping costs you nothing if you already backed up. Wipe data, cache and Dalvik in recovery.

## Step 4 — flash the ROM zip

Select the zip and let it run. Do not interrupt it. Recovery progress bars on this platform go quiet near the end, and that silence is not a hang.

## Step 5 — format data if the ROM asks

If the installer asks for a data format after the flash, do it. It is usually about encryption changing between the build you came from and this one. Skipping it is how people end up watching a boot animation loop.

## Step 6 — reboot and wait

The first boot takes a few minutes. Longer than you expect, especially on a clean install with an empty cache. Walk away from the phone and let it finish rather than tapping the screen to check on it.

## Step 7 — sign in and let it settle

Finish the setup wizard, sign in, and use the phone normally. Do not judge battery life on day one. The system is restoring apps and building caches. Give it a full day, then look at how it is draining.

## What you get with Nusantara 4.7 Selarong

The base is Android 12L, so you get the tablet-and-foldable-aware layout work Google did for that version, on a phone that mostly does not need it. Practical result: slightly better use of screen space in some apps, plus everything from Android 12 — the themed system colours, the updated notification shade, the privacy indicators.

Nusantara layers on top of that:

- A handful of useful extras — network traffic in the status bar, a customisation section for the status bar and lock screen, gesture options.
- Clean Android behaviour underneath. No reskinned notification shade, no MIUI account nagging.
- Stability as the priority. It is an official release for this platform, which means it got tested on alioth rather than assembled for it.

What it does not give you is a camera upgrade. Same hardware, same sensor. Expect the usual clean-Android camera experience.

## Where people get stuck

- **Flashing on a newer firmware base and blaming the ROM.** Random crashes, a warm phone, a camera that fails. Check the firmware recommendation in the release post first.
- **Forgetting the data format after the flash.** Bootloop. This is the most common one.
- **Grabbing a zip for a different device.** Alioth builds only. The three retail names share hardware, nothing else does.
- **Interrupting the first boot.** It is slow. Leave it alone.

## Who should install this

If you want official, close-to-AOSP, Android 12L on alioth and you do not need a ROM that throws every feature at you, this fits well. If you want heavy customisation or you depend on Xiaomi-specific camera processing, look elsewhere. And if your bootloader is still locked, sort that first — it wipes the phone, so do it before you spend time setting anything up.

The driver side of this is where a lot of people stall before they even reach recovery. The free Rom Flasher tool on GitHub puts the ADB and fastboot driver install into a couple of clicks so you are not fighting Device Manager. It is free, and the link is in the downloads section.

::faq
Q: Which devices can flash the Nusantara 4.7 Selarong build?
A: The MI 11X, POCO F3 and Redmi K40 all use the alioth platform, so the Nusantara 4.7 Selarong zip covers all three. A build made for any other device will flash successfully and then refuse to boot.

Q: Do I need to wipe data for this ROM?
A: Yes. Wipe data, cache and Dalvik for a clean flash. Coming from a different ROM or a different Android base, a dirty flash usually ends in crashes or a bootloop, and you cannot fix that after the fact.

Q: What Android version is Nusantara 4.7 Selarong?
A: It runs on the Android 12L base. That gives you the Android 12 feature set — themed colours, the updated notification shade, privacy indicators — plus the layout work Google did for large screens.

Q: Does the bootloader unlock wipe my data?
A: Yes, unlocking the bootloader wipes the phone. Do that before you set anything up or move files back, otherwise you will be unlocking and re-setting-up the phone twice.

Q: Does this ROM come with Google apps?
A: Check the release post for the build you download and flash GApps exactly the way it describes. Do not guess, and do not stack a package on top if the post does not ask for one.
