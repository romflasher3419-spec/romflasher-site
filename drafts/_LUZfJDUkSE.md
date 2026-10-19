::summary
LineageOS 19.1 on the Xiaomi 11T Pro installs from recovery in four moves: format data, reboot back into recovery, sideload the ROM zip over ADB, then reboot to system. Google apps and root are a separate second pass afterwards. Step one wipes all internal storage, so take the backup seriously.

::body
LineageOS 19.1 is the clean pick for the 11T Pro. No vendor skin, no background services you did not ask for, just the system doing its job. This is the exact order I used, and the order is short enough that people rush it — then they end up with a half-broken system and wonder which step they got wrong.

The one thing I will say twice: step one wipes everything on the phone. Internal storage goes, and there is no undo. Take the backup before you start, not while you are mid-flash.

## Before you flash

- A full backup of your photos, downloads and anything else you care about. Internal storage is wiped and that is not a scare tactic.
- A custom recovery of your choice. TWRP and OrangeFox both work for this.
- Platform Tools on the PC, so ADB sideload can talk to the phone.
- A charged battery, and a cable that is not falling apart. Most mid-flash failures are the cable, not the ROM.
- The LineageOS 19.1 zip for the 11T Pro, from the link below.

## Step 1 - back up, because everything goes

Copy your photos, your downloads and anything you would be upset to lose off the phone. Then check the copy opened properly on the other side. An unverified backup is not a backup.

This is the step people skip and then remember during the wipe. Do not be that person.

## Step 2 - format data and reboot recovery

Boot into recovery. Choose format data, which is the full wipe, not the ordinary factory reset option — they are not the same thing. Then reboot back into recovery before doing anything else.

That reboot in the middle matters. Formatting data can leave the recovery session in a state where a sideload fails or lands oddly. Coming back in fresh avoids the whole class of problem.

## Step 3 - sideload the ROM

With recovery running again, select apply update from ADB. Then from the PC, in the folder where your ROM zip sits:

`adb sideload <rom zip>`

The phone shows progress and the terminal shows a percentage. Let it get to the end. The first boot after this takes a while because everything is being built fresh.

## Step 4 - reboot to system

Reboot and wait. When the setup wizard appears, LineageOS 19.1 is installed and you are done with the base flash.

Set the phone up enough to check that calls, mobile data and Wi-Fi work before you pile anything else on top. If something is broken, you want to find out now, not after restoring two hours of data.

## Optional pass - Google apps or root

This is the part people rush. Slow down here.

1. Reboot back into recovery after the ROM flash. Lineage recovery can take a good while to appear and it looks like it has hung. It gets there. Wait.
2. Select apply update, then apply from ADB, and sideload your Google apps package or your root package. Google apps must match Android 12.1 and ARM64, or you will get a broken Play Services install that is very annoying to unpick.
3. If Lineage recovery complains about a mismatching signature, that is normal. Tap continue and let the sideload finish.
4. Reboot to system and you are done.

Order matters in that second pass. Google apps and root both modify system, and doing them in one recovery session without a clean reboot between the main flash and them is where half-installed builds come from.

## Where people get stuck

- **Flashing Google apps from the wrong Android version.** On Android 12.1 you need a Google apps package built for 12.1 and for ARM64. The wrong architecture or the wrong version gives you a system that boots but has constant Play Services errors.
- **Missing the recovery reboot.** Sideloading straight after formatting data, without coming back into recovery, is a common source of a failed or partial install.
- **Panicking at the Lineage recovery screen.** It is slow to appear. Give it time rather than pulling the battery.
- **Forgetting the backup.** There is no recovery from this one. The wipe is not reversible.

## An honest note

LineageOS 19.1 will not win an award for excitement. It is stable, it is light, and it does what it says. The effort is all in the setup, especially if you want Google apps on top, and that second pass is where the fiddly parts live: version matching, the recovery being slow, and the signature warning that looks scarier than it is.

If you are not sure yet whether you want Google services, flash the ROM first and live with vanilla for a day. Adding Google apps later is the same sideload, and you get to know whether you need them at all.

If the PC side of this is where you always stall — ADB, fastboot and the driver — the free Rom Flasher tool on GitHub sets that up in a couple of clicks, and the link is in the downloads list.

::faq
Q: Which recovery should I use for LineageOS 19.1 on the 11T Pro?
A: TWRP and OrangeFox both work here, and Lineage recovery works too since the ROM is sideloaded through it. Use whichever you already trust, as long as it is current for your device.

Q: Do I format data once or twice?
A: Once. Format data, reboot back into recovery, then start the sideload from that fresh session. The reboot is the part that matters, not a second format.

Q: Is Google apps mandatory on LineageOS 19.1?
A: No, LineageOS boots and works fine without it. If you do want Google services, the package has to be for Android 12.1 and ARM64, and it is flashed afterwards as a separate sideload.

Q: Why does the recovery take so long to appear?
A: Lineage recovery is known for a slow start after a ROM flash. It is not hung. Give it time rather than pulling the battery, and it will come up.

Q: What does the signature mismatch warning mean during sideload?
A: It means the package is signed with a different key than the recovery expected. That is normal for a Google apps or root sideload. Tap continue and let it finish.

Q: Will flashing this wipe my photos?
A: Yes. Formatting data clears all internal storage, so every photo, download and file on the phone goes. Copy everything off first and check the copy actually opens before you start flashing.
