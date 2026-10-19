::summary
HyperOS 4 RODIN Edition is running on the POCO X7 Pro, and you can install it
straight from the Android tool on the phone with no PC and no Termux. You flash
the recovery image, format data and sideload the ROM. Here is what is new, how it
feels, and whether it is worth flashing.

::body
HyperOS 4 for the POCO X7 Pro exists in a RODIN Edition build, and the way you
install it is the interesting part. There is no PC involved and no Termux. The
whole job runs from the Android tool on the phone: pick the ROM, boot to
fastboot, flash, and you are done. I used OrangeFox R12.0 for the recovery side
and kept every step on the device itself.

I installed it, booted it and lived with it long enough to have an opinion. Here
is the whole thing, honestly.

## What it looks like

You notice HyperOS 4 in the interface before you notice anything else.

- Glass effects across the system, used heavily
- Cleaner notifications than before
- Widgets you can resize and edit properly
- Folders you can actually shape instead of just dumping apps in
- A pile of small touches that lean toward iOS in places

The AI additions are in there too, and so is the performance work. Once the phone
settles after the first hours, the animations are smooth.

## What changed under the hood

Beyond the paint job, the build is the latest HyperOS 4 release for RODIN, and it
carries the performance tuning that comes with it. I am not going to pretend I
can measure that with a stopwatch. What I can say is that after the first day it
stopped feeling like a fresh install and started feeling like a phone.

## What is broken or worth knowing

Nothing fell over for me during normal use, but there are two things to keep in
mind:

- First boot takes a long time. Longer than a normal restart by a lot. Do not
  panic, and do not pull the cable.
- Dirty flashing this build is asking for a bootloop. Format data. Every time.

That is a short list, and that is a good sign for a build this recent.

## What you need

- A POCO X7 Pro (rodin) with an unlocked bootloader
- The HyperOS 4 RODIN Edition zip
- The OrangeFox R12.0 recovery image
- The Rom Flasher tool installed on an Android phone
- A full backup of your photos, chats and files

Note the RODIN part. If you grab a zip built for another phone, it will not go
well. This is for the POCO X7 Pro only.

## Step 1 - get the files into one folder

Download the ROM zip and keep it somewhere you can find again, in a single
folder. Hunting for a file halfway through a flash is how mistakes happen.

## Step 2 - connect the phone and open the tool

Connect the phone and open the tool. Send the device to fastboot mode from there.
No PC, no command window, no driver wrestle.

## Step 3 - flash the recovery image and boot into recovery

Flash the OrangeFox recovery image, then boot into recovery. Give it a moment to
come up the first time.

## Step 4 - format data

Format data, then go back to the main recovery menu. This step is not optional
here. Skip it and you get a bootloop, and then you get to do it all again.

## Step 5 - sideload the ROM

Choose Apply update from ADB, then sideload the ROM zip and let it run all the
way to the end. Do not touch the cable while it is moving.

## Step 6 - reboot and wait

Reboot to system and let the first boot take its time. This is the step where
people get impatient and start pressing buttons. Do not. It will come up.

## Where people get stuck

- **Skipping the data format.** Dirty flashing this build is the number one
  cause of a bootloop.
- **Using a zip for another phone.** RODIN only. The build is device specific.
- **Losing the cable connection mid-flash.** If it drops, unplug, reconnect and
  redo the step rather than hoping it finished.

## Who should install it

If you like being on the newest HyperOS and you want the interface changes now
rather than later, this is a good build to run. It is also the easiest install I
have done on this phone, purely because nothing touches a computer.

If your phone is the thing you depend on and you do not want to spend an evening
on a fresh setup, there is no rush here. The build is not going anywhere, and
waiting a version or two costs you nothing but patience.

If you have never used the tool before, install it before you start the flash
rather than in the middle of it. The free Rom Flasher tool handles this whole
no-PC flow, and the link is in the downloads section.

::faq
Q: Can I install HyperOS 4 on the POCO X7 Pro without a PC?
A: Yes. This build flashes from the Android tool on the phone, with no PC and no Termux involved. You flash the recovery image, format data and sideload the ROM from the device.

Q: Which recovery do I need for HyperOS 4 RODIN Edition?
A: OrangeFox R12.0. Flash the recovery image first, boot into recovery, and then sideload the ROM zip from there.

Q: Is a clean flash required for this build?
A: Yes. Format data before sideloading. Dirty flashing this ROM leads to a bootloop, so do the format even when it feels like extra work.

Q: Why does the first boot take so long?
A: The phone is setting up the new system and rebuilding caches, so the first boot is much slower than a normal restart. Keep the cable connected and wait it out.

Q: Can I flash this build on another POCO phone?
A: No. It is the RODIN Edition, built for the POCO X7 Pro only. A zip for a different phone will not work, so match the device before you download.
