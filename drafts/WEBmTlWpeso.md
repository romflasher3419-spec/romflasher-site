::summary
DyperOS 3.0.300 CN is a Chinese HyperOS based build for the POCO X7 Pro and Redmi Turbo 4 (Rodin). The installer offers two paths: install with format data, or upgrade if you are already on a CN DyperOS build. The draw is a very clean system and the Leica camera.

::body
The first thing you notice on this build is how empty it feels. No pile of preinstalled apps, a short list of things you would actually open, and a home screen that gets out of the way. That is the point of these CN ports, and DyperOS 3.0.300 CN does it well.

It is a Chinese HyperOS based build for the POCO X7 Pro and the Redmi Turbo 4, both rodin. I did a clean flash, because that is the only fair way to judge a new build, and let the phone settle before touching anything.

## What you need

- The **DyperOS 3.0.300 CN package** for Rodin. Not for another device.
- A **PC with working ADB and fastboot drivers**, or the Termux route if you would rather flash from a phone.
- An **unlocked bootloader** and working fastboot access.
- Over **60% battery** and a **full backup**, because the clean path wipes your data.
- Time for a slow first boot. Give it that time before you judge smoothness.

## Step 1 - boot to fastboot

Power off, hold **Volume Down + Power**, then plug the phone into the PC. Confirm it is visible with `fastboot devices` before you go near the installer.

## Step 2 - extract the package

Unpack the downloaded package on the PC with 7-Zip or WinRAR. Work from the extracted folder, never from inside the zip.

## Step 3 - run the installer for your system

The package ships installers for Windows and Linux, plus the Android and Termux route. Pick the one that matches the machine you are on and start it.

## Step 4 - install with format data, or upgrade

The installer gives you two choices and this is the decision that matters:

- **Install and format data.** Choose this if you are coming from another ROM. It is the clean path and it wipes internal storage.
- **Upgrade.** Choose this only if you are already running a CN DyperOS build. A dirty flash from an earlier version of the same base is supported here.

## Step 5 - confirm and let it run

The installer prints a confirmation prompt. Type it exactly as shown, then keep your hands off the phone. The flash runs to the end on its own. Do not unplug the cable to check on it.

## Step 6 - let the phone settle

After first boot, leave the phone for a while. Apps are still optimising in the background, so it will feel less smooth in the first hour than it will later. Judge it after it has settled, not in the first ten minutes.

## Where people get stuck

- **Choosing upgrade while coming from a different ROM.** That is the classic bootloop. If you were not already on a CN DyperOS build, format data.
- **Skipping the data format**, then blaming the ROM for apps behaving oddly. A clean base avoids that whole conversation.
- **Flashing a package built for another device.** This one is Rodin only. The POCO X7 Pro and the Redmi Turbo 4 are the same phone under two names, and nothing else is.

## The tour

The home screen is restrained, which is what you want from a debloated build. The control centre has that Apple-style look, and there are iPhone-style widgets you can pull in if that is your taste.

The Karios toolbox ships with this base, and that is where the useful plumbing lives: the integrity fix and app spoofing. You will want it, for the next reason.

Play Store will show device not certified out of the box. That is normal for a build like this, not a fault, and it is exactly what the toolbox exists to handle. The other headline addition is the Leica camera, which is the reason a lot of people try this ROM in the first place.

## One honest paragraph

The empty app list is a feature, not a missing part, but do not read it as a guarantee that everything will be certified and happy on first boot. Set the integrity side up through the toolbox, do the clean path if you are coming from another ROM, and give the phone a day before you decide.

The free Rom Flasher tool handles the driver check and the flashing on Windows, and it is free. There is also a Termux flash file in the downloads section if you would rather do it all from the phone.

::faq
Q: Should I choose install or upgrade in the installer?
A: Format data if you are coming from a different ROM, since that is the clean path and it prevents bootloops. Upgrading is only fine when you are already on a CN DyperOS build, where a dirty flash from an earlier version is supported.

Q: Why does Play Store say device not certified?
A: That is normal for this kind of build out of the box, not a problem with your install. The Karios toolbox that ships with the base has the integrity fix, and that is where you sort it out.

Q: Does this ROM work on the Redmi Turbo 4?
A: Yes. The POCO X7 Pro and the Redmi Turbo 4 are the same device, codename Rodin, so the same package works on both. Do not flash it on any other phone.

Q: Does installing DyperOS wipe my phone?
A: The install and format data option wipes internal storage, so back up your photos and files first. Keep the backup until the phone has fully booted and set up.

Q: What is the Leica camera on this build?
A: It is the headline addition in DyperOS 3.0.300 CN, and it is the main reason people try the ROM. You get the Leica camera experience as part of the system rather than as something you add afterwards.

Q: Why does the phone feel slow right after the flash?
A: The first boot and the first hour are busy with background optimisation. Let it settle before judging smoothness, and the same applies after an upgrade.
