::summary
You can roll back from HyperOS 3 to HyperOS 2 on a Xiaomi or POCO phone with the
official fastboot ROM and Mi Flash Tool. It wipes internal storage, so back up
first, and the one thing that matters most is the option at the bottom of the
tool: pick Clean all, never Clean all and lock.

::body
So HyperOS 3 did not sit right with you. Maybe the battery drops faster than it
used to, maybe the phone warms up on things that used to be fine, or maybe one
annoying bug followed you through two updates and never got fixed. Whatever it
is, you are sitting on a build you do not want, wondering if going back means
living on a custom ROM forever.

It does not. HyperOS 2 is still available as an official fastboot ROM, and the
rollback is a normal flash. You need an unlocked bootloader, a full backup off
the phone, and about twenty minutes. What you do not need is patience for a
weekend of command line work.

## Read this part before the steps

A fastboot ROM flash through Mi Flash Tool writes the whole image. Internal
storage is gone. Photos, downloads, your chat backups, the lot. If that is not
a trade you want, stop here and live with the bug.

## What you need

- The **HyperOS 2 fastboot ROM for your exact model and region**. Not a ROM
  from another phone, not a recovery zip. Model and region both matter.
- **Mi Flash Tool** installed on a Windows PC.
- The **ADB and fastboot driver**, so the PC actually sees the phone.
- Your **bootloader unlocked**. If it is not, unlock it first. That itself wipes
  the phone, so do it before you get attached to any data.
- A **full backup**, already moved off the phone and onto something else.
- Enough charge to get through the flash without the phone dying.

## Step 1 - get the right fastboot ROM

Download the HyperOS 2 fastboot package for your exact model and region. These
files are large, usually several gigabytes. Extract it with 7-Zip or WinRAR into
a folder you can find again, and check the extraction actually produced the image
files and the flash scripts rather than a folder full of loose leftovers.

If the package is small and contains a recovery style updater instead of raw
images, you grabbed the wrong one.

## Step 2 - boot into fastboot

Power the phone off completely. Hold **Volume Down + Power** until the fastboot
screen appears. Plug it into the PC and confirm Windows sees it. If it shows as
an unknown device, fix the driver now rather than halfway through a write.

## Step 3 - load the ROM folder into Mi Flash Tool

Open Mi Flash Tool and point it at the folder you extracted. Select the folder
itself, not the zip. Hit refresh so the tool picks up your connected device, and
wait until it actually lists a device before you go any further.

## Step 4 - choose Clean all, and only Clean all

This is the whole article in one line. At the bottom of the tool you get options.
Choose **Clean all**.

Never choose **Clean all and lock**. That option relocks the bootloader during
the flash. If anything goes wrong while it is writing, you end up with a locked
bootloader and a phone that will not boot, and getting out of that is far worse
than the bug you were trying to escape.

The third option, the one that saves user data, is not what you want here either.
A rollback across a major version is exactly the case where a clean slate helps.

## Step 5 - flash, then leave it alone

Hit flash. The tool starts writing partitions and printing progress. Some parts
take a while. Do not unplug the cable. Do not close the window. Do not tap the
phone to check on it.

When it finishes, the phone reboots into HyperOS 2 and drops you at the setup
wizard. Finish the wizard first, get a clean boot, and only then start restoring
anything.

## Where people get stuck

- **Clean all and lock.** The single most common way a rollback turns into a dead
  phone. Set the option before you hit flash, not after.
- **Wrong model or region.** The flash stalls partway, or the phone boots to a
  black screen. Match your exact variant.
- **Skipping the backup.** "It is only a rollback" is how people lose three years
  of photos. Internal storage is erased either way.

## One honest note

Applying an older build does not lock you out of updates forever, but the phone
may well offer HyperOS 3 again the next time it checks. If it does, that is a
separate decision, and you can decline the update or let it install. Going back
is not a permanent statement. It is just getting your phone usable again today.

If the driver side of this is the part that keeps failing, the free Rom Flasher
tool bundles the ADB and fastboot driver install into a couple of clicks so you
are not hunting through Device Manager.

::faq
Q: Will I lose my data going from HyperOS 3 back to HyperOS 2?
A: Yes, everything on internal storage. The fastboot flash writes the full image,
so photos, files and app data are all gone. Move what matters to a PC or cloud
before you start.

Q: What is the difference between Clean all and Clean all and lock?
A: Clean all wipes the phone and leaves the bootloader unlocked. Clean all and
lock also relocks the bootloader during the flash, which can leave you with a
phone that will not boot and is much harder to recover.

Q: Can I roll back to HyperOS 2 without unlocking the bootloader?
A: No. The fastboot route needs an unlocked bootloader. Unlocking itself erases
the phone, so do that step first and treat it as part of the same job.

Q: Do I need a custom ROM to get off HyperOS 3?
A: No. HyperOS 2 is an official fastboot ROM, so you can go back to stock without
installing anything custom. That keeps updates and normal phone behaviour intact.

Q: My phone will not boot after the flash. Is it dead?
A: Not usually. If the flash completed and it still will not boot, go back into
fastboot and redo the flash with the correct model and region ROM, and make sure
you used Clean all rather than Clean all and lock.

Q: How long does the rollback take?
A: Around twenty minutes on a normal machine once the ROM is downloaded. The
download and extraction usually take longer than the flash itself.
