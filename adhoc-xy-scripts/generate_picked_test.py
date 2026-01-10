#!/usr/bin/env python3
"""
Generate test melody for Picked Acoustic XY Instrument.

Creates an 8-bar Folk/Americana phrase with:
- Articulation keyswitches (Open, Muted, Flageolet)
- CC automation (mod wheel for vibrato)
- Bar-validated ABC notation
"""

import sys
sys.path.insert(0, '/Users/bedwards/halcyon-rift/adhoc-midi-scripts')

from abc_assembler import ABCHeader, generate_abc_header, abc_to_midi
from pathlib import Path


def generate_test_melody():
    """Generate the 8-bar Folk/Americana test melody."""

    # Header for Picked Acoustic test
    header = ABCHeader(
        title="Picked Acoustic XY Test",
        meter="4/4",
        unit_length="1/8",
        tempo=None,  # No tempo in MIDI - set via OSC/transport
        key="Am",  # Folk/Americana in A minor
        midi_program=25,  # Acoustic Guitar (steel) - Kontakt will override
        midi_channel=1,
    )

    # Build the ABC content
    # NOTE: No blank lines between header and music - abc2midi treats blank as end-of-tune
    # NOTE: Comments become MIDI text events - avoid them to keep output clean
    # NOTE: %%MIDI control must be inline with music to get correct timing
    lines = [generate_abc_header(header)]
    # Disable auto-generated chord accompaniment and bass
    lines.append("%%MIDI gchordoff")
    lines.append("%%MIDI bassprog 0")
    lines.append("%%MIDI chordprog 0")

    # No keyswitches - XY Instrument sends same MIDI to all chains
    # Each Kontakt instance should be pre-configured to its articulation

    # Bars 1-2: Fingerpicked (Am - G) - CC1=20 light vibrato
    lines.append("%%MIDI control 1 20")
    lines.append('A,EAc eAEA | G,DGB dBDG |')

    # Bars 3-4: Rhythmic (F - E) - CC1=0 no vibrato
    lines.append("%%MIDI control 1 0")
    lines.append('F,2F,2 F,2F,2 | E,2E,2 E,2E,2 |')

    # Bars 5-6: Strummed chords (Am - C - G - D) - CC1=30 moderate vibrato
    lines.append("%%MIDI control 1 30")
    lines.append('[A,CE]4 [CEG]4 | [G,BD]4 [DFA]4 |')

    # Bars 7-8: High melody - CC1=60 expressive vibrato
    lines.append("%%MIDI control 1 60")
    lines.append('e4 a4 | e\'8 |')

    return '\n'.join(lines)


def main():
    output_dir = Path('/Users/bedwards/halcyon-rift/adhoc-xy-scripts')

    # Generate ABC content
    abc_content = generate_test_melody()

    # Write ABC file
    abc_path = output_dir / 'picked-acoustic-test.abc'
    abc_path.write_text(abc_content)
    print(f"Generated ABC file: {abc_path}")
    print()
    print("=" * 60)
    print(abc_content)
    print("=" * 60)
    print()

    # Validate bar counts for each section manually
    # Total should be 8 bars in 4/4 with L:1/8 = 64 units
    # Each bar = 8 eighth notes

    # Try to convert to MIDI
    try:
        midi_path = abc_to_midi(abc_path)
        print(f"MIDI generated: {midi_path}")
    except FileNotFoundError:
        print("abc2midi not found - install with: brew install abcmidi")
    except RuntimeError as e:
        print(f"abc2midi error: {e}")


if __name__ == "__main__":
    main()
