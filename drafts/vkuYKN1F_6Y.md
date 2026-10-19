::summary
TengeOS 3.0.301.0.WPJCNXM is a port on the Android 16 base for the POCO X7 Pro (Rodin), flashed from a Windows PC with the batch installer inside the package. Take the clean flash option, leave root off if you want to see the build as it ships, and give the first boot ten to fifteen minutes. Play Store starts uncertified until you sort the integrity fix.

::body
TengeOS 3.0.301.0.WPJCNXM port on the POCO X7 Pro. You have the package, you have a PC, and you want to know how to flash it without creating a problem for yourself. Let me give you the order of operations and the two decisions that actually matter.

This is a port on the Android 16 base. That one word — port — decides most of the advice below.

## What you need

- The **POCO X7 Pro (Rodin)** with an **unlocked bootloader**.
- The **TengeOS 3.0.301.0 PORT package for Rodin**. Link is in the downloads section.
- A **PC with working ADB and Fastboot**, and the driver installed.
- **Battery above 60%** and a **full backup**.
- The flash guide open next to you while you work.

## Step 1 — boot to Fastboot and connect the PC

Reboot the phone into **Fastboot** mode and connect it to the PC. Confirm the PC detects the device before you go further. A missing driver is the number one reason these installers die early.

## Step 2 — extract the ROM zip on the PC

Extract the package on the PC. There is an installer batch file inside it. Run it from inside the extracted folder so it can find the images — do not move the batch file out on its own.

## Step 3 — choose clean flash, not dirty

The installer asks. Answer **clean**.

On a port, clean is the only answer worth giving. A dirty flash leaves yesterday's leftovers in the system partition, and then every odd behaviour gets blamed on a ROM that never had a fair start.

## Step 4 — answer the root question

The installer also asks about root. For this run I left it **off**, because I wanted to see the build exactly as it ships, with nothing else in the picture. That is a perfectly good choice if you are evaluating it rather than living in it.

If you want root, take the option. If you are not sure, leave it off and add it later.

## Step 5 — confirm and wait

Confirm and let the flash finish. Keep your hands off the phone and the cable while it works.

## Step 6 — give the first boot 10 to 15 minutes

This is the step people get wrong, and it costs them their opinion of the build.

After first boot, give it **ten to fifteen minutes**. Background installs and setup work are still running during that window. Judging smoothness at minute two is exactly how good builds get called laggy in forum posts.

Walk away. Come back. Then decide.

## What is worth knowing about the build

Once it settles, the modded extras and the customisation options are the fun part. This is a port on Android 16, so it is not stock HyperOS and it is not trying to be.

Two practical things:

- **Play Store shows device not certified on first boot.** There is a Karios toolbox in the system that handles the integrity side. Sort that before you install anything that checks certification.
- **Banking apps especially.** Install the integrity fix first, or they will simply refuse to open, and you will spend an evening chasing a problem that is not a bug.

## Where people get stuck

- **Choosing a dirty flash on a port.** Do not. Take clean.
- **Judging performance while first-boot background work is still running.** Give it the ten to fifteen minutes.
- **Installing banking apps before the integrity fix.** They will not open, and that is expected, not broken.
- **Running the installer from outside the extracted folder.** The batch file cannot find what it needs.

## The honest bit

TengeOS is a port, so it lives or dies on how it behaves after the first day, not on the first boot screen. There is a changelog and a credits page in the links if you want to see what moved between builds — that is more useful than any single impression.

The install itself is a Windows job. If the ADB and fastboot driver setup is the part that always slows you down, the free Rom Flasher tool bundles that driver install into a couple of clicks. It is free, and the link is in the downloads section on this page.

::faq
Q: Should I choose clean flash or dirty flash for TengeOS?
A: Choose clean flash. On a port like this, a dirty flash carries old system files forward and causes odd behaviour that has nothing to do with the ROM itself.

Q: Do I need a PC to install TengeOS on the POCO X7 Pro?
A: Yes, for this build. The package contains a batch installer you run from a Windows PC with working ADB and Fastboot, while the phone is in fastboot mode.

Q: Why does the Play Store say device not certified?
A: That is normal on first boot for this port. There is a Karios toolbox in the system that handles the integrity side. Sort that out before installing apps that check certification, banking apps in particular.

Q: How long should the first boot take?
A: Give it ten to fifteen minutes. Background installs and setup are still running during that time, and it often looks slow or uneven until they finish.

Q: Do I have to root the phone?
A: No. The installer asks whether you want root, and leaving it off is a valid choice. The build runs fine without it.
