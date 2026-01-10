# ABC-to-MIDI Generation Workflow

## Overview

Three-layer workflow: structure definition → ABC assembly → MIDI generation.

## 1. Section-Based ABC Snippets

Store small snippets keyed by section name:

```yaml
sections:
  verse:
    bars: 8
    instruments:
      bass:
        abc: '"Cm"C,2 C,2 G,,2 G,,2 | "F"F,2 F,2 C,2 C,2 |'
```

The `bars` count is the contract. Every instrument's ABC must equal exactly that many bars.

## 2. Assembly via Structure Array

```yaml
structure: [intro, verse, chorus, verse, chorus, bridge, chorus, outro]
```

To build a complete ABC file:
1. Iterate through structure array
2. Look up each section name
3. Concatenate that instrument's ABC snippet
4. Write standard ABC headers + assembled body

A section appearing twice means its ABC snippet gets included twice.

## 3. ABC Headers That Matter

```abc
X:1
T:Song Title - bass
M:4/4
L:1/8
Q:1/4=88
K:Cmin
%%MIDI program 33
%%MIDI channel 2
```

| Header | Purpose |
|--------|---------|
| `L:1/8` | Default note length (eighth note). All durations relative to this. |
| `Q:1/4=88` | Tempo in quarter notes per minute |
| `%%MIDI program N` | General MIDI instrument (0-127) |
| `%%MIDI channel N` | MIDI channel (10 for drums) |

## 4. Validation Before Assembly

Bar counting is the critical check. In 4/4 with L:1/8:
- One bar = 8 eighth-note units
- `C2` = 2 units, `C4` = 4 units, `z` = 1 unit rest

Parse the ABC snippet, sum durations, divide by 8, compare to declared bars. If mismatch, reject.

## 5. abc2midi

```bash
abc2midi song.abc -o song.mid
```

Standard tool for ABC → MIDI conversion. Key behaviors:
- Chord symbols like `"Cm"` become text events (ignored unless chord accompaniment enabled)
- Bar lines `|` are structural, help validate timing
- Rests `z` create actual silence in MIDI

## 6. Drums: Separate Files, Single Note

For DAW workflows, generate one MIDI file per drum sound:

```yaml
drums:
  kick: "C4 C4 | C4 C4 |"
  snare: "z4 C4 | z4 C4 |"
```

Each becomes its own ABC file with:
```abc
K:C
%%MIDI channel 10
```

All notes are C (MIDI 60). In DAW, each track triggers a single sample. Works with any drum plugin without GM mapping.

## 7. Control Notes (Keyswitches)

For plugins with articulation keyswitches:

```yaml
control_notes:
  - note: sustains    # Maps to MIDI note via lookup table
    beat: 0           # Insert at beat 0
  - note: staccato
    beat: 15.9        # Just before beat 16
```

These become short-duration notes at specific beat positions:
```abc
[C,,/8]z7/8 ...  % keyswitch at beat 0
```

**Trick:** Place keyswitches 0.1 beats before the note they affect. Clean triggering, no overlap.

## 8. CC Automation

MIDI continuous controllers via `%%MIDI` directives:

```yaml
automation:
  - cc: 1  # mod wheel
    values: [[0, 0], [4, 127], [8, 0]]  # [beat, value] pairs
```

Inject at correct beat positions:
```abc
%%MIDI control 1 0
... notes for beats 0-4 ...
%%MIDI control 1 127
... notes for beats 4-8 ...
%%MIDI control 1 0
```

For smooth automation, interpolate between keyframes and emit CC changes at regular intervals.

## 9. The Assembly Algorithm

```python
for instrument in instruments:
    write ABC headers (X, T, M, L, Q, K, MIDI program/channel)
    for section_name in structure:
        section = sections[section_name]
        abc_snippet = section.instruments[instrument].abc
        if control_notes:
            inject keyswitch notes at specified beats
        if automation:
            inject CC directives at interpolated positions
        append abc_snippet to body
    write complete ABC file
    run abc2midi to generate MIDI
```

## 10. Plugin Control Database

Store keyswitch mappings separately:

```yaml
# plugins/controls.yaml
mojo-2:
  keyswitches:
    sustains: { note: 24 }
    staccato: { note: 25 }
    falls: { note: 36 }
```

Reference by name in song.yaml, resolve to MIDI note numbers during generation.

## Core Insight

ABC notation is text. Text is easy to concatenate, validate, and template. abc2midi handles the MIDI encoding. You just need to:
1. Keep snippets small and section-scoped
2. Validate bar counts before assembly
3. Inject control events at the right beat positions
4. Let abc2midi do the rest
