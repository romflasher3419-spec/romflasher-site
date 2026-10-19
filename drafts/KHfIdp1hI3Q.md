::summary
Miku UI on the Redmi K50i is a generic system image, so you flash it in fastbootd and let your existing vendor and kernel do the hardware work. The order matters: flash vbmeta with verity off, erase system, flash the image, wipe data, then boot. Skip a step and you get a bootloop, not a working phone.

::body
Miku UI is one of those Android projects with a personality of its own. On the Redmi K50i it runs as a generic system image, Android 13 base, phh-treble, ARM64 AB. In plain terms: the ROM half is Miku UI, the hardware half is whatever vendor and kernel are already on your phone. So how the camera, calls and sensors feel depends on what you had before, not on the image itself.

That is the one thing to understand before you start. A GSI does not bring its own drivers. It sits on top.

## What this build is

- Android version: 13.0
- ROM type: generic system image
- Device target: phh-treble
- Architecture: ARM64 AB
- Two flavours: a version with Google apps baked in, and a vanilla one
- SELinux on either setting works, enforcing or permissive
- Maintainer: @xiaoleGun

The maintainer reports no bugs inside the ROM yet, and asked to be told if any show up. Device-side issues are the ones to expect, and those come from your vendor and kernel, not from Miku UI.

## What you need first

- Platform Tools on the PC, with fastboot actually seeing your phone.
- An unlocked bootloader. That is the entry ticket, and unlocking wipes the phone.
- The Miku UI system image, either the version with Google apps or the vanilla one.
- The vbmeta image from the link in the downloads section.
- A backup. This flash wipes data, and there is no undo.
- A cable you trust and a battery above half.

## Step 1 - get fastboot seeing the phone

Install Platform Tools, open a command window in that folder, and check the tools respond. Boot the K50i into fastboot with Volume Down and Power, plug it in, and run `fastboot devices`. You want a serial number and the word `fastboot` on the same line.

No serial number means a driver problem. Fix that now. It will not fix itself halfway through the flash.

## Step 2 - move to fastbootd

Miku UI is a system image, and system lives in the dynamic partition. Normal fastboot cannot touch it. You need fastbootd for that, which is the userspace fastboot inside recovery.

From the bootloader, run:

`fastboot reboot fastboot`

The screen changes to a fastboot UI driven by the recovery. If `fastboot devices` still lists your phone here, you are in the right place.

## Step 3 - flash vbmeta with verification off

This is the step that decides whether the phone boots or loops. Flash the vbmeta image with verity and verification disabled:

`fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img`

Do not skip this and do not flash a vbmeta from another build. A mismatched one is a black screen with extra steps.

## Step 4 - erase system

`fastboot erase system`

Erase takes a moment. If it fails, you are almost certainly not in fastbootd, or the partition is busy. Go back to step 2 and check where you are.

## Step 5 - flash the Miku UI image

Now flash the image you downloaded. If it is a sparse image split into chunks, flash every chunk in order. Then confirm it landed:

`fastboot flash system <the-image-you-downloaded>`

If your download is a plain image file, that is the one fastboot wants. Nothing else goes here.

## Step 6 - wipe data in recovery, then boot

Reboot to recovery. On the K50i that is the stock Mi Recovery, which is fine for this. Wipe data there, not just cache. Then choose reboot to system.

The first boot on a GSI takes a while. It patches and settles before it shows you the setup screen. Give it a few minutes before you decide it is stuck.

## Where people get stuck

- **Flashing system in bootloader fastboot.** It simply does not work there. You must be in fastbootd. The error is usually about the partition not being found, which sends people looking for the wrong problem.
- **Skipping vbmeta.** The phone boots once and then loops, or refuses to start at all. Flash it with verity and verification disabled and do it before you erase system.
- **Dirty flashing over another GSI.** Do not. Erase system and wipe data, every time. Carrying old data into a new GSI is the single most common cause of a bootloop.

## Honest notes

A GSI is a trade. You get a fast, clean Android 13 with Miku UI's look, and you keep whatever camera and kernel behaviour your phone already had. That means a bug you see might not be Miku UI at all, which makes forum hunting harder. Start from a clean stock base if you can, because that gives the image the best vendor to sit on.

If the driver side of the PC setup is the part you dread, the free Rom Flasher tool on GitHub packages the ADB and fastboot driver install into a few clicks, so you are not reading Device Manager at midnight. The link is in the downloads section.

One quiet reassurance: flashing system over a bad attempt is not the end of the phone. Boot back to fastbootd and do the order again, slowly. The steps above are less fragile than they look.

::faq
Q: Why does my Redmi K50i bootloop after flashing the Miku UI GSI?
A: Almost always vbmeta or data. Flash vbmeta with verity and verification disabled before you erase system, and wipe data in recovery after the flash. Skipping either one leaves the phone on the boot animation.

Q: Do I need fastbootd to flash a GSI on the Redmi K50i?
A: Yes. System lives in the dynamic partition, so bootloader fastboot cannot write it. Run fastboot reboot fastboot from the bootloader to reach the userspace fastboot, then erase and flash system there.

Q: Should I use the GApps build or the vanilla Miku UI image?
A: Take the GApps build if you want Google apps already in place, since a GSI is a system image and you cannot simply flash a Gapps zip over it. Take vanilla if you do not want Google services on the phone.

Q: Is a custom recovery needed for this flash?
A: Not to flash the image. The steps run through fastboot and fastbootd, and the stock Mi Recovery is enough for the data wipe. A custom recovery is optional here.

Q: Do I lose my data flashing Miku UI on the K50i?
A: Yes. You wipe data as the last step before booting, and that clears internal storage. Copy your photos and anything else you care about off the phone first, and expect the setup screen on first boot.
