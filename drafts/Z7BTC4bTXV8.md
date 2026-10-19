::summary
OxygenOS on the Redmi Note 5 Pro puts the OnePlus interface on whyred — its own launcher, its own gestures, the familiar settings layout. The look is the reason to flash it. The ported software underneath is the reason to keep your expectations small.

::body
The Redmi Note 5 Pro is ancient, and that is exactly why people keep flashing it. There is nothing left to lose on a phone this old, so you can afford to be curious. OxygenOS brings the clean OnePlus interface to whyred, and seeing it boot on Xiaomi hardware is genuinely fun the first time.

This is a review, not a tutorial. If you have flashed a ROM before, you already know the shape of the job: unlock the bootloader, get a recovery running, back up, wipe, flash, wait. Here I am going to talk about what a normal day on this ROM actually feels like, and where it lets you down.

## What it looks like

The first thing you notice is the launcher. It is the OnePlus launcher, with its own icon style, its own shelf on the home screen, and the app drawer that pulls up from the bottom rather than the middle. If you have used a OnePlus phone, your hands know it immediately.

The settings app is the other giveaway. Sections are grouped the way OnePlus groups them, not the way Xiaomi does. The quick toggles in the shade are rounder and laid out in a different rhythm. The lock screen clock style is distinct.

None of this is cosmetic-only. The whole navigation language changes. OxygenOS gestures — swipe up from the bottom for home, swipe up and hold for recent apps — replace whatever you were using. Some people find them cleaner than the stock Android gesture setup. I did, mostly.

## What was tested

- First boot and the setup wizard, end to end.
- The launcher: home screen, app drawer, icons, widgets.
- The system apps that come with it — dialer, messages, clock, file manager.
- Gestures and navigation, including switching between the button and gesture modes.
- Settings, quick toggles and the notification shade.
- The camera app: opening it, framing a shot, taking a basic photo.
- Battery drain across a normal day of light use.
- How the phone feels during everyday scrolling.

## What changed

The interface is the whole story. Going from MIUI to OxygenOS on the same phone is a bigger change than going from MIUI to most custom ROMs, because you are swapping one complete design language for another complete design language.

The system apps feel lighter than the Xiaomi equivalents. Fewer background services, fewer places asking you to sign in. The settings menu has fewer dead ends.

The navigation change surprised me more than the launcher. Once you are used to the OnePlus gesture model, going back to button navigation feels clunky.

What did not change is the Android underneath. This is older software, and you should not open it expecting the system features current Android ships with. No recent notification categories, no newer permission controls. You get the interface, not the era.

## What is broken

- **The camera is the weakest part.** That is true of almost any port on old hardware, and this one follows the pattern. It opens. It takes photos. It is not what you would call good, and low light is where it hurts most.
- **Banking apps are a coin flip.** Do not count on them with a ported ROM. Some will open, some will refuse because the device no longer looks like what they expect. If your bank app is essential, you have your answer.
- **Heavy gaming is out.** This phone is old and the software is ported. The two together do not make a gaming machine. Light games are fine. Anything demanding will heat the phone and drop frames.
- **Battery is unremarkable.** It drains like a phone this old drains with a normal day of use. Do not flash this expecting better battery life as a bonus, because you will not get one.

## Who should install it

Flash OxygenOS if you want the OnePlus look on a phone you already own, and you are happy to treat it as a curiosity or a light daily driver. It is the right pick for that. The interface alone justifies the evening it takes.

Do not flash it if your banking apps matter, if you game seriously, or if you expect a camera you can rely on. Those three are the honest dealbreakers here, and no amount of setup will fix any of them.

One more thing worth saying plainly. Ported ROMs on old hardware are kept alive by people doing this in their spare time. Updates are rare and can stop without warning. That is not a flaw in this build specifically — it is the nature of the category. Keep the zip you flashed somewhere safe so you can get back to a known state.

If the unlocking and driver side of getting here is what slows you down, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Do I need to unlock the bootloader to flash OxygenOS?
A: Yes. There is no way around it on this device. The unlock wipes the phone, so do it before you set anything up or copy your files back.

Q: Is OxygenOS on the Redmi Note 5 Pro good enough as a daily driver?
A: For light use, yes — calls, messages, browsing, music, photos all work. For heavy gaming or anything that needs current Android features, no. It is older software on older hardware.

Q: Will banking apps work on this ROM?
A: Do not count on it. Ported ROMs often fail the checks banking apps run, and some will refuse to open. Test your essential apps before you commit to making this your main phone.

Q: Is the camera better than MIUI on this phone?
A: No. The camera is the weakest part of almost any port on old hardware, and this one is no exception. It works, but low light and detail are both a step behind what MIUI got out of the same sensor.

Q: Is this an official OxygenOS build for whyred?
A: It is an official build for this device, meaning it was put together to run properly on this hardware rather than being a half-finished experiment. It is still old software, so expect the limits that come with that.
