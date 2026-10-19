::summary
Project Infinity X 3.5 brings Android 16 to the POCO X7 Pro (rodin) with fixes that matter: Bluetooth calls in Meet, Discord and WhatsApp stopped cutting out, and the front camera now behaves in those same apps. It also swaps in the Infinity dialer and adds Mi Camera. It is a signed GApps userdebug build with SELinux enforcing.

::body
Some updates are a pile of small changes you never notice. This one is not that. Project Infinity X 3.5 fixes two things that quietly ruin a build if you leave them alone: Bluetooth calls dropping in chat apps, and the front camera misbehaving in those same apps.

It is Android 16 for the POCO X7 Pro, codename rodin, signed and userdebug, GApps included, SELinux enforcing.

## What changed in 3.5

- Synced with the latest source
- Fix for Bluetooth calls in Meet, Discord, WhatsApp and similar apps
- Front camera fix in those same apps
- The Infinity dialer, replacing the one that used to stutter
- Mi Camera included
- Minor changes and improvements underneath

The dialer swap is the small one that you will actually feel every day. A stutter when you open the dialer sounds minor until you are calling someone back and it lags while you wait.

## Why the fixes matter more than they look

Bluetooth calls cutting out is the kind of bug that makes you blame your headphones. You try a different pair, then a different app, then you give up and use the phone against your ear. It was the ROM.

The front camera fix is the same story in reverse. Video calls look wrong, you assume the lighting is bad, and you never suspect the build. Both of those are now off the list.

## What you need

- A POCO X7 Pro (rodin)
- vendor_boot.img for this build
- The Project Infinity X 3.5 ROM zip
- A PC with ADB and fastboot, plus the driver
- A backup of your IMEI before you flash
- Battery above half and a cable you trust

## Step 1 - back up your IMEI first

Back up your IMEI before you flash, not after. It takes a few minutes and it is the one backup people only take once they need it.

## Step 2 - flash vendor_boot to both slots

Boot to fastboot and flash vendor_boot to both slots. Both, not just the active one.

## Step 3 - reboot and hold Volume Up for recovery

Reboot, then hold Volume Up to land in recovery.

Do not use fastboot reboot recovery. It can brick the phone on builds like this, and the button hold costs you nothing.

## Step 4 - format data

Format data in recovery. A dirty flash over a different ROM will not give you the fixes you came for, and it usually gives you new problems instead.

## Step 5 - sideload the ROM

Go to Apply update, then Apply from ADB, and sideload the ROM zip. Choose yes when it asks, then reboot to system.

## Step 6 - let it settle, then judge it

Give the phone a full boot and a normal day before you decide how 3.5 feels. Power behaviour and Bluetooth both show their real character after a few hours of use, not in the first ten minutes.

## Where people get stuck

- Skipping the IMEI backup. Do it before you flash, not after.
- Using fastboot reboot recovery. It can brick the phone.
- Dirty flashing over a different ROM and expecting the fixes to behave.
- Restoring old data before the phone has finished settling, then blaming the ROM for odd behaviour.

## Honest notes

The build is signed and userdebug, which is a good place to be. Signed means it behaves predictably, and userdebug means the developer can still pull the logs they need from you.

Credit where it belongs: @rthedream for help and the device tree, @ZTV86, @katajaree and @Mnskkyy for testing, @katajaree and @sleepingboys15 for the server, and ido@rexprjkt for the flashing guide.

## Who should install it

Install it if you are already on Project Infinity X and these bugs have been annoying you. Especially if you take calls on Bluetooth earbuds or use the front camera for work calls, which is most people now.

Install it clean if you are coming from a different ROM, not as a dirty flash on top. And if you are new to this, take the IMEI backup seriously before anything else.

If the PC side is what slows you down, the free Rom Flasher tool on GitHub handles the ADB and fastboot driver setup in a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Does Project Infinity X 3.5 fix Bluetooth calls?
A: Yes. Bluetooth calls in Meet, Discord, WhatsApp and similar apps stopped cutting out in this build. If you have been blaming your earbuds, this update is the fix you were looking for.

Q: Do I need to clean flash Project Infinity X 3.5?
A: Clean flash it. Format data in recovery before sideloading, especially if you are coming from a different ROM. A dirty flash over another ROM will not give you these fixes and usually adds new problems.

Q: Can I use fastboot reboot recovery to get into recovery?
A: No. It can brick the phone on this build. Reboot normally and hold Volume Up as the phone comes back up to reach recovery safely.

Q: Is the front camera fixed in this build?
A: Yes. The front camera now behaves in Meet, Discord and WhatsApp, which were the apps that showed the problem. Mi Camera is also included in the build.

Q: What is different about the dialer in 3.5?
A: The Infinity dialer replaced the one that used to stutter. Opening the dialer and placing calls now feels normal, which is a small change you notice every day.

Q: Do I need to back up my IMEI before flashing?
A: Yes, do it before you flash. Take the backup first, because a bad flash that damages your IMEI data leaves you without a working network and no easy way back.
