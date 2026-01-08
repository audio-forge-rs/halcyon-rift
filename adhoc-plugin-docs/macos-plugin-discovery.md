# Plugin & Instrument Discovery on macOS

## Standard Plugin Locations

| Format | Path |
|--------|------|
| VST2 | `/Library/Audio/Plug-Ins/VST/` |
| VST3 | `/Library/Audio/Plug-Ins/VST3/` |
| CLAP | `/Library/Audio/Plug-Ins/CLAP/` |
| AU | `/Library/Audio/Plug-Ins/Components/` |

User-specific variants also exist at `~/Library/Audio/Plug-Ins/[FORMAT]/`

---

## VST2 Plugins

```
/Library/Audio/Plug-Ins/VST/
~/Library/Audio/Plug-Ins/VST/
```

`.vst` bundles. Legacy format, still used by many vendors.

Example: Ample Sound Ethno Banjo = `AEBJ.vst`

---

## VST3 Plugins

```
/Library/Audio/Plug-Ins/VST3/
~/Library/Audio/Plug-Ins/VST3/
```

`.vst3` bundles. Modern format with better preset handling.

---

## CLAP Plugins

```
/Library/Audio/Plug-Ins/CLAP/
~/Library/Audio/Plug-Ins/CLAP/
```

`.clap` bundles. Newest format, gaining adoption.

---

## Audio Units

```
/Library/Audio/Plug-Ins/Components/
~/Library/Audio/Plug-Ins/Components/
```

`.component` bundles. Query registered AUs:
```bash
auval -a
```

---

## M-Tron Pro IV

### Patches
```
/Library/Application Support/GForce/M-Tron Pro IV/Patches/*.xml
```

**The trick**: These are plain XML. Parse them:
```bash
grep -E "<(Name|Creator|Category|Collection)>" "/Library/Application Support/GForce/M-Tron Pro IV/Patches/Hammond C3 Clean Basic.xml"
```

Returns: patch name, author, category, collection name.

### Expansion Packs
```
/Volumes/External/M-Tron Pro Library/*.cpt2
```

`.cpt2` files are expansion packs (ChamberTron, OrchesTron, Streetly Tapes, etc.).

---

## Kontakt Libraries

### Standard locations
```
/Library/Application Support/Native Instruments/Kontakt 8/Content/
/Library/Application Support/Native Instruments/Kontakt 7/Content/
~/Documents/Native Instruments/User Content/
```

### Native Access default location
```
/Users/Shared/
```

Example libraries:
```
/Users/Shared/Session Guitarist - Picked Acoustic Library/
/Users/Shared/Session Guitarist - Electric Sunburst Deluxe Library/
/Users/Shared/Session Guitarist - Strummed Acoustic Library/
```

Instruments inside: `.../Instruments/*.nki`

### External drive
```
/Volumes/External/kontakt_libraries/
```

Subfolders for vendors (8Dio, Spitfire, etc.)

### NI Product Registry
```
/Users/Shared/Native Instruments/installed_products/*.json
```

JSON files contain library metadata (name, version, paths).

### The tricks

1. **Find all .nki files**:
   ```bash
   find /Volumes -name "*.nki" -type f 2>/dev/null
   ```

2. **Player vs Full Kontakt**: If a library folder contains `.nicnt` file, it's Player-compatible (free Kontakt Player works). No `.nicnt` = requires full Kontakt.

3. **Library structure**: Most libraries organize as:
   ```
   LibraryName/
   ├── Instruments/          # .nki files here
   ├── Samples/              # .ncw or .wav files
   ├── Data/
   └── LibraryName.nicnt     # Player registration
   ```

4. **NKI files are binary** - can't easily parse metadata. Use filename and folder hierarchy for organization.

---

## Sample Libraries (WAV/AIFF)

Extract metadata from audio files:
```bash
# Using afinfo (macOS built-in)
afinfo somefile.wav

# Using ffprobe
ffprobe -show_format -show_streams somefile.wav 2>/dev/null | grep -E "duration|sample_rate|channels"
```

Embedded metadata: Some samples have BWF (Broadcast WAV) chunks with tempo, key, description.

---

## Native Instruments Database

NI stores library registration in:
```
~/Library/Application Support/Native Instruments/Service Center/
```

And content paths in:
```
~/Library/Preferences/com.native-instruments.*.plist
```

```bash
plutil -p ~/Library/Preferences/com.native-instruments.Kontakt*.plist
```

---

## Bitwig Content

Bitwig's internal devices/presets:
```
/Applications/Bitwig Studio.app/Contents/Resources/content/
~/Documents/Bitwig Studio/Library/
```

### Factory Preset Documentation

No exhaustive public list exists. Research findings:

| Source | Has Descriptions? |
|--------|-------------------|
| [bitwiggers.com/presets](https://bitwiggers.com/presets/) | User-submitted only |
| [polarity/bitwig-community-presets](https://github.com/polarity/bitwig-community-presets) | Community presets |
| [bitwig.com/userguide](https://www.bitwig.com/userguide/latest/) | Device descriptions only |
| [bitwig.com/sound-content](https://www.bitwig.com/sound-content/) | Marketing only |
| Factory presets | Encrypted (format 0004) |

Factory preset descriptions are locked inside encrypted `.bwpreset` files. No one has published a scraped/documented list.

---

## General Pattern

Most DAW plugins follow this:

| Type | Location |
|------|----------|
| System-wide | `/Library/Audio/Plug-Ins/[FORMAT]/` |
| User-specific | `~/Library/Audio/Plug-Ins/[FORMAT]/` |
| App Support | `/Library/Application Support/[VENDOR]/` |
| Preferences | `~/Library/Preferences/com.[vendor].[product].plist` |
