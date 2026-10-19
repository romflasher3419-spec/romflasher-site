::summary
You can flash MIUI 13 dev beta 13.1.22.9.5 on the Redmi K50i straight from TWRP, with no PC and no fastboot. Push the zip to internal storage, boot recovery, wipe, format data if recovery cannot read storage, and flash. It is a beta, so expect rough edges.

::body
This is the lazy route to a developer beta, and on this phone the lazy route is the good one. No fastboot, no platform tools, no PC sitting next to you. You push the zip to the phone, boot recovery, and flash it. You can even keep your data if you want to, though I would not count on that working from every starting point.

The build here is MIUI 13 dev beta 13.1.22.9.5 on the Redmi K50i. Developer builds are where you see new MIUI features first. They are also where you meet bugs first. Both of those are the deal, and you should know that going in.

## What you need

- Redmi K50i with an unlocked bootloader. There is no flash without this.
- TWRP for this device, already installed and working. If touch is dead or internal storage reads zero, your recovery is wrong and you should stop.
- The MIUI 13 dev beta zip sitting on internal storage.
- 50% battery or better.
- A backup of your photos and files if you plan to format data. You probably will.

## Step 1 - get the zip onto the phone

Download the beta zip and copy it to internal storage, somewhere you can find it easily. Do not put it on a pendrive or leave it on a PC. Recovery reads it from the phone, and internal storage is the path with the fewest surprises.

Do not extract it. Recovery flashes the zip as-is.

## Step 2 - back up before you wipe

Do this now, not after. Grab your photos, downloads and anything else you would miss and move it off the phone. Copying files out is the only part of this job you cannot undo later.

If you are upgrading from an older MIUI build you might get away with keeping data. If you are coming from a custom ROM, do not even try. You will be formatting.

## Step 3 - boot into TWRP

Power the phone off and boot into recovery with your device combo. You should land in TWRP with working touch and readable storage.

Take a second here and look at the storage line on the main screen. If it shows zero or a nonsense number, TWRP cannot see internal storage, and that changes the next step.

## Step 4 - wipe, and format data if storage is not readable

For a clean install, wipe system, data, cache and dalvik. That clears the way for the new build.

Then the part people skip. If TWRP cannot read internal storage, or you are coming from another ROM, you need to format data, not just wipe it. Format data is the option that actually removes encryption. After a format, internal storage will be empty, and the zip you copied earlier is gone.

That is the trap. If you format data, you have to push the ROM zip again before you can flash. Plan for it — either keep a copy on a USB drive you can read from recovery, or be ready to push the file over from a PC. This is the one step where a PC still helps, even on the no-PC method.

## Step 5 - flash the ROM zip

Back in TWRP, tap Install, pick the MIUI 13 dev beta zip, and confirm. It takes several minutes. Let the progress bar finish on its own. Do not tap anything, do not reboot early, do not conclude it is stuck because the bar has not moved in a minute.

When it finishes, wipe cache and dalvik once more, then reboot to system.

## Step 6 - the first boot and what to expect

The first boot after a MIUI flash is slow. Several minutes of a boot animation is normal. Do not pull the cable, do not hold power, do not assume it is dead. Interrupting this is how people turn a working flash into a bootloop.

## What to expect from this build

- The MIUI 13 look, with the newer widgets and the side bar.
- Developer beta behavior. Features land here first, and so do bugs. An app crash here and there is part of the package.
- Battery life that needs two or three charge cycles before it settles into a pattern.
- Updates that you flash manually. Nobody is pushing these to you over the air.

## Where people get stuck

- **Flashing without formatting data**, then bootlooping straight back into TWRP. If you are coming from a different ROM base, format data.
- **The wrong TWRP for this device**, so touch is dead or internal storage shows zero. A mismatched recovery is worse than no recovery, because it lets you start something you cannot finish.
- **Interrupting the first boot** because it looked stuck for thirty seconds. That thirty seconds can stretch to five minutes and still be fine.
- **Formatting data after copying the zip**, and then finding nothing to flash. Push the file again before you go back to the Install menu.

## Who should try this

Flash this if you want to see MIUI 13 features early and you are comfortable with recovery. Keep your expectations honest, because a developer beta is not a daily driver guarantee.

If your phone is your work phone and everything has to work tomorrow morning, the stable India build is the safer place to be. Going back is simple — flash the stable zip the same way.

If the driver and recovery side is where you normally stall, the free Rom Flasher tool on GitHub puts the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Do I lose my data flashing this MIUI 13 beta?
A: If you format data, yes, and internal storage is cleared. Copy your photos and files off first. If you are upgrading from an older MIUI build without formatting, you may keep your data, but that option is not available coming from another ROM.

Q: Can I flash this without a PC?
A: Yes. The whole method is recovery-based. Copy the zip to internal storage, boot TWRP and flash. The only time you may want a PC is if you format data and need to push the ROM zip back onto the phone.

Q: Can I go back to the stable India MIUI build?
A: Yes. Flash the stable zip the same way through TWRP. Coming from the beta, format data first so you are not carrying beta leftovers into a stable install.

Q: Why does TWRP show zero internal storage on my K50i?
A: Your recovery is not the right one for this device, or it cannot read the encrypted storage. Flash the correct TWRP for the K50i, and remember that if you need to format data, the zip on internal storage will be erased too.

Q: Is MIUI 13 dev beta daily-driver ready?
A: It is a beta, so expect the odd bug and app crash, and give battery life a few charge cycles before judging it. If you need everything to be reliable right now, use the stable build instead.
