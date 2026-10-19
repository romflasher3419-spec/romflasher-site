::summary
Elite ROM on the Xiaomi 11T Pro is MIUI 14 Stable EEA with Android 13 underneath, and the January 2023 build I ran carries EliteMod v1.0. The customizations are the reason to flash it: a dual statusbar you configure separately on each side, blur options, unlimited Google Photos in storage saver, and a fix for the brightness dip during games.

::body
This one landed on 20 January 2023, built on the EEA stable branch. So the base is Xiaomi MIUI 14 with Android 13, and on top of it sits a long list of Elite customizations that would normally need three separate modules stacked on top of each other. I went through the settings screen by screen, used the phone properly for a while, and this is the honest read.

## What it looks like

Out of the box it looks like MIUI 14, which is the point. Same launcher layout, same control centre, same settings tree. The new MIUI 14 launcher is in there with the super icons, and the package installer handles apps with different signatures, which matters more than it sounds when you are installing sideloaded builds.

You notice the difference the moment you open the Elite Customizations menu. That menu is deep. It takes an evening to work through properly, and that is a real cost, not a feature list item.

## What actually changed

- **Dual statusbar.** Left and right sides configured separately, with clock, network speed, battery and notification icons all tunable — size, color, scaling, font and font style.
- **Blur controls.** Options for folder and recents backgrounds, plus list animations and list interpolation choices.
- **Screenshot in secured apps.** Allowed, which is one of those small things you only miss when it is gone.
- **Global dark mode.** One toggle applied across every app instead of per app.
- **Unlimited Google Photos.** Enabled in storage saver, so uploads stay free without resizing tricks.
- **Brightness dip fixed.** It no longer dims itself mid gaming session, which was an old MIUI annoyance.
- **AOD deep sleep fixed.** With a toggle to disable AOD in a dark room, and show or hide for AOD notification icons.
- **Anti flicker mode on**, WiFi region unlocked, and the permission timer removed.
- **Edges effects and charging animations** on the statusbar and the sides.

## Under the hood

The build is fully deodexed and debloated, so it feels lighter than the stock EEA package. System is R/W, which matters if you like to modify things yourself, and the ROM is fully decrypted.

Those two facts explain most of the difference you feel. A debloated deodexed base boots lighter and leaves fewer background processes fighting for memory.

## What is broken or fiddly

- **The animation feel.** The base underneath is still MIUI, so do not expect Pixel smoothness in animations. Transitions have that MIUI weight to them.
- **Folder icons shrink.** Push the icon size too far and the folders get smaller than they should. They fixed the obvious case, but extreme values still show it.
- **Quick Reply is missing.** It was pulled from Settings because it was buggy on the base side. If you used it daily, that is a real loss.
- **The setup time.** The Elite Customizations menu is huge. You will not finish it in ten minutes, and rushing it usually means you forget what you changed.

Everything else held up in normal use over the time I ran it. No crashes I could tie to the ROM, and the day-to-day stuff behaved.

## Who should install it

Install this if you like tuning your phone. If you spend time in statusbar settings and hate being locked to a stock layout, the customization set is the product and it is worth the flash. The blur options and the unlimited Photos alone are things people flash several modules to get.

Skip it if you want a clean AOSP experience. This is MIUI with better manners, not a different operating system. If MIUI's animation style or its settings layout annoys you, Elite ROM will not fix that, because it is the base.

One practical note. Before you flash, back up what matters, and be ready for the first boot to take a while. If the driver and ADB side of your setup is the part that always fights you, the free Rom Flasher tool on GitHub installs that in a couple of clicks, and the link is in the downloads section.

::faq
Q: Is Elite ROM based on Android 13?
A: The build I reviewed is MIUI 14 Stable EEA with Android 13 under it, packaged on 20 January 2023 with EliteMod v1.0. So yes, Android 13, but the interface is MIUI rather than stock Android.

Q: What is the point of Elite ROM over normal MIUI 14?
A: The customizations. A dual statusbar configured per side, blur options for folders and recents, screenshot in secured apps, unlimited Google Photos in storage saver, global dark mode and a long list of small fixes. On stock MIUI you would stack several modules to get even close.

Q: Does Elite ROM fix the brightness dimming during games?
A: Yes, that is one of the listed fixes. The build no longer lowers brightness on its own mid gaming session, and the AOD deep sleep problem is fixed as well, with a toggle to disable AOD in a dark room.

Q: Does Google Photos upload stay free on this build?
A: The build enables unlimited Google Photos in storage saver, so uploads do not need resizing tricks to stay free. It applies to storage saver quality, not original quality.

Q: Does Elite ROM pass SafetyNet and can I use banking apps?
A: Nothing in the build promised that, and this is MIUI-based, so treat it like any modified ROM. Test your own banking and payment apps after the first boot. If they complain, that is normal for a modified system and not something the ROM guarantees against.

Q: Is it smooth like a Pixel ROM?
A: No. It is still MIUI underneath, so animations carry MIUI's weight instead of Pixel's. What you gain is deodexed, debloated, R/W system and a huge customization set, not a change in how the system moves.
