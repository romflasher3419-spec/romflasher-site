::summary
Matrixx OS on the POCO X7 Pro (rodin) is an Android 16 build that installs through fastboot and recovery in about ten minutes, as long as you avoid one trap: never run fastboot reboot recovery on this phone. Reboot the normal way and hold Volume Up to catch recovery instead.

::body
So you want Matrixx OS on the POCO X7 Pro. Good news first: this one is short, and the build behind it is a signed userdebug Gapps build with SELinux enforcing. That sounds like paperwork, but it is the reason this ROM behaves like a daily driver instead of an experiment you reboot every hour.

Bad news is one step. There is a real brick trap in the flashing guide for this device, and it hides inside a command that looks completely normal.

## What you need before you start

- An unlocked bootloader on the POCO X7 Pro (rodin).
- The Matrixx OS ROM zip, the vendor file for this device, and the vendor_boot image.
- ADB and fastboot on your PC, plus a USB driver that Windows is actually happy with.
- The KSU patched image, only if you want root.
- A cable you trust and a battery above 50%.

Do not skip the vendor file. It is not optional decoration.

## Step 1 - push vendor_boot to both slots

Boot the phone into fastboot, plug it in, and check the PC sees it:

`fastboot devices`

You want a serial number back. An empty line means the driver is wrong, not the phone, so fix that before you touch anything else. Then flash:

`fastboot flash vendor_boot --slot=all vendor_boot.img`

Both slots, one command. That part is fine.

## Step 2 - reboot by hand, this is the trap

Do not type `fastboot reboot recovery` on this device. It can brick the phone. I am not being dramatic; this is the single command the flashing guide warns about, and it is easy to run by habit.

Instead run a plain reboot:

`fastboot reboot`

The second the screen goes dark, hold Volume Up yourself and keep holding until recovery appears. It feels clumsy. It is still the correct way here.

## Step 3 - format data, then sideload

In recovery, format data first. This wipes internal storage, so if your photos are still on the phone, stop now and move them off.

Then pick Apply update, then Apply from ADB, and sideload the ROM zip:

`adb sideload <rom zip>`

The progress readout on the phone can sit on one number for a long time. That is normal. When it asks you to confirm, choose yes, and let it fall back to recovery.

## Step 4 - optional extras, then leave it alone

Want Google apps on top, or root? This is the window. Flash the Gapps package or the KSU patched image while you are still in recovery, before the system ever boots.

Then reboot to system and walk away. First boot on a build like this takes longer than a stock phone would, and staring at it does not speed it up.

## Where people get stuck

- **Running fastboot reboot recovery.** This is the one that costs people a phone. Hold Volume Up instead.
- **Formatting data after sideloading instead of before.** Wrong order usually ends in a boot loop and a second attempt.
- **Changing the Reality Display Engine setting.** There is a known issue with it on this build. Leave that setting exactly where it is.

## One honest note

Sideload is the slow part and nobody warns you. A large ROM zip takes a while to scan through recovery, and the on-screen progress does a poor job of proving anything is happening. Keep the phone plugged in and let it finish.

If the PC side is the part that annoys you, the free Rom Flasher tool handles the ADB and fastboot driver setup without you hunting through Device Manager.

::faq
Q: Can I use fastboot reboot recovery on the POCO X7 Pro?
A: No. On this device that command can brick the phone. Run a plain fastboot reboot and hold Volume Up the moment the screen goes dark, then keep holding until recovery appears.

Q: Does flashing Matrixx OS wipe my data?
A: Yes. You format data in recovery as part of the install, so internal storage goes. Copy your photos, chats and downloads off the phone before you begin.

Q: Do I need the vendor file as well as the ROM?
A: Yes. The vendor image has to match the ROM build and it is flashed alongside the rest. Skipping it usually leaves you stuck on the logo or on a black screen.

Q: Is this build rooted out of the box?
A: No. It is a signed userdebug Gapps build with SELinux enforcing. If you want root, flash the KSU patched image in recovery before the first boot into the system.

Q: How long does the first boot take?
A: Longer than you expect, and the sideload before it is the slow part. Leave the phone plugged in and untouched, and do not pull the cable while recovery is still writing.
