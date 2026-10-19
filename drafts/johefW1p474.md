::summary
RiceDroid 8.6 runs on the Xiaomi 11T Pro as a GSI on Android 13, installed with fastboot over your existing vendor image. The flash is short: fastbootd, vbmeta with verity and verification off, erase and flash the system image, then wipe data in recovery. The wipe is the step people forget, and forgetting it is the classic bootloop.

::body
RiceDroid 8.6 is a generic system image, phh-treble based. That means the ROM itself is clean, and the device side of things depends entirely on your vendor and kernel.

That is the whole trade with a GSI. You can put it on almost anything Treble-ready in a few minutes, but how well the camera or calls behave is your vendor's business, not the ROM's.

Device here is the Xiaomi 11T Pro.

## What you need

- An **unlocked bootloader** and a Treble-ready device, which the 11T Pro is.
- The **RiceDroid 8.6 system image**. ARM64 or A64 AB, and GApps, vanilla and slim builds are all available here.
- The **vbmeta** file, since you flash it with both flags.
- **Platform tools** on your PC.
- A **working custom recovery** for the final data wipe.

Good news on the build choice: this release has a vanilla option, which is rare for a GSI. If you want a Google-free system, you can actually take it here.

## Step 1 — boot to the bootloader and check the connection

Power off, then hold Volume Down and Power until you reach the bootloader screen. Plug in and run:

`fastboot devices`

A serial number with the word `fastboot` next to it is what you are looking for. Nothing means a driver problem, and the flash will not work until that is fixed.

## Step 2 — switch to fastbootd

`fastboot reboot fastboot`

The system partition can only be written in fastbootd. If the next commands fail, this is why.

## Step 3 — flash vbmeta with verity and verification off

`fastboot --disable-verity --disable-verification flash vbmeta`

Both flags matter. Verification is the check that blocks a modified system image from booting. Leave it on and the phone rejects the GSI at boot. Do this before you touch the system partition.

## Step 4 — erase the system partition

`fastboot erase system`

This clears out whatever system image was there before, so the new one has a clean space to land in.

## Step 5 — flash the RiceDroid image

`fastboot flash system`

It is a large image and it takes a few minutes. Let it run. Do not unplug the cable and do not close the window. A flash that stalls for thirty seconds is usually just a slow USB port, not a failure.

## Step 6 — reboot to recovery and wipe data

`fastboot reboot recovery`

In Mi Recovery, wipe data. This is the step people forget, and it is the one that decides whether you see a setup wizard or a boot animation for the rest of the evening.

The reason is encryption. Your old userdata is encrypted with keys from the old system, so a new system partition sitting on old userdata cannot start. Wipe it, then reboot. The first boot takes a while, which is normal.

## Step 7 — reboot and finish setup

Boot the phone, run the setup wizard, and let it settle for ten minutes before you start installing everything. Then check the things you use constantly:

- Calls and mobile data
- The camera app
- Bluetooth audio
- The fingerprint sensor

If any of those is off, remember what a GSI is. Those are vendor items, not ROM items.

## What is broken

Nothing is listed in the ROM itself, which is rare and genuinely nice to be able to say. SELinux works both ways here, so enforcing and permissive are both fine.

On the device side, it depends entirely on your vendor and kernel. Two people on the same phone model can have different experiences and both be accurate. A recent vendor and kernel is what keeps the surprises away.

## Where people get stuck

- **Skipping the vbmeta flags.** Without `--disable-verity` and `--disable-verification`, the GSI will not boot.
- **Forgetting the data wipe at the end.** A dirty system partition plus old userdata is the classic bootloop.
- **Blaming the ROM for broken hardware features.** On a GSI, camera, calls and sensors ride on your vendor and kernel, and the ROM cannot fix that.
- **Flashing system from plain bootloader** instead of fastbootd, which quietly does nothing useful.

If the driver and platform tools side of this is the part you dread, the free Rom Flasher tool on GitHub installs the ADB and fastboot drivers in a couple of clicks so you are not hunting through Device Manager. It is free, and the link is in the downloads section.

One last thing. Do the full setup and one reboot before restoring your apps. If something is going to break, let it break on an empty phone.

::faq
Q: Why does RiceDroid 8.6 bootloop on the Xiaomi 11T Pro?
A: The data wipe was most likely skipped. Old userdata is encrypted with keys from the previous system, so a new system partition on it will not boot. Reboot to recovery and wipe data.

Q: Which RiceDroid 8.6 image should I download?
A: ARM64 or A64 AB, depending on your device, and the 11T Pro takes the ARM64 AB image. This release also has GApps, vanilla and slim variants, so you can pick a Google-free system if you want one.

Q: Do I need to flash vbmeta to install RiceDroid?
A: Yes, and with both `--disable-verity` and `--disable-verification`. Verification blocks a modified system image, so without those flags the GSI is rejected at boot.

Q: Does RiceDroid work with SELinux enforcing?
A: Yes. SELinux works in both modes on this release, so enforcing and permissive are both fine. You do not have to switch to permissive to boot it.

Q: What can a GSI not fix on the 11T Pro?
A: Anything hardware side. Camera quality, calls, sensors and fingerprint come from your vendor and kernel, not from the system image. A recent vendor gives you far fewer surprises.
