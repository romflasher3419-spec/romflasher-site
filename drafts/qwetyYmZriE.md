::summary
Project Diva 1.1.2 is an official Android 17 build for the POCO X7 Pro, and it installs in three clicks through the free Rom Flasher tool. No PC, no Termux, no recovery menu and no commands to type. Back up first, because the flash wipes storage, and let the first boot finish without touching anything.

::body
So you have seen the Project Diva video and now you are wondering whether to put it on your own POCO X7 Pro. Fair question. Let me walk you through what the install involves and what you are actually getting.

The short version: this is an official Android 17 build for **rodin**, the POCO X7 Pro's codename. The install runs on the phone through the free Rom Flasher tool. There is no PC in the flow, no Termux terminal, no recovery menu and nothing to type.

What has not changed is that you are flashing firmware. It wipes. It can fail. The tool just removes the typing, not the risk.

## What you need

- The **POCO X7 Pro (rodin)**.
- The **Project Diva 1.1.2 package for rodin** — the official one.
- The **free Rom Flasher tool** on the phone. The link is in the downloads section.
- A **complete backup**. Everything on internal storage goes.
- Enough battery to survive a slow first boot.

## Step 1 — get the backup out of the way

Copy your photos, downloads, voice notes and chat backups off the phone before anything else. If a backup is uploading to the cloud, let it finish. You want the phone in a normal, booting state while you do this, because after the flash it is too late.

## Step 2 — open the tool on the phone

Launch the free Rom Flasher tool. The install is designed to run from the device, so the phone does the work instead of your laptop.

## Step 3 — reboot to fastboot when asked

The tool will tell you when it is ready to move the phone into **fastboot**. Confirm on the device when the prompt shows up. You do not need to hold any buttons yourself — the tool starts that for you.

## Step 4 — select the ROM package

Open the **Flash** section and pick the Project Diva 1.1.2 package you downloaded. It takes the file you point it at, so this is the moment to check the name says rodin.

Using a package for a different device is the mistake that turns a fifteen-minute job into a dead phone. Spend five seconds reading the filename.

## Step 5 — let it flash, hands off

Start the flash and then leave the phone alone. Do not unplug anything. Do not close the tool. Do not tap the screen to check on it. The progress will feel slow in places, and that is normal.

## Step 6 — wait out the first boot

When it reboots, you are on the first boot of a fresh ROM. This is slow. Background installs and setup are running, and interrupting now is exactly how people end up in a boot loop with the phone stuck on a logo.

Give it time, then run through the setup wizard and set up Android 17.

## What Project Diva looks like

This is the part the video tour covers, and it is worth watching before you flash rather than after. You get to see the UI, the settings layout and how Android 17 actually presents itself on the X7 Pro hardware.

It is a first look and a general feel, not just a boot test. That matters, because a ROM that boots fine can still be annoying to live with for a week.

## Where people get stuck

- **Using a package for another device.** rodin only. No exceptions.
- **Cutting the first boot short.** It looks frozen for a long stretch. It generally is not.
- **Skipping the backup.** This is the one that hurts, and it is the one people skip most.
- **Unplugging mid-flash.** A loose cable is the quiet cause of a lot of "this ROM bricked my phone" posts.

## The honest part

Any custom ROM is a trade. Project Diva is a different Android 17 build, and you are giving up the polish of stock HyperOS in exchange for something new on this hardware. If a specific banking app or game matters to you, check it works on this build before you commit to it as your daily driver.

The install itself is genuinely short. Three clicks through the tool, no command line, no recovery gymnastics. The long parts are the backup and the first boot, and neither of those can be rushed.

Both links you need — the package and the tool — are in the downloads section on this page. The tool is free and it is the same one used in the video.

::faq
Q: Do I need a PC to install Project Diva on the POCO X7 Pro?
A: No. The install runs on the phone itself through the free Rom Flasher tool, with no computer, no Termux and no commands to type.

Q: Is Project Diva official?
A: Yes, this is the official Project Diva 1.1.2 build. It is Android 17 and it is built for rodin, the POCO X7 Pro's codename.

Q: Will this wipe my data?
A: Yes. Flashing resets internal storage, so photos, apps and files are gone. Back everything up before you start and expect the setup wizard on first boot.

Q: Why did my phone end up in a boot loop?
A: The most common cause is interrupting the first boot because it looked frozen. First boot does a lot of background work and can sit on the logo for a while. Restarting it partway is what creates the loop.

Q: Can I flash Project Diva on a different POCO phone?
A: No. The package is built for rodin only. Flashing the wrong device's package can write partitions your phone cannot boot from.
