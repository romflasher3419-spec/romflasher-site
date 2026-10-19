::summary
You can flash a custom ROM from Termux on a second Android phone, without a PC in the room. The tool talks ADB and fastboot over a USB cable, checks that your phone is visible, reboots it to fastboot, pushes recovery to both slots, then handles the sideload. LineageOS 22 is just the demo subject here.

::body
Your laptop is dead, you are away from home, or you need to flash a ROM on someone else's device and you are not installing ADB drivers on their machine. That is the situation this method is for. It is not really about LineageOS. LineageOS 22 is simply the ROM I used on camera to prove the route works.

The idea is simple. Termux on one Android device runs the tool. A USB cable connects that device to the phone you want to flash. From there you get a menu that speaks ADB and fastboot, and you do the same job a PC would do.

## What the tool does

- Connects your phone to a second Android device over USB and talks ADB and fastboot.
- Checks whether the phone is visible before anything gets flashed, so failures show up early instead of halfway through.
- Reboots the phone into fastboot mode from a menu rather than a key combination.
- Flashes recovery to both slots, then handles the sideload, so the ROM install stays in one place.
- Uses the files already sitting in your Download folder.

## What you need

- **Termux** set up on the flashing device, with the tool and the ADB driver inside it. This is the part that takes the time.
- A **USB cable** that actually carries data. Charge-only cables are a real thing and they will waste your evening.
- The **ROM zip**, the **recovery image**, and the right **vendor** files for your phone, already downloaded.
- An **unlocked bootloader**. This route does not do that part for you.
- A backup, because a clean install wipes the phone.

## Step 1 - check the phone before you flash anything

Plug the phone into the flashing device with the cable and open the tool's menu. The first item checks the ADB device. Do that first, every time. If the phone does not appear here, nothing later in the menu will work, and you have saved yourself a failed flash.

## Step 2 - reboot to fastboot from the menu

Pick the option that reboots the phone into fastboot. Using the menu instead of a key combo is the small quality-of-life win in this method, especially if the phone's buttons are stiff.

## Step 3 - confirm the fastboot list

Once the phone is in fastboot, run the fastboot check in the menu. You want to see your device listed before you write anything to it. This is the second checkpoint, and it is the one that tells you whether your driver setup in Termux is right.

## Step 4 - flash recovery to both slots

Flash the recovery image to both slots. On this phone there are A and B slots, and if recovery only goes to one of them, you land in the wrong one sooner or later.

## Step 5 - sideload the ROM

The tool takes you into the sideload step. This is where you pick the ROM zip from your Download folder and let it push. Keep the cable still and leave the screen on.

## Step 6 - first boot

Reboot to system from the menu and wait. The first boot after a clean install is slow. Let the phone settle before you decide whether the ROM is any good.

## What this route does not do

- It will not unlock your bootloader. That still has to be done properly, first, and it wipes the phone when you do it.
- It will not fix a wrong vendor file or a ROM built for another device. Bad files stay bad.
- It will not skip the wipe. A clean install still means formatting data.
- It will not work without the ADB driver set up inside Termux. If your phone does not show up, the driver is the culprit far more often than the phone.

## One honest paragraph

This is boring when it works and confusing when it does not. The tool removes the typing but not the thinking. Every checkpoint in the menu exists because I hit that exact failure while testing, so resist the urge to skip the first two checks to save thirty seconds. When your phone does not appear, it is nearly always the driver inside Termux rather than anything wrong with the phone or the cable.

Being able to do this from another Android device is genuinely handy. If your PC dies, or you are on the road, or you simply do not want to install drivers on a borrowed laptop, this route still gets a ROM onto the device. The same steps work on other Android phones as long as your files are right.

The Termux setup itself is a separate job with its own steps. Once that is in place, this is the everyday flashing route.

The free Rom Flasher tool is the same tool used on the PC side, and the Termux flash file in the downloads section is what you put on the flashing device.

::faq
Q: Can I flash a ROM without a PC at all?
A: Yes, that is the whole point of this method. Termux on a second Android device runs the tool and does the flashing over USB, so no computer is involved.

Q: Why does my phone not show up in the tool?
A: The ADB driver inside Termux is the usual culprit, not the phone. Check that the ADB device appears in the menu before you try anything else.

Q: Does this work on phones other than the POCO X7 Pro?
A: Yes. The method works across Android devices as long as the ROM, recovery and vendor files are correct for the phone you are flashing.

Q: Will this unlock my bootloader?
A: No. Unlocking the bootloader has to be done separately, and it is a step that wipes the phone. Do that first, then come back to this method.

Q: Can I use files that are already on my phone?
A: Yes. The tool picks the ROM zip from your Download folder, so you do not need to move anything around before you start.
