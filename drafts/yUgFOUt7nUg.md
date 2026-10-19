::summary
Pixel Experience Plus on the Redmi K50i got the December security patch, and with it a set of small everyday changes: you can remove the dead space under the keyboard, switch the LTE icon to a 4G icon, and use a proper black theme. It is an AOSP build with GApps included, so you need an unlocked bootloader and a recovery to install it.

::body
Pixel Experience is the ROM I would hand to someone who is tired of MIUI but still wants a phone that feels finished. The Plus edition keeps that clean Pixel feel and adds the extras on top, and this update is mostly quality of life. Some of it sounds small until you live with it for a week.

That is the honest way to describe this one. Nothing here is dramatic. It is a December patch and a list of small things that you notice every single day, which is a better deal than it sounds.

## What changed in this build

- The December security patch is merged.
- You can remove the space under the keyboard. That strip of dead area above the keys is finally gone for people who want it gone.
- The 4G icon option, if you would rather see 4G than LTE in your status bar.
- Support for the new Game Mode.
- GamesProps added, which helps games be treated properly by the system.
- Black theme support, for real dark surfaces rather than a washed-out grey.
- reTicker support for notifications that behave like you expect.
- MatLog included, which is genuinely handy, because you can take logs without root.
- The usual fixes and small improvements.

## What it looks like

If you have used Pixel Experience before, this is more of the same and that is meant as praise. Notification shade, quick settings and the launcher all have that Pixel shape to them. With black theme support switched on, the dark look is properly dark instead of slightly blue, and the option to drop the keyboard gap cleans up the bottom of the screen in a way you feel more than you see.

## What to know before installing

- It needs an unlocked bootloader. That is the first step and it wipes the phone, so back up after unlocking, not before.
- You do not need GApps. Pixel Experience builds include them already.
- For an AOSP build like this, keep a correct vbmeta ready. If your package asks for it, use the vbmeta for AOSP ROMs, not one borrowed from another build.
- Xiaomi's own camera app is not part of this ROM. If you rely on it, plan for a replacement camera app before you flash, not after.

## How to install it

1. Unlock the bootloader if it is not already done.
2. Install the ADB and fastboot driver, plug the phone in, and confirm it is detected.
3. Flash a recovery built for the Redmi K50i. Do not use one from another device.
4. In recovery, format data before flashing, since this is a clean start.
5. Flash the Pixel Experience Plus package and let it finish.
6. Reboot to system and let the first boot run all the way through.

## What is broken, honestly

This is an unofficial ROM, so treat it like one. Xiaomi's camera is missing, so your camera experience changes. Some hardware-specific features that MIUI has are not here, and if you rely on a banking app that is strict about a modified device, it may complain. None of that is unusual for a custom ROM, but you should know it before you commit a weekend to it.

## Who should install it

Install it if you want a clean, Pixel-style phone on the Redmi K50i and you are happy to give up Xiaomi's own apps to get it. Skip it if you need the stock camera, or if you want a phone that needs zero fiddling. This build is for people who like the idea of a finished-feeling phone that does not belong to the manufacturer's app suite.

If the driver setup is the part that slows you down, the free Rom Flasher tool bundles the ADB and fastboot driver install so you can get to the flash quicker. It is free, and the link is in the downloads section, next to the ROM, platform tools and recovery files.

::faq
Q: Does Pixel Experience Plus need GApps on the Redmi K50i?
A: No. Pixel Experience builds include GApps already, so you do not flash them separately. Just install the ROM package and reboot.

Q: Does Pixel Experience Plus need an unlocked bootloader?
A: Yes. The bootloader has to be unlocked before you can flash any custom ROM, and unlocking wipes the phone. Back up after unlocking, not before, so you are not doing the job twice.

Q: Do I need vbmeta for Pixel Experience on the Redmi K50i?
A: For an AOSP-based build like this, keep a correct vbmeta ready in case your package asks for it. Use the vbmeta intended for AOSP ROMs rather than one from a different build or device.

Q: Does Pixel Experience Plus include the Xiaomi camera app?
A: No. Xiaomi's own camera app does not come with this ROM, so your camera app changes. Decide on a replacement before you flash so you are not stuck without one.

Q: What is new in the December patch build?
A: The December security patch is merged, and it adds the option to remove the space under the keyboard, a 4G icon instead of LTE, black theme support, Game Mode support, reTicker and the MatLog app, plus fixes.
