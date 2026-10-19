::summary
A POCO X7 Pro that will not power on is usually not dead. Nine times out of ten it is a failed flash, and MediaTek download mode is still there underneath. You fix it with SP Flash Tool on Windows using the firmware upgrade option, and you finish with the bootloader still unlocked.

::body
Your phone does not turn on. No fastboot screen, no recovery, no logo, just a black screen and maybe a small vibration when you plug it in. You have probably already tried holding every combination of buttons.

Take a breath. On this hardware, that state is usually a failed flash rather than a dead phone. MediaTek download mode sits below the software that you were flashing, and it survives when everything above it does not. That is your way back in.

## What you need

- A Windows PC with a free USB port.
- The MediaTek USB drivers, both the All driver and the USB DK driver.
- adb and fastboot installed.
- SP Flash Tool.
- The ROM file for your device, from the link below.
- A data USB cable. Not a charge-only one.

The cable is not a small detail. Half of these "the tool cannot detect my phone" evenings end with a different cable.

## Step 1 - download everything first

Get the drivers, the tool and the ROM before you start any of it. Do not begin flashing while a file is still downloading. The tool does not pause politely while you wait.

## Step 2 - install the drivers, then restart

Install the MediaTek USB drivers, then install adb and fastboot. Then restart the PC.

Skipping the restart is the most common reason the phone never shows up. Windows registers the new driver properly on the next boot, and until then the tool is talking to nothing.

## Step 3 - open SP Flash Tool as administrator

Right-click SP Flash Tool and run it as administrator. Load your ROM file when the tool asks for it.

## Step 4 - pick firmware upgrade, not format all

This is the decision that matters most. Choose the firmware upgrade option.

Do not choose format all plus download. That option wipes partitions you actually need, and it turns a small recovery job into a bigger one. Firmware upgrade writes what you select over the top and leaves everything else alone, which is exactly what a failed flash needs.

## Step 5 - start the download and connect the phone

Press the download button, and only then connect the phone.

If the tool does not detect it, hold Volume Up and Power on the phone as you plug the cable in. That pushes it into the mode the tool is waiting for. You may need to try this a couple of times before it catches.

## Step 6 - do not touch the cable

The tool prints progress as it writes. When it says it is finished, it is finished. Do not unplug the cable before that.

Recovery is not instant. A few minutes of waiting is normal, and the phone will look lifeless for most of it. Let the tool be the one that tells you what is happening.

## Where people get stuck

- Skipping the restart after the driver install, so the phone is never detected.
- Picking format all plus download and wiping more than was necessary.
- Using a charge-only cable and blaming the tool for it.

## After it finishes

The phone should boot into the ROM you flashed, with the bootloader still unlocked. Let it boot fully and finish setup before you restore anything. If something is going to go wrong, better it happens on a fresh phone than on top of two hours of restored files.

Then decide where you go next. Some people run the tool, get the phone back, and stop flashing for a while. That is a completely reasonable outcome.

## One honest warning

This is a recovery method, not a magic button. It depends on the download mode still being intact underneath. It usually is, which is why I am writing this. But if the phone genuinely will not enter download mode no matter what you try, no tool can help from a PC, and you are looking at a service center rather than a weekend project.

If the driver side is what usually slows you down, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks, so you are not fighting Windows while the phone is sitting there dead. It is free, and the link is in the downloads section.

::faq
Q: Why is my POCO X7 Pro not powering on at all?
A: A dead-screen POCO X7 Pro is usually a failed flash rather than dead hardware. MediaTek download mode sits below the normal software, so you can often bring the phone back with SP Flash Tool on a Windows PC.

Q: Should I use firmware upgrade or format all in SP Flash Tool?
A: Always use firmware upgrade. Format all plus download wipes partitions you actually need and turns a small recovery job into a bigger problem.

Q: My phone is not detected by SP Flash Tool. What should I do?
A: Install the MediaTek USB drivers, restart the PC so they register, and run SP Flash Tool as administrator. Then press download first and connect the phone while holding Volume Up and Power.

Q: Does the bootloader stay unlocked after the fix?
A: Yes. This process brings the phone back with the bootloader unlocked, so you can still flash a ROM normally afterwards.

Q: Can this fix any hard brick?
A: No. It depends on download mode still being there underneath. If the phone will not enter that mode at all, a PC tool cannot help and you need a service center.
