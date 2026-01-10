#!/usr/bin/env python3
"""
Generate M-Tron bass line to accompany Picked Acoustic XY test.

Chord progression:
- Bars 1-2: Am | G
- Bars 3-4: F | E
- Bars 5-6: Am C | G D
- Bars 7-8: Am resolution
"""

import sys
sys.path.insert(0, '/Users/bedwards/halcyon-rift/adhoc-midi-scripts')

from abc_assembler import ABCHeader, generate_abc_header, abc_to_midi, validate_bars
from pathlib import Path


def generate_bass_line():
    """Generate 8-bar folk bass line matching the picked acoustic test."""

    header = ABCHeader(
        title="M-Tron Bass - Folk Americana",
        meter="4/4",
        unit_length="1/8",
        tempo=None,  # No tempo - set via transport
        key="Am",
        midi_program=32,  # Acoustic Bass (GM) - M-Tron will override
        midi_channel=2,
    )

    lines = [generate_abc_header(header)]
    lines.append("%%MIDI gchordoff")

    # CC7 = volume, CC1 = mod wheel (can control filter/expression in M-Tron)
    # Start with moderate expression
    lines.append("%%MIDI control 1 40")
    lines.append("%%MIDI control 7 100")

    # Bars 1-2: Am | G - steady root-fifth pattern
    # Am: A,,2 E,,2 A,,2 E,,2 | G: G,,2 D,,2 G,,2 D,,2
    lines.append("A,,2E,,2 A,,2E,,2 | G,,2D,,2 G,,2D,,2 |")

    # Bars 3-4: F | E - same pattern, slightly more drive
    lines.append("%%MIDI control 1 50")
    lines.append("F,,2C,,2 F,,2C,,2 | E,,2B,,,2 E,,2B,,,2 |")

    # Bars 5-6: Am C | G D - busier, two chords per bar
    lines.append("%%MIDI control 1 60")
    lines.append("A,,2A,,2 C,,2C,,2 | G,,2G,,2 D,,2D,,2 |")

    # Bars 7-8: Am resolution - whole notes, fade expression
    lines.append("%%MIDI control 1 70")
    lines.append("A,,8 | A,,8 |")

    return '\n'.join(lines)


def main():
    output_dir = Path('/Users/bedwards/halcyon-rift/adhoc-xy-scripts')

    abc_content = generate_bass_line()

    # Validate bar count
    # Extract just the music lines (skip headers and directives)
    music_lines = [l for l in abc_content.split('\n')
                   if l and not l.startswith(('%', 'X:', 'T:', 'M:', 'L:', 'K:', 'Q:'))]
    music = ' '.join(music_lines)

    valid, error = validate_bars(music, expected_bars=8, meter="4/4", unit_length="1/8")
    if not valid:
        print(f"Validation error: {error}")
        return

    abc_path = output_dir / 'mtron-bass.abc'
    abc_path.write_text(abc_content)
    print(f"Generated ABC: {abc_path}")
    print()
    print("=" * 60)
    print(abc_content)
    print("=" * 60)
    print()
    print("Bar validation: PASSED (8 bars)")

    try:
        midi_path = abc_to_midi(abc_path)
        print(f"MIDI generated: {midi_path}")
    except FileNotFoundError:
        print("abc2midi not found - install with: brew install abcmidi")
    except RuntimeError as e:
        print(f"abc2midi error: {e}")


if __name__ == "__main__":
    main()
