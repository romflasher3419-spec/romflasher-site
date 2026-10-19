::summary
Matrixx on the POCO X7 Pro is a fastboot flash, not a recovery zip, and the whole job comes down to order: back up, flash vbmeta first, then the ROM, then boot to recovery and format data once. Miss the vbmeta step and the phone just sits on the logo. Here is the exact sequence I use.

::body
You have been on the same ROM for a while, it works, but you keep reading about Matrixx and the amount of stuff you can change once it is running. It is Android 15, it is a short flash, and the POCO X7 Pro handles it easily. The risk here is not the length of the job. It is the order.

I will say the one thing that decides whether this takes twenty minutes or your whole evening. vbmeta goes first. It is an AOSP-based ROM, so the vbmeta image is flashed before the ROM package, with verity and verification disabled. Skip it, or flash it last, and the phone never gets past the boot logo.

## What you need before you start

- The Matrixx ROM package from the link below, built for the POCO X7 Pro.
- The vbmeta image for an AOSP ROM, from the downloads section.
- Platform tools on the PC, so adb and fastboot actually run.
- The ADB and Fastboot driver, so Windows sees the phone in fastboot mode.
- A recovery that matches this device.
- A full backup. Everything on internal storage goes.

## Step 1 - back up and accept the wipe

Copy your photos, downloads and anything else you care about off the phone. This ROM needs a data format, so the phone comes back empty. There is no dirty flash here if you are coming from stock.

If the bootloader is still locked, unlock it first. That wipes data on its own, so do it before you start caring about a backup.

## Step 2 - get the PC ready

Install platform tools and the ADB and fastboot driver. Then open a command window in the platform tools folder and run:

`fastboot devices`

With nothing plugged in you should get an empty line and no error. If it says fastboot is not recognized, the tools are not where the window is looking. Fix that now, not halfway through a flash.

## Step 3 - fastboot mode and a real serial number

Power the phone off. Hold Volume Down and Power until you see the fastboot screen. Plug it into the PC and run `fastboot devices` again.

This time it has to print a long serial number followed by the word fastboot. No serial number means the driver is the problem, and no amount of re-running the flash will fix it. Sort the driver out first.

## Step 4 - vbmeta before the ROM

Flash the vbmeta image first, with the disable-verity and disable-verification flags that come with the AOSP vbmeta file. Only after that do you send the Matrixx package.

If the package ships with a flash script, run the script rather than typing each partition command yourself. If you are writing the commands by hand, follow the order shown in the video exactly. The one rule that never changes: vbmeta first.

## Step 5 - recovery, then format data

When the images are written, reboot into recovery. Factory reset, then format data. That second one matters. A plain factory reset leaves the old encryption in place, and the phone loops because it is still trying to read the old data partition.

Do the format once, before the first boot attempt. If you let it try to boot, fail, and then go back and format, you are starting the whole job again.

## Step 6 - first boot and then leave it alone

Reboot to system. The first boot on a fresh custom ROM takes longer than a normal boot, and several minutes of a black screen with a boot animation is normal. Do not unplug anything and do not force a reboot. Wait for the setup wizard.

## Where this usually goes wrong

- **The vbmeta step.** Missing, or done after the ROM. The phone stays on the logo.
- **A recovery built for another device.** It seems to work and then the flash fails partway through.
- **Formatting data after a failed boot instead of before it.** You end up doing the whole flash again.

## The honest part

Matrixx is a community ROM, so give it a few days before you decide you are keeping it. Battery behaviour and one or two small features usually settle after a day of use, and the update channel is where the current bug list lives. Hold on to your backup until you are settled.

Going back is not a big deal either. An official fastboot ROM for your model, flashed from a PC, takes you back to stock. Nothing you do here is permanent.

If the driver side is the part that always slows you down, the free Rom Flasher tool on GitHub rolls the ADB and fastboot driver install into a couple of clicks, so you are not hunting through Device Manager. It is free, and the link is in the downloads section.

::faq
Q: Does Matrixx on the POCO X7 Pro need vbmeta?
A: Yes. It is an AOSP-based ROM, so you flash the vbmeta image before the ROM package, with verity and verification disabled. Leave it out and the phone will not get past the boot logo.

Q: Does flashing this ROM wipe my data?
A: Yes. You format data in recovery before first boot, so internal storage is reset. Move your photos and files off the phone before you start.

Q: Can I install Matrixx without a PC?
A: No. This is a fastboot flash, so you need a computer with platform tools and the ADB and fastboot driver installed.

Q: How do I go back to stock HyperOS afterwards?
A: Flash the official fastboot ROM for the POCO X7 Pro from a PC. It writes the full stock image and gets you back to a clean phone you can lock again.

Q: Is Matrixx stable enough to use every day?
A: For most people, yes, but it is a community build. Keep a backup, check the update channel for the current bug list, and give it a few days before you decide.
