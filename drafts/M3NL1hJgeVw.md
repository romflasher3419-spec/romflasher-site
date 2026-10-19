::summary
crDroid 12.5 is out for the POCO X7 Pro, and it sits on Android 16 with the QPR1
update and the December security patch. It is a signed Vanilla build, so you flash
vendor_boot, sideload the ROM, and add GApps yourself if you want the Play Store.
One warning before anything else: never type fastboot reboot recovery on this
phone.

::body
It landed quickly. crDroid 12.5 already sits on top of Android 16 QPR1, the
December security patch is in, and I flashed it end to end on the POCO X7 Pro
the day it showed up. Two things change the order of the job compared with older
builds, and both of them are below. Read them before you touch the phone.

## What is new in this build

- Synced with the latest crDroid source, so the QPR1 merge is in.
- December security patch included.
- It ships eng-preloader, and that changes the flash order. Do not reuse last
  month's routine without reading the steps.
- The thermal profile is updated, which is the part gamers will feel first.
- jiiov fingerprint calibration now works on AOSP. If your X7 Pro has that sensor,
  this is the build you were waiting for.
- Signed build, Vanilla flavour, so no Google apps inside.

## What you need before you start

- `vendor_boot.img` from the download link for this build.
- The crDroid 12.5 zip for the POCO X7 Pro.
- A PC with ADB and fastboot, or Termux on a second phone if you want to skip the
  PC entirely.
- The ADB and fastboot driver installed, and USB debugging switched on.
- A full backup. Every step here wipes data.
- MindTheGapps or a Magisk zip, only if you actually want them.

That last backup line is not boilerplate. Format data is a step in this process,
not a risk at the end of it.

## Step 1 - put vendor_boot where your tools live

Download `vendor_boot.img` into the same folder as `fastboot.exe`. Not Downloads,
not the desktop. Keeping it beside the tools means the commands below find it
without a path fight, which is a small thing that saves real time.

## Step 2 - boot into fastboot

Power the phone off, then hold Volume Down and Power until the fastboot screen
appears. Plug it into the PC and confirm with:

`fastboot devices`

You want a long serial number and the word `fastboot`. No serial number means the
driver is missing, and no amount of retrying will fix that. Sort the driver out
first.

## Step 3 - flash vendor_boot to both slots

`fastboot flash vendor_boot --slot=all vendor_boot.img`

The `--slot=all` part matters. This phone has two slots, and flashing vendor_boot
to only one of them is how people end up in a boot loop that takes an hour to
unpick. Let it write to both.

## Step 4 - reboot and catch recovery with your own thumb

`fastboot reboot`

The second the screen goes dark, hold Volume Up. That is how you land in recovery
on this device.

Now the warning the whole article exists for. Do not type `fastboot reboot
recovery`. On the X7 Pro that command can hard brick the phone, and I mean the
kind where it does not come back. Hold the volume key yourself and go in the slow,
predictable way.

## Step 5 - format data, properly

In recovery: Factory reset, then Format data. Both. Factory reset alone leaves
the encrypted data in place, and that is why some people stare at the boot logo
forever. Format data is the step that clears it.

## Step 6 - sideload the ROM

In recovery, pick Apply update, then Apply from ADB. On the PC, run:

`adb sideload` followed by the crDroid zip name.

Let it run all the way to 100 percent. If it stalls early, it is usually an old
platform-tools package, so update ADB and try again.

## Step 7 - say yes, then add GApps if you want them

When the sideload finishes, recovery returns and asks whether you want to install
extra packages. Choose yes. This is your one window in this session to flash
MindTheGapps or Magisk, because this is a Vanilla build. Skip it and you have no
Play Store until you go back into recovery and do it again.

## Step 7b - or use the no-PC route

If you would rather not sit at a PC at all, the Termux route does the same job
from a second Android device. Same commands, just typed on hardware you already
carry. The link is in the downloads section if you want that path.

## Where people get stuck

- **Typing fastboot reboot recovery.** It can hard brick this phone. Hold Volume
  Up instead and go through recovery by hand.
- **Leaving your fingerprint and lock screen settings in place.** Remove the PIN,
  pattern and fingerprint before you flash, or the sensor can misbehave after
  boot. This is especially true if you use a jiiov sensor and you want the new
  calibration.
- **Skipping Format data** and then wondering why it loops on the boot logo.
- **Forgetting GApps** on a Vanilla build, then hunting a Play Store that was
  never installed.

## First boot and after

Give the first boot a few minutes. A fresh Android 16 install with a clean data
partition takes longer than a dirty flash, and that is normal, not a sign that
something broke. Finish the setup wizard before you start restoring files, so
anything that is going to misbehave does it on an empty phone.

If the driver side of this feels like the annoying part, the free Rom Flasher
tool on GitHub bundles the ADB and fastboot driver install into a couple of
clicks, so you are not hunting through Device Manager. It is free, and the link
is in the downloads section.

::faq
Q: Can I use fastboot reboot recovery on the POCO X7 Pro?
A: No. That command can hard brick the phone. Run fastboot reboot and hold Volume
Up the moment it restarts, so it enters recovery the normal way.

Q: Is crDroid 12.5 a GApps build?
A: No, it is Vanilla, so Google apps are not included. Sideload MindTheGapps in
the same recovery session, right after the ROM, or you will have no Play Store.

Q: How do I install this without a PC?
A: Use Termux on a second Android phone and flash the same files from there. The
steps are identical, you just replace the PC terminal with the Termux one.

Q: Do I have to format data?
A: Yes, and format data is not the same as a factory reset. Skip it and the phone
usually hangs on the boot logo because the old encrypted data is still there.

Q: What does eng-preloader change?
A: It shifts the flash order, so do not follow an older crDroid guide from a
previous build. Flash vendor_boot with --slot=all first, then reboot into recovery
and sideload the ROM the way the steps above describe.
