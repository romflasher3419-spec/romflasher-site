::summary
crDroid v12.10 is the Android 16 official build for the POCO X7 Pro (rodin), and
it moves to a LineageOS 23.2 base for steadier gaming. Flash vendor_boot, format
data, sideload the ROM, and sideload GApps in the same session, because this build
is Vanilla and ships without the Play Store. Clean flash only for this one.

::body
The changelog for crDroid v12.10 is short, and that is a good sign on a gaming
ROM. This one moved to a LineageOS 23.2 base for more stable gaming, the I/O
scheduler switched from BFQ to mq-deadline, debug logging is off on non-eng
builds, and Factory Reset Protection is disabled. Boring lines on paper. You feel
them in a long match.

Here is the whole process in the order I actually did it, including the GApps
step people forget and then panic about.

## What changed, in plain words

- Moved to a LineageOS 23.2 base, which is the stability part for gaming.
- The I/O scheduler switched from BFQ to mq-deadline.
- Debug logging is off on non-eng builds, so less background noise.
- Factory Reset Protection is disabled.
- GApps are not included. crDroid ships vanilla, so you add them yourself.

That vanilla line is the one that catches people. If you sideload only the ROM and
reboot, you get a clean Android install with no Play Store, and then you have to
go back into recovery a second time.

## What you need

- A POCO X7 Pro (rodin) with an unlocked bootloader.
- The crDroid v12.10 ROM zip from the link for your device.
- The `vendor_boot` image that matches this exact build.
- crDroid Recovery, or a recovery you already trust.
- A GApps zip if you want Google services.
- A full backup of your data.

Unlocking the bootloader wipes the phone, so if you have not done that yet, do it
first and set the phone up empty. There is no point restoring a backup you are
about to delete.

## Step 1 - fastboot, and make sure the PC sees the phone

Move the device to fastboot mode with Volume Down and Power, plug it in, and run:

`fastboot devices`

A serial number plus `fastboot` means you are good. Anything else, and it is the
driver, not the ROM.

## Step 2 - flash the vendor_boot image

`fastboot flash vendor_boot --slot=all vendor_boot.img`

Match the image to this build. A vendor_boot from an older crDroid release is a
fast route to a phone that will not boot, and the fix is a lot longer than the
five minutes you saved.

## Step 3 - reboot into recovery

Run `fastboot reboot`, then hold Volume Up immediately. Do not use the fastboot
command that jumps straight to recovery on this phone. Catch it with the volume
key instead.

## Step 4 - factory reset, then format data

Factory reset first, then Format data. This build wants a clean start. A dirty
flash over an older ROM is the number one cause of strange behaviour here, so
resist the shortcut.

## Step 5 - sideload the ROM

Apply update, then Apply from ADB. From the PC:

`adb sideload` and the crDroid zip name.

Let it finish. If the transfer stops partway, update your platform-tools and try
again rather than blaming the zip.

## Step 6 - say yes and sideload GApps in the same session

After the ROM finishes, recovery asks whether you want to install additional
packages. Answer Yes.

This is the step people forget. Because the build is vanilla, this is your one
clean chance to add Google services. Pick the GApps zip and sideload it right
there, in the same recovery session, before you reboot to system. If you skip it,
the ROM boots fine but there is no Play Store, and you are back in recovery
reloading packages while your setup wizard waits.

## Step 7 - reboot to system and wait

The first boot on a clean data partition takes a few minutes. Let it finish the
setup wizard before you start gaming or restoring anything. If something is going
to misbehave, you want it to happen on an empty phone.

## Where people get stuck

- **Flashing over a dirty install.** A clean flash is mandatory for the first
  install on this build.
- **Forgetting GApps**, then wondering where the Play Store went.
- **Using a recovery from a different ROM**, which throws mount errors and fails
  the sideload partway through.
- **A vendor_boot from the wrong build.** The image has to match this release.

## The gaming part

The changelog looks quiet, and that is the point. Moving to a LineageOS 23.2 base
and swapping the I/O scheduler are the kind of changes you only notice when a
long session normally starts to stutter. This build is set up to hold its rhythm
rather than sprint for the first five minutes. If you play in long matches, that
difference is the whole reason to update.

If the driver side of this is the tiresome part, the free Rom Flasher tool on
GitHub installs the ADB and fastboot driver for you in a couple of clicks. It is
free, and the link is in the downloads section.

::faq
Q: Do I need GApps with crDroid v12.10?
A: Yes, if you want the Play Store. The build is vanilla, so sideload a GApps zip
in the same recovery session, right after the ROM, and before you reboot.

Q: Can I dirty flash crDroid v12.10 over an older version?
A: No, do a clean flash for this one. Factory reset and format data first, or you
risk the odd behaviour that dirty flashes are known for.

Q: Which vendor_boot image do I use?
A: The one that matches this exact build, from the download link for your device.
An image from an older release can leave the phone unable to boot.

Q: Does crDroid v12.10 work on other POCO phones?
A: No. This build is for the POCO X7 Pro, codename rodin. A package built for a
different model can write partitions your phone cannot boot from.

Q: Is the bootloader unlock going to wipe my phone?
A: Yes, unlocking always wipes data. Back up your files before you start, and
expect to run the setup wizard on the first boot after flashing.
