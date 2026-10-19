::summary
Unlocking the bootloader on the Xiaomi 11T Pro uses Xiaomi's Mi Unlock Tool on a PC, and it is five steps once the waiting period is done. The part nobody warns you about is the wait — your Mi account usually has to stay bound to the phone for 168 hours before the unlock button works.

::body
Every custom ROM, every recovery, every root guide on the 11T Pro starts here. No unlocked bootloader, no flashing. Full stop. So this is the one step worth doing carefully, because it is also the one you cannot undo quietly — unlocking wipes the phone.

The route is Xiaomi's own Mi Unlock Tool on a PC. It is not complicated. It is just picky: it wants the right drivers, the same Mi account on the phone and the PC, and it wants you to wait.

That waiting period is where most people give up and start hunting for shortcuts that do not exist. There is no way around it. Start the clock early if you know you will flash something.

## What you need

- **Xiaomi 11T Pro** with a charged battery and your data backed up
- **A PC** with ADB and fastboot drivers installed — grab them if you do not have them
- **The Mi Unlock Tool**
- **The same Mi account** signed in on both the phone and the tool
- **Patience.** The account usually has to sit bound to the phone for 168 hours first

## Step 1 — back up the phone first

Do this before Step 2, not after. Unlocking erases the phone. Photos, messages, app data, downloads — all of it is gone when the unlock completes. If you back up afterwards you are backing up an empty phone.

Also make sure the battery is charged. You do not want the phone dying in the middle of this.

## Step 2 — enable developer options and bind your Mi account

On the phone, turn on developer options, then enable **OEM unlocking** and **USB debugging**. Then bind your Mi account to the device — this is the step that starts the clock. The phone and the PC have to use the same Mi account, or the tool refuses.

This is the moment to think about the wait. The binding is what starts the 168-hour timer, so binding it today means you can unlock next week.

## Step 3 — reboot to bootloader and check the PC sees it

Power the phone off and hold **Volume Down + Power** to reach fastboot, or use the developer options menu. Plug in and run:

`fastboot devices`

You want the serial number back. If nothing shows up, it is the driver or the cable — install the ADB and fastboot driver and try another cable. The unlock tool will not see a phone your PC cannot see.

## Step 4 — open the Mi Unlock Tool

Run the Mi Unlock Tool on the PC and sign in with the same Mi account you bound on the phone. Do not rush this. A different account on the PC than on the phone is a refusal, and the tool does not always explain why.

## Step 5 — click unlock

Press the unlock button and let it work. It takes a few minutes. If the waiting period has not finished, this is where it tells you how long is left. And that is it — those five steps are the whole job once the wait is done.

If it succeeds, the phone reboots and comes up erased. Setup wizard, fresh start.

## Where people get stuck

- **The 168-hour wait.** Fresh account binding, and there is no way around it. The clock starts the day you bind, so bind early.
- **Driver trouble.** If the tool does not see the phone, it is almost always the drivers or the cable, not the phone. This is the single most common hold-up.
- **A different Mi account on the PC.** It refuses, and it does not always say why. Check both sides.
- **The data wipe.** Unlocking erases the phone. Back up before Step 1, not after.

## One honest note

The wait is genuinely annoying, and I understand why people go looking for a way to skip it. There is not one, and the guides promising otherwise are wasting your time or worse. The good news is that once it is done, it is done — the bootloader stays unlocked, and every guide after this one becomes possible.

If the driver side is where you keep getting stuck, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Does unlocking the bootloader wipe the Xiaomi 11T Pro?
A: Yes. Everything on the phone is erased when the unlock completes. Back up your photos, messages and app data before you start, and expect the setup wizard afterwards.

Q: How long do I have to wait to unlock the 11T Pro bootloader?
A: The Mi account usually has to stay bound to the phone for 168 hours first. The clock starts when you bind the account, so bind it as soon as you know you want to unlock.

Q: Can I unlock the bootloader without a PC?
A: Not with the official route. The Mi Unlock Tool runs on Windows, so you need a computer with the ADB and fastboot drivers installed.

Q: Why does the Mi Unlock Tool not see my phone?
A: Usually the drivers or the cable. Install the ADB and fastboot driver so Windows recognises the phone in fastboot mode, and try a data cable rather than a charge-only one.

Q: What happens if the phone and the PC use different Mi accounts?
A: The unlock is refused. The tool wants the same Mi account signed in on the phone and on the PC, and it does not always explain the refusal clearly.

Q: Does unlocking void the warranty?
A: Xiaomi's policy on this has changed over the years and varies by region, so check the terms for your country rather than relying on a general answer. Relocking later is possible, but it carries its own risk of leaving the phone unbootable.
