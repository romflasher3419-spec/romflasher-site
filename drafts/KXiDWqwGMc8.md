::summary
E OS 3.2 for the Poco X7 Pro is a two-file job: the ROM zip plus a matching vendor image. Flash the vendor image to both slots over fastboot, boot recovery, factory reset, then sideload the ROM. Do the wipe before the sideload and the two files from the same release, or you will be looking at a bootloop.

::body
E OS 3.2 has landed for the Poco X7 Pro as an advanced secured Android build. The reason this one needs its own guide is simple: there are two pieces to handle, the ROM and its vendor image, and getting those two wrong is how people end up in a loop.

If you have flashed a custom ROM on this phone before, this will feel familiar — fastboot, vendor image, recovery, wipe, sideload. If it is your first time, follow the order exactly and do not rush the data wipe. It is there for a reason.

## What you need

- The **E OS 3.2 ROM file** and its **vendor image**, both from the same release.
- **ADB and fastboot** working on your PC, with the driver installed and confirmed.
- An **unlocked bootloader**.
- A backup of your data and **a backup of your IMEI**.

That last bullet is not boilerplate. Clean flash is the safe path here, so your data is going regardless.

## Step 1 - download both files to your PC

Get the ROM and the vendor file, and get them from the same release. A ROM from one build and a vendor image from another is a mismatched pair, and mismatched pairs cause problems. Keep them together in one folder so you cannot mix them up.

## Step 2 - reboot to fastboot and connect

Reboot the phone into fastboot mode and connect it. Run `fastboot devices` and make sure you get a serial number back. If you get an empty line, your driver is not working and nothing after this will work either.

## Step 3 - flash the vendor image to both slots

Flash the vendor image to **both** slots. Not one. This is the single most common mistake with this ROM, and it is why the recovery sometimes comes up on one boot and not the next. Do both slots, exactly as the instructions say.

## Step 4 - reboot into recovery

Reboot into recovery and confirm you are actually in recovery before you go any further. If it does not come up, go back to step 3 and check the vendor flash.

## Step 5 - factory reset and format data

Factory reset and format data now, before the sideload. Sideloading first and wiping after is the classic route to a looped boot, and it is completely avoidable. Wipe, then flash. In that order.

## Step 6 - sideload the ROM zip

Sideload the ROM zip and let it finish. Do not touch the cable, do not unplug anything, and give it the time it needs. Cheap cables dropping connection halfway through is the third way this job goes wrong.

## Step 7 - reboot to the system

Reboot to system and let the first boot run its course. First boots after a clean flash are slow. That is normal, not a sign of a problem.

## Where people get stuck

- **Flashing the vendor image to only one slot.** The recovery then behaves inconsistently and you chase a fault that is not really a fault.
- **Sideloading before the data wipe.** That usually ends in a looped boot. Wipe first, every time.
- **A cheap cable that drops the connection halfway through.** If the sideload starts and then dies, suspect the cable before you suspect the ROM.

## What to know about this build

E OS is pitched as an advanced secured build, so keep an eye on the ROM thread for the current changelog and any known issues before you flash. Check what has changed since the last release, and check whether anything is currently broken.

Clean flash is the safe path. There is no reason to dirty flash here, and no benefit to it either.

Root is not included by default. If you want it, add it after the ROM is up and running, not during the install.

And keep the vendor and ROM files from the same release. Say it with me.

## If it bootloops

This is recoverable, so do not panic. Go back to fastboot, flash the vendor image to both slots again if you only did one, wipe data, and re-sideload the ROM. In most cases the loop came from the wipe order or the vendor slot, and redoing those two things properly fixes it.

If the driver side is the part you dread, the free Rom Flasher tool on GitHub gets the ADB and fastboot driver installed in a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Do I need both the ROM and the vendor image for E OS 3.2?
A: Yes. This is a two-file flash, and both go on. The vendor image needs to go to both slots over fastboot, then the ROM zip is sideloaded from recovery after the data wipe. Missing either file leaves you with an incomplete install.

Q: Why does E OS 3.2 bootloop?
A: Almost always one of two things. Either you sideloaded before the data wipe, or you flashed the vendor image to only one slot. Go back to fastboot, flash the vendor image to both slots, wipe data, then re-sideload the ROM.

Q: Can I keep my data when flashing E OS 3.2?
A: Do a clean flash. It is the reliable route on this ROM, and a dirty flash across a build like this is where the bootloops come from. Back up your files and your IMEI first, since the wipe is going to happen either way.

Q: Is root included in E OS 3.2?
A: Not by default. The ROM installs without root, and you add root yourself afterwards if you want it. Finishing the ROM install first and adding root on top is the cleaner order.

Q: Will the vendor image from another release work?
A: Do not mix releases. Keep the vendor image and the ROM zip from the same release, because a mismatched pair causes problems and is hard to diagnose. Download both together so they cannot get separated.
