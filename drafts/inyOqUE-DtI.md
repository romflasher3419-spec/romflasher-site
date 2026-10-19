::summary
Evolution X 11.5.3 is an unofficial Android 16 build for the POCO X7 Pro (Rodin), flashed from a PC. You push vendor_boot to both slots, catch recovery with Volume Up, format data, then sideload the zip. Two jobs come before the download: back up your IMEI, and remove your fingerprint and lock screen.

::body
I want to start with the two things that ruin this install, because they have nothing to do with the flash itself. The first is your IMEI. Back it up before you touch anything. The second is your lock screen and fingerprint. Remove both. People skip that step, then report sensor problems after first boot, and it is almost always this.

That done, the flash is short. This is an Android 16 build on a QPR1 base, the build is signed and SELinux stays enforcing. That combination is what makes it reasonable to run as a daily driver instead of a weekend experiment.

## What you need

- The **ROM zip**. There is a Vanilla build and a GApps build. Pick one. Do not flash both.
- The **vendor_boot.img** for this exact device.
- A **PC with working ADB and fastboot**, drivers included.
- The **recommended 3.0.0.8 firmware base** in place before you start.
- IMEI backed up, fingerprint and lock screen removed.
- A cable you trust, a battery above 50%, and a backup of your files.

## A note on vendor_boot before you flash

Where your phone came from decides which vendor_boot you use. If you are moving off 2.0.0.X firmware, use the vendor_boot that ships with this build. Do not grab one from somewhere else because it looks newer. The 3.0.0.8 base is the recommended starting point for this release, and the flash guide goes through it properly.

## Step 1 - boot to fastboot

Power off, then hold **Volume Down + Power** until fastboot appears. Connect the phone and confirm it is seen:

`fastboot devices`

## Step 2 - flash vendor_boot to both slots

`fastboot flash vendor_boot --slot=all vendor_boot.img`

Both slots, not one. The phone boots from whichever slot it likes, and the recovery has to match on both.

## Step 3 - reboot and catch recovery

Run `fastboot reboot` and hold **Volume Up** the moment you do. There is a real window here and it is easy to miss. If you miss it, the phone carries on into the Android setup and you start the step again. Annoying, not damaging.

## Step 4 - wipe properly

In recovery, do a **factory reset**, then **format data**. Both. Format data is the one people try to skip, and it is the one that prevents strange app behaviour on first boot.

## Step 5 - sideload the ROM

Go to **Apply update**, then **Apply from ADB**, and from the PC:

`adb sideload your-rom.zip`

Let it finish without moving the cable.

## Step 5b - Magisk or GApps, only if you want them

Recovery offers this while it is still in sideload mode. Magisk first: rename the `.apk` file to `.zip` and sideload that. GApps only if you downloaded the Vanilla build. If you took the GApps build, skip that part entirely.

## Step 5 - step 5 done? Then boot it

Reboot to system and leave it. First boot on a QPR1 base takes a few minutes and may restart once on its own. Let the setup wizard finish before you start restoring anything. If something is going to break, it is better breaking on an empty phone.

## Where people get stuck

- **Missing the Volume Up window.** The phone boots into the system and the whole thing starts again.
- **The wrong vendor_boot.** Coming from 2.0.0.X, use the one provided with this build rather than a newer-looking one from elsewhere.
- **Skipping the lock screen and fingerprint removal.** This is the classic cause of fingerprint trouble after first boot.
- **Jio users.** There are special instructions in the flash guide for you. Read those before starting, not after.

## What it is like to use

Evolution X on this base feels close to stock Android with the extras you would otherwise look for separately. The customisation is there, but nothing feels bolted on. Because the build is signed and SELinux is enforcing, apps that care about system integrity behave more like they do on a stock phone.

## One honest paragraph

Unofficial means exactly that. The maintainers credited on this build do good work, but you are running something that is not from your phone's maker, and the first day will have small rough edges. Do the IMEI backup. Do the fingerprint removal. Come at it with a proper backup and the whole thing is uneventful.

If you would rather not hand-install ADB and the fastboot driver on Windows, the free Rom Flasher tool does that part for you. It is free, and the link sits in the downloads section.

::faq
Q: Should I use the Vanilla build or the GApps build?
A: Pick one before you flash. Take the GApps build if you want Play services included from the start, or the Vanilla build if you prefer to add only what you need. Do not sideload GApps on top of the GApps build.

Q: Why do I have to remove my fingerprint and lock screen first?
A: Because leaving them in place is the usual cause of fingerprint problems after the first boot on this ROM. Remove the fingerprint and the lock screen before you start, then set them up fresh once Android finishes setting up.

Q: Do I really need to back up my IMEI?
A: Yes, do it before anything else. A backup costs you a couple of minutes, and it is the only copy you will have if something goes wrong with the flash.

Q: Which firmware base should I be on?
A: The recommended base is 3.0.0.8, and the flash guide walks through it. If you are coming from 2.0.0.X firmware, use the vendor_boot provided with this build rather than one from a different release.

Q: Why does the phone boot to Android instead of recovery?
A: You missed the Volume Up window. After `fastboot reboot`, hold Volume Up straight away. If the phone reaches the setup screen, boot back to fastboot and run the step again.

Q: Is Evolution X 11.5.3 good enough for daily use?
A: On this base it is signed, SELinux is enforcing, and the install is a standard sideload, so it holds up for everyday use. Keep in mind it is an unofficial build, so small issues are possible and you should have a backup handy.
