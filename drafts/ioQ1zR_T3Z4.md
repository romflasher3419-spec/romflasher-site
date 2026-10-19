::summary
Joker Face MIUI 14 on the Xiaomi 11T Pro is modded MIUI, not an AOSP port, so the phone still feels like a Xiaomi. It ships with the newer Leica camera app, iOS emoji baked in, a battery health screen, SafetyNet passing, and a debloated base with MiuiDaemon and the browser gone.

::body
This is modded MIUI, so the first thing to understand is that nothing about the phone's feel changes. Same control centre, same settings tree, same gestures. If you handed it to someone who did not know, they would say it is MIUI, and they would be right.

What changes is the detail work. The build is cleaned up, the camera app is the newer Leica one, and a pile of stock annoyances have been patched out. I walked through every screen I could, and the phone held up. Banking apps opened normally and the Play Store showed up certified, which is the part most modded builds get wrong.

The device is the Xiaomi 11T Pro running Joker Face MIUI 14, based on 14.0.1.

## What is actually inside

- Thunder animation while charging, on the statusbar.
- iOS emoji set baked into the system, so every app sees it, not just a few.
- SafetyNet passing by default, with no extra steps from you.
- The newer MiuiHome v2 launcher running on MIUI 14.
- The new Leica camera app.
- A battery health screen added, which stock MIUI does not show you.
- An extended power menu.
- Notification groups, and a screenshot frame.
- Extra options in MIUI Lab under Accessibility.
- Automatic screen refresh rate adjustment.
- Unlimited Google Photos.
- Super icon unlock, and this one needs no root.
- Debloated. MiuiBugReport, MiuiDaemon, MiBrowserGlobal and Updater are gone.
- The control centre MiPlay bug fixed.

## The parts that genuinely change daily use

The debloating is the quiet one that matters most. MiuiDaemon and the various report and updater pieces run in the background whether you notice them or not. Taking them out is why the build feels lighter than stock, and it is also why the Updater app is missing — you will not be checking for MIUI updates from the phone any more, because there is nothing there to check with.

The battery health screen is the second one. On stock MIUI you have no idea what state your battery is in without a third-party tool. Having it built in is a small thing that you end up checking more often than you would expect.

The third is the automatic refresh rate adjustment. The 11T Pro has a high refresh panel, and letting the system decide when to drop it saves battery in the places you would never manually remember to switch.

## Where it holds up and where it does not

The certified Play Store, unlimited Google Photos, and banking and payment apps opening without complaints together make this feel like a daily driver rather than a project. That combination is rare in a modded build, and it is the strongest argument for this one.

The camera is the trade-off. It is Xiaomi's Leica app, so do not expect the Google camera processing you would get from an AOSP ROM. If you flash AOSP builds for the photo quality, this is not that. The Leica app is good in decent light and behaves the way MIUI's camera always has in poor light.

And MIUI 14 keeps its own quirks. A modded build fixes plenty of them, not every single one. Expect the usual MIUI habits to still be there underneath.

## Who should install it

Install this if you are happy with MIUI and you want it tidier. If you like the control centre, you have no complaints about the gestures, and what annoys you is the clutter and the missing screens rather than the interface itself, this build is pointed straight at you. The no-root super icon unlock and the baked-in emoji set are the kind of things you would otherwise chase through separate modules.

Skip it if MIUI is the actual problem. If the animation style or the settings layout is what you want gone, this will not help, because it is MIUI with the rough parts sanded down.

## How to flash it

1. Back up anything you care about. This is first for a reason.
2. Reboot to recovery and format data if you are coming from a different base. A dirty flash across bases is where odd crashes come from.
3. Flash the ROM zip and let it finish completely.
4. Reboot to system and set the phone up fresh.

If you are on stock MIUI 14 already, the wipe situation is the thing to get right before you start. Coming from a different base without a format is the single most common reason a modded MIUI build boots and then behaves strangely.

One last thing, on setup: get through the first boot and finish the wizard before you restore anything. If something is going to break, you want it breaking on an empty phone rather than on top of a restored set of apps.

If the ADB, fastboot and driver side is what slows you down every time, the free Rom Flasher tool on GitHub does that part in a couple of clicks. It is free, and the link is in the downloads list.

::faq
Q: Is Joker Face MIUI 14 an AOSP ROM?
A: No. It is modded MIUI based on 14.0.1, so the interface, the control centre, the settings tree and the gestures are all still MIUI. Only the detail level changes, not the feel of the software.

Q: Does this build pass SafetyNet and work with banking apps?
A: SafetyNet passes by default in this build, and banking and payment apps opened normally in my use. The Play Store also showed up certified, which is the part modded builds usually fail at.

Q: Does Joker Face MIUI 14 need root?
A: No. The super icon unlock is included and does not need root to work. That is one of the features that would normally push you into installing a separate root module.

Q: What is debloated in this ROM?
A: MiuiBugReport, MiuiDaemon, MiBrowserGlobal and the Updater are removed. That is why the build feels lighter than stock, and it is also why there is no MIUI update checker on the phone any more.

Q: How is the camera on Joker Face MIUI 14?
A: It uses Xiaomi's Leica camera app rather than Google camera processing, so do not expect the look you get from an AOSP ROM. It is solid in good light and behaves like MIUI's camera in poor light.

Q: Do I need to wipe data before flashing it?
A: Yes, format data in recovery if you are coming from a different base. Flashing over a different base without a wipe is the usual reason a modded MIUI build boots and then crashes or hangs.
