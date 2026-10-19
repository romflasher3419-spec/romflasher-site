::summary
PixelExperience Plus on the Xiaomi Pad 5 runs Android 13 and flashes by sideload through recovery. The build is stable and SafetyNet passes. The one thing that decides whether you get a working tablet or a black screen is order: wipe first, then push the images and the zip.

::body
You want the Pad 5 to feel like a big Pixel — clean launcher, Google apps you actually use, none of the extra software Xiaomi piles on. PixelExperience Plus is the build I keep coming back to on this tablet for exactly that reason.

Sideloading it is not hard. It is just unforgiving about sequence. Skip the wipe at the start and you will be staring at a black screen wondering which step went wrong. Follow the order below and it boots the first time.

## What you need

- A PC with the ADB and Fastboot driver installed, so Windows can see the tablet.
- Platform Tools extracted on that PC, so you can run fastboot and adb from the folder.
- `boot.img` and `vendor_boot.img` pulled straight out of the ROM package. You need them as separate files, so keep the extracted zip around.
- The full ROM zip, untouched, ready to sideload.
- A charged tablet and a cable that holds a connection. This is not the place for the cable that only charges.

## Step 1 - get the images out of the ROM package

Open the ROM zip and copy out `boot.img` and `vendor_boot.img`. Leave the zip itself intact, because that is the file recovery will sideload later. If you unpack the zip into a folder and lose the zip, go back to the download.

## Step 2 - wipe before anything else

Boot the tablet to the bootloader and run:

`fastboot -w`

Do this first. Wiping after you flash is the single mistake behind most black screens on this device. The wipe clears the old system and the old data, and it gives the new build a clean surface to land on.

## Step 3 - flash the two boot images

Still in the bootloader, push the images:

`fastboot flash boot boot.img`
`fastboot flash vendor_boot vendor_boot.img`

Both must match the ROM package you downloaded. Do not mix images from an older build with a newer zip. If they do not match, the tablet is likely to hang on the boot animation.

## Step 4 - get into recovery

`fastboot reboot recovery`

Give it a moment. Recovery takes a few seconds to come up on the Pad 5. When you are in, confirm your PC still sees the tablet:

`adb devices`

You want a device serial and the word `sideload` or `device` next to it. If the list is empty, the driver or the cable is the problem, and sideloading will fail no matter how many times you retry.

## Step 5 - sideload the ROM

Tell recovery to wait for a package:

`adb reboot sideload`

Then push the zip you kept from step 1:

`adb sideload`

Followed by the ROM zip name or its full path. The transfer takes a while, and the percentage on screen is not always accurate. Do not touch the cable. If it stalls, it is almost always the connection, not the ROM.

## Step 6 - wipe data and reboot

When the sideload finishes, get a shell on the device:

`adb shell`

Then run:

`recovery --wipe_data`

That last wipe clears the data left behind by the flash. After that, exit the shell with `exit` and run:

`adb reboot`

The first boot on a clean flash is slow. Leave the tablet alone and let it work. Plugging something in or tapping the screen does not make it faster.

## Where people get stuck

- **Running the wipe after the flash instead of before it.** Wipe first, then push the images. This is the one that costs people an evening.
- **A cable that half-drops during sideload.** The transfer stops mid-way and you start over. Use a cable you trust and a port straight on the PC, not a hub.
- **Expecting a quick first boot.** On a clean flash it takes a while. That is normal on this build, not a failure.

## Notes from this build

SELinux is Enforcing, and SafetyNet passes, so banking and payment apps behave normally. The one thing to know is Xiaomi's keyboard and the pen will not work here unless you set SELinux to permissive. If you use the Pad 5 as a pen tablet, that is worth thinking about before you wipe MIUI off it.

For the driver and platform tools side, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install so you are not hunting Device Manager. It is free, and the link is with the others on this page.

::faq
Q: Which file do I sideload, the zip or the image?
A: The full ROM zip. You extract `boot.img` and `vendor_boot.img` from it and flash those two separately in fastboot, then sideload the same zip in recovery.

Q: Why does my tablet show a black screen after flashing PixelExperience Plus?
A: You almost certainly flashed before wiping. Run `fastboot -w` first, then flash the boot images, then sideload. Wiping after the flash is the usual cause of a black screen on this device.

Q: Does SafetyNet pass on this build?
A: Yes, SafetyNet passes, and SELinux is Enforcing. Banking and payment apps work normally. Only the Xiaomi keyboard and pen need SELinux set to permissive, and that is a separate choice you make.

Q: Do I need to flash vbmeta with PixelExperience Plus?
A: Follow the installation notes that come with the package. The steps above cover the boot and vendor_boot images the build needs, and you should not add extra files that are not part of the release.

Q: How long should the first boot take?
A: Longer than a normal reboot. On a clean flash the tablet has to rebuild its caches, so give it several minutes and leave it plugged in. If it is still on the boot animation after that, redo the wipe and sideload.
