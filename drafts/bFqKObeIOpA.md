::summary
OrangeFox Recovery is a touch recovery for the MI 11X, POCO F3 and Redmi K40 on Android 12. It replaces your existing recovery, flashes ROM zips, GApps and Magisk packages, and backs up your partitions — and you install it with one fastboot flash.

::body
If you flash ROMs at all, the recovery is the tool you touch most. Every zip, every backup, every wipe goes through it. So it is worth picking one that does not fight you at one in the morning when a flash has gone sideways.

OrangeFox is the one I keep coming back to. Full touch controls, it handles zip packages the way they are meant to be handled, and it asks before doing something destructive instead of assuming.

This is the Android 12 build, set up for the MI 11X and its POCO F3 and Redmi K40 twins. There is nothing exotic here. It is a recovery. It flashes things. The real question is whether it behaves reliably, and that is what you see on screen.

## What it actually does

- Replaces whatever recovery you are running now — flashing it overwrites the existing one.
- Flashes custom ROMs, GApps packages and Magisk zips.
- Backs up and restores partitions, including boot, data and system.
- Includes a built-in file manager, terminal access and USB OTG support.
- Handles the zip and ROM packages you would normally flash on this device.

## What it is not

- It will not unlock your bootloader. That happens first, on its own, before any of this.
- It will not rescue a corrupted firmware base or a hard brick by itself.
- It is not a ROM. Flashing OrangeFox does not change Android at all. Your system stays exactly what it was.

That last point confuses people who are new. A recovery sits next to Android, not instead of it.

## What you need

- An unlocked bootloader. Non-negotiable, and unlocking wipes the phone.
- Platform tools and the ADB and fastboot driver installed, so the PC sees the phone.
- The OrangeFox build for alioth, matching this Android 12 base.
- A USB cable that stays connected.

## What it looks like

The interface is touch, and it is built around large buttons rather than a wall of tiny text. The main screen greets you with the OrangeFox logo and a set of icons — install, backup, restore, wipe, mount, settings.

There is a theme engine, and yes, you can set a password so the recovery does not sit wide open. That is a small thing that matters more than it sounds if you keep the phone unlocked for flashing.

## Step 1 — check the build matches your device and base

Your device is alioth. The MI 11X, POCO F3 and Redmi K40 share that hardware, which is why one build serves all three. The Android 12 build is the one for a 12 base.

A recovery is tied to the Android version more than people expect. Flashing an Android 11 recovery onto a 12 system, or the other way round, is a reliable way to spend an evening confused.

## Step 2 — get into fastboot

Power the phone off. Hold **Volume Down + Power** until the fastboot screen appears. Plug it into the PC and confirm the connection with the devices command from platform tools.

If nothing shows up, that is the driver, not the recovery. Install the ADB and fastboot driver before going further.

## Step 3 — flash the recovery image

A recovery image is flashed to the recovery partition with a single fastboot flash command, with `recovery` as the partition and the image file as the target. Use the file you downloaded — read the name off the folder rather than retyping it.

It finishes in a second. That is normal.

## Step 4 — boot straight into recovery

Here is the one step people skip. Do not reboot to the system first. Use the command that reboots directly into recovery, or hold the button combination for recovery mode.

Booting the system first can let the phone overwrite the recovery you just flashed with the stock one. Then you sit there wondering why your new recovery vanished.

## Step 5 — set it up and take a backup

Once you are in, set your preferences and your password if you want one. Then take a full backup before you flash anything else.

That backup is the whole reason you installed this. Having it before the first ROM flash is the difference between a ten minute fix and a long night.

## Where people get stuck

- **Rebooting to system instead of recovery after flashing.** The stock recovery comes back and yours is gone. Boot directly into recovery the first time.
- **The wrong Android version.** The build has to match your base. A mismatch causes boot problems that look like a broken ROM.
- **Driver trouble in fastboot.** Nothing connects, so nothing flashes. Fix the ADB and fastboot driver before you blame the image.
- **Expecting it to unlock the bootloader.** It cannot. That has to be done first, and it wipes the phone when you do it.

## One honest paragraph

The free Rom Flasher tool on GitHub takes care of the ADB and fastboot driver install, and that is the step where most of these evenings actually go wrong. It is free, and the link is in the downloads section.

Everything above assumes one thing: your bootloader is already unlocked. If it is not, stop here and do that first. Nothing in this article works before it, and unlocking will erase the phone, so it is not something to do halfway.

Once that is done, the recovery takes about two minutes. Then it quietly does its job for months, which is the highest praise a recovery can get.

::faq
Q: Do I need root to flash OrangeFox Recovery?
A: No. Flashing a recovery image from fastboot does not need root and does not need the phone rooted afterwards. You do need an unlocked bootloader, which is a different thing entirely.

Q: Will OrangeFox replace my TWRP recovery?
A: Yes. Flashing it overwrites whatever recovery is currently installed. You cannot run both, and after the flash TWRP is gone unless you flash it back.

Q: Can I flash Android 12 ROMs with this OrangeFox build?
A: That is exactly what this build is for. It is the Android 12 version for the MI 11X, POCO F3 and Redmi K40. Match the recovery to your Android base to avoid boot problems.

Q: Why did my OrangeFox recovery disappear after rebooting?
A: You booted into the system instead of straight into recovery after flashing. The phone replaced it with the stock recovery. Flash it again and reboot directly to recovery the first time.

Q: Does flashing a recovery wipe my data?
A: No. Flashing the recovery image only writes the recovery partition. Your system and data stay as they are. Wiping is a separate step you choose inside the recovery.
