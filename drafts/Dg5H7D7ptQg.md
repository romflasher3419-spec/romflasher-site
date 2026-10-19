::summary
Lunaris AOSP 3.4 is the first Android 16 build for the POCO X7 Pro, and it flashes the usual X7 Pro way: flash vendor_boot to both slots, reboot, hold Volume Up to reach recovery, factory reset, then sideload the ROM. GApps are already inside, so you do not flash a GApps package.

::body
Lunaris starts as a clean AOSP base and adds just enough to feel finished. Build 3.4 is the first Android 16 release for this phone, and the day-one experience is a working phone rather than a project: it is a signed userdebug build, SELinux is enforcing, and GApps are already inside.

The flash follows the same pattern as the other X7 Pro builds. Two boring warnings before we start, because they matter. Hold Volume Up for recovery. Never use `fastboot reboot recovery` on this device.

## What is in this build

- Initial Lunaris Android 16 release.
- Source synced.
- Firmware moved to OS2.0.204.0.VOJMIXM, kernel at 6.6.56.
- Signed userdebug, SELinux enforcing, GApps included.

## What you need

- An unlocked bootloader. There is no way around it.
- The Lunaris AOSP 3.4 ROM zip plus its vendor file, from the links below.
- The vendor_boot image from the same download. Do not mix it with one from another build.
- A PC with ADB and Fastboot ready.
- Your IMEI backed up, and the lock screen and fingerprint removed before you start.

## Step 1 - grab the right files

Download the ROM zip and the vendor file and unpack them on the PC. The vendor_boot image has to come from this exact build. A vendor_boot from a different version is a fast route to a bootloop, and it is the mistake I see most often on this phone.

## Step 2 - fastboot and confirm the PC sees the phone

Reboot the phone to fastboot and run `fastboot devices`. You want a serial number back. If the command returns nothing, fix the fastboot driver before you go any further.

## Step 3 - flash vendor_boot to both slots

Push vendor_boot to slot A and then to slot B. Both, not just the one the phone happens to be booted on. If you only flash A, the next OTA or a later slot switch can hand you a phone that drops straight back to fastboot.

## Step 4 - reboot and catch recovery with Volume Up

Reboot the phone, then hold Volume Up immediately and keep holding until recovery appears. Do not use `fastboot reboot recovery` here. On the POCO X7 Pro it does not take you where you think, and it is the fastest way to confuse yourself.

## Step 5 - clean it, then sideload

In the Lunaris recovery, do a factory reset so nothing from the old ROM survives. Then choose Apply update, then Apply from ADB, and sideload the ROM zip from the PC. Let the recovery tell you when the install is finished rather than guessing.

Do not flash a separate GApps package over this build. GApps are already inside it. If you want root, this is the moment to flash Magisk, during recovery, before the first boot.

## Step 6 - first boot and the two quirks

Reboot to system and give the first boot its time. When you are in, two small things are worth knowing.

- If wallpapers and styles misbehave, install Google Photos. For whatever reason, they settle once it is there.
- Keep the display colour on its default instead of X-Reality. X-Reality hands you a blank white screen on these builds, and people assume the ROM is broken when it is only a setting.

## Where this usually goes wrong

- A vendor_boot that does not match this build.
- Tapping through to system instead of holding Volume Up, so you never reach recovery.
- Forgetting the factory reset, which leaves the old encryption in place.

## Dirty flashing

Not on the first Android 16 build. Clean it. Once you are on 3.4, later 3.4.x builds are usually a different story, but for this one, wipe and start fresh.

If the driver and tools setup is the part that always slows you down, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks, so you are not fighting Device Manager. It is free, and the link is in the downloads section.

::faq
Q: Do I need to flash GApps separately on Lunaris AOSP 3.4?
A: No. This is a GApps build, so the Google apps are already inside it. Only add Magisk during recovery if you want root, and skip the GApps package.

Q: Can I dirty flash Lunaris AOSP 3.4?
A: Not for the first Android 16 build. Do a clean install with a factory reset so nothing from the old ROM survives.

Q: Why does the phone not boot into recovery?
A: You have to reboot and hold Volume Up immediately. And never use fastboot reboot recovery on the POCO X7 Pro, because it does not take you to recovery on this device.

Q: Is root included in this ROM?
A: No. The build ships without root. If you want it, flash Magisk during recovery before the first boot.

Q: My wallpaper and styles app is misbehaving. What now?
A: Install Google Photos and they usually settle. Also leave the display colour on its default instead of X-Reality, which causes a blank white screen on these builds.
