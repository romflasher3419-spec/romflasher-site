::summary
AfterLife OS on the Poco X7 Pro (rodin) is an official Android 16 build with Gapps baked in, a signed system image and SELinux left enforcing. Here is how the clean flash goes, what works on day one, and the two quirks you should know about before you start.

::body
The Poco X7 Pro is a phone that invites custom ROMs. It is quick, it has room to spare, and stock HyperOS keeps adding things you did not ask for. So you start looking at Android 16 builds and the usual question shows up: which one do I actually trust?

AfterLife OS is a decent answer. It is official for rodin, it is signed, and it ships with Gapps already inside. That last part matters more than people admit. On most custom ROMs you flash the ROM, reboot, discover Play Store is missing, then go hunting for a separate Gapps package that has to match your Android version exactly. Here you skip that whole evening.

This is a review and a flash guide in one. The flash itself is not hard. What trips people is treating it like a dirty flash.

## What you need before you touch anything

- The AfterLife OS build for the Poco X7 Pro, plus the vendor package from the same download page.
- A working recovery. Most Android 16 builds for this device get sideloaded from recovery rather than pushed with fastboot.
- Platform tools on a PC, with the phone driver installed so `adb` sees it. If Device Manager shows an unknown device, fix that first.
- A cable that stays put, and a battery above half.
- Your IMEI written down somewhere that is not the phone.
- A backup. A clean flash means the phone comes back blank.

That IMEI point sounds like something old tutorials say. It is not. If a flash goes wrong and you have no IMEI recorded, getting the phone back on a network turns into a much bigger problem. One photo of the box label or the About screen is enough.

## Step 1 - back up, for real this time

Copy photos, videos and anything in internal storage to your PC or a cloud folder. Then note your IMEI. If the phone still boots, do it now. Do not trust a backup you have not opened and checked.

## Step 2 - unzip and check what you actually have

Extract the ROM zip with 7-Zip or WinRAR, not the built-in Windows extractor, which sometimes flattens the folder structure and leaves you with loose files. Same for the vendor package. If the ROM archive is an image-based zip meant for sideloading, you will not find a flash script inside it, and that is correct.

## Step 3 - get into recovery

The exact key combination depends on what is already on the phone, but the reliable order is: power off, then hold the volume key for recovery while you power on, and release when the screen lights up. If a custom recovery is already installed, this is easy. If the phone is on stock HyperOS with a locked bootloader, stop and handle unlocking first, because unlocking erases everything.

## Step 4 - format data, then sideload

Format data in recovery. This is the part that makes it a clean flash, and on this build it is not optional. Then choose the sideload option in recovery and send the ROM from your PC. Some recoveries let you drag the zip straight into the terminal window instead.

While it runs, keep the cable still. The screen will look like it is doing nothing for a while. That is normal.

## Step 5 - first boot and setup

The first boot after a clean flash is slow, and it can look stuck on a logo for several minutes. Leave it. When the setup wizard appears, sign in and restore. Because Gapps are built in, Play Store is there and waiting, no extra flash required.

## What works on day one

- Play Store and the usual Google apps, straight after setup.
- WhatsApp voice calls. This is the fix worth calling out. If you have ever had a call connect with total silence on a custom ROM, you know how irritating that is. On this build, calls behave.
- SELinux stays enforcing. That is a good sign for stability and for the apps that quietly check it.
- The build is signed, which means it is not an unsigned test zip someone assembled on a laptop at midnight.

## What is rough around the edges

- The camera. Specifically, Aperture has known quirks right now and needs a workaround. If the camera is the main reason you own this phone, factor that in.
- The fingerprint reader. Behaviour depends on which sensor your particular unit shipped with. Some people report it fine, some report it fussy. It is a hardware variant thing, not something you can flash away.

Neither of these makes the build unusable. You just deserve to know before you spend an hour.

## Who should install it

If you want Android 16 on the Poco X7 Pro with Google apps already in place, without hunting down a separate Gapps package, this is the build I would hand you. It is the hassle-free pick of the Android 16 options I have tried on this device.

If a fully working camera app out of the box is a dealbreaker, wait a build or two, or keep stock. And if you were hoping to skip the data wipe, this one is not for you. Clean flash is non-negotiable here.

## A couple of honest notes

Budget a full hour, not twenty minutes. The sideload itself is quick, but the first boot, the setup wizard and the app restore are not, and rushing that part is how people end up with a half-restored phone they blame on the ROM.

Also: root is not included. If you want Magisk or KernelSU Next, that is a separate job after the ROM is settled. Do not flash both in one sitting. Get the ROM booting first, use it for a day, then root.

::faq
Q: Do I need to flash Gapps separately on AfterLife OS?
A: No. Gapps are built into this build for the Poco X7 Pro, so Play Store shows up right after setup. That is one of the main reasons to pick it over a bare AOSP build.

Q: Can I dirty flash AfterLife OS over my current ROM?
A: No. Clean flash is mandatory, which means formatting data in recovery before you sideload. Dirty flashing over a different ROM usually ends in bootloops or a phone that boots with broken system services.

Q: Is root included in AfterLife OS?
A: No. The build is clean, so you flash Magisk or KernelSU Next yourself if you want root. Let the ROM boot and settle first, then root as a separate step.

Q: Will my data survive the flash?
A: No. A clean flash wipes internal storage completely, so the phone comes back to the setup wizard. Back up your files and note your IMEI before you start.

Q: Is SELinux set to permissive?
A: No, it stays enforcing. That is what you want, because apps that check the system state behave better when SELinux is enforcing, and it is a sign the build is not cutting corners.
