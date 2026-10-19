::summary
Elite Rom on the Xiaomi 11T Pro is a MIUI-based build that gets flashed from a custom recovery, not from fastboot. You need an unlocked bootloader and a working recovery already in place, then it really is five steps: flash the zip, reboot back to recovery, wipe data, reboot. The only step people skip is the one that matters.

::body
Here is the situation you are probably in. You have a Xiaomi 11T Pro that is already unlocked and already running a custom recovery, and you want a MIUI build that behaves a little better than stock without leaving MIUI behind. Elite Rom is that. It sits on top of MIUI, so the control centre, the settings tree and the gestures all feel familiar. What changes is the polish and the extras underneath.

The whole flash happens on the phone. You put the zip on storage, you boot into recovery, and recovery does the work. No PC needed in the middle of it, which is the part that surprises people who are used to fastboot flashing.

## What you need before you touch anything

- A Xiaomi 11T Pro with an unlocked bootloader. This is the gate. Without it, nothing else works.
- A working custom recovery already installed. Elite Rom flashes from recovery, so if recovery is not there yet, that is the job you do first.
- The Elite Rom zip for your device, from the link below.
- Enough charge to get through the first boot. That boot is the slow one.
- A backup. Step four wipes your data and there is no way around it.

## Step 1 - reboot to recovery

Power off, then hold the volume up and power keys until recovery appears. Use whatever key combination your recovery was installed with, because on the 11T Pro it is easy to overshoot and land in fastboot instead. If you see the fastboot screen, hold power until it switches off and try again.

Get to the recovery menu and stop. Do not start poking at wipe options yet.

## Step 2 - flash the zip file

In recovery, choose the option to install or apply a zip from storage. Pick the Elite Rom zip you copied onto the phone. Let it run to the end without interrupting it. The progress bar will sit still for a while, and that is normal for a MIUI-based package of this size.

When it finishes, the recovery message will say it is done. Read it before you touch anything else.

## Step 3 - reboot back into recovery

This is the step that decides whether you spend the evening staring at a boot loop. Boot back into recovery. Do not boot into system.

The reason is simple. The flash has just replaced the system, and the phone is still holding things from the old install in memory and in the data partition. Booting straight to system from here is what makes people think the ROM is broken.

## Step 4 - wipe data

Now you wipe. In recovery that is usually called format data or factory reset. This is the step that erases everything on internal storage, so if you skipped the backup, this is your last moment to change your mind.

A dirty flash, meaning a wipe you skipped, is not worth the risk coming from another ROM. Different bases leave different leftovers, and those leftovers are exactly what causes odd crashes a day later.

## Step 5 - reboot and wait

Reboot to system and leave the phone alone. The first boot on a MIUI-based ROM takes a few minutes. The screen may sit on the logo longer than you expect. People pull the cable or force a restart far too early here and then blame the ROM.

Once it lands, you get the setup wizard and a clean phone. Set it up fresh and check the things you actually use: calls, camera, banking apps. Then restore your data.

## Where people get stuck

- **Skipping the recovery reboot.** The order above is flash, reboot to recovery, wipe. If you wipe right after the flash without that reboot in between, you are likely to hang on boot.
- **Wiping before the flash instead of after.** Same idea, different order. The sequence that works is the one written above.
- **Pulling the plug on the first boot.** A few minutes of logo is normal. Ten minutes of logo with no change is when you start thinking about it.
- **A recovery that is too old for the build.** If recovery throws an error partway through the zip, check you are on a current recovery for your device rather than an old one you had lying around.

## One honest note

Elite Rom is a MIUI build at heart, so do not expect the smoothness of a clean AOSP ROM. The extras are the reason to run it. If you want a lighter, more bare system, an AOSP-based build will feel quicker, but you lose the MIUI features you are used to.

If setting up ADB, fastboot and the driver is the part that always trips you up, the free Rom Flasher tool on GitHub handles that side in a couple of clicks, and the link is in the downloads list.

::faq
Q: Do I need a PC to flash Elite Rom on the Xiaomi 11T Pro?
A: No, not for the flash itself. You copy the zip onto the phone, reboot into custom recovery and flash it there. A PC is only useful before this stage, when you are unlocking the bootloader or installing recovery.

Q: Do I have to wipe data?
A: Yes, that is step four and it is not optional. Coming from another ROM without a wipe leaves old data behind, and the system will misbehave or hang on boot. Back up photos, downloads and anything else you care about first.

Q: Why does my phone boot loop after flashing Elite Rom?
A: Usually the reboot back into recovery was skipped. The order is flash the zip, reboot to recovery, then wipe data, then reboot to system. Do the recovery reboot in between and the loop goes away, which means a clean reflash in the right order.

Q: Which recovery should I use for the 11T Pro?
A: Any working custom recovery built for the 11T Pro. The important part is that it is current, not a version you downloaded months ago. If the zip fails partway through, the recovery is the first thing to check.

Q: What happens to my apps and files?
A: They are gone with the data wipe. Internal storage is reset, so you start with the setup wizard and a clean phone. Restore your backups only after the first boot has fully finished and you have checked that calls and data work.

Q: Can I flash this from fastboot instead?
A: Elite Rom for this device is meant to be flashed from recovery, so stick to that route. Fastboot flashing belongs to the fastboot ROM packages, which is a different method for a different kind of file.
