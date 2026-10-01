# Cyberpunk Theme Presets

RetroFlow includes selectable color-and-media presets inspired by the Cyberpunk 2077 setting. No game artwork, video, or music is included; provide media you have the rights to use.

## Presets

| Preset | Accent / interface color | Font color | Media folder |
| --- | --- | --- | --- |
| Classic | Existing RetroFlow color | White | None |
| Arasaka | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/ARASAKA/` |
| Afterlife | `#A930EC` | `#59F0FF` | `ux0:/data/RetroFlow/THEMES/AFTERLIFE/` |
| Night City | `#00BEDC` | `#FFCF52` | `ux0:/data/RetroFlow/THEMES/NIGHT_CITY/` |
| Arasaka Tower | `#C5182C` | `#FFE8E0` | `ux0:/data/RetroFlow/THEMES/ARASAKA_TOWER/` |
| Ending | `#F1AE30` | `#2AE0E8` | `ux0:/data/RetroFlow/THEMES/ENDING/` |
| Johnny Silverhand | `#E62F36` | `#C2D2DC` | `ux0:/data/RetroFlow/THEMES/JOHNNY_SILVERHAND/` |
| Main Theme | `#F7DA38` | `#2DDDF4` | `ux0:/data/RetroFlow/THEMES/MAIN_THEME/` |
| Mikoshi | `#25DAE8` | `#F64EBE` | `ux0:/data/RetroFlow/THEMES/MIKOSHI/` |
| Militech | `#2F71C6` | `#F2B04A` | `ux0:/data/RetroFlow/THEMES/MILITECH/` |
| Alt Cunningham | `#D43AD3` | `#44E1EC` | `ux0:/data/RetroFlow/THEMES/ALT_CUNNINGHAM/` |
| Just Another Weapon: Phantom Liberty | `#EB9927` | `#B7E1EB` | `ux0:/data/RetroFlow/THEMES/JUST_ANOTHER_WEAPON_PHANTOM_LIBERTY/` |
| Nocturne OP55N1 | `#C42D39` | `#EFD7D4` | `ux0:/data/RetroFlow/THEMES/NOCTURNE_OP55N1/` |

Each themed folder can contain:

- `background.mp4` for a full-screen looping background video. Use a silent video; RetroFlow mutes the video track.
- `music.ogg` for a matching looping soundtrack. Enable Music in RetroFlow's Audio settings.

The video and music files are optional. If a theme video is missing or cannot be opened, RetroFlow keeps using its selected wallpaper. If a theme soundtrack is missing, RetroFlow uses the normal `MUSIC` folder and its existing shuffle settings.

## Selecting a Preset

Open Settings > Theme > Cyberpunk Theme and press Select to cycle through the presets. RetroFlow saves the selection and reloads itself to apply both colors. The accent is used for interface highlights; the font color is used for interface text.

The Vita Lua Player Plus runtime supports MP4 playback. For a first test, use a short, silent H.264 MP4 at 960 x 544. Codec/container compatibility can vary with the runtime build, so validate the chosen file on the Vita. Keep the clip modest in size and duration to limit storage and playback overhead.
