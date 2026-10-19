::summary
You can flash LineageOS 22 on the POCO X7 Pro without a PC, using Termux on a second Android device to run the recovery steps over USB. It works, but the whole job depends on the ADB driver inside Termux being right, and that is where most attempts fail.

::body
You do not own a Windows laptop, or the one you have refuses to see the phone, or you just want to prove this can be done from a phone. Whatever the reason, flashing LineageOS 22 on the POCO X7 Pro from Termux is a real route, and I ran the whole thing that way.

The idea is simple. A second Android phone or tablet runs Termux, you connect the POCO to it with a USB cable, and the recovery tool in Termux talks to the phone over ADB and fastboot. No desktop, no platform-tools folder, no driver installer on Windows.

The catch is the same catch as always. When the device ID does not show up, that is almost never the phone. It is the ADB driver.

## What you need

- Termux, plus the recovery tool, already set up and working on the second device.
- A second Android phone or tablet to run Termux. This is the device doing the flashing.
- The LineageOS 22 ROM zip and the vendor file for this device.
- USB debugging turned on, on the phone you are flashing.
- A cable that actually moves data. Charge-only cables are useless here.
- Your IMEI written down and your data copied off the phone.

That last point matters more than people think. Write the IMEI down somewhere you can find it. You cannot recreate it later.

## Step 1 - prepare the phone you are flashing

On the POCO X7 Pro, enable Developer options and turn on USB debugging. Connect it to the Termux device with the cable and pick the option that checks the ADB device.

If that returns an ID, you are in business. If it returns nothing, jump to the troubleshooting section below before you go any further. Do not push on and hope.

## Step 2 - reboot to fastboot

From the tool's menu, reboot the phone to fastboot. Then check the fastboot device list before you touch anything else. You want to see the ID listed there too. This is the checkpoint that saves you from a bad flash later.

## Step 3 - put the files where the tool expects them

Move the LineageOS 22 zip and the recovery file into the Download folder on the Termux device, so the tool can find them without you typing long paths. This is boring and it is worth doing properly.

## Step 4 - flash recovery

Flash the recovery image to the phone. The tool handles it, and you want it on both slots. If it does not offer that as a menu option, do it manually for each slot.

## Step 5 - sideload the ROM

Boot into the LineageOS recovery you just flashed, format data, then use Apply update and Apply from ADB. Sideload the ROM zip and let it finish.

First boot after that takes a while. Leave the phone alone.

## Where people get stuck

- **The fastboot ID never shows up.** Nine times out of ten this is the ADB driver inside Termux, not the phone. Reinstall the driver there and try again before you assume the device is dead.
- **A cable that only charges.** If the device list is empty no matter what you do, try a different cable before you reinstall anything else.
- **Skipping the vendor file.** The vendor file has to go on with the ROM. Without it the phone will not boot properly.

## One honest note

Flashing from a phone is slower and fussier than from a PC. Every time something does not respond, you are troubleshooting two Android devices instead of one, and the tool's output on a phone screen is cramped. I checked the device at every stage rather than trusting the tool, because a tool that looks connected while your phone sits there doing nothing is the worst feeling in this hobby.

That said, it works, and it is a genuinely good option if a PC is not available to you. Just be patient with the driver step and verify each checkpoint before moving on. If you would rather do it from a computer, the free Rom Flasher tool covers the ADB and fastboot driver setup there.

::faq
Q: Can I flash LineageOS 22 without a PC?
A: Yes. You can run the flash from Termux on a second Android device over a USB cable, using the recovery tool to handle the ADB and fastboot steps. It works, but the driver setup inside Termux has to be right first.

Q: Why does the fastboot device ID not show up in Termux?
A: It is almost always the ADB driver rather than the phone. Reinstall the driver inside Termux and try again. Also check the cable, since a charge-only cable will never show a device.

Q: Does flashing LineageOS 22 wipe the phone?
A: Yes. You format data as part of the install, and unlocking the bootloader wipes the phone as well. Copy your files off and write down your IMEI before you start.

Q: Do I need the vendor file with the LineageOS 22 zip?
A: Yes. The vendor file goes on with the ROM and the build will not behave correctly without it. Get both files on the Termux device before you start flashing.

Q: Why is there no fastboot device showing even though the cable is connected?
A: Check the cable first, then the driver inside Termux. A charge-only cable will never pass data, and a missing ADB driver looks exactly like a dead phone. Fix those two before you blame the ROM.
