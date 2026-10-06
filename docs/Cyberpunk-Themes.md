# Cyberpunk Theme Presets

RetroFlow includes selectable color-and-media presets inspired by the Cyberpunk 2077 setting. No game artwork, video, or music is included; provide media you have the rights to use.

## Presets

Every preset shares the same CyberFlow interface colours (the Arasaka red accent and light font colour); presets differ only in their media and preview.

| Preset | Accent / interface color | Font color | Media folder |
| --- | --- | --- | --- |
| Classic | Existing RetroFlow color | White | None |
| Arasaka | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/ARASAKA/` |
| Dogtown | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/DOGTOWN/` |
| Night City | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/NIGHT_CITY/` |
| Ending | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/ENDING/` |
| Main Theme | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/MAIN_THEME/` |
| Mikoshi | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/MIKOSHI/` |
| Alt Cunningham | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/ALT_CUNNINGHAM/` |
| Just Another Weapon: Phantom Liberty | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/JUST_ANOTHER_WEAPON_PHANTOM_LIBERTY/` |
| Nocturne OP55N1 | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/NOCTURNE_OP55N1/` |
| Edgerunners | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/EDGERUNNERS/` |
| Custom | `#DC1C2E` | `#FFDCDA` | `ux0:/data/RetroFlow/THEMES/CUSTOM/` |

Each themed folder can contain:

- `background.mp4` for a full-screen looping background video. Use a silent video; RetroFlow mutes the video track.
- `music.ogg` for a matching looping soundtrack. Enable Music in RetroFlow's Audio settings.

The video and music files are optional. If a theme video is missing or cannot be opened, RetroFlow keeps using its selected wallpaper. If a theme soundtrack is missing, RetroFlow uses the normal `MUSIC` folder and its existing shuffle settings.

## Custom Theme

Choose **Custom** in the theme picker to use your own media. Copy your own `background.mp4` and/or `music.ogg` into `ux0:/data/RetroFlow/THEMES/CUSTOM/` (the folder is created automatically when Custom is selected), then restart RetroFlow. Both files are optional and follow the same rules as the other presets.

## Selecting a Preset

Open Settings > Theme > Cyberpunk Theme and press Select to cycle through the presets. RetroFlow saves the selection and reloads itself to apply both colors. The accent is used for interface highlights; the font color is used for interface text.

The Vita Lua Player Plus runtime supports MP4 playback. For a first test, use a short, silent H.264 MP4 at 960 x 544. Codec/container compatibility can vary with the runtime build, so validate the chosen file on the Vita. Keep the clip modest in size and duration to limit storage and playback overhead.
