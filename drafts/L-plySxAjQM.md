::summary
MIUI 14 Super Icon gives you the big tile-style home screen icons, and face it, there is no toggle for it anywhere in settings. You enable it through a module instead, which means Magisk root first, then LSPosed, then the theme manager file. The whole job is a few minutes and two reboots.

::body
You have seen the Super Icon look in screenshots. Big, chunky tiles on the home screen, no icon labels, a very specific MIUI 14 feel. You go looking for the setting and there is nothing. No toggle, no theme option, no hidden menu.

Here is why. Super Icons are not really a theme you can apply from the theme store. They are part of MIUI 14's home screen look, and MIUI does not hand you a switch for it. So you go around the problem rather than through it: you install a module that turns the feature on.

That means root. LSPosed is an Xposed-style framework, and it does not run without root. If you are not rooted yet, this is not the article you need first.

## What you need

- MIUI on the phone as the base. This is a MIUI feature being switched on, not something you can bolt onto a stock Android build.
- Root with Magisk, installed and settled. Not freshly flashed and still shaky, actually working.
- The MIUI theme manager file and LSPosed, both from the links.
- Five minutes and a reboot or two.
- Nothing else. This does not wipe your data and it does not touch your bootloader.

That last line is the reassuring part. This is an app and a module. Your files, your apps and your setup stay exactly where they are.

## Step 1 - get root working first

No root, no LSPosed, no Super Icon. Open Magisk and confirm it is actually granting root to apps, not just installed. If you are still at the point where the Magisk app shows something odd, sort that out before you continue.

This is also the step where you should be honest with yourself about the phone. If your device is not running MIUI, the feature you are switching on does not exist underneath, and nothing good will come of forcing it.

## Step 2 - install the theme manager file

Install the MIUI theme manager file from the link. Treat it as a normal app install and let it finish completely before you move on.

## Step 3 - install LSPosed and enable the module

Install LSPosed from its link. Open it, find the module in the list, and enable it. Scope matters here: make sure the module is scoped to the theme manager and the home screen side of things, not left with no scope at all. A module enabled with the wrong scope loads, does nothing, and leaves you convinced the whole method is broken.

Then reboot. The framework needs a fresh boot to pick up a newly enabled module.

## Step 4 - apply the Super Icon style

Open the theme manager, find the Super Icon style, and apply it. If the icons do not change straight away, reboot once more. Sometimes the home screen holds onto the old icon layout until the next boot.

Once it takes, it sticks. You do not need to reapply it after every restart.

## Where people get stuck

- **No root.** This is the big one. LSPosed will not run, and without it the module has nothing to hook into.
- **Module enabled but not scoped.** It shows as on, the phone behaves exactly the same, and you assume the method does not work. Check the scope before you give up.
- **Not rebooting.** Enabling a module and immediately checking the home screen is a waste of a minute. Reboot, then look.
- **Installing something you cannot vouch for.** Modules run inside your system. Stick to the linked files rather than whatever a thread suggests.

## One honest note

The reboot dance is mildly annoying. Enable, reboot, apply, maybe reboot again. It is not a one-tap job, and the first time you do it the pauses feel longer than they are. Once it is set up, though, you forget about it. That is the trade: five fiddly minutes, then it is just how your phone looks.

If you are rooted on MIUI and you like the way this looks, it is worth the five minutes. If you are on a build that is not MIUI underneath, save your evening. And if you are not rooted at all, the free Rom Flasher tool on GitHub exists precisely for that part of the journey, and it is free.

::faq
Q: Do I need root for MIUI 14 Super Icon?
A: Yes. Super Icon is enabled through an LSPosed module, and LSPosed is an Xposed-style framework that will not run without root. Get Magisk working first, then install the module.

Q: Is there a built-in setting for Super Icons in MIUI?
A: No. MIUI does not expose a toggle for it. That is exactly why the module route exists. You enable the feature through LSPosed rather than through settings.

Q: Will enabling Super Icon wipe my phone or break MIUI?
A: No. It is an app install plus a module, so your data stays put and your bootloader is untouched. The main risk is installing module files from a source you do not trust.

Q: Does the Super Icon change survive a reboot?
A: Yes. Once the module is enabled and the style is applied, it stays applied across restarts. If it does not show right away, one more reboot usually settles it.

Q: Why is the module enabled but nothing changed?
A: The module is probably not scoped correctly inside LSPosed, or you did not reboot after enabling it. Set the scope to the theme manager and home screen, then reboot before checking the icons.
