::summary
LineageOS 20 brings Android 13 to the Xiaomi Pad 5 as a weekly test build. This one installs through fastboot, not recovery sideload, and the route differs depending on whether you are coming from MIUI or another custom ROM. Gapps are already baked in, so you only add Magisk and the safetynet fix afterwards if you want Play Certification.

::body
You want LineageOS on the Pad 5, and this particular build has a quirk worth knowing before you start: it goes on with fastboot, not with a recovery sideload. Future builds for this tablet arrive as OTA packages you flash in recovery, but this one still needs the fastboot route.

The build is a weekly test build from source, and it can work as a daily driver. It ships with Gapps already baked in, so you skip a separate flash. If you want Play Certification to behave, you add Magisk and the safetynet props afterwards, and that combination does the heavy lifting.

## What changed in this build

- Partition sizes aligned with stock firmware, which avoids the space surprises older builds had.
- A boot failure caused by magiskinit is fixed.
- Bluetooth audio HAL updated.
- Controls added for adjusting the refresh rate.
- Power button glitches fixed.
- Xiaomi Pen and stylus support added.
- Double tap to wake added.
- Aligned with the latest LineageOS source.

The pen support is the one people notice. The Pad 5 is often bought as a note-taking tablet, and a build without working stylus input is a non-starter for that job.

## What you need

- The ROM zip from the link below.
- Latest platform tools on your PC.
- The ADB and Fastboot driver installed, so fastboot sees the tablet.
- A charged battery and a backup, because whatever route you take, the tablet gets wiped.

## If you are coming from MIUI

Pull `boot` and `vendor_boot` out of the ROM zip and flash them from the bootloader. This is fastboot proper, not fastbootd — the normal bootloader screen, not the fastboot mode inside recovery. Getting those two mixed up is the most common reason people think the flash failed.

Once the images are in, reboot and continue with the build.

## If you are coming from another custom ROM

1. Reboot to the bootloader.
2. Run `fastboot -w` to wipe.
3. Reboot to fastbootd.
4. Flash the update package.

The wipe matters more than people expect when moving between custom ROMs. Different builds write different vendor content, and skipping the wipe leaves you with a tablet that boots to the logo and hangs there.

## Step by step, both routes

1. Download the LineageOS zip from the link below.
2. Keep the latest platform tools ready.
3. From MIUI: reboot to bootloader, flash boot and vendor_boot from the zip.
4. From another custom ROM: reboot to bootloader, run `fastboot -w`, reboot to fastbootd, flash the update package.
5. Let it boot fully before you set anything up. Do not rush the setup wizard while the tablet is still settling.
6. Add Magisk and the safetynet props afterwards if you want Play Certification.

## Where people get stuck

- **Confusing fastboot with fastbootd.** From MIUI, the boot images go on from the real bootloader. fastbootd is the recovery-side mode and it will not accept the same set of commands.
- **Skipping the wipe when crossing between custom ROMs.** You get a boot loop or a hang at the logo, and it looks like a broken ROM when it is really a dirty install.
- **Setting the tablet up too quickly.** Finish the first boot, then configure. Adding accounts and restoring during the initial boot makes any early problem much harder to read.

## One honest note

This is a weekly test build, which means the maintainers are still moving things around. That is fine for daily use most of the time, but do not expect the polish of a stable channel. Keep a working package around so you can go back if a weekly build misbehaves.

The free Rom Flasher tool on GitHub handles the ADB and fastboot driver install for you, so the platform tools side is two clicks instead of a Device Manager hunt. It is free, and the link is with the others on this page.

## Who should install it

Install it if you want LineageOS 20 on the tablet without flashing Gapps separately, and you can live with a test build. Skip it if you cannot tolerate the occasional rough weekly, or if you want the stable channel and nothing else.

::faq
Q: Do I need to flash Gapps with LineageOS 20 on the Mi Pad 5?
A: No. This build ships with Partner Gapps baked in, so you skip the separate flash. You only add Magisk and the safetynet props afterwards if you want Play Certification to pass.

Q: Is this build fastboot or recovery?
A: This one goes on with fastboot. The build images go on from the bootloader. Later LineageOS builds for this tablet arrive as OTA packages you flash in recovery instead.

Q: How do I get Play Certification working?
A: Set it up with Magisk, the safetynet props and the safetynet fix that comes with this build. That combination is what makes Play Certification behave. Do it after the ROM has booted fully.

Q: Does the Xiaomi Pen work on LineageOS 20 for the Pad 5?
A: Yes. Pen and stylus support was added in this build, along with double tap to wake. Refresh rate controls were added too, so you can adjust that from the settings.

Q: Will flashing this wipe the tablet?
A: Yes. If you come from MIUI the images replace the system, and if you come from another custom ROM the wipe is part of the process. Back up anything you care about before you start.
