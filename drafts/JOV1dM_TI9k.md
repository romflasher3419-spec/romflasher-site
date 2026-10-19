::summary
LineageOS on the Xiaomi Pad 5 is a clean, stripped-back AOSP build with no ads, no storefront and none of the usual software pile. It is fast and plain and honest, and it does the basics very well — but you give up the MIUI extras, and there is no getting them back.

::body
LineageOS has been the safe pick in custom ROMs for years, and that is exactly why it lands on tablets like the Pad 5. Nothing on the screen is trying to sell you anything. The interface is AOSP with the rough edges smoothed off, and after a day of use the tablet starts feeling like hardware instead of a shop window.

I flashed it clean and lived with it, and this is what actually changed.

## What it looks like

The home screen is bare in the good sense. A launcher that just shows your apps, an app drawer that does not push a store in your face, and quick settings that are a grid of toggles rather than a wall of suggestions. On a tablet this reads as calm. There is less on the screen, and nothing moves that you did not ask to move.

First boot lands you in a plain setup flow. No Xiaomi account nagging, no recommendation folder waiting on the second page. It feels like someone cleared the desk before you sat down.

## What changed after the switch

- **Speed.** The tablet is quick in a way bloated stock software rarely manages, especially at the first couple of app launches after boot.
- **Gestures.** Navigation is responsive and predictable — swipes register where you expect them to.
- **Split-screen.** Everyday apps and split-screen use on the big display both behave. The screen is the reason you bought this tablet, and LineageOS lets it do its job.
- **Battery.** Daily use is normal for this hardware. Nothing alarming either way — it is not a magic battery win and it is not a drain.
- **Clutter gone.** The system apps that exist are the ones you would install anyway.

## What you give up

This is the part the review has to be honest about. Moving away from MIUI costs you the pieces that only work with Xiaomi software:

- **The pen and keyboard niceties.** The stock software had features built around those accessories. LineageOS does not carry them over.
- **Xiaomi's camera processing.** The camera works, but it is not the same camera you had.
- **The MIUI layout.** If you learned where things live in MIUI, you are relearning now.
- **Google apps.** They are not included. Flash a GApps package after the ROM if you want the Play Store.

If you bought the tablet for the pen, the keyboard or the camera, this build feels like a step backwards. If you bought it for the screen and the price, it fits like a glove.

## What is broken

Nothing in my daily use was broken in a way that stopped me. The friction is all "missing" rather than "malfunctioning" — features that did not come across, not features that fail. That is a different kind of disappointment than a crash, and it matters when you decide.

## Who should install it

Install it if you want the tablet lean, plain and free of the software pile, and you do not care about the pen or the camera pipeline. Skip it if those extras are why the Pad 5 is in your bag. The honest test: open your last ten photos and think about how you took them. If most were shot on this tablet, do not switch.

## Before you start

- **A PC.** Unlocking and the fastboot flashing both need one.
- **The driver.** Get ADB and fastboot working first — the free Rom Flasher tool brings the driver install down to a couple of clicks.
- **Platform Tools** for the fastboot commands.
- **A backup.** Coming from MIUI, this is a clean flash. Your data is not staying.
- **The recovery and vbmeta** this build needs. Signs of a mismatched recovery show up mid-write, which is the worst time to find out.

Going back is easy, which is the reassurance here. A MIUI fastboot package flashes straight over LineageOS whenever you decide you have had enough.

::faq
Q: Do I need a PC to install LineageOS on the Xiaomi Pad 5?
A: Yes. Unlocking the bootloader and the fastboot flashing steps both happen from a computer. You cannot do this entirely on the tablet.

Q: Does LineageOS include Google apps?
A: No. The ROM ships without them. Flash a GApps package after the ROM if you want the Play Store and Google services.

Q: Will installing LineageOS wipe my data?
A: Yes. Moving from MIUI is a clean flash, so back up your files first and expect the setup wizard on first boot.

Q: What do I lose by moving to LineageOS from MIUI?
A: The extras that depend on Xiaomi software — the pen and keyboard features, Xiaomi's camera processing and the familiar MIUI layout. The tablet is faster and plainer, but those parts do not come along.

Q: Can I go back to MIUI later?
A: Yes. A MIUI fastboot package for the Pad 5 flashes straight over LineageOS. Plan for another wipe when you switch back, so keep a backup from the LineageOS side if you need it.
