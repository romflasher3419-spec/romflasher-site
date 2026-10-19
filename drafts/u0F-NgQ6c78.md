::summary
HyperOS 3 Robinhood Edition is a ported Global HyperOS 3.0.5.0 build on Android 16 for the POCO X7 Pro, flashed from a Windows PC with a one-click installer. It brings a modded launcher, Hyper AI, AI Boost and the latest Mi camera app. Clean flash wipes data, and you can answer the installer to skip root.

::body
HyperOS 3 Robinhood Edition, build 3.0.5.0, on Android 16. This is the Global HyperOS 3 base with the edges sanded off, and it goes onto the POCO X7 Pro from a Windows PC using the installer batch file that comes inside the package.

Let me clear up one thing before we start, because it confuses people. This is a **port**, not a custom AOSP ROM. It is HyperOS 3 Global, built with mods, and it shows in a good way.

## What it looks like

The launcher is where the difference hits you first. Extra blur, both the old and new app opening animations, and controls for icon sizing. The recents view gets an iOS-style bar. If you have used HyperOS 3 stock, you will recognise it and still notice the changes.

Hyper AI and AI Boost are both present, and the camera is the latest Mi camera app rather than an older build. Preinstalled HyperOS apps are already there, ready for you to sign in.

## What you need

- **POCO X7 Pro (Rodin)**.
- The **HyperOS 3 Robinhood package** for the X7 Pro — link in the downloads section.
- A **Windows PC**. It has to be Windows, because the installer is a `.bat` file. There is no phone-only route here.
- **ADB and fastboot** working on that PC, plus the driver, so the phone shows up.
- An **unlocked bootloader**.
- A **backup**, since a clean flash wipes everything.

## Step 1 — unpack the ROM on your PC

Extract the package into a folder you can find again. Keep the folder structure intact — if the `.bat` ends up separated from the images it needs, the installer will not be able to do its job.

## Step 2 — boot the phone to fastboot and connect it

Power the phone off, hold the fastboot key combination to enter fastboot mode, and connect it to the PC. Check the PC can see it before you run anything. If it cannot, sort the driver first — no installer can fix a phone Windows does not recognise.

## Step 3 — run the installer

Run `Robinhood_os_installer.bat` from inside the unpacked folder. It asks you two questions.

First question: **clean flash?** Type `Y`. On a port, clean is the right answer. A dirty flash carries yesterday's system leftovers forward, and then everything gets blamed on the ROM.

Second question: **which root method?** You get four options. Answer `4` if you do not want root.

## Step 4 — wait, then let it come back

Let the installer run to the end. It reboots the phone on its own when it is finished, or it asks you to tap `S` to do it. Do not unplug while it is working.

First boot after a clean flash is slow. That is the setup work running, not a hang.

## What is broken or awkward

I would rather you hear this now than find it later.

- **The Play Store is uncertified on first boot.** Basic integrity does pass, so UPI and most banking apps go through. If something refuses to open, that certification state is usually why.
- **Some preinstalled apps cannot be disabled.** Do not expect a totally clean app drawer.
- **No PC, no install.** The installer only runs on Windows. There is no phone-only path for this particular build.

Those are the real trade-offs. None of them are surprises if you go in knowing them.

## Who should install it

Install Robinhood if you want the HyperOS 3 Global experience with more control over the launcher and animations, and you are comfortable doing a Windows fastboot flash. Skip it if you need a fully certified Play Store out of the box or you cannot live with unremovable preinstalled apps.

If your daily driver depends on a specific banking or UPI app, install it and test that app before you move your whole life onto the phone.

## Where people get stuck

- **Running the installer without a working driver.** The phone never appears and the batch file fails immediately.
- **Choosing a dirty flash.** On a port, this is the fastest way to a boot loop.
- **Picking a root option by accident.** If you did not want root, answer 4.
- **Expecting the Play Store to be certified straight away.** It is not.

If the driver side is the part that always slows you down, the free Rom Flasher tool bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section along with the ROM.

::faq
Q: Is HyperOS 3 Robinhood a custom ROM?
A: No. It is a ported HyperOS 3 Global build, not AOSP. It is based on HyperOS 3.0.5.0 on Android 16 with modded system apps and launcher changes.

Q: Will flashing Robinhood wipe my data?
A: Yes, on a clean flash, which is what you should choose. Back up your photos and files first and expect the setup wizard after first boot.

Q: Do I have to root my phone to install it?
A: No. The installer asks which root method you want and offers option 4 for no root. Pick that if you do not want root, and the build installs without it.

Q: Why does my banking app not open after flashing?
A: The Play Store starts uncertified, though basic integrity passes. Most UPI and banking apps still work. If one refuses, that certification state is the usual reason, so test your essential apps early.

Q: Can I install this without a PC?
A: No. The installer is a Windows batch file, so this one needs a PC, a working ADB and fastboot setup, and the phone in fastboot mode.
