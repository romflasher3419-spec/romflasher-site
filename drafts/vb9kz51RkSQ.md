::summary
Spark OS on Android 13 runs on the Xiaomi 11T Pro as a GSI, and the flash itself is short: platform tools, fastbootd, vbmeta with verity and verification off, erase and flash the system image, then wipe data. The important half comes after the first boot, where a handful of toggles decide whether calls, the always-on display and the camera API behave properly. Skip the settings and the ROM feels half-finished.

::body
Most GSI guides stop when the phone boots. That is the easy part on the 11T Pro. What makes Spark OS worth writing about is the ten minutes after that first boot, where you go through a set of toggles. Skip them and the ROM feels unfinished. Do them and it feels like a real daily driver.

So this page is in two halves: the flash, then the setup.

Device here is the Xiaomi 11T Pro. ROM is Spark OS on Android 13, flashed as a GSI.

## What you need

- **Platform tools** on the PC, so adb and fastboot are available.
- The **Spark OS Android 13 GSI** for your phone.
- The **vbmeta** file, because you will flash it with verity and verification disabled.
- A **custom recovery**, since the last flash step is a data wipe from recovery.
- A **full backup**. This wipes data, no exceptions.
- An unlocked bootloader, which wipes the phone the first time you do it.

## Step 1 — boot to fastboot and confirm the PC sees the phone

Power the phone off. Hold Volume Down and Power until the bootloader screen appears. Plug in the cable and run:

`fastboot devices`

You need a serial number back with the word `fastboot` next to it. Nothing there means a driver problem, and no amount of retrying the flash will fix that. Sort it out now, not in the middle of writing the system partition.

## Step 2 — switch to fastbootd

`fastboot reboot fastboot`

The system partition can only be written from fastbootd, not the plain bootloader. If the next commands fail, this is almost always why.

## Step 3 — flash vbmeta with both flags

`fastboot --disable-verity --disable-verification flash vbmeta`

Both flags matter. Verification is the check that stops a modified system image from booting. Leave it enabled and your GSI is rejected at boot. Do this before you touch the system partition.

## Step 4 — erase and flash the system image

`fastboot erase system`

`fastboot flash system`

The image is big, so give it a couple of minutes and let it print progress. Do not unplug the cable and do not close the window. A flash that looks stuck is usually a slow USB port rather than a real failure.

## Step 5 — reboot to recovery and wipe data

`fastboot reboot recovery`

In recovery, wipe data. This is not housekeeping. Old userdata is encrypted with keys from the previous system, so a new system partition on old userdata is a guaranteed bootloop. Wipe, then boot.

## Step 6 — work through the settings after first boot

This is the part most guides skip. Once the phone is up, go through the setup and then handle these:

- **Network and call behaviour toggles.** These decide whether calls behave properly. If calls are flaky, come back here first.
- **Screen brightness slider and force alternative options.** The brightness handling on a GSI often needs a nudge.
- **Skin and mode picks.** Which look and which mode the ROM runs in.
- **Camera2 API.** Turning this on is what lets third-party camera apps work properly.
- **A2DP**, for Bluetooth audio behaviour.
- **The always-on display toggle.** Off by default in some setups, and it is easy to think the ROM does not have it.
- **Qualcomm feature options**, including an alternative camera profile if you want one.

Take your time here. Ticking these in a hurry and then wondering why Bluetooth audio sounds wrong is a wasted evening.

## One good surprise

On this flash, the device showed up **certified**, with no extra patching needed. Google Photos gave limited backup, which is normal, but certification being there out of the box is a nice break from the usual.

Theme customisation is also present, including black and transparent looks, if that is your thing.

## Where people get stuck

- **Skipping the vbmeta flags.** Without both `--disable-verity` and `--disable-verification`, the GSI will not boot.
- **Flashing system from the plain bootloader.** It has to be fastbootd, or the erase and flash do nothing useful.
- **Skipping the data wipe.** New system plus old userdata equals a bootloop, every time.
- **Ignoring the post-boot settings.** Then blaming the ROM for calls, Bluetooth audio or camera apps not working.

## Something honest about GSIs

Your vendor and kernel decide half of what this ROM can do. The image side is clean, but if the camera or a sensor is off, that is your vendor talking. A recent vendor and kernel gives far fewer surprises, and no GSI on earth changes that.

If the driver and platform tools part is what puts you off, the free Rom Flasher tool on GitHub handles the ADB and fastboot driver install in a couple of clicks. It is free, and the link is in the downloads section.

One last thing. Finish the settings pass before you restore apps. You want to know the ROM is behaving on an empty phone first.

::faq
Q: Why do calls not work properly after flashing a GSI on the 11T Pro?
A: Usually a settings toggle, not the ROM. Spark OS needs the network and call behaviour toggles enabled after the first boot. Check those before you assume the build is broken.

Q: Do I need to flash vbmeta when installing Spark OS?
A: Yes, and with both flags: `--disable-verity` and `--disable-verification`. Verification blocks a modified system image, so without those flags the GSI will not boot.

Q: Why is my camera app not working on Spark OS?
A: Turn on the Camera2 API in the post-boot settings. Many third-party camera apps rely on it, and it is off by default. There are also Qualcomm feature options, including an alternative camera profile.

Q: Is Spark OS certified on the Xiaomi 11T Pro?
A: On this flash it showed up certified without extra patching, which is unusual for a GSI. Google Photos still gave limited backup, which is what you would expect.

Q: Do I have to wipe data after flashing Spark OS?
A: Yes. The wipe happens from recovery as the last step of the flash. Skip it and you will see a bootloop, because old userdata is encrypted with keys from the previous system.
