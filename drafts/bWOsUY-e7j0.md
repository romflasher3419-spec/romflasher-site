::summary
One Magisk module on the official HyperOS ROM wakes up the Themes app on the POCO X7 Pro and lets you import themes that are not listed for your device or region. It needs root, it takes one reboot, and it does not touch the rest of your system. Here is how it goes, and how you know it worked.

::body
You are on stock HyperOS, you like the Themes app, and you are tired of it refusing imports because the theme is not listed for your device or your region. There is one small module for this, and it does not replace the app you already have.

I did not expect much from this one. One module, one reboot, done. It turned out to be one of the tidier mods I have run on the POCO X7 Pro, because it changes exactly one thing and leaves everything else alone.

## What it does

- Swaps in a modded theme store on top of the official HyperOS Themes app
- Lets you import themes that are not listed for your device or your region
- Opens up widgets, dynamic wallpapers, ringtones, fonts, always-on display and icons
- Runs as a Magisk module, so the rest of the stock system stays untouched
- Signals success in an obvious way: Chinese text appears inside the official Themes app

That last point sounds strange, but it is reliable. When the Chinese language shows up inside the stock Themes app, the modded store is active. That is your confirmation, and you can relax after seeing it.

## What you need first

- A POCO X7 Pro on official HyperOS. This is not for a custom ROM.
- A rooted device. No root, no module, no modded store. There is no way around that.
- Test Theme Manager installed. This is a prerequisite, so get it in place before the module.
- The theme module itself, from the link on this page.
- Five minutes and a reboot. That is the whole time cost.

## The steps

## Step 1 — confirm root is actually working

Open Magisk and check that it is installed and happy. If root is half working, the module will install and do nothing, and you will spend an hour wondering why. Settle this first.

## Step 2 — install Test Theme Manager

Get this in place before the module. It is listed as a prerequisite, which means the module expects it to be there.

## Step 3 — install the theme module in Magisk

Open Magisk, go to the modules section, and install the theme module from the link here. Let it finish on its own.

## Step 4 — reboot and wait for a full boot

Reboot the phone and let HyperOS come all the way up. Do not start poking at the Themes app while the phone is still settling.

## Step 5 — check for the success signal

Open the official Themes app and look for the Chinese language. If it is there, the modded store is live. That is your green light.

## Step 6 — import and start swapping

Go into themes, import what you want, then change wallpapers, widgets and icons. Fonts, ringtones and always-on display come along with it.

## What it is not

- It is not a third-party theme store you sideload and update every month. You keep the official app.
- It does not unlock anything tied to an account. It changes which themes your device will accept as imports.
- It will not survive a clean reflash of HyperOS. Flash and you install the module again. That is normal.

## Where people get stuck

- **No root.** This is the big one. If the phone is not rooted, nothing here happens, and there is no workaround.
- **Skipping Test Theme Manager.** It is a prerequisite for a reason. Install it first.
- **Expecting it to look different.** The success signal is the Chinese text inside the app you already have. If you are hunting for a new app icon, you are looking in the wrong place.

## An honest note

The result is a theme library that no longer argues with you. You open the Themes app, paste in a theme you downloaded, and it takes it. After that the phone starts looking like yours instead of like the default it came with.

Keep in mind every one of these mods rides on top of a stock system, so a HyperOS update can change behaviour. If something stops working after an update, reinstalling the module is the first thing to try.

The module needs root, and getting root usually starts with an unlocked bootloader and a PC. If the driver and fastboot part is what slows you down, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is on this page.

::faq
Q: Do I need root for the modded theme store on HyperOS?
A: Yes. It is a Magisk module, so root is required. Without root there is no way to install it, and no workaround exists.

Q: How do I know the modded theme store is working?
A: Open the official Themes app and look for the Chinese language. When that text shows up inside the stock app, the modded store is active. It is an odd signal, but it is reliable.

Q: Does this replace the official Themes app?
A: No. It keeps the official HyperOS Themes app and changes what it will import. There is no third-party store to sideload and keep updating.

Q: Does the theme module survive a HyperOS reflash?
A: No. A clean reflash of the ROM wipes it, so you install the module again afterwards. A HyperOS update can also affect behaviour, so reinstalling is the first thing to try if it stops working.

Q: What can I change after it is installed?
A: Wallpapers, widgets, dynamic wallpapers, ringtones, fonts, icons and the always-on display. Once the modded store is active, you import the theme you want and apply the pieces from it.
