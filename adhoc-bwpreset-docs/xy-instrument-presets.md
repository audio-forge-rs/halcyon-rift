# XY Instrument Presets

## Device Overview

XY Instrument is a container device with 4 chains (A, B, C, D) and an X/Y pad that crossfades between them:
- **Corner A** (0,0): Bottom-left
- **Corner B** (1,0): Bottom-right
- **Corner C** (0,1): Top-left
- **Corner D** (1,1): Top-right

Each chain can contain its own note→instrument→fx signal path.

**Default Device**: No "init" preset exists. Adding XY Instrument creates 4 empty chains. This is useful as a blank canvas but produces no sound until you add content.

---

## Available Presets (22 total)

### Simple/Foundational (small file size, likely minimal modulation)

| Preset | Size | Description |
|--------|------|-------------|
| Totally Lost | 30KB | Minimal setup, ambient/lost theme |
| Quad Bass | 31KB | 4 bass variants at each corner |
| Radio Transmission | 36KB | Radio-themed texture morphing |
| Colorchord XY | 36KB | Chord voicing across XY space |
| Quad Pad | 37KB | 4 pad sounds, basic crossfade |
| Modular System | 37KB | Modular synth simulation |
| Chowning Street | 38KB | FM synthesis (John Chowning reference) |
| Tiefschlaf | 38KB | "Deep sleep" - ambient/drone |

### Mid-Complexity

| Preset | Size | Description |
|--------|------|-------------|
| Frog Chant | 39KB | Organic/nature textures |
| Chord Trigger | 42KB | Chord-based triggering |
| Digi Jungle | 43KB | Digital/jungle hybrid |
| Bitbrotha XY ARP | 44KB | Arpeggiator with XY control |
| Spook The Pook | 58KB | Spooky/haunting textures |
| Lunar Bliss | 64KB | Spacey, ethereal sounds |
| Follow The Leader | 69KB | Follower/sequenced elements |
| Counting Sheep | 75KB | Dreamy, sleep-themed |

### Complex (large files, likely have built-in X/Y modulation)

| Preset | Size | Description |
|--------|------|-------------|
| Paper Plane | 81KB | Floating, airy textures |
| Crystal Palace | 86KB | Crystalline, evolving sounds |
| Gnarly Snarly | 90KB | Aggressive sound morphing |
| Quadralien | 91KB | Alien/unusual sound design |
| Martian Mealtime | 99KB | Otherworldly, evolving |
| DaggerArpStagger | 104KB | Complex arpeggiation + stagger |

---

## Presets with Built-in X/Y Modulation

These presets are most likely to have internal modulation of X and Y parameters (LFOs, envelopes, or step modulators driving the XY position):

### DaggerArpStagger (104KB) - LARGEST
The largest preset suggests complex internal routing. Name implies:
- Dagger: Sharp, percussive attacks
- Arp: Arpeggiator patterns
- Stagger: Time-offset modulation between chains

Likely has step modulators or LFOs driving X/Y position to create rhythmic morphing between the 4 chains.

### Martian Mealtime (99KB)
"Mealtime" suggests consumption/transformation over time. Large file size indicates:
- Multiple internal modulators
- Probably slow-evolving X/Y movement
- Alien/unusual timbral shifts

### Quadralien (91KB)
"Quad" + "alien" - designed around the 4-corner concept with otherworldly modulation. Likely features:
- Unusual modulation curves
- Non-linear X/Y movement patterns
- Strange timbral territories at each corner

### Gnarly Snarly (90KB)
Aggressive naming suggests:
- Fast, chaotic X/Y modulation
- Distorted/processed chains
- Dynamic morphing between aggressive textures

### Crystal Palace (86KB)
"Crystal" often means:
- Resonant, bell-like tones
- Slow, shimmering modulation
- Likely gentle X/Y drift creating evolving harmonics

---

## Notes

- `.bwpreset` files are Bitwig's proprietary binary format
- **Metadata is filesystem-based**: No binary parsing needed
  ```
  .../Presets/XY Instrument/Quad Pad.bwpreset
              ↑              ↑
              device type    preset name (from filename stem)
  ```
- File size correlates with complexity - larger files have more devices/modulation
- All presets are read-only in installed-packages; copy to user library to modify
- Device UUID: `bab3f04d-d3b6-4dfa-86f9-506e0b091ca8`

## Binary Format

| Type | Header | Entropy | Readable |
|------|--------|---------|----------|
| Factory presets | `0004` | 256/256 (encrypted) | No |
| User presets | `0002` | 172/256 | Yes |

Factory presets are encrypted - descriptions inaccessible without Bitwig's key.
User-created presets are unencrypted and contain parseable metadata (comment, creator, tags).

Tools: [bwEdit-Python](https://github.com/jaxter184/bwEdit-Python) works on user presets.
