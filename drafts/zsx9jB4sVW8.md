::summary
PixelOS on Android 15 is running on the POCO X7 Pro after a clean flash done step
by step. It is a signed GApps build with SELinux enforcing and OTA support, so
updates keep coming without a cable. The whole job is vendor_boot, one reboot, a
data format and a sideload.

::body
PixelOS is what you flash when you want your Xiaomi hardware to behave like a
Pixel. On the POCO X7 Pro the Android 15 build has been worth the swap, and this
written version walks the same order I used, because on this phone the order is
the part that matters. Do the steps out of sequence and it will look like the ROM
does not boot. Do them in order and it comes up first time.

## What is in the build

- GApps already included, so Play Store is there out of the box
- Signed build with OTA implemented, which means later updates do not need this
  whole procedure again
- SELinux enforcing
- The build notes list no known issues and just ask you to send logs if you find
  something
- If it refuses to boot, the advice is to reflash the latest firmware and go again

A signed build with OTA support is the detail I care about most, because it means
you are not on a dead end. Once you are up, updates arrive like they would on any
other phone.

## What you need

- The PixelOS ROM zip for the POCO X7 Pro
- The vendor_boot image for that same build
- ADB and Fastboot driver installed on your PC
- Platform Tools
- A backup of your IMEI and your data, off the phone
- A charged battery and a good cable

The vendor_boot image has to match the ROM build. A mismatched one is a silent
ticket to a phone that does not get past the logo.

## Step 1 - get into fastboot and confirm the connection

Boot to fastboot mode and run `fastboot devices` on the PC. A serial number means
you are good. Nothing at all means the driver is missing, and no amount of
retrying the later steps will fix that. Install the driver first.

## Step 2 - flash vendor_boot to both slots

This is the single most important command in the whole guide:

`fastboot flash vendor_boot --slot=all vendor_boot.img`

The `--slot=all` part is not decoration. Both slots need the image, and skipping
one of them is how you get a phone that boots correctly once and then misbehaves
after an update.

Wait for it to report finished on both slots.

## Step 3 - reboot and catch recovery

Run:

`fastboot reboot`

and hold Volume Up straight away. You have a short window here. If you miss it
and the old system starts loading, reboot and try again. Being early is fine.
Being late means starting over.

Do not use `fastboot reboot recovery` on this phone. The build notes warn that it
can brick the device, so take the Volume Up route every time.

## Step 4 - format data

Format data before you sideload anything. This is a clean flash and it is
mandatory here. Dirty flashing this build is the direct route to a bootloop, so
please do not skip the format to save two minutes.

## Step 5 - sideload the ROM

Go to Apply update, then Apply from ADB. On the PC, type `adb sideload` and drag
the ROM zip into the terminal window so the path fills itself in. Press enter.

Watch the progress percentage reach the end. Do not disconnect before it does.

## Step 6 - extras, then first boot

When it asks whether to reboot back to recovery, say yes if you want to add
GApps or Magisk. This build already has GApps, so most people skip straight past
this. Then reboot to system.

The first boot takes longer than you expect. Let it work. Do not unplug anything
and do not force a restart.

## Where people get stuck

- **`fastboot reboot recovery`.** The notes are explicit that it can brick this
  phone. Use Volume Up after a normal reboot instead.
- **Missing the recovery key window.** Timing is tight. If you land in the old
  system, restart from the vendor_boot step.
- **Skipping the data format.** This is the classic bootloop cause, and it always
  looks like the ROM is at fault when it is not.
- **The wrong vendor_boot image.** It must come from the same build as the ROM
  zip you are sideloading.

## One honest note

The frustrating thing about this flash is how much of it is timing and
digit-holding rather than real complexity. The commands are short. The waiting is
long. I would rather you know that going in than spend the first reboot wondering
if you broke something when the phone sits on the logo for two minutes.

If it does not boot at all after a second honest attempt, reflash the latest
firmware and run the whole thing again from step 1. That is the recovery path the
build notes recommend, and it works.

If the driver install is the part that keeps stopping you before you even start,
the free Rom Flasher tool puts the ADB and fastboot driver in for you in a couple
of clicks. It is free, and the link is in the downloads section.

::faq
Q: Does PixelOS on the POCO X7 Pro include Google apps?
A: Yes. It is a GApps build, so Play Store and Google services are included in the ROM zip. You do not need a separate GApps package.

Q: Is a clean flash mandatory for PixelOS?
A: Yes. Format data before sideloading. Dirty flashing over another ROM or another Android version here is the fastest way to a bootloop.

Q: What happens if I use fastboot reboot recovery?
A: The build notes warn that this command can brick the POCO X7 Pro. Do not use it. Run a normal fastboot reboot and hold Volume Up immediately to enter recovery.

Q: Will I get OTA updates after installing PixelOS?
A: Yes. It is a signed build with OTA implemented, so later updates arrive as normal updates rather than another full sideload session.

Q: My phone will not boot after the flash. What do I do?
A: The first boot is slow, so give it a couple of minutes. If it still will not come up, reflash the latest firmware and run the flash again from the start.
