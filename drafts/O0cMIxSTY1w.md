::summary
Evolution X 11.3 on the POCO X7 Pro (rodin) is an Android 16 build flashed with vendor_boot and sideload, then finished off with two small settings fixes. Firmware in this release is OS2.0.204.0.VOJMIXM on a 6.6.56 kernel, and it syncs with the latest source.

::body
Evolution X is the ROM people move to when they want Pixel-style polish plus a settings menu that goes deeper than they will ever use. On the POCO X7 Pro, version 11.3 sits on Android 16, and the changelog for this release is short and specific: source synced, firmware moved to OS2.0.204.0.VOJMIXM, kernel moved to 6.6.56.

That last part is the quiet one. Firmware and kernel are what decide how stable a build feels day to day, long after the first impression wears off. So this is not just a cosmetic update.

## Two rules before you touch anything

- **Do not use `fastboot reboot recovery` on this phone.** It is the risky shortcut. Reboot normally and hold Volume Up instead.
- **Back up your IMEI first.** It is the one file you cannot recreate. Write it down or save a dump, then forget about it.

That second rule is not optional. People skip it and then find out why it existed.

## What you need

- The Evolution X 11.3 ROM zip for this device.
- The matching vendor file and the vendor_boot image.
- A PC with ADB and fastboot working, and a driver Windows accepts.
- Your IMEI backed up and your data copied off the phone.
- A cable that is not on its last legs.

## Step 1 - put vendor_boot beside platform-tools

Download the vendor_boot image and drop it in the same folder as your platform-tools. This avoids the classic "file not found" that stops the flash before it starts.

## Step 2 - boot to fastboot and flash it

Boot the POCO into fastboot mode, connect it, and confirm the PC sees it:

`fastboot devices`

Then flash across both slots:

`fastboot flash vendor_boot --slot=all vendor_boot.img`

## Step 3 - reboot, then catch recovery by hand

Run:

`fastboot reboot`

The moment the screen goes dark, hold Volume Up and keep holding until recovery appears. This is the part that replaces the risky command, and it works as long as you are ready to press.

## Step 4 - format data and sideload

In recovery, format data first. Then go to Apply update, then Apply from ADB, and sideload the ROM zip. Confirm when it asks, and let it write.

Do not dirty flash this one. Format data is part of the routine, not an optional extra.

## Step 5 - GApps or Magisk, then boot

Google apps are already included in this build, so you do not need a separate package for those. If you want root, flash Magisk now, in recovery, before the first boot into the system.

Then reboot to system and let first boot take its time.

## Two fixes for things you will notice

These are small and both are worth knowing before you start wondering if you broke something.

- **Quick settings drag feels sluggish?** Turn window-level blurs off and then back on. That clears it.
- **Wallpapers and styles acting up?** Install Google Photos. Once it is there, the styles picker behaves and the wallpaper section stops misbehaving.

Neither of these is a big deal, but both look like a broken ROM if you run into them cold.

## What you should know about SELinux and the build

The build is signed as userdebug and SELinux is enforcing in this release. In plain language, that means it is not running in a wide-open debugging state. It behaves more like a normal system, which is what you want on a phone you use every day.

If you ever see an Aperture video problem, there is a dedicated fix referenced in the build notes. Check those before reporting anything.

For the PC side, the free Rom Flasher tool handles the ADB and fastboot driver setup, so `fastboot devices` returns a device instead of an empty line.

::faq
Q: Does Evolution X 11.3 include Google apps?
A: Yes, it is a GApps build, so Google apps come with the ROM. Version 11.3 on the POCO X7 Pro runs on Android 16 with updated firmware and kernel underneath.

Q: Do I need to format data after flashing?
A: Yes. Format data in recovery before you sideload, and do not dirty flash this build. Skipping it is a fast route to a boot loop.

Q: Why does quick settings feel slow after the update?
A: Toggle window-level blurs off and then back on again. That clears the sluggish drag on this build, and it takes a few seconds to do.

Q: How do I enter recovery after flashing vendor_boot?
A: Run a plain fastboot reboot and hold Volume Up as soon as the screen goes dark. Do not use fastboot reboot recovery on this device.

Q: Should I back up my IMEI before flashing?
A: Yes, always. Your IMEI is the one thing you cannot recreate, so save it before you start. It is a two-minute job that saves a very long day.
