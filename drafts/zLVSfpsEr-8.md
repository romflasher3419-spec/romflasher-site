::summary
DerpFest on the Redmi K50i is a clean AOSP-based custom ROM, and you feel the difference from the first boot. There is no MIUI skin in the way, the interface sits closer to Pixel, and the phone stops fighting you for the dialer, the launcher and the quick settings. You trade the MIUI camera and a few Xiaomi habits for it.

::body
DerpFest comes out of the AOSiP side of the custom ROM world, and you notice that immediately. The phone boots and there is nothing between you and the system. No skin, no wall of vendor apps, no second guessing how the settings should be arranged.

The Redmi K50i has the hardware to make a clean build fly, and an AOSP base is what lets it. Here is what it looks like, what actually changed, what is broken, and who should install it.

## What it looks like

The launcher is close to the Pixel launcher. The notification shade is plain and fast. Quick settings are the stock tiles, not Xiaomi's version of them, and the settings app follows Android rather than MIUI. If you have used a Pixel or any AOSP build, you already know the layout, and it takes about an hour to feel at home.

The screen benefits from this. With less running in the background, scrolling and app switching feel lighter than on a stock build. That is not a benchmark, it is just what a leaner system does on hardware like this.

## What changed

- **The whole interface.** Dialer, launcher, quick settings and settings app are AOSP, with none of MIUI's layer over the top.
- **Customization.** DerpFest carries the options you would expect from a build in this family — status bar tweaks, gesture controls and behavior settings that stock MIUI buries or never offers.
- **Vendor apps gone.** Nothing is fighting you for the default dialer, or pushing its own version of a system app.
- **The camera.** The stock MIUI camera app is not here. The AOSP camera is a different animal, and that is the biggest thing you give up.

## What you trade

- **The MIUI camera.** If you shoot a lot, you will miss it. The replacement does not behave the same way.
- **Some Xiaomi habits.** Little conveniences you stopped noticing because you used them every day simply do not exist here.
- **Gapps are usually separate.** On most AOSP builds you flash Google apps yourself, so plan for a second zip in the same recovery session unless your build includes them.
- **Play Integrity.** Banking apps and some payment apps treat custom ROMs badly. Test the ones you rely on early.

## What is broken or rough

Honest answer: it depends on your build. DerpFest on this phone is a community build on MediaTek hardware, which is the least forgiving combination there is.

- Support moves build to build. Something that works in one release can break in the next.
- Battery behavior wants a few days before you judge it.
- Aim for a clean install. Dirty flashing over an older base is where the strange little bugs come from.
- Keep a path back to stock. This is not the phone to experiment on without a way home.

## What you need before you flash

- Unlocked bootloader. On this phone that is step zero, and it wipes the phone the first time.
- Platform tools on a PC.
- A recovery built for the K50i or its known counterpart. TWRP or OrangeFox, not the stock recovery — the stock one will not do this.
- The ROM zip on internal storage.
- vbmeta on hand. AOSP builds usually need it, and going in without it is how you end up with a bootloop instead of a boot.

## The install, in short

1. Unlock the bootloader and install TWRP or OrangeFox for this device.
2. Copy the ROM zip and vbmeta to internal storage.
3. Reboot to recovery and check that touch works and storage is readable. If not, stop and fix recovery first.
4. Wipe data, cache and dalvik, then format data.
5. Flash vbmeta the way your build's instructions say, then flash the ROM zip.
6. Reboot and leave the phone alone for the first boot. It is slow.

If you are unsure about the exact vbmeta step for your build, follow the instructions that came with the ROM rather than guessing at a filename. Getting that one wrong is the most common reason a clean flash turns into a bootloop.

## Who should install it

Install DerpFest if you want a clean AOSP phone, you are comfortable with recovery and fastboot, and you are willing to test the build yourself before trusting it.

Skip it if the MIUI camera is why you bought the phone, or if you need a specific app that has to work without argument. On MediaTek, every custom ROM is a test first and a daily driver second.

Keep your stock firmware and know the way back before you start. That habit is the difference between a fun experiment and a long night.

If the driver and platform tools side is where you usually stall, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Does DerpFest need an unlocked bootloader?
A: Yes. Unlocking is step zero on the K50i, and it wipes the phone the first time you do it. There is no way to install this ROM without it.

Q: Do I need vbmeta to flash an AOSP ROM on the K50i?
A: On AOSP builds, usually yes. vbmeta is part of the boot verification chain, and skipping it is a common cause of a bootloop after a clean flash. Use the vbmeta step that came with your specific build instructions rather than guessing.

Q: Does DerpFest come with Google apps?
A: Most AOSP builds do not, so plan to flash a Gapps package in the same recovery session as the ROM. Check whether your particular DerpFest build includes them before you start.

Q: Can I keep the stock recovery and still flash this?
A: No. The stock recovery will not do this job. Install TWRP or OrangeFox for the K50i, and make sure touch works and internal storage is readable before you flash anything.

Q: Is DerpFest a good daily driver on the Redmi K50i?
A: It depends on your build and your usage. Test it for a few days, check the apps you depend on, and keep a path back to your stock setup. On this MediaTek hardware, that caution is the difference between a good experience and a frustrating one.
