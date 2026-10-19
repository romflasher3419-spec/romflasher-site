::summary
Nusantara ROM goes onto the Xiaomi 11T Pro with a short fastboot flash followed by a recovery sideload. Both boot and vendor_boot have to be written to the _ab slots — skip one and the phone will not even reach recovery. After that it is sideload the ROM zip, factory reset, reboot.

::body
This is a custom ROM with a two-part install, and the part people trip on is the A/B side of things. The 11T Pro uses A/B slots, so boot and vendor_boot both go to the _ab targets rather than a plain partition name. If you write only one of them, the phone will not boot into recovery at all, and you get a black screen with no obvious clue why.

Get that right and the rest is quick. Sideload the ROM zip, do a factory reset, reboot. It is also easy to undo, which matters — keep a stock package around and you can go back.

## What you need

- A custom recovery image for the 11T Pro. OrangeFox is the one linked below, and it works for this.
- The Nusantara ROM zip.
- Platform Tools on the PC so ADB and fastboot are available.
- An unlocked bootloader. No way around this part.
- A backup, because a factory reset is baked into the process.

## Step 1 - boot into the bootloader

With the phone on and USB debugging allowed, run:

`adb reboot bootloader`

If ADB is not talking to the phone, reboot the phone manually into fastboot with the volume and power keys. Then check the PC sees it:

`fastboot devices`

You need a serial number back. Without it, every command below will sit and do nothing.

## Step 2 - flash boot to the _ab slot

`fastboot flash boot_ab boot.img`

Note the `_ab`. On a device with A/B slots, the plain `boot` target is not what you want for this install. This is the single most common mistake with Nusantara, and it fails quietly — the command reports success and the phone still will not start.

## Step 3 - flash vendor_boot to the _ab slot

`fastboot flash vendor_boot_ab vendor_boot.img`

Same idea, second partition. Do not stop after step 2. Both images go on before you leave fastboot, because recovery on this device needs vendor_boot to bring up the display and the ramdisk properly. One without the other gets you a dead screen.

## Step 4 - reboot into recovery

`fastboot reboot recovery`

The recovery should come up. If it does not, and you get a black screen or a loop back to fastboot, go back to steps 2 and 3 and check that both writes went to the _ab targets.

## Step 5 - factory reset in recovery

In recovery, choose the wipe data option, which is the factory reset. Do this now, before the sideload, not after. The ROM expects a clean data partition when it first boots, and skipping this is why a lot of people end up hanging on the boot animation.

## Step 6 - sideload the ROM zip

In recovery, select apply update from ADB. Then from the PC, with the ROM zip in the same folder you are running commands from:

`adb sideload <rom zip>`

The recovery screen will show progress, and the command line will show a percentage. When it reaches the end, the phone will report the result. A message about a signature or verification failure is common during sideloads and is usually fine to continue past, but read it before you do.

## Step 7 - reboot and wait

Reboot to system and leave it. First boot on a fresh custom ROM takes a few minutes. Do not tap at the screen and do not pull the cable. Once the setup wizard appears you are done.

## Where people get stuck

- **Flashing only one of boot and vendor_boot.** Both are needed, and both to the _ab slots. One alone gets you no recovery.
- **Sideloading with the wrong recovery booted.** If the sideload fails with no clear reason, check which recovery is actually running. The wrong one will reject the package or die partway.
- **Skipping the factory reset.** The system then hangs on boot against old data, and it looks like a bad ROM when it is really a missing wipe.
- **A stale recovery.** A recovery built for an older base can fail on a fresh ROM zip. If in doubt, flash a current recovery image for your device first.

## An honest note

This install is fiddly in one specific way: the fastboot part has no room for guessing. Steps 2 and 3 either both happen or the phone does not start, and nothing on the screen tells you which one you missed. Write the commands out before you start rather than reading them off at the keyboard.

The recovery side is friendlier. Once you are sitting in OrangeFox or whatever you installed, sideload is a single command and the wipe is a menu tap.

If you are tired of hand-installing ADB and the fastboot driver every time you do this, the free Rom Flasher tool on GitHub bundles that into a couple of clicks. It is free, and the link is in the downloads list.

::faq
Q: Why does my phone not boot after flashing Nusantara on the 11T Pro?
A: Most likely only one of the two images went on. Both boot and vendor_boot have to be flashed, and both to the _ab slots. Boot into fastboot again, write both, and then reboot to recovery.

Q: What is the difference between boot_ab and boot?
A: The 11T Pro has A/B slots, so the ROM images target the combined _ab partitions. Writing to the plain boot target reports success but does not put the image where the device looks, which is why the phone still fails to start.

Q: Can I sideload Nusantara without a custom recovery?
A: No. The ROM lands through a recovery sideload, so a working recovery for the 11T Pro has to be running first. OrangeFox is the one linked in the downloads list.

Q: Do I need to factory reset before sideloading?
A: Yes, do the wipe before the sideload. The ROM expects clean data on first boot, and installing over old data is the usual reason people end up stuck on the boot animation.

Q: How long should the first boot take?
A: A few minutes on a fresh custom ROM. Give it that time without touching the screen or unplugging the cable, and only start worrying if it is clearly stuck well beyond that.

Q: Is Nusantara easy to undo?
A: Yes, provided you kept a stock package around. The same recovery tools flash a stock build back, and the fastboot side writes the original boot images. Keeping the stock files costs you nothing and saves an evening.
