::summary
Bliss OS on Android 13 is a GSI, so on the Xiaomi 11T Pro it installs as one system image over your existing vendor and kernel. Download the ARM64 AB or A64 AB build, flash vbmeta with verity and verification off, erase and flash the system image, then wipe data in recovery before the first boot. Miss the vbmeta flags or the data wipe and you will sit on a boot animation all evening.

::body
Here is the thing about flashing a GSI on the 11T Pro. You are not replacing Android. You are replacing one partition — the system partition — and leaving your vendor and kernel exactly where they are. That is the deal, and once you accept it, everything about this flash makes sense.

Bliss OS for Android 13 ships as a phh-treble style generic system image. The good part: nothing is listed as broken inside the ROM itself. The trade: how the camera, calls and sensors behave is your vendor's job, not the ROM's.

## What you actually need

- An unlocked bootloader. There is no way around this, and unlocking wipes the phone the first time.
- The **Bliss OS Android 13 GSI** for your device. ARM64 AB and A64 AB are both published.
- The **vbmeta** file for your phone, so you can disable verity and verification.
- **Platform tools** on your PC.
- A custom recovery, because the last step is a data wipe from recovery.
- A recent vendor and kernel on the phone. Older vendor blobs are where the camera complaints come from.

## Step 1 — get the right image and the right build type

Grab the Bliss OS Android 13 GSI. Two architecture variants are out: ARM64 AB and A64 AB. The 11T Pro is a 64-bit device, and you will almost always want the ARM64 AB image here.

On the build type: GApps and slim are what is available. Vanilla is not published for this one, so plan for Google apps being present. If you wanted a Google-free system, this is not the release that gives you one.

## Step 2 — boot to fastbootd, not plain fastboot

Power the phone off, hold Volume Down and Power to reach the bootloader, plug in the cable, and confirm the PC sees it:

`fastboot devices`

You should get a serial number back with the word `fastboot` next to it. No serial number means a driver problem, and nothing later in this guide will work until you fix that.

Then move into fastbootd:

`fastboot reboot fastboot`

This matters. The system partition can only be erased and written in fastbootd. If you try the next steps in the plain bootloader, the commands fail.

## Step 3 — flash vbmeta first, with both flags

This is the step people skip and it is the one that decides whether the phone boots.

`fastboot --disable-verity --disable-verification flash vbmeta`

Both flags matter. Verification is what stops a modified system image from booting. Leave it on and the phone rejects your GSI at boot with errors you cannot recover from without a PC. Flash the vbmeta for your phone before anything else.

## Step 4 — erase system, then flash the GSI

`fastboot erase system`

`fastboot flash system`

The image is large, so this takes a minute or two and prints progress. Let it finish. Do not unplug the cable, and do not close the window.

One small reassurance: a stalled-looking flash is usually just a slow USB port, not a brick. Give it a full two minutes before you assume anything went wrong.

## Step 5 — wipe data before the first boot

`fastboot reboot recovery`

In Mi Recovery, wipe data. This is not optional and it is not just housekeeping. The old userdata is encrypted with keys from the old system, so a new system partition plus old userdata is the classic GSI bootloop. Wipe it, reboot, and the first boot takes a while.

## What a GSI can and cannot fix

This is where expectations go wrong, so let me be blunt.

- **It cannot fix the camera.** GSI camera quality follows your vendor blob. If the vendor image on your phone is old, the photos will show it, and no GSI on the planet changes that.
- **It cannot fix calls or sensors.** Same story. Modem behaviour, fingerprint, proximity, all vendor side.
- **It can give you a clean, modern Android 13 base.** That part is genuinely good here, and the ROM side is documented and stable.

If your vendor is recent, you will wonder what the fuss is about. If it is old, you will notice within an hour.

## Where this usually goes wrong

- **Skipping the vbmeta flags.** Without `--disable-verity --disable-verification`, the GSI will not boot.
- **Flashing system in plain bootloader instead of fastbootd.** The command fails, or the partition never gets written.
- **Skipping the data wipe.** Old userdata plus a new system equals a bootloop, every time.
- **Blaming the ROM for hardware.** Camera, calls and sensors come from your vendor and kernel on a GSI.

## After the first boot

Set the phone up, let it settle for ten minutes, then start using it. If something hardware-related is off, that is your vendor talking, not the ROM. A recent vendor plus a current kernel is the answer there.

If the driver and platform tools side of this is the annoying part, the free Rom Flasher tool on GitHub installs the ADB and fastboot drivers in a couple of clicks so you are not fighting Device Manager. It is free, and the link sits in the downloads section.

One last thing. Turn off automatic system updates for a while. An OTA on a GSI can overwrite what you just flashed, and then you are doing this whole evening again.

::faq
Q: Do I need to wipe data to install a GSI on the Xiaomi 11T Pro?
A: Yes. The last step is a data wipe in recovery, and skipping it usually ends in a bootloop. Old userdata is encrypted with keys from the previous system, so a new system partition needs fresh userdata.

Q: Why do I need to disable verity and verification in vbmeta?
A: Verification blocks a modified system image from booting. Flashing vbmeta with both `--disable-verity` and `--disable-verification` turns that check off so your GSI can boot. Skip it and the phone rejects the image.

Q: Which Bliss OS Android 13 file should I download for the 11T Pro?
A: The ARM64 AB image. A64 AB is also published, but for this device the ARM64 AB build is the one you want. Vanilla is not available for this release, so take GApps or slim.

Q: Will the camera work properly on a Bliss OS GSI?
A: It will work, but quality depends on your vendor image. On a GSI the camera is downstream of your vendor blob, so an older vendor means visibly worse photos. A newer vendor and kernel helps.

Q: Can I go back to MIUI after flashing this GSI?
A: Yes. A fastboot ROM for your exact model flashed over the cable puts you back on stock MIUI. A full fastboot flash wipes everything, so back up first.
