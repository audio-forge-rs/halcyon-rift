#!/usr/bin/env python3
"""
Discover Bitwig presets by scanning filesystem.

Metadata is inferred from directory structure:
    .../Presets/DeviceName/preset-name.bwpreset
                ↑           ↑
                device      preset name (filename stem)
"""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class BitwigPreset:
    device: str
    name: str
    path: Path
    size: int

    @property
    def size_kb(self) -> float:
        return self.size / 1024


def find_presets(search_paths: list[Path], device_filter: str | None = None) -> list[BitwigPreset]:
    """Find all .bwpreset files, extracting metadata from path structure."""
    presets = []

    for base_path in search_paths:
        if not base_path.exists():
            continue

        for preset_file in base_path.rglob("*.bwpreset"):
            parts = preset_file.parts
            try:
                presets_idx = parts.index("Presets")
                device = parts[presets_idx + 1]
            except (ValueError, IndexError):
                device = "Unknown"

            if device_filter and device_filter.lower() not in device.lower():
                continue

            presets.append(BitwigPreset(
                device=device,
                name=preset_file.stem,
                path=preset_file,
                size=preset_file.stat().st_size
            ))

    return sorted(presets, key=lambda p: (p.device, p.name))


def main():
    home = Path.home()

    search_paths = [
        home / "Library/Application Support/Bitwig/Bitwig Studio/installed-packages/5.0/Bitwig",
        home / "Documents/Bitwig Studio/Library/Presets",
    ]

    import sys
    device_filter = sys.argv[1] if len(sys.argv) > 1 else None

    presets = find_presets(search_paths, device_filter)

    if device_filter:
        print(f"Presets for device matching '{device_filter}':\n")
    else:
        print("All presets:\n")

    current_device = None
    for p in presets:
        if p.device != current_device:
            current_device = p.device
            print(f"\n## {current_device}")
            print("-" * 40)

        print(f"  {p.name:40} ({p.size_kb:6.1f} KB)")

    print(f"\nTotal: {len(presets)} presets")


if __name__ == "__main__":
    main()
