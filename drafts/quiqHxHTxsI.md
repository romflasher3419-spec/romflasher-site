::summary
There are three main ways to install a ROM on an Android phone: the stock-style fastboot ROM, an AOSP build through recovery, and a modded ROM like OxygenOS or DyperOS that needs vendor_boot flashed by hand. Two of them work without a PC if you set up Termux first. Method three is the one that catches people.

::body
Not everyone has a Windows laptop sitting next to the phone. Plenty of people flash ROMs from the phone itself, and for most jobs that is completely fine. What matters is knowing which of the three routes your ROM belongs to, because they are not interchangeable and getting it wrong is how phones end up unusable.

The setup part is short: two APKs, Termux Monet and Termux API, both installed with their permissions granted before you start. Then the flash file from the link. After that everything splits into three paths.

## What you need

- Termux Monet and Termux API, installed with permissions granted. Grant them before you start, not when a command fails and you are mid-flash.
- The Termux flash file from the link, placed where Termux can see it.
- The ROM zip for your device, plus the vendor_boot image if your build needs one.
- USB debugging on if you are going to use a PC, or a working terminal setup if you are not.
- A backup. Every one of these routes has a step that erases data somewhere.
- The habit of reading a command before you run it. Some of these are device-specific.

## Method 1 - the fastboot ROM

This is the stock-style route. You open the flash tool, choose the fastboot flash option, put the phone in fastboot mode, and let it run. The tool handles the partition writes for you, which is exactly why this is the safest of the three for someone who is new to this.

The catch is what it does to your phone. A fastboot ROM flash writes the full image set, so internal storage comes back empty. That is not a bug in the tool. That is the job. Move your photos off first.

Expect it to take a few minutes and print a long list of partition names while it works. Do not unplug. Do not poke the screen to see if it is alive.

## Method 2 - an AOSP ROM through recovery

This route is for clean AOSP builds that come as a flashable zip rather than a fastboot package. Set up the recovery tool first, then flash the recovery and boot images, then send the ROM across.

The order is the part that matters. Recovery and boot images go on before the ROM, because the recovery you already have is usually not the one this build expects. Flashing the ROM first and then trying to fix recovery afterwards is a much harder evening.

Once recovery is in place, the ROM goes across the same way it would from a PC: sideload style, with the phone sitting in recovery and the terminal doing the pushing.

## Method 3 - modded ROMs and the vendor_boot step

This is the one to slow down on. Modded ROMs like OxygenOS and DyperOS do not follow either of the first two routes. Here you flash vendor_boot by hand with the fastboot command, then sideload the ROM.

That manual command is where people get hurt. It is short, it looks harmless, and if it was written for a different device you will find out the hard way. Read it. Check that the file name matches the vendor_boot image you downloaded for your exact model. Do not paste a command out of a forum post for another phone.

Then boot recovery, format data, sideload the ROM, and let it boot. If you skipped vendor_boot, recovery will not mount anything and it will look like the zip is corrupt. It is not. You missed a step.

## Where people get stuck

- **Jumping straight to the ROM.** Both the recovery route and the modded route need something flashed before the ROM itself. Skipping it wastes an hour.
- **A command written for another device.** Fastboot commands that name files and partitions are specific. Copying one from another model's guide is a real way to brick a phone.
- **Forgetting the wipe.** A fastboot ROM flash erases everything. So does formatting data in recovery. People notice when the photos are gone, not before.
- **Permissions not granted.** Termux needs its permissions up front. Granting them halfway through a command run is not a good time.

## One honest note

Doing this entirely from the phone is convenient, and it works. But a PC is genuinely easier for the recovery and vendor_boot routes, because you can see the output scroll by and you are not fighting a small terminal on a touchscreen. If you have any option at all, and the job is method two or method three, borrow a laptop.

If you do go the PC route, the free Rom Flasher tool on GitHub installs the ADB and fastboot driver for you so you are not stuck with an unrecognised device in Device Manager.

::faq
Q: Can I flash a ROM without a PC?
A: Yes. Termux Monet and Termux API give you a terminal on the phone, and two of the three methods here work without a computer. A PC just makes the recovery and vendor_boot steps easier to follow.

Q: Which flashing method is the safest?
A: The fastboot ROM route, because the flash tool does the partition work for you and there is less to type by hand. It still erases your data, so back up first.

Q: Which method bricks people most often?
A: Method three, the modded ROM route, where you flash vendor_boot by hand. A wrong or device-specific command there is the usual cause of a phone that will not boot.

Q: What is vendor_boot and why do I have to flash it?
A: Vendor_boot is a partition that holds device-specific boot pieces, and on Android 16 builds for many devices it has to be flashed before recovery will work. Skip it and recovery cannot mount anything, which looks like a corrupt ROM zip.

Q: Do the fastboot ROM methods erase my data?
A: Yes. A fastboot ROM flash writes the full image, and the recovery methods need you to format data. Internal storage is gone either way, so move your files off the phone before you start.
