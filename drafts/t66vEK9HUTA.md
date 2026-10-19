::summary
DerpFest on the Xiaomi 11T Pro runs genuinely smooth with no stutter and no random glitches, and battery backup is strong at around 13 to 14 hours of real use. The problems are Play Certification, banking apps that behave as if the phone is rooted, slow charging, no face unlock and unreliable auto call recording. It can be a daily driver if those trade-offs are acceptable to you.

::body
Let me give you the honest version up front, because that is what this build deserves.

DerpFest on the 11T Pro runs smooth. Genuinely smooth. No stutter, no random glitches, once it settles down after the first boot. That is not a small achievement on a custom ROM, and it is the reason some people stay on this build.

But some things need fixing, and a few of them decide whether this can be your daily driver. So let me go through what I actually tested rather than what the feature list says.

Device here is the Xiaomi 11T Pro, codename vili. ROM is DerpFest on an AOSP base.

## What it looks like

It looks like clean AOSP. The launcher, the shade, the Settings tree — all recognisable, none of it MIUI. If you have been on MIUI and you jump here, the first day is a small adjustment. By day three you stop noticing.

The camera app is where the difference is most visible. The MIUI camera app is not here. That is normal for an AOSP build, and it is the number one thing people miss.

## What I tested

- Play Certification status and how banking apps react to it
- Google Photos behaviour, specifically the unlimited storage treatment
- Gaming, where titles hold the usual 60fps
- Call recording, which is present but does not always record on its own
- Charging speed and real battery backup
- The camera, including video recording at 60fps

## Play Certification and banking apps

This is the part that bothers people more than any benchmark number ever will. Play Certification is missing on this build, so banking apps react as if the phone is rooted, even though it is not.

Nothing you did wrong. The device simply is not certified, and several banking apps check that. Some will refuse to open. Some open and then complain. A few carry on as if nothing happened. Which camp your bank is in is not something I can tell you in advance, and it is worth checking before you commit the evening.

The knock-on effect is Google Photos. It will not hand you the unlimited storage treatment on this build. If you back up a lot of photos, price that in.

## Battery and charging, the split decision

Charging is slow. That is the cleanest way I can put it. Plugged in, it feels like you are on a 33W brick rather than the phone's real fast-charge capability. It is annoying, and it is the one hardware behaviour that genuinely bugs me.

Endurance is the opposite story. With voice calls, GPS on and brightness high, I still got around 13 to 14 hours of comfortable use out of it. That is a full day with change for most people, on a phone being pushed hard.

So: slow to fill, slow to empty. Depending on how you use a phone, that trade is either fine or a dealbreaker.

## Gaming

Games run at the usual 60fps on this build. Same as any normal ROM. Gaming is not the problem here, and there is nothing about DerpFest that makes titles behave badly.

## What is missing or broken

- **Face unlock is not available.** Not a bug, just not present. If you rely on it, that is a real loss.
- **Call recording is present but does not always record on its own.** You cannot fully trust it to catch a call without you doing something about it.
- **Play Certification is missing**, with the banking and Google Photos consequences above.
- **Charging is slow.** The most daily-annoying of the lot.
- **No MIUI camera app.** The included camera takes decent shots and records at 60fps, but it is not the MIUI camera.

## Who should install it

- Someone who wants clean AOSP performance and does not depend on banking apps that check Play Certification.
- Anyone who cares more about smoothness and battery endurance than fast charging.
- People who can live without face unlock and with manual call recording.
- Anyone who wants a fast, settled custom ROM and is willing to test their own must-have apps before trusting the build.

If you need face unlock, or you rely on a certification-checking banking app, skip this one. No amount of smoothness makes up for a bank app that will not open.

## Before you flash

- **Unlocked bootloader.** Required, and it wipes the phone the first time.
- **A full backup.** Everything on internal storage goes.
- **Platform tools and the right recovery** for your device, ready before you start.
- **vbmeta**, if the method you follow needs it, because AOSP builds usually need verity and verification handled.

If the driver side is the part you dread, the free Rom Flasher tool on GitHub installs the ADB and fastboot drivers in a couple of clicks. It is free, and the link is in the downloads section.

One last thing. Test your banking app on day one, before you have restored a single file. Finding out late is much worse than finding out early.

::faq
Q: Why do banking apps think my phone is rooted on DerpFest?
A: Play Certification is missing on this build, so apps that check device integrity treat the phone as if it is rooted even though it is not. The fix is certification, not removing root, because there is no root to remove.

Q: Is battery life good on DerpFest for the Xiaomi 11T Pro?
A: Yes, endurance is one of the strong points. With voice calls, GPS on and brightness high, around 13 to 14 hours of comfortable use was realistic. Charging, on the other hand, is slow.

Q: Why is charging so slow on DerpFest?
A: Charging does not reach the phone's full fast-charge speed on this build, so it feels like a much lower wattage brick. It is one of the main annoyances and worth knowing before you flash.

Q: Does DerpFest have face unlock?
A: No. Face unlock is not available on this build. If that is a feature you use every day, it is a real reason to look at another ROM.

Q: Does Google Photos give unlimited storage on DerpFest?
A: No. Because Play Certification is missing, Google Photos gives limited backup only. If you rely on that, either back up elsewhere or pick a build that carries certification.
