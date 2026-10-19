::summary
HyperOS 3 has been ported to the Xiaomi Pad 5 from the Xiaomi Pad 6S Pro ROM, with Android 16 underneath and a long list of features unlocked. It is a beta fastboot ROM, packaged as erofs, with KernelSU already built into the kernel. The refresh rate issue is fixed, and that alone changes how the tablet feels.

::body
HyperOS 3 on a Pad 5 sounds like it should not exist. The tablet shipped years before this software, and yet here it is running, pulled from the Xiaomi Pad 6S Pro ROM and put together as an unofficial beta port. The vendor uses the official nabu vendor, and the hardware composer port comes from Dagu.

It is a fastboot ROM packaged as erofs, and it is marked unofficial and beta. Read that again before you flash it. This is not something Xiaomi signed off on, so treat it as a test device while you get to know it.

## What it looks like

The headline is the refresh rate fix. If you have been on an older HyperOS or MIUI build on this tablet, you know the stutter — the panel not running where it should, scrolling that never quite feels smooth. That is fixed here, completely. For a tablet you mostly read and scroll on, it is the change you feel every single minute.

Around that, the software finally looks like tablet software. The interface is built for the size instead of stretched onto it, and the animations are the newer HyperOS ones you would see on current Xiaomi hardware.

## What changed and what is unlocked

This port does not just boot the newer software. It switches on a pile of features that Xiaomi normally keeps for other devices:

- **Features for tablets** section now shows up in Settings.
- **Xiaomi Super Island** is enabled.
- **Triple-speed game startup** for faster app launches.
- **Speaker cleaning** for clearing dust out of the drivers.
- **AI dynamic wallpapers**.
- **Workstation mode**.
- **Rhythm Eye Protection**.
- **Magnet keyboard quick settings** toggle.
- **AI Master Graphics Engine** for the UI.
- **Leica camera app version 6.0** — the camera from the phones, on a tablet. Unusual, and a genuinely nice surprise.
- **Via Browser built in**, so you can strip out the Xiaomi browser if you prefer.

## Root is already there

If you want root, this is easier than usual. KernelSU 0.9.4 is built into the kernel, so you do not need to patch a boot image and flash it separately. Root is in place from the moment it boots. SELinux is running in enforcing mode for now, which is the more locked-down of the two modes.

## What is broken

Beta means beta. Two things I would want to know going in:

- **The -999 APK install error, and lockscreen passwords.** If apps refuse to install, or the tablet will not let you set a lockscreen password, reboot to fastboot and run `fastboot erase frp` from platform tools. That clears the factory reset protection flag and both problems go away.
- **Super Island and the three-dot window controls clash.** The dynamic Super Island position can overlap the window controls you use to close or minimize apps. Super Island wins the priority, so the controls move rather than the island.

There is also the general roughness you get with any port — an occasional hitch, something in Settings that does not apply until a reboot. Nothing that has stopped me using it.

## Who should install it

Install this if you live on the tablet and you care about how it feels. You get the refresh rate fix, a proper tablet UI, root without extra work, and a camera app that is better than anything that shipped on this thing.

Skip it if you need it to be boring. It is unofficial, it is beta, and there is no warranty behind it. If your tablet is a work device you cannot afford to fiddle with, wait. For everyone else, the refresh rate fix alone makes this worth the flash.

::faq
Q: Is HyperOS 3 for the Xiaomi Pad 5 official?
A: No. It is an unofficial beta port based on the Xiaomi Pad 6S Pro ROM, using the official nabu vendor. Treat it as a test build rather than something Xiaomi supports.

Q: Does this HyperOS 3 port fix the refresh rate on the Pad 5?
A: Yes, the refresh rate issue is listed as fully fixed. That is the headline change and the one people notice most, because scrolling finally runs the way the panel should.

Q: How do I fix the -999 error when installing apps in HyperOS 3?
A: Boot the tablet into fastboot from your PC and run `fastboot erase frp` using platform tools. That clears the factory reset protection flag, which also fixes being unable to set a lockscreen password.

Q: Is root included in this port?
A: Yes. KernelSU 0.9.4 is already built into the kernel, so you do not need to patch and flash a boot image. SELinux is running in enforcing mode.

Q: Does Super Island work on the Xiaomi Pad 5 in this ROM?
A: Yes, Xiaomi Super Island is unlocked in this port. It can overlap the three-dot window controls, but Super Island takes priority, so the controls shift instead.
