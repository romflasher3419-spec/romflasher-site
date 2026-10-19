::summary
Unlocking the bootloader on a POCO or Xiaomi phone means three things: applying inside the Mi Community app, adding your Mi account on the device under Mi Unlock Status, and then waiting seven days before Mi Unlock on a PC finishes the job. There is no shortcut, and rushing it only restarts the clock.

::body
Xiaomi did not make this easy. What they did make it is predictable, and that is worth knowing before you start.

The flow is: apply in the app, link your account on the phone, wait seven days, then finish on a PC. That order matters. Doing the steps out of sequence is the most common reason people end up repeating the whole week.

This is the order that worked on a POCO X7 Pro, and the same flow applies to most other POCO, Redmi and Xiaomi models.

## What you need

- The Mi Community app, from the link in the downloads section.
- The Mi Unlock software on a Windows PC, for the final step.
- The ADB and fastboot driver installed, so that PC can actually see the phone.
- The **same** Mi account signed in on the phone and inside the app.
- Mobile data switched on for the account step. Not Wi-Fi.

That fourth point sounds obvious and people still get it wrong. Two different accounts means the device is not linked to the account that got the approval, and the wait never starts counting properly.

## Step 1 — get the app and sign in

Install the Mi Community app and sign in with your Mi account. This is the account that will own the unlock, so use one you will still have access to in a week. Do not create a throwaway.

## Step 2 — grant every permission it asks for

This is not the moment to be stingy. The app needs the permissions it requests, and if you deny them the bootloader unlock option simply never appears in your profile. You will sit there refreshing a menu that has nothing in it.

Give it everything it asks for.

## Step 3 — find the unlock option in your profile

Open your profile inside the app, tap **Mi**, and look for the bootloader unlock entry. That is where the application lives.

## Step 4 — apply inside the request window

The application only opens during a limited window each day. There is a timer in the app, and it counts down roughly nine and a half hours until the window opens.

When it hits zero, tap immediately. These windows fill up, and if you come back ten minutes later the option is often gone until the next one.

You will be asked to answer a short quiz style check as part of applying. Read the questions properly. Fumbling them means starting over.

## Step 5 — link the account on the phone

Now go to the phone itself. Open **Settings**, then **Developer options**, then **Mi Unlock Status**, and agree to the terms shown there.

If you cannot find Developer options, go to About phone and tap the build number repeatedly until it unlocks. That is normal on MIUI and HyperOS.

## Step 6 — turn Wi-Fi off before you add the account

This is the step that catches the most people. Turn Wi-Fi off. The account has to be added over mobile data, and it will fail on Wi-Fi.

With Wi-Fi off, tap **Add account** in the Mi Unlock Status screen and confirm it goes through. Only move on once it clearly succeeded — a half-finished add means the seven days have not started.

## Step 7 — wait seven days, properly

Once the account is added, the countdown starts. Seven days from that moment.

During that week, two things will reset the timer back to zero:

- Removing the Mi account from the phone.
- Resetting the phone.

So leave it alone. Do not factory reset it, do not sign out of the account, do not switch to a different Mi account. Boring is correct here.

## Step 8 — finish with Mi Unlock on the PC

After the seven days, power the phone off and hold **Volume Down + Power** to reach fastboot mode. Connect it to the PC with the driver installed.

Open Mi Unlock and sign in with the same Mi account. The software will see the phone, confirm the waiting period is over, and run the unlock. The phone reboots and wipes itself as part of this.

If Mi Unlock says the device is not connected, that is a driver problem, not a Xiaomi problem. Fix the ADB and fastboot driver first — the link is in the downloads section.

## Where people get stuck

- **Wi-Fi switched back on during the account step.** The add fails silently, or fails with a message about the network. Turn Wi-Fi off and do it again on mobile data.
- **Two different Mi accounts.** One in the app, one on the phone. The link never completes, and the week never starts.
- **Removing the account or resetting during the wait.** The full seven days restart from zero. There is no support ticket that fixes this.
- **Missing permissions in the app.** No permissions, no unlock option, no application.

## One honest thing to know

Unlocking the bootloader **wipes the phone**. Everything on internal storage goes, so move your photos and anything else you care about off it before Step 8, not after.

You also do not need the free Rom Flasher tool for unlocking — Mi Unlock does that. Where the tool helps is the driver install on the PC, which is the part people quietly give up on. It is free, and it is in the downloads section.

The week feels long while you are waiting for it. Use it to download your ROM and read the flashing steps for your model, so the day the countdown ends you are ready to go instead of starting your research then.

::faq
Q: Can the 7 day bootloader unlock wait be skipped?
A: No. The timer starts when the account is successfully added on the device and nothing shortens it. Attempting to rush it, removing the account or resetting the phone, starts the full seven days again.

Q: Will unlocking the bootloader wipe my data?
A: Yes. Unlocking wipes the phone, so back up photos, downloads and anything else you care about before you run Mi Unlock on the PC. Accounts and app data go with it.

Q: Why does the bootloader unlock option not appear in Mi Community?
A: You probably denied a permission the app asked for. Grant all of them, then reopen your profile and check the Mi section again. Without the permissions the option stays hidden.

Q: Why does Add account fail in Mi Unlock Status?
A: Wi-Fi is on. Turn it off and add the account over mobile data instead. Also check that the phone and the app are signed into the same Mi account.

Q: Do I need a PC to unlock a Xiaomi bootloader?
A: For the final step, yes. Mi Unlock runs on Windows. The application and the account linking happen on the phone, but the actual unlock is done from a PC with the phone in fastboot mode.
