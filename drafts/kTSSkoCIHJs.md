::summary
You can run a One UI Android 14 port of the Galaxy Tab S9 Ultra on the Xiaomi Pad 5 without wiping your current setup, using the DSU Sideloader app. Two settings decide whether it boots at all: vbmeta verification disabled on stock firmware, and SELinux set to permissive.

::body
This is the smart way to try a big-screen interface. Instead of replacing your whole system, you run the One UI GSI on top of what is already on the tablet, using DSU. If it misbehaves, you reboot and it is gone. Nothing you had before is touched.

The port comes from the Galaxy Tab S9 Ultra, so what you get is Samsung-style multitasking and a layout that actually respects a tablet display. That is the reason to bother. Most GSIs are phone interfaces stretched across a big screen, and it shows. This one was built for a large panel to begin with.

The catch is entirely in the setup. On stock firmware you have to disable vbmeta verification first, and SELinux has to be set to permissive or it will not boot. Skip either one and you get a black screen — no error, no hint, just nothing.

## What you need

- **An unlocked bootloader** on the Xiaomi Pad 5
- **adb and fastboot**, plus the right driver on your PC
- **The One UI GSI file** — link below
- **The DSU Sideloader app**, and **root** to run it
- **SELinux switched to permissive**

## Step 1 — download the GSI

Grab the One UI GSI file first so you are not hunting for it halfway through. Keep it somewhere you can point the sideloader at.

## Step 2 — disable vbmeta verification, if you are on stock

This step applies when you are on stock firmware. The GSI will not boot while verification is still enforcing, because the system image does not match what your firmware expects. Disabling verification is what lets a foreign system image start.

If you are already on a custom ROM that has this handled, you can skip past it. On stock, do not skip.

## Step 3 — make SELinux permissive

This one catches people. This particular GSI needs SELinux in permissive mode. Left on enforcing, it will not come up. It is a real requirement of this port, not a suggestion, and there is no workaround that keeps enforcing on.

Be aware of what permissive means: the security policy is not being enforced. That is fine for a test system you reboot out of, and it is a reason not to leave this setup running as your daily driver forever.

## Step 4 — install the DSU Sideloader app

Install DSU Sideloader on the tablet. It needs root to work. If you are not rooted, this method does not start — that is just how the tool interacts with the system.

## Step 5 — flash the GSI inside DSU Sideloader

Point the app at the GSI file and let it flash. This takes a while and it is worth watching rather than walking away. When it finishes, you will have the option to boot straight into the DSU.

## Step 6 — reboot into DSU and let it boot

Reboot into the DSU and wait. A first boot of a full GSI is not fast. Give it time before you decide it has hung.

If you get a black screen instead of a boot, go back and check Step 2 and Step 3. Those two settings are the answer roughly every time.

## Where people get stuck

- **Forgetting vbmeta verification.** On stock firmware the GSI simply will not boot. No error message, just a black screen.
- **Leaving SELinux enforcing.** This port needs permissive. Enforcing is a no-boot.
- **Setting it as the main system too early.** Test it through DSU first. That is the entire point of using DSU — you keep your working setup while you find out what this one does.

## One honest note

DSU is built for testing, and this is exactly the right use for it. You get to live with One UI on your tablet for an afternoon and decide whether you actually like it, without betting your daily setup on the answer. If you love it, you can look at installing the GSI properly. If you do not, reboot and you are back where you started.

::faq
Q: Does this One UI port replace my current ROM on the Xiaomi Pad 5?
A: No. DSU runs the One UI GSI alongside your existing system. Your current setup stays untouched, and a reboot puts you back on it.

Q: Do I need root to run DSU Sideloader?
A: Yes. DSU Sideloader needs root to install the GSI. Without root this particular method does not work.

Q: Why does the GSI show a black screen instead of booting?
A: Two usual causes: vbmeta verification is still enabled on stock firmware, or SELinux is still set to enforcing. This port needs verification disabled and SELinux permissive.

Q: Does it survive a reboot?
A: By default, no. DSU is meant for testing, so a reboot returns you to your normal system. Your One UI install is still there to boot into again unless you set it up to persist.

Q: Is it safe to run SELinux in permissive mode?
A: Only for testing. Permissive means the security policy is not enforced, which is acceptable for a system you reboot out of. Do not leave it as your everyday driver for a long period.
