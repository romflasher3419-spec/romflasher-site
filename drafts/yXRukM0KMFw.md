::summary
CrDroid Android 12L on the Redmi K50i is a customization-first custom ROM, and it installs cleanly from recovery if you treat it as a MediaTek device instead of a Qualcomm one. You get a near-stock base plus more tweaks than you will have time to go through. The catch is support and battery, so keep a way back to stock.

::body
CrDroid is the ROM you flash when you want the keys to everything. Status bar layout, gestures, theming, per-app control, quick settings tiles — it hands you all of it and then some. On a phone like the Redmi K50i the appeal is obvious, because stock MIUI makes you live inside its own idea of how a phone should look.

But the K50i is a MediaTek phone. The codename is xaga, and the road to a working build is rougher here than it is on a Qualcomm device. Fewer builds get made, recovery setups are fussier, and the steps matter more. Follow a POCO tutorial and you will end up somewhere unpleasant.

## What it looks like once it boots

The first thing you notice is how little is in your way. No MIUI skin over the top, no wall of Xiaomi apps in the drawer. The launcher is close to Pixel, the quick settings pull down clean and simple, and the whole thing moves with less friction than a stock build.

Then you open the settings menu and realize how much is hidden in there. This is where CrDroid earns its place. You can reshape the status bar, change the clock style, rearrange the navigation, tweak animations, and control notifications app by app. If you like tuning a phone, you will lose an evening here and enjoy every minute of it.

## What actually changed for me

- A cleaner base than MIUI, with none of the manufacturer clutter on top.
- Customization that goes past cosmetic. Gestures and per-app behavior are the useful part.
- Google apps and the Play Store present and working, so nothing has to be bolted on afterward.
- The stock MIUI camera app is gone. The camera you get instead behaves differently, and that is a real trade if you shoot a lot.

## What is broken or rough

I will be honest with you here, because this part is what makes or breaks a daily driver.

- Support on MediaTek varies from build to build. Something that works perfectly in one release can misbehave in the next.
- Battery behavior is the thing to watch. Give it a few charge cycles before you judge it, because the first day is never representative.
- Random small things turn up. A sensor that reads oddly, an app that refuses to open, a gesture that does not stick. On this hardware you should expect to find something.
- Some banking and payment apps fight custom ROMs. If you depend on one for daily money, test it early instead of discovering it at a checkout counter.

## How to install it on the K50i

Treat this as a recovery-based clean install, with the MediaTek caveats respected.

## Step 1 - get the phone ready

You need an unlocked bootloader, and on this phone that is a separate process with its own waiting period. You also need platform tools on your PC, because the unlock and the recovery flash both happen over USB.

Do not skip the backup. Flashing wipes data, and that is not optional.

## Step 2 - recovery first

Flash or boot a custom recovery that is actually built for the K50i or its known counterparts. If touch is dead or internal storage reads as zero, the recovery is wrong and you should stop and fix it before doing anything else.

A recovery that half works is worse than none, because it lets you start a flash you cannot finish.

## Step 3 - clean flash, not dirty

- Wipe data, cache and dalvik.
- Format data if you are coming from MIUI or any other ROM. Coming from an older CrDroid build you may get away with less, but a clean start saves you chasing ghosts later.
- Flash the CrDroid zip and let it finish completely.
- Reboot and let the first boot run. It takes several minutes. Do not touch anything.

## Step 4 - setup and a real test

Run through the setup wizard, sign into your accounts, and then actually use the phone for a few days before you decide anything. Open your bank app. Take some photos. Use the phone on a bad signal day. Battery and stability only show themselves over time.

## Who should install this

If you want control over how your phone behaves and you are comfortable with recovery, CrDroid on the K50i is a good fit. You will be spending time in settings by choice, and the payoff is a phone that does exactly what you told it to.

If you want something you set and forget, or you cannot go a day without one specific app working, think twice. On MediaTek the honest answer is that every build needs testing before it becomes your daily phone.

Keep a path back. Know how to restore your stock firmware before you start, so that if this build does not suit you, going home is a short job instead of a research project.

If the driver side of preparing the phone is where you usually stall, the free Rom Flasher tool on GitHub puts the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Is CrDroid hard to flash on the Redmi K50i?
A: The flash itself is a normal recovery install, but the K50i is a MediaTek device, so the process is less forgiving than on a Qualcomm phone. Use steps written for this phone, not a tutorial from a POCO or a Redmi Note.

Q: Do I need a PC to install CrDroid on the K50i?
A: Yes for the setup. Unlocking the bootloader and getting a custom recovery onto the phone both happen over USB from a PC. Once recovery is running, the ROM flash itself is done on the phone.

Q: Is CrDroid stable enough to use every day?
A: Test it yourself for a few days. Stability on this hardware varies between builds, and battery life needs a couple of charge cycles before it settles. Keep a backup so you can go back if it does not hold up.

Q: Does CrDroid come with Google apps?
A: This build has Google services and the Play Store in place, so you can sign in right after setup. If you ever move to a build that does not, you would flash a Gapps package in the same recovery session as the ROM.

Q: Can I go back to MIUI after flashing CrDroid?
A: Yes. Keep your stock firmware around, and remember that going back means a full flash that wipes data. Know the way home before you start, and the decision to try a ROM stops being risky.
