::summary
Project Blaze OS on Android 12L runs on the Xiaomi 11T Pro as a GSI, so it installs as a single system image over your existing vendor and kernel. Only an ARM64 AB image is published, and there is no vanilla build, so take GApps or slim. Flash vbmeta with verity and verification off, erase and flash the system image, then wipe data in Mi Recovery before the first boot.

::body
This is the light version of a ROM review. One image, one flash, and the part that actually matters: how Project Blaze behaves once your vendor layer is in the mix.

Project Blaze on Android 12L is the base here, and it ships as a phh-treble style GSI. That means you are replacing the system partition and leaving the vendor and kernel alone. Once you understand that, the rest of this page is straightforward.

Device here is the Xiaomi 11T Pro.

## What a GSI actually means for your phone

Worth a minute, because it is the source of most disappointment with generic system images.

The ROM is the portable part. Android 13 or 12L, the launcher, the settings, the framework — all of that comes from the image you flash. The hardware support — camera, modem, sensors, fingerprint — comes from your phone's own vendor and kernel.

So when something hardware-related is off, the ROM is not the one to blame. That is your vendor. A recent vendor and kernel gives you far fewer surprises.

## What you need

- An **unlocked bootloader**. Required, and unlocking wipes the phone the first time.
- The **Project Blaze OS GSI** download. ARM64 AB is the only architecture published.
- The **vbmeta** file for your phone.
- **Platform tools** on the PC.
- A **custom recovery**, since the last step is a data wipe from recovery.
- A **full backup**. This wipes data.

## Step 1 — download the right image

Take the ARM64 AB image. It is the only one published for this release, so there is no guesswork and no A64 variant to pick between.

On build type: this release is GApps or slim. There is no vanilla build, so if you wanted a fully Google-free system, this is not the release for it.

## Step 2 — fastboot, and make sure the PC sees the phone

Power off, then hold Volume Down and Power to reach the bootloader. Plug in and run:

`fastboot devices`

A serial number with the word `fastboot` next to it is what you want. Nothing means a driver issue, and the flash will not work until you fix it.

## Step 3 — move to fastbootd

`fastboot reboot fastboot`

The system partition can only be erased and written in fastbootd. In the plain bootloader those commands fail.

## Step 4 — flash vbmeta with both flags

`fastboot --disable-verity --disable-verification flash vbmeta`

Both flags. This is the step that decides whether the phone boots at all. Leave verification on and the device rejects the modified system image at boot.

## Step 5 — erase and flash system

`fastboot erase system`

`fastboot flash system`

Give it a couple of minutes. The image is large, and a flash that looks slow is usually just a slow USB port. Do not unplug the cable and do not close the window.

## Step 6 — wipe data, then reboot

`fastboot reboot recovery`

Wipe data in Mi Recovery, then reboot. Step six is step six for a reason. Old userdata is encrypted with keys from the previous system, so new system on old userdata is the classic bootloop. If you skip one thing on this page, do not let it be this.

## The first look

Once it is up, the setup wizard runs and the phone settles. This is the cold boot and first setup part, and it is where you find out how the vendor layer is going to behave.

Have a look around. Check the things you use constantly first:

- The camera app, because on a GSI this is where vendor quality shows.
- Calls and mobile data, which depend on your modem firmware.
- The fingerprint sensor, which is vendor side.
- Bluetooth audio, since that catches people out.
- How the phone handles a heavy notification stack.

If those all behave, a GSI is usually a solid daily. If the camera looks soft or a sensor is flaky, that is your vendor, and the answer is a newer vendor and kernel rather than a different GSI.

## What is broken

Nothing is listed inside the ROM. That is worth saying plainly, because it is unusual. On the device side it depends entirely on your vendor and kernel, so results differ from phone to phone. Two people on the 11T Pro can have very different experiences and both be telling the truth.

## Where people get stuck

- **Skipping the data wipe.** The classic bootloop, and it is a step six problem every time.
- **Wrong architecture.** Only ARM64 AB is published here, so download that one.
- **Skipping the vbmeta flags.** Without both flags the GSI will not boot.
- **Blaming the ROM for hardware.** Camera, calls and sensors ride on your vendor and kernel, not the image.

## Honest notes

A GSI is portable and quick to swap. That is the appeal. Put it on, and if you do not like it, flash the next GSI over it without touching your vendor.

The cost is that the ROM cannot fix hardware, and you are always at the mercy of how recent your vendor is. If you have been meaning to update your vendor and kernel, do that before you judge this build.

If the driver side of the flash is the annoying part, the free Rom Flasher tool on GitHub handles the ADB and fastboot driver install in a couple of clicks. It is free, and the link is in the downloads section.

One last thing. Finish the setup wizard on an empty phone before restoring anything, so you find out what is broken before you have two hours of restored files on top of it.

::faq
Q: Which Project Blaze image should I download for the 11T Pro?
A: ARM64 AB. That is the only architecture published for this release, so there is no variant to choose between. Take GApps or slim, because there is no vanilla build.

Q: Do I have to wipe data when installing Project Blaze as a GSI?
A: Yes, and it is step six for a reason. Old userdata is encrypted with keys from the previous system, so skipping the wipe in Mi Recovery usually ends in a bootloop.

Q: Is there a vanilla Project Blaze build?
A: No. This release is GApps or slim only. If you want a Google-free system, you will need a different GSI that publishes a vanilla image.

Q: Is Project Blaze stable enough for daily use on a GSI?
A: Nothing is listed as broken inside the ROM. On the device side it depends on your vendor and kernel, so how well the camera, sensors and modem behave is decided by your phone, not the image.

Q: Do I need a specific vendor version for Project Blaze?
A: Not a specific one, but a recent vendor and kernel gives far fewer hardware surprises. An older vendor is where camera and sensor problems come from on any GSI.
