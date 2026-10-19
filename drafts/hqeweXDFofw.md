::summary
MistOS v4.6 Lucent is an iOS-style Android 16 QPR2 build for the POCO X7 Pro (rodin), and it flashes through vendor_boot and sideload like the other AOSP builds on this phone. Remove your lock screen password and fingerprints before you start, or you will be the next person reporting a fingerprint problem after first boot.

::body
The whole pitch of MistOS v4.6 Lucent is the look. Transparent glass panels, iOS-style motion in the animations, and a home screen that does not look like anything else on this phone. If you have ever wanted your POCO to feel like a different operating system the moment you unlock it, this is the build that tries it.

It is an UNOFFICIAL build on an Android 16 QPR2 base, and it is the first release under this version. So expect an early-build edge here and there. Nothing about that is a reason to avoid it, as long as you know what you are walking into.

## What it looks like

The whole pitch is the glass. Panels are translucent, and the animation style leans on iOS motion rather than AOSP. It is a very different feel from HyperOS, and it is the reason to try this build at all.

The rest of it is a normal Android 16 base underneath, so your usual apps and setup do not change.

## What you need first

- The MistOS v4.6 Lucent ROM zip, GApps build.
- The vendor_boot image for the POCO X7 Pro (rodin).
- The boot and init_boot images if you want root. They are linked below.
- A PC with working ADB and fastboot, and a driver Windows accepts.
- Your fingerprint and lock screen password removed, and a full backup.

## Step 1 - remove your locks before anything else

Delete your fingerprint and your lock screen password on the phone before you start flashing. This is not paranoia. Skip it and you will be the next person reporting a fingerprint problem after first boot, and that is a messy thing to fix afterwards.

While you are at it, take a full backup. You are wiping data either way, so this is the last chance to get your files off cleanly.

## Step 2 - boot to fastboot and flash vendor_boot

Reboot the phone into fastboot and connect it to the PC. Check it is really there:

`fastboot devices`

Then push the vendor_boot image to both slots:

`fastboot flash vendor_boot --slot=all vendor_boot.img`

## Step 3 - hand-catch recovery

Run a normal reboot:

`fastboot reboot`

The moment the screen goes dark, hold Volume Up and keep holding until recovery comes up. Same routine as every other build on this phone. The shortcut that reboots straight into recovery is not the one to use here.

## Step 4 - format data and sideload

In recovery, format data. Then choose Apply update, then Apply from ADB, and sideload the ROM zip:

`adb sideload <rom zip>`

The transfer is slow for a full ROM. Leave the phone alone while it writes, then let first boot finish on its own.

## Step 5 - optional root

If you want root, this is where the boot and init_boot images come in. Flash them in the same session, in recovery, before you boot into the system for the first time. Doing it later means another round trip.

## Where people get stuck

- **Leaving fingerprint and a lock password in place.** This is the classic one. Remove both before you download anything.
- **Flashing a vendor_boot that does not match this build.** It has to be the image for this ROM and this device, not one from another release.
- **Reporting a bug with no logcat.** If something goes wrong, grab a log. It is the first thing the developer will ask for.

## One honest note

Because this is the first release under this version, expect a rough corner somewhere. Early builds are like that. The flash routine itself is the same one you already know from other Android 16 builds on this phone, so the risk is not in the install, it is in expecting a first release to be perfect.

The battery and first boot are the slow parts. Give it time.

If setting up fastboot and the driver is where you usually stall, the free Rom Flasher tool takes care of that part.

::faq
Q: Do I need to remove my fingerprint before flashing MistOS?
A: Yes. Delete your fingerprint and your lock screen password before you start. Leaving them in place is the most common cause of sensor problems after first boot.

Q: Does flashing MistOS v4.6 Lucent wipe my data?
A: Yes. You format data in recovery as part of the install, so everything on internal storage goes. Take a full backup before you begin.

Q: How do I enter recovery after flashing vendor_boot?
A: Run a plain fastboot reboot and hold Volume Up the moment the screen goes dark. Keep holding until recovery appears instead of using the reboot-to-recovery shortcut.

Q: Is MistOS v4.6 Lucent official?
A: No, it is an UNOFFICIAL build, on an Android 16 QPR2 base, and it is the first release under this version. That is not a problem, it just means you should expect a small rough edge somewhere.

Q: Can I root it?
A: Yes, if you want to. The boot and init_boot images are linked, and the cleanest time to flash them is in recovery in the same session, before the first boot into the system.
