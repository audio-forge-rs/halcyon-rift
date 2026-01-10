#!/usr/bin/env python3
"""
Parse NKI (Kontakt Instrument) files to extract metadata.

Based on reverse-engineered format documentation.
"""

import struct
import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class NKIMetadata:
    path: Path
    name: str | None = None
    author: str | None = None
    library: str | None = None
    version: str | None = None
    categories: list[str] | None = None
    description: str | None = None


def read_utf16le_string(data: bytes, offset: int) -> tuple[str | None, int]:
    """Read a length-prefixed UTF-16LE string. Returns (string, bytes_consumed)."""
    if offset + 4 > len(data):
        return None, 0

    length = struct.unpack('<I', data[offset:offset+4])[0]

    # Sanity check - reasonable string length
    if length > 300 or length < 2:
        return None, 0

    end = offset + 4 + (length * 2)
    if end > len(data):
        return None, 0

    raw = data[offset+4:end]

    # Strict validation: high bytes must be 0 for printable ASCII range
    # This catches garbage data that looks like valid length prefixes
    for i in range(0, len(raw), 2):
        if i + 1 >= len(raw):
            break
        low, high = raw[i], raw[i+1]
        # Must be printable ASCII (0x20-0x7E) or common extended (\, :, etc)
        if high != 0:
            return None, 0
        if low < 0x20 and low not in (0x09, 0x0A, 0x0D):  # tab, newline, cr
            return None, 0

    try:
        decoded = raw.decode('utf-16-le')
        # Additional check: must be mostly printable
        printable = sum(1 for c in decoded if c.isprintable() or c.isspace())
        if printable < len(decoded) * 0.8:
            return None, 0
        return decoded, 4 + (length * 2)
    except UnicodeDecodeError:
        return None, 0


def find_strings_in_region(data: bytes, start: int, end: int) -> list[tuple[int, str]]:
    """Scan a region for valid UTF-16LE strings."""
    strings = []
    offset = start

    while offset < end - 4:
        s, consumed = read_utf16le_string(data, offset)
        if s and len(s) >= 2:
            strings.append((offset, s))
            offset += consumed
        else:
            offset += 1

    return strings


def classify_string(s: str) -> str | None:
    """Classify a string as name, author, version, category, or description."""
    # Version pattern
    if re.match(r'^\d+\.\d+\.\d+(\.\d+)?$', s):
        return 'version'

    # Author patterns
    author_keywords = ['Audio', 'Sound', 'Instruments', 'Productions', 'Music',
                       'Studios', 'Labs', 'Samples', 'Orchestra']
    if any(kw in s for kw in author_keywords) and len(s) < 50:
        return 'author'

    # Category patterns
    category_keywords = ['Strings', 'Bass', 'Piano', 'Synth', 'Pad', 'Lead',
                         'Brass', 'Woodwind', 'Percussion', 'Drums', 'Guitar',
                         'Vocal', 'Choir', 'Orchestral', 'Ethnic', 'World']
    if any(kw in s for kw in category_keywords) and len(s) < 30:
        return 'category'

    # Description pattern
    if s.startswith('This ') and len(s) > 50:
        return 'description'

    # Technical/internal strings to skip
    skip_patterns = ['Kontakt', 'KontaktInstrument', '@', 'DSIN', 'hsin', '4KIN']
    if any(p in s for p in skip_patterns):
        return None

    # Short codes to skip
    if re.match(r'^[A-Z]\d{2}$', s):  # P79, W06, etc.
        return None

    return 'name'


def parse_nki(filepath: Path) -> NKIMetadata:
    """Parse an NKI file and extract metadata."""
    meta = NKIMetadata(path=filepath)

    try:
        data = filepath.read_bytes()
    except IOError:
        return meta

    if len(data) < 0x300:
        return meta

    # Look for version around 0x180
    strings_version = find_strings_in_region(data, 0x160, 0x200)
    for _, s in strings_version:
        if re.match(r'^\d+\.\d+\.\d+(\.\d+)?$', s):
            meta.version = s
            break

    # Look for metadata in 0x200-0x400 region
    strings_meta = find_strings_in_region(data, 0x200, 0x600)

    categories = []
    for _, s in strings_meta:
        classification = classify_string(s)
        if classification == 'name' and not meta.name:
            meta.name = s
        elif classification == 'author' and not meta.author:
            meta.author = s
        elif classification == 'category':
            categories.append(s)
        elif classification == 'description' and not meta.description:
            meta.description = s

    if categories:
        meta.categories = categories

    # Fallback: use filename as name
    if not meta.name:
        meta.name = filepath.stem

    return meta


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: parse_nki.py <path-to-nki-or-directory>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        nki_files = [target]
    else:
        nki_files = list(target.rglob("*.nki"))

    for nki_path in sorted(nki_files):
        meta = parse_nki(nki_path)
        print(f"\n{nki_path.name}")
        print("-" * 40)
        if meta.name:
            print(f"  Name:       {meta.name}")
        if meta.author:
            print(f"  Author:     {meta.author}")
        if meta.version:
            print(f"  Version:    {meta.version}")
        if meta.categories:
            print(f"  Categories: {', '.join(meta.categories)}")
        if meta.description:
            desc = meta.description[:80] + "..." if len(meta.description) > 80 else meta.description
            print(f"  Description: {desc}")


if __name__ == "__main__":
    main()
