::summary
To lock the bootloader on a POCO X7 Pro and go back to the official ROM, flash the official fastboot ROM with Mi Flash Tool, confirm it boots clean, and only then lock the bootloader again. Lock it while a custom or modified ROM is installed and a soft brick turns into a hard brick.

::body
There is always a day when the custom ROM stops feeling worth it. Battery drains faster than it used to, the phone gets warm on a call, and one app refuses to open. You just want the phone to behave like it came out of the box again.

Going back is not hard. It is just unforgiving. One renamed folder, or one space in a file path, and Mi Flash Tool throws an error at you that sends people straight to a "my phone is dead" post. Here is the whole process, including the boring parts.

## What you need

- The official fastboot ROM for the POCO X7 Pro.
- Mi Flash Tool.
- The ADB and Fastboot driver for Windows.
- WinRAR or 7-Zip to unpack the ROM archive.
- A Windows PC and a data cable you trust.

## Step 1 - download and extract the ROM

Get the official fastboot ROM for your model and region. Extract it with WinRAR or 7-Zip, not the built-in Windows tool. These archives unpack into a nested folder structure, and the built-in extractor sometimes flattens it just enough to break the flash.

## Step 2 - install Mi Flash Tool and open it once

Install the tool and run it a single time, so it creates whatever it needs on first launch.

Then create a folder named `log` inside the Mi Flash Tool folder. This is one of those details that sounds made up. It is not. The tool looks for that folder before it will run a flash, and a missing one means nothing happens when you press the button.

## Step 3 - boot the phone into fastboot

Power the phone off and hold Volume Down and Power until the fastboot screen appears. Connect it to the PC.

## Step 4 - check the driver in Device Manager

Open Device Manager and look for the phone. It should appear as Android Bootloader Interface.

If you see a yellow warning mark next to it, the driver is not installed properly. Install the ADB and Fastboot driver, reconnect the phone, and check again. Do not move on until that yellow mark is gone. A flash that starts with a bad driver usually fails halfway, and halfway is the worst place for a flash to fail.

## Step 5 - put the ROM folder where Mi Flash can find it

Move the extracted ROM folder to the desktop. Do not rename it, and make sure the full path has no spaces anywhere in it.

This is the number one reason the flash fails. A space in the folder path makes the tool lose the images, it errors out, and people decide the phone is bricked when nothing has actually been written to it yet. Fix the folder name, not the files inside it.

## Step 6 - flash

In Mi Flash Tool, press refresh. Your device should appear in the list. Select it, point the tool at your ROM folder, and start the flash.

Let it run. The phone reboots on its own when the tool is finished. Do not unplug anything while it is working.

## Step 7 - lock the bootloader, but only now

Here is the part that matters most. Lock the bootloader only once you are sure the ROM that is installed is official and properly signed, and the phone has booted cleanly at least once.

Locking on a custom or modified ROM is how a soft brick becomes a hard brick. A locked bootloader refuses to flash or run anything that is not signed by the manufacturer. If what is on the phone is not a signed stock image, you have locked yourself out of the one route that could have fixed it.

If in doubt, leave it unlocked. An unlocked bootloader is a small security trade-off. A hard brick is a much bigger problem.

## Where it goes wrong

- A space in the ROM folder path. Fix the folder, not the files.
- The missing `log` folder in the Mi Flash Tool directory.
- Locking the bootloader on a custom or modified ROM.

## One honest note

After flashing, let the phone boot fully and finish the setup wizard before you restore anything. If something is going to go wrong, you want it going wrong on an empty phone rather than on top of two hours of restored data.

Also, locking the bootloader wipes nothing by itself, but the fastboot flash does. Your internal storage is reset, so get your photos off the phone first.

If the driver side of this is what usually stops you, the free Rom Flasher tool on GitHub installs the ADB and fastboot driver in a couple of clicks, which is exactly the step that needs to be clean before Mi Flash Tool will work. It is free, and the link is in the downloads section.

::faq
Q: Does locking the bootloader wipe my data?
A: Locking itself does not, but going back to the official fastboot ROM does. The fastboot flash resets internal storage, so move your photos and files off the phone first.

Q: Can I lock the bootloader on a custom ROM?
A: Do not. A locked bootloader only runs signed stock software, so locking it while a custom or modified ROM is installed can turn a soft brick into a hard brick. Lock only after a stock, signed ROM has booted cleanly.

Q: Why does Mi Flash Tool say it cannot find my device?
A: Usually the driver. Open Device Manager and check the phone shows as Android Bootloader Interface with no yellow warning mark. Reinstall the ADB and Fastboot driver, reconnect, and refresh the tool.

Q: Why does Mi Flash Tool fail with a path error?
A: There is very likely a space in the ROM folder path, or the folder was renamed. Move it to the desktop, leave the name alone, and make sure the full path has no spaces.

Q: Do I need to create the log folder inside Mi Flash Tool?
A: Yes. Mi Flash Tool looks for a folder named log inside its own directory before it will run, and without it the tool will not flash. Create it once and forget about it.
