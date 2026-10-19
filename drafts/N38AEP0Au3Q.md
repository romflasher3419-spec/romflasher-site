::summary
YAAP OS on the POCO X7 Pro (Rodin) is an Android 16 build you flash from scratch using vendor_boot and ADB sideload. It is AOSP with the small fixes that make a phone nicer to live with, it is signed userdebug with SELinux enforcing, and strong integrity passes by default. Here is the flash and what you actually get.

::body
You have seen YAAP mentioned for the POCO X7 Pro and you want to know two things: is it stable enough to use, and what is the flash actually like. This is a first look at an Android 16 build, flashed from scratch, with the real steps and an honest read on what you get.

YAAP does not try to win a feature contest. There is no theme engine stacked on another theme engine, no folder of toggles you will open once and forget. It is AOSP with the small fixes that make a phone nicer to live with. If that sounds like the phone you want, keep reading.

## What is in this build

- Initial build of YAAP for this device
- Source synced with the latest upstream
- USB tethering fixed
- Firmware bumped to OS2.0.204.0.VOJMIXM, kernel at 6.6.56
- SELinux is enforcing
- Signed userdebug build, so it behaves more like a factory image than a weekend experiment
- Strong integrity passes by default
- GApps build, so the Play Store is already there
- Known issues: nothing listed. The maintainer asked for logs.

That integrity point matters more than people expect. Strong integrity passing by default is what decides whether your banking apps keep working after the flash. A lot of custom ROMs fail that check out of the box and you then spend an evening hunting for a fix. Here you do not.

The known issues line is worth reading plainly. The maintainer wrote that they want logs, so read this as a first build that is looking for testers, not a promise that nothing is broken. That is the normal deal with an early release.

## Before you start

- Unlocked bootloader. Nothing below works without it.
- A PC with ADB and fastboot working, and the driver installed.
- The YAAP ROM zip and the matching vendor_boot image.
- Your IMEI backed up somewhere outside the phone. Take a screenshot of it in settings and put it in your email or cloud storage.
- Your data copied off, because you are formatting.

## The flash, step by step

## Step 1 — download vendor_boot and drop it into platform tools

Put the vendor_boot image in the same folder as your fastboot and adb executables. Not in a subfolder. Keeping everything in one place is what stops the "command not recognised" moment before it happens.

## Step 2 — boot to fastboot and confirm the PC sees the phone

Power off, boot into fastboot mode, then check with your PC that the device is detected. If it is not, the driver is the problem and no amount of retrying will fix it. Sort the driver first.

## Step 3 — flash vendor_boot to all slots

Flash the vendor_boot image to both slots in one command. Both. This is not a step to trim, and a build that expects a matching vendor_boot will not boot cleanly without it.

## Step 4 — reboot and go straight into recovery

Reboot the phone and hold the recovery key combination immediately, the moment it restarts.

## Step 5 — do not use the fastboot reboot-to-recovery shortcut

This is the one real trap on this phone. On the POCO X7 Pro, the fastboot shortcut into recovery is the classic brick story. Reboot normally and hold the keys yourself instead. It takes one extra second and it keeps you out of trouble.

## Step 6 — format data in recovery

Format data, then go to Apply update and choose Apply from ADB.

## Step 7 — sideload the ROM zip

Run the adb sideload command and drag the ROM zip into the terminal window. Let it run to the end. Sideloading takes a while, and it looks like it has stalled when it has not.

## Step 8 — add GApps or Magisk while recovery is still open

Choose yes if you want GApps or Magisk. Doing it now, while recovery is open, saves you a second trip later.

## Step 9 — reboot to system and wait

First boot on a clean Android 16 install takes a few minutes. The logo will sit there. Do not panic and do not pull the cable.

## Where people get stuck

- **Skipping the vendor_boot step.** The build expects it, and flashing it to both slots is not optional.
- **Using the fastboot shortcut into recovery.** On this device that is the known way to land in trouble. Reboot and hold the keys.
- **Not checking the device before flashing.** Run the devices check first, every time. It costs nothing and it catches a missing driver before you have written anything.

## An honest note

This is a first build. It is tidy, it is signed, and integrity works, which is more than a lot of early releases manage. But the maintainer is asking for logs, and that tells you everything about where it is.

Keep your IMEI backup, keep your files somewhere else, and keep the ROM zip on your PC after you flash. If you ever need to go back over the same steps, having the exact zip you used saves you a download and a worry.

If the driver and fastboot side is the part that slows you down, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is on this page.

::faq
Q: How do I flash YAAP OS on the POCO X7 Pro?
A: Put the vendor_boot image in your platform tools folder, flash it to both slots in fastboot, then reboot and hold the recovery keys yourself. Format data in recovery, then sideload the ROM zip with ADB and reboot to system.

Q: Why should I not use fastboot reboot recovery on the POCO X7 Pro?
A: That shortcut is the classic brick story on this phone. Reboot normally instead and hold the recovery key combination the moment the phone restarts. It costs one second and keeps you out of trouble.

Q: Is YAAP OS stable on the POCO X7 Pro?
A: It is a first build. It is signed userdebug with SELinux enforcing, and it passed my run, but the maintainer is asking for logs, so treat it as an early release and keep your backup.

Q: Do banking apps work on YAAP OS?
A: Strong integrity passes by default on this build, which is the check that usually decides whether banking apps keep working. That is a good sign, though individual apps have their own rules.

Q: Do I need to flash vendor_boot?
A: Yes. This build expects the matching vendor_boot image, flashed to both slots, before the ROM. Skipping it is one of the common reasons a flash does not boot cleanly.
