::summary
Axion OS 2.4 on the POCO X7 Pro is an Android 16 ROM with a short install: flash vendor_boot to both slots, catch recovery with Volume Up, wipe, then sideload the zip over ADB. Set aside about ten minutes of waiting, then a first boot you actually want to sit through.

::body
Axion OS 2.4 is the install I would point a first-timer at if they wanted a clean Android 16 base without a pile of extra steps. The flash is short when your vendor_boot is the right one, and the phone comes up looking finished rather than half-built.

The whole thing fits in one sitting. Here is the order, plus the two or three things that decide whether it boots on the first try.

## What you need

- The Axion OS 2.4 ROM zip from the link below.
- The vendor_boot image that matches this exact build.
- A PC with ADB and Fastboot installed.
- A cable that does data, not a charge-only one. This is not a small detail.

The cable point is worth repeating. A charge-only cable will let the phone show up and then die in the middle of a sideload, and you will spend an hour blaming the ROM.

## Step 1 - confirm the PC sees the phone

Boot the phone into fastboot and run `fastboot devices`. It should list the device. If it lists nothing, fix the driver now. Everything after this depends on a stable connection.

## Step 2 - flash vendor_boot to both slots

Push the vendor_boot file to slot A and to slot B. Both. It takes a moment longer and saves you a bootloop later if the phone ever switches slots.

## Step 3 - reboot and hold Volume Up

Run `fastboot reboot`, then hold Volume Up straight away and keep holding until recovery appears. If you let go, the phone boots into system instead, and the sideload has nowhere to go.

## Step 4 - factory reset, then format data

In recovery, do a factory reset first, then format data. The format is the one that clears the old encryption. Skip it and the phone can loop on the first boot, because the old data partition is still sitting there encrypted with the wrong key.

## Step 5 - sideload the zip

Go to Apply update, then Apply from ADB. On the PC, run the sideload command with the ROM zip. Recovery prints progress as it goes and tells you when it is finished. Do not close the window early.

## Step 6 - optional extras

If you want root, flash Magisk now, while you are still in recovery. If you want a separate GApps package, this is also the moment. Do one or the other, in the same session, so you do not have to come back.

## Step 7 - first boot

Reboot to system and go through setup. The first boot takes longer than a normal boot on a fresh install. Let it finish.

## Where this usually goes wrong

- Missing the Volume Up hold, so the phone lands in system instead of recovery.
- A vendor_boot from a different build mixed with this zip.
- Skipping the factory reset and format data, which leaves the old encryption in place.

## What is actually new in 2.4

The part I filmed properly is what happens after the first boot, because that is what you live with. Smoothness on a clean Android 16 base, the settings worth turning on in the first ten minutes, and how the battery behaves on day one. Day-one battery is always a rough read, so treat the first charge as a guess and judge it again after a week.

For gaming, there is a quick pass rather than a five-second tour, so you can see what the phone does under a real load instead of a scroll through menus.

## The honest part

Axion OS is a community build, so there is no official update path once you flash it. Keep your backup until you have used it for a few days, and read the changelog before every update, because a build that installs cleanly can still change how your phone behaves.

If the driver and tools setup is the slow part for you, the free Rom Flasher tool on GitHub handles the ADB and fastboot driver install in a couple of clicks, so you can skip the Device Manager hunt. It is free, and the link is in the downloads section.

::faq
Q: Do I need to flash GApps on Axion OS 2.4?
A: It is optional. You can flash a GApps package in recovery right after the ROM sideload finishes, in the same session. If you skip it, install it while still in recovery rather than after you have booted.

Q: Does flashing Axion OS wipe my data?
A: Yes. The install needs a factory reset and a format data in recovery, so internal storage is cleared. Back up your files before you start.

Q: Why did my phone boot into system instead of recovery?
A: You missed the Volume Up hold. Run fastboot reboot and hold Volume Up the moment it restarts, keeping it held until recovery appears.

Q: Can I use a vendor_boot from another build?
A: No. The vendor_boot has to match this exact Axion OS 2.4 build. Mixing versions is a fast route to a bootloop.

Q: How long does the install take?
A: The flash itself is quick once your vendor_boot is right. Add roughly ten minutes of waiting for the sideload and the first boot, and leave the phone plugged in until it is done.
