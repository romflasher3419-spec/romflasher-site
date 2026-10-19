::summary
crDroid 12.3 is the official Android 16 build for the Xiaomi Pad 5. You flash the vendor image from the bootloader, boot to recovery, factory reset, then sideload the ROM zip. It is a Vanilla build with no Google apps, and because it is official you get OTA updates afterwards.

::body
crDroid 12.3 for the Pad 5 being official matters more than it sounds. You get proper OTA support, so if you are on an older crDroid build the update gets pushed to you and it is worth taking it the same way — through the updater rather than a full reflash.

This build is Vanilla, meaning no Google apps baked in. If you want the Play Store and the rest, you add them yourself. Nothing wrong with that, but do not finish the flash and then wonder why the tablet came up without them.

The changelog is mostly audio work: more fine tuning, mic path refinement, and the tablet moving to a newer audio and effects HAL. A surfaceflinger setting was removed that could cause jitter during scrolling and animation. Small on paper, but it is the kind of cleanup you feel in daily use.

## What you need

- An unlocked bootloader on the Xiaomi Pad 5.
- An adb and fastboot tool plus the correct driver, so the PC sees the tablet.
- The crDroid 12.3 ROM file and the matching vendor image.
- Optionally the Adreno driver, which the build notes suggest pairing for a smoother experience.

The vendor image has to match the build. Flashing the wrong one is one of the three ways people break this install.

## Step 1 - connect and boot to the bootloader

Open your adb and fastboot tool and connect the Pad 5. Reboot to the bootloader from the tool itself — no button combo needed. That is easier than the volume key dance, and it removes one place to make a mistake.

Confirm your PC sees the tablet before you go further. If the device list is empty, the driver or the cable is the problem, and the flash will not start.

If the driver is the part that always slows you down, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install so you are not fighting Device Manager. It is free, and the link is with the others on this page.

## Step 2 - flash the vendor_boot file

Still in the bootloader, flash the vendor_boot file from the release you downloaded. Match it to the exact build. Do not mix a vendor image from an older crDroid release with a newer ROM zip, because that combination boots to a logo and stays there.

## Step 3 - boot to recovery and factory reset

Boot to recovery and do a factory reset before you sideload anything. This is the step that decides between a smooth boot and a bootloop. It takes a minute and it is not optional on a clean flash.

## Step 4 - sideload the ROM

Choose apply update from ADB in recovery, then sideload the crDroid zip from your PC. The transfer takes a while, and the percentage on screen is not always accurate. Do not touch the cable. If it stalls, it is almost always the connection rather than the file.

## Step 5 - say no to extras and reboot

During the install you get asked about extra root and Gapps. For a clean install, say no to both. You can add them later once the ROM is booting properly, and that keeps the first boot simple to read if something goes wrong. Then reboot to system.

## Step 6 - let the first boot finish

The first boot on a clean flash is slow. Leave the tablet alone and let it work. Do not set anything up while it is still settling.

## Where people get stuck

- **Not factory resetting first.** This is the number one cause of a bootloop here. Reset, then sideload.
- **Flashing the wrong vendor image.** It has to match the build, not just the device.
- **Assuming it ships with Google apps.** It is the Vanilla build. Google apps are a separate install, and there is nothing broken about the tablet coming up without them.

## One honest note

If you are already on an older crDroid build, use the updater rather than a full clean flash. The release notes recommend upgrading the same way, and it saves you the wipe. A clean flash is for when you are coming from another ROM entirely, or when the smaller upgrade path misbehaves.

The suggested Adreno driver is worth trying if animation and scrolling are the things you notice most. It is listed as optional, so treat it that way and add it after the ROM has booted properly.

## Who should install it

Install it if you want an official Android 16 build with OTA support and you are fine adding Google apps yourself. Skip it if staying on the Vanilla build does not suit you, or if you would rather wait for a build with more of the extras included.

::faq
Q: Is crDroid 12.3 on the Xiaomi Pad 5 official?
A: Yes, it is the official build. That matters because official builds get OTA updates, so future versions arrive through the updater instead of a manual flash.

Q: Does crDroid 12.3 come with Google apps?
A: No. It is the Vanilla build, so there are no Google apps baked in. You install them yourself if you want the Play Store and the rest.

Q: Why does crDroid bootloop on my Pad 5?
A: You most likely skipped the factory reset before sideloading. Boot to recovery, do a factory reset first, then apply the update from ADB. That order is the difference between a smooth boot and a bootloop.

Q: When I flash crDroid, should I add root and Gapps?
A: For a clean install, say no to both and add them later once the ROM boots. Keeping the first boot simple makes any problem much easier to read.

Q: Do I need to flash a vendor image with crDroid 12.3?
A: Yes. Flash the vendor_boot file from the bootloader before you boot to recovery, and make sure it matches the build exactly. A mismatched vendor image is a common reason the tablet hangs at the logo.
