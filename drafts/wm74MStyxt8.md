::summary
Project Infinity X v3.5 is out on Android 16, and it is not the QPR1 release — that arrives with v3.6 in January. This build is a load of polish: a NothingOS style ringer tile, updated Google Sans Flex, R8 shrinking on by default, and better idle drain. If you are already on Infinity X, it is a sensible update.

::body
The team said it up front, so let me say it too: v3.5 is not QPR1. QPR1 is confirmed for January as version 3.6. If you were waiting on that, this is not it yet.

What you do get is a thick list of quality-of-life work. No giant new app, nothing you would put on a poster. Just a lot of "why was this broken before" fixes, plus a few additions that genuinely look and feel better. I went through them one by one on the video, and here is what actually matters.

## What it is

Project Infinity X v3.5, unofficial, on an Android 16 base. It is a continuation build, not a fresh start, so if you are on an earlier Infinity X version the update path is the normal one. If you are new to it, this is a good moment to try it, because the rough edges have been sanded down.

## What changed

The headliner for me is the NothingOS style ringer quick settings tile. It looks clean and finally matches the rest of the panel instead of sticking out. Small thing, but you look at quick settings every day.

The rest of the list:

- Add NothingOS style ringer QS tile (author: rmp22).
- Update Google Sans Flex font package to Google's latest release (author: neobuddy89).
- Add system animation styles: Android P, Scale, Slide.
- Allow override of Mock Location restriction (author: userariii).
- More aggressive idle killing for better idle draining.
- Colored icon customizations now only apply to settings homepage icons.
- Add spark pulse renderer style (author: neobuddy89).
- Add three more display cutouts: render below cutout, hide, wide cutout.
- Enable R8 code shrinking and optimizations by default (author: jdduke).
- Fix half-clipped status bar on lockscreen for some devices.

## What is fixed

Two of those are real fixes rather than features, and both are worth calling out.

The colored icon customization fix is the one people were complaining about. Before this build, the setting leaked into submenus and left you with mismatched icons you could not explain. Now it only touches the icons on the settings homepage, which is what everyone expected in the first place.

The lockscreen status bar fix cleans up a half-clipped bar some devices were showing. If you had that and it annoyed you, this build ends it.

There is also a smoother quick settings transition when blurs are off, and the about phone cards are enlarged again, back to how they looked in v3.2 and v2.9. If you liked that layout, it is back.

## What is broken

Nothing new that the team has flagged. This is the least dramatic release in a while, and that is the point. It is a polish pass, not a rebuild. If you hit something, report it the way the team asks, with logs.

## Who should update

- You are already on Infinity X and want the idle drain and R8 improvements. Update.
- You were waiting on QPR1. Wait for v3.6 in January.
- You are happy on an older Infinity X build with no complaints. Updating is still fine, but nothing here will change your day.
- You are new to Infinity X. This is a settled build to start from.

## The honest read

A quiet but solid release. The R8 code shrinking and optimization being on by default is a real background win for smoothness and size, and the aggressive idle killing should help standby drain. The flashy items are the ringer tile and the new animation styles, and neither will change your life — they just make the ROM feel more finished.

If you flash it over your current setup, do the normal backup first. This is a ROM update, and an update is still a flash. Keep a stable build nearby in case a beta-style regression shows up, and set the phone up clean if anything feels off.

If the flashing side is the part you skip weeks avoiding, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Is Project Infinity X v3.5 the QPR1 release?
A: No. The team confirmed v3.5 is not QPR1, and QPR1 arrives with version 3.6 in January. If QPR1 is what you are waiting for, hold off until 3.6.

Q: What is the main new feature in v3.5?
A: The NothingOS style ringer quick settings tile is the headliner, along with updated Google Sans Flex, new system animation styles, and three more display cutouts. It is a polish-heavy release rather than one big addition.

Q: Does this update improve battery life?
A: It should help standby drain. The build adds more aggressive idle killing, and R8 code shrinking and optimizations are now enabled by default, which trims the system in the background.

Q: Which Android version is it based on?
A: Android 16. This is an unofficial build of Project Infinity X v3.5, continuing on the same base as the earlier versions.

Q: Should I update from an older Infinity X build?
A: If you are already on Infinity X, yes, it is a sensible update with real fixes and background improvements. Just back up first, since an update is still a flash.
