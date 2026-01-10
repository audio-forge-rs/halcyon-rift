#!/usr/bin/env python3
"""
Generate Part 2 for both Picked Acoustic and M-Tron Bass.

Part 1 progression: Am-G | F-E | Am-C-G-D | Am
Part 2 progression: Dm-G | C-Am | F-G | Am (contrasting, more open)
"""

import sys
sys.path.insert(0, '/Users/bedwards/halcyon-rift/adhoc-midi-scripts')

from abc_assembler import ABCHeader, generate_abc_header, abc_to_midi, validate_bars
from pathlib import Path


def generate_guitar_part2():
    """Generate 8-bar guitar Part 2."""

    header = ABCHeader(
        title="Picked Acoustic Part 2",
        meter="4/4",
        unit_length="1/8",
        tempo=None,
        key="Am",
        midi_program=25,
        midi_channel=1,
    )

    lines = [generate_abc_header(header)]
    lines.append("%%MIDI gchordoff")
    lines.append("%%MIDI bassprog 0")
    lines.append("%%MIDI chordprog 0")

    # Bars 9-10: Dm - G - open arpeggios, lighter feel
    lines.append("%%MIDI control 1 30")
    lines.append("D,FAd fAFD | G,BDg dBDG |")

    # Bars 11-12: C - Am - strummed, building
    lines.append("%%MIDI control 1 45")
    lines.append("[CEG]4 [CEG]4 | [A,CE]4 [A,CE]4 |")

    # Bars 13-14: F - G - driving rhythm
    lines.append("%%MIDI control 1 60")
    lines.append("F,2A,2 C2F2 | G,2B,2 D2G2 |")

    # Bars 15-16: Am resolution - high melodic line
    lines.append("%%MIDI control 1 50")
    lines.append("a4 g4 | e8 |")

    return '\n'.join(lines)


def generate_bass_part2():
    """Generate 8-bar bass Part 2."""

    header = ABCHeader(
        title="M-Tron Bass Part 2",
        meter="4/4",
        unit_length="1/8",
        tempo=None,
        key="Am",
        midi_program=32,
        midi_channel=2,
    )

    lines = [generate_abc_header(header)]
    lines.append("%%MIDI gchordoff")

    # Bars 9-10: Dm - G - walking bass
    lines.append("%%MIDI control 1 45")
    lines.append("%%MIDI control 7 100")
    lines.append("D,,2F,,2 A,,2D,,2 | G,,2B,,,2 D,,2G,,2 |")

    # Bars 11-12: C - Am - steady pulse
    lines.append("%%MIDI control 1 55")
    lines.append("C,,2C,,2 E,,2G,,2 | A,,2A,,2 E,,2A,,2 |")

    # Bars 13-14: F - G - driving eighths
    lines.append("%%MIDI control 1 65")
    lines.append("F,,F,,F,,F,, A,,A,,C,C, | G,,G,,G,,G,, B,,,B,,,D,,D,, |")

    # Bars 15-16: Am - whole note resolve
    lines.append("%%MIDI control 1 50")
    lines.append("A,,8 | A,,,8 |")

    return '\n'.join(lines)


def validate_and_save(name, abc_content, output_dir):
    """Validate bar count and save ABC/MIDI."""
    music_lines = [l for l in abc_content.split('\n')
                   if l and not l.startswith(('%', 'X:', 'T:', 'M:', 'L:', 'K:', 'Q:'))]
    music = ' '.join(music_lines)

    valid, error = validate_bars(music, expected_bars=8, meter="4/4", unit_length="1/8")
    if not valid:
        print(f"{name} validation FAILED: {error}")
        return False

    abc_path = output_dir / f'{name}.abc'
    abc_path.write_text(abc_content)
    print(f"{name}: 8 bars validated")
    print(abc_content)
    print()

    try:
        midi_path = abc_to_midi(abc_path)
        print(f"  -> {midi_path}")
    except Exception as e:
        print(f"  MIDI error: {e}")
        return False

    return True


def main():
    output_dir = Path('/Users/bedwards/halcyon-rift/adhoc-xy-scripts')

    print("=" * 60)
    print("PART 2 - Guitar")
    print("=" * 60)
    validate_and_save('picked-acoustic-part2', generate_guitar_part2(), output_dir)

    print()
    print("=" * 60)
    print("PART 2 - Bass")
    print("=" * 60)
    validate_and_save('mtron-bass-part2', generate_bass_part2(), output_dir)


if __name__ == "__main__":
    main()
