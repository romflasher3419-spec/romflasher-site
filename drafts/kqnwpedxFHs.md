::summary
Lineage OS on the Redmi K50i does not come with Google apps, so a clean flash leaves you with no Play Store and no Google services. You fix that by flashing the ROM and a Gapps package back to back in the same recovery session, before the first boot. Miss that order and you are formatting data and starting over.

::body
You flashed Lineage OS, the phone booted, and now you are staring at a setup screen with no Play Store in sight. Nothing is broken. Lineage ships bare on purpose, and Google apps are a separate zip you flash yourself. That is the one thing people are not told, and it costs them an evening.

This guide is that missing half. The ROM download, the Gapps package, and the order that keeps you out of a wipe loop.

## What you need before you start

- Redmi K50i with an unlocked bootloader. Unlocking wipes the phone, so do it before you care about anything on the device.
- A custom recovery already installed and working. TWRP is the usual choice on this phone.
- The Lineage OS build for the K50i, and a Gapps package that matches the Android version of that build.
- Both files copied to internal storage before you touch recovery.
- 50% battery or better, a cable you trust, and a backup of your photos.

That last bullet matters more than it looks. This is a clean flash, so internal storage is going to be reset.

## Step 1 - get both files onto the phone

Download the Lineage OS zip and the Gapps zip. Move both to internal storage, in the top-level folder, where you can find them without hunting. Do not leave one on the PC. If you flash the ROM, reboot, and only then go looking for the Gapps file, you have already lost the session.

Check the Android version on the ROM filename against the Gapps package you picked. A Gapps zip built for a different Android release is one of the most common reasons a flash fails halfway.

Do not unzip either file. Recovery reads them as zips.

## Step 2 - boot into recovery and wipe first, not after

Power off, then hold Volume Down and Power to reach fastboot, and from there boot your recovery. Or use the recovery key combo if you have it on this device. You should land in TWRP with the touch working and internal storage readable.

If internal storage shows as zero, or touch does nothing, your recovery does not match this phone. Stop here and sort that out. Flashing on top of a broken recovery is how people end up with a phone that will not boot.

Now wipe. This is the clean install path:

- Wipe data, cache and dalvik.
- Format data if you are coming from MIUI or another custom ROM, and if encryption is still in place. Format data is the one that actually removes encryption, and no, a plain wipe does not do the same job.

Do the wipe now, before flashing. Wiping after you flash is pointless and confusing.

## Step 3 - flash the ROM, then Gapps, immediately

In TWRP, tap Install, pick the Lineage OS zip, and let it run to the end. Do not reboot.

Without leaving recovery, tap Install again and pick the Gapps zip. Flash it right now, in the same recovery session, before the system has ever booted.

This is the whole trick. Gapps needs to write into the system while it is still fresh, before the first boot sets up the system partition. Reboot in between and the second flash usually fails, and then you are wiping data and starting from step 2.

If your recovery lets you queue zips, queue them. If it does not, just tap back into Install after the first one finishes.

## Step 4 - first boot, and what it actually looks like

Reboot to system. The first boot on a clean Lineage flash is slow. Minutes slow, with a black screen or a spinning logo that does not move for a while. That is the system compiling and setting up, not a bootloop.

When the setup wizard appears, you will sign into your Google account and the Play Store will be there. If the Play Store is still missing, you flashed the ROM and skipped Gapps. Go back to recovery and do step 3 in one session.

## Where people get stuck

- **Rebooting between the ROM and Gapps.** This is the number one mistake. One recovery session, ROM first, Gapps second, then reboot once.
- **Wiping after flashing.** The wipe goes before, always. Doing it after just deletes what you installed.
- **Choosing the wrong Gapps build.** Match the Android version of the ROM. If it is not obvious, check before you flash rather than after.
- **Pulling the cable or holding power during first boot.** The screen can sit still for what feels like forever. Leave it.

## Do you need root?

No. Lineage runs fine without it, and this whole process is about getting a working daily phone, not about root. Root is a separate choice you can make later, and it is not required for the Play Store or for Google apps to work.

## Why Lineage feels different from MIUI

If you came from MIUI, expect a change in feel. Lineage is close to stock Android, so the launcher, the settings layout and the camera app are not the ones you had. The MIUI camera is gone. What you get instead is a lighter system that does not carry the extra layers Xiaomi ships.

That trade is the reason to flash it, and it is also the reason some people go back. Try it for a few days before deciding.

If the recovery and driver side of this feels like the annoying part, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks so you are not fighting Device Manager. It is free, and the link is in the downloads section.

One last thing. Get through the setup wizard and a full boot before you start restoring anything. If something is going to break, you want it breaking on an empty phone, not on top of a folder full of restored files.

::faq
Q: Does Lineage OS come with Google apps?
A: No. Lineage does not ship Google services or the Play Store. You flash a Gapps package yourself, in the same recovery session as the ROM, before the first boot. That is what the Gapps link is for.

Q: Do I flash Gapps before or after the ROM?
A: Right after the ROM, in the same recovery session, before you reboot. Flash Lineage first, flash Gapps second, then reboot once. Reboot in between and the Gapps flash normally fails and you have to wipe and start again.

Q: Will flashing this wipe my data?
A: Yes, on a clean flash. Moving from MIUI or another custom ROM means wiping data and formatting data. Copy your photos and downloads off the phone first, and expect the setup wizard on the first boot.

Q: Do I need to root the K50i for Lineage OS?
A: No. Root is optional and separate. Lineage boots and works fine without it, and Google apps do not need root either. You can add root later if you want it.

Q: Can I use this Lineage build on another Xiaomi phone?
A: No. The build here is for the Redmi K50i specifically. It is a MediaTek device, and builds from other phones will not boot on it. Keep the ROM and the device matched.
