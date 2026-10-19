::summary
PixelOS 16.1 brings a clean Pixel-style Android 16 experience to the POCO X7 Pro
(rodin). It is an unofficial build, flashed with Fastboot and ADB sideload, and
the Jio fingerprint calibration fix is already baked in. The one step that bites
people is recovery: hold Volume Up, never use fastboot reboot recovery.

::body
If you want the Pixel feel without buying a Pixel, this is one of the tidier ways
to get it. PixelOS 16.1 is an unofficial Android 16 build for the POCO X7 Pro
(rodin), updated in late January, and it is the sort of ROM that stays out of your
way once it is on.

It is also the build where the recovery step bites people hardest, so let me put
that warning up front and then walk through the whole thing.

## Before you touch anything

- Take out the lock screen, PIN, pattern and fingerprint. Remove them properly,
  do not just set the phone to not lock.
- Back up your data. This flash wipes the phone.
- Have the PixelOS 16.1 zip for rodin ready on the PC.
- Have the `vendor_boot.img` that matches this build.
- Use a recent platform-tools package. Old ADB is the usual reason a sideload
  stalls partway.

That lock screen point is not superstition. Leaving a PIN, pattern or fingerprint
registered is how sensor issues start after the flash, and it costs you nothing to
remove them beforehand.

## What is in this build

- Signed, with SELinux staying enforcing.
- Dirty flashes are supported from the same build line.
- The Jio fingerprint calibration fix is already baked in.
- Based on Android 16, and updated near the end of January.

It is an UNOFFICIAL build, maintained by @Mnskkyy, so treat it like one: know that
small bugs can appear between releases.

## Step 1 - fastboot, and check the connection

Boot the phone into fastboot with Volume Down and Power, connect it to the PC, and
run:

`fastboot devices`

A serial number and the word `fastboot` means you are ready. Anything else is a
driver problem, and the flash will not work until you fix it.

## Step 2 - flash vendor_boot to both slots

`fastboot flash vendor_boot --slot=all vendor_boot.img`

Both slots, not one. Match the image to this build.

## Step 3 - reboot and catch recovery with the volume key

Run `fastboot reboot`, and the moment it restarts, hold Volume Up.

Now the warning. Do not use the fastboot command that jumps straight into
recovery. On the POCO X7 Pro that shortcut can leave you with a phone that refuses
to boot, and there is no comfortable way back from that. Hold Volume Up yourself.

## Step 4 - factory reset, then format data

Factory reset, then Format data. Both steps, in that order. Format data is the one
that clears encryption, and it is the difference between a clean install and a
boot loop.

## Step 5 - sideload the ROM

In recovery, choose Apply update, then Apply from ADB. From the PC:

`adb sideload` followed by the PixelOS zip name.

If the transfer stalls partway through, update your platform-tools and try again.
Nine times out of ten that is the cause.

## Step 6 - confirm, then reboot to recovery

Confirm when it asks, then reboot back into recovery. Do not boot to system yet if
you are planning to add anything.

## Step 7 - optional GApps or Magisk

If you want Google apps or root, this is the clean moment to add them, before the
first boot. Magisk at this stage is the tidier route than patching a boot image
afterwards.

## Step 8 - reboot to system

Let the first boot run its course. A clean install takes a few minutes, and setup
wizard first, restores second, is the order that saves you trouble.

## Where people get stuck

- **Using the fastboot reboot recovery command.** Not the way in on this device.
  Hold Volume Up instead.
- **Leaving the lock screen, PIN, pattern or fingerprint registered**, which is
  how sensor issues begin.
- **Sideloading from an old platform-tools package.** If the transfer stalls,
  update ADB before you blame the ROM.

## Is it worth flashing

If you want the Pixel experience without buying a Pixel, this is one of the tidier
routes to it. It is signed, SELinux stays enforcing, GApps and root are optional
add-ons rather than requirements, and dirty flashes work inside the same build
line. The catch is the word UNOFFICIAL, so keep a backup of the previous working
setup somewhere you can reach it.

If the driver side is the part that slows you down, the free Rom Flasher tool on
GitHub installs the ADB and fastboot driver in a couple of clicks. It is free, and
the link is in the downloads section.

::faq
Q: Can I use fastboot reboot recovery on the POCO X7 Pro?
A: No. That command can leave the phone unable to boot. Run fastboot reboot and
hold Volume Up immediately so it enters recovery normally.

Q: Is PixelOS 16.1 an official build?
A: No, it is UNOFFICIAL, maintained by @Mnskkyy. It is signed and SELinux stays
enforcing, but expect the odd small bug between releases.

Q: Do I need to remove my PIN and fingerprint before flashing?
A: Yes. Remove the lock screen, PIN, pattern and fingerprint first. Leaving them
registered is a common cause of sensor problems after the flash.

Q: Can I dirty flash PixelOS over an older build?
A: Within the same build line, yes. Dirty flashes are supported there. Coming from
a different ROM, do a clean flash with a factory reset and format data.

Q: Does sideloading PixelOS wipe my phone?
A: Yes, the recovery steps include a factory reset and a data format. Back up
everything you care about before you start.
