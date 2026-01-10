#!/usr/bin/env python3
"""
ABC notation assembler for MIDI generation.

Assembles section-based ABC snippets into complete ABC files,
validates bar counts, injects keyswitches and CC automation,
then calls abc2midi to generate MIDI.

IMPORTANT: abc2midi treats blank lines as end-of-tune markers.
Never insert blank lines between header and music, or between
music sections. Use comments (% ...) for visual separation instead.
"""

import re
import subprocess
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ABCHeader:
    title: str
    meter: str = "4/4"
    unit_length: str = "1/8"
    tempo: int | None = None  # None = no tempo in MIDI (set via DAW/OSC)
    key: str = "C"
    midi_program: int = 0
    midi_channel: int = 1


@dataclass
class Section:
    name: str
    bars: int
    abc: str


@dataclass
class Keyswitch:
    note: int  # MIDI note number
    beat: float


@dataclass
class CCAutomation:
    cc: int
    values: list[tuple[float, int]]  # (beat, value) pairs


def units_per_bar(meter: str, unit_length: str) -> int:
    """Calculate how many unit lengths fit in one bar."""
    # Parse meter like "4/4" or "3/4"
    num, denom = map(int, meter.split('/'))

    # Parse unit length like "1/8" or "1/4"
    match = re.match(r'1/(\d+)', unit_length)
    if not match:
        return 8  # default
    unit_denom = int(match.group(1))

    # In 4/4 with L:1/8, one bar = 4 quarter notes = 8 eighth notes
    return (num * unit_denom) // denom


def count_abc_units(abc: str) -> float:
    """
    Count the total duration units in an ABC snippet.

    Duration modifiers:
    - C = 1 unit (default)
    - C2 = 2 units
    - C/2 = 0.5 units
    - C3/2 = 1.5 units
    - z = 1 unit rest
    - z2 = 2 unit rest
    """
    total = 0.0

    # Remove chord symbols, bar lines, and other non-note content
    clean = re.sub(r'"[^"]*"', '', abc)  # Remove chord symbols
    clean = re.sub(r'\|+', ' ', clean)   # Remove bar lines
    clean = re.sub(r'%%.*', '', clean)   # Remove directives
    clean = re.sub(r'\[.*?\]', '', clean)  # Remove chord brackets (count separately if needed)

    # Pattern for notes: optional accidental, note letter, optional octave, optional duration
    note_pattern = re.compile(r"([_^=]?)([A-Ga-gz])([,']*)(\d*)(/?)(\d*)")

    for match in note_pattern.finditer(clean):
        # accidental, note, octave, num, slash, denom
        num = match.group(4)
        slash = match.group(5)
        denom = match.group(6)

        if num and slash and denom:
            # e.g., C3/2 = 1.5
            duration = int(num) / int(denom)
        elif slash and denom:
            # e.g., C/2 = 0.5
            duration = 1.0 / int(denom)
        elif num:
            # e.g., C2 = 2
            duration = int(num)
        else:
            # e.g., C = 1
            duration = 1.0

        total += duration

    return total


def validate_bars(abc: str, expected_bars: int, meter: str = "4/4", unit_length: str = "1/8") -> tuple[bool, str]:
    """Validate that ABC snippet has the expected number of bars."""
    upb = units_per_bar(meter, unit_length)
    actual_units = count_abc_units(abc)
    actual_bars = actual_units / upb

    if abs(actual_bars - expected_bars) < 0.01:
        return True, ""
    else:
        return False, f"Expected {expected_bars} bars ({expected_bars * upb} units), got {actual_bars:.2f} bars ({actual_units} units)"


def generate_abc_header(header: ABCHeader, index: int = 1) -> str:
    """Generate ABC file header."""
    lines = [
        f"X:{index}",
        f"T:{header.title}",
        f"M:{header.meter}",
        f"L:{header.unit_length}",
    ]
    # Only include tempo if specified (otherwise set via DAW/OSC)
    if header.tempo is not None:
        lines.append(f"Q:1/4={header.tempo}")
    lines.extend([
        f"K:{header.key}",
        f"%%MIDI program {header.midi_program}",
        f"%%MIDI channel {header.midi_channel}",
    ])
    return '\n'.join(lines)


def inject_keyswitch(note: int, beat: float, unit_length: str = "1/8") -> str:
    """Generate ABC for a keyswitch note at a specific beat."""
    # Keyswitches are very short notes
    # Convert MIDI note to ABC notation
    # MIDI 60 = C, 61 = ^C, etc.
    octave = (note // 12) - 5  # MIDI 60 is middle C (C in ABC)
    pitch_class = note % 12

    pitch_names = ['C', '^C', 'D', '^D', 'E', 'F', '^F', 'G', '^G', 'A', '^A', 'B']
    pitch = pitch_names[pitch_class]

    # Add octave modifiers
    if octave < 0:
        pitch += ',' * abs(octave)
    elif octave > 0:
        pitch = pitch.lower()
        if octave > 1:
            pitch += "'" * (octave - 1)

    # Very short duration (1/8 of unit length)
    return f"[{pitch}/8]z7/8"


def inject_cc(cc: int, value: int) -> str:
    """Generate ABC MIDI control directive."""
    return f"%%MIDI control {cc} {value}"


def assemble_instrument(
    instrument_name: str,
    sections: list[Section],
    structure: list[str],
    header: ABCHeader,
    keyswitches: list[Keyswitch] | None = None,
    automation: list[CCAutomation] | None = None,
) -> str:
    """Assemble a complete ABC file for one instrument."""

    # Build section lookup
    section_map = {s.name: s for s in sections}

    # Validate all sections first
    for section in sections:
        valid, error = validate_bars(section.abc, section.bars, header.meter, header.unit_length)
        if not valid:
            raise ValueError(f"Section '{section.name}': {error}")

    # Generate header
    header.title = f"{header.title} - {instrument_name}"
    abc_content = [generate_abc_header(header)]
    abc_content.append("")  # blank line before body

    # Assemble body from structure
    for section_name in structure:
        if section_name not in section_map:
            raise ValueError(f"Unknown section: {section_name}")

        section = section_map[section_name]

        # TODO: inject keyswitches and automation at correct beat positions
        # For now, just append the ABC snippet
        abc_content.append(f"% Section: {section_name}")
        abc_content.append(section.abc)

    return '\n'.join(abc_content)


def abc_to_midi(abc_path: Path, midi_path: Path | None = None, strip_tempo: bool = True) -> Path:
    """Convert ABC file to MIDI using abc2midi.

    Args:
        abc_path: Path to ABC file
        midi_path: Output path (default: same name with .mid extension)
        strip_tempo: Remove tempo meta messages (set tempo via DAW/OSC instead)
    """
    if midi_path is None:
        midi_path = abc_path.with_suffix('.mid')

    result = subprocess.run(
        ['abc2midi', str(abc_path), '-o', str(midi_path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"abc2midi failed: {result.stderr}")

    # Strip tempo messages if requested (let DAW control tempo)
    if strip_tempo:
        try:
            import mido
            mid = mido.MidiFile(str(midi_path))
            for track in mid.tracks:
                # Remove set_tempo messages
                track[:] = [msg for msg in track if msg.type != 'set_tempo']
            mid.save(str(midi_path))
        except ImportError:
            pass  # mido not available, skip stripping

    return midi_path


def main():
    """Demo: assemble a simple song."""

    # Define sections
    sections = [
        Section(
            name="verse",
            bars=4,
            abc='"Cm"C,2 C,2 G,,2 G,,2 | "F"F,2 F,2 C,2 C,2 | "G"G,2 G,2 D,2 D,2 | "Cm"C,2 C,2 G,,2 G,,2 |'
        ),
        Section(
            name="chorus",
            bars=4,
            abc='"Cm"C,4 C,4 | "Ab"A,,4 A,,4 | "Eb"E,4 E,4 | "G"G,4 G,4 |'
        ),
    ]

    structure = ["verse", "chorus", "verse", "chorus"]

    header = ABCHeader(
        title="Demo Song",
        meter="4/4",
        unit_length="1/8",
        tempo=100,
        key="Cmin",
        midi_program=33,  # Electric Bass (finger)
        midi_channel=2,
    )

    try:
        abc = assemble_instrument("bass", sections, structure, header)
        print("Generated ABC:")
        print("-" * 40)
        print(abc)
        print("-" * 40)

        # Write to file
        output_path = Path("/tmp/demo_bass.abc")
        output_path.write_text(abc)
        print(f"\nWritten to: {output_path}")

        # Try to convert to MIDI
        try:
            midi_path = abc_to_midi(output_path)
            print(f"MIDI generated: {midi_path}")
        except FileNotFoundError:
            print("abc2midi not found - install with: brew install abcmidi")

    except ValueError as e:
        print(f"Validation error: {e}")


if __name__ == "__main__":
    main()
