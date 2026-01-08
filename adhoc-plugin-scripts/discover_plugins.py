#!/usr/bin/env python3
"""
Discover audio plugins and instruments on macOS.

Scans standard locations for VST3, CLAP, AU, and vendor-specific content.
"""

from pathlib import Path
from dataclasses import dataclass
import subprocess
import re


@dataclass
class Plugin:
    name: str
    format: str
    path: Path
    vendor: str | None = None


def find_vst2_plugins() -> list[Plugin]:
    """Find VST2 plugins in standard locations."""
    locations = [
        Path("/Library/Audio/Plug-Ins/VST"),
        Path.home() / "Library/Audio/Plug-Ins/VST",
    ]
    plugins = []
    for loc in locations:
        if loc.exists():
            for bundle in loc.glob("*.vst"):
                plugins.append(Plugin(
                    name=bundle.stem,
                    format="VST2",
                    path=bundle,
                ))
    return plugins


def find_vst3_plugins() -> list[Plugin]:
    """Find VST3 plugins in standard locations."""
    locations = [
        Path("/Library/Audio/Plug-Ins/VST3"),
        Path.home() / "Library/Audio/Plug-Ins/VST3",
    ]
    plugins = []
    for loc in locations:
        if loc.exists():
            for bundle in loc.glob("*.vst3"):
                plugins.append(Plugin(
                    name=bundle.stem,
                    format="VST3",
                    path=bundle,
                ))
    return plugins


def find_clap_plugins() -> list[Plugin]:
    """Find CLAP plugins."""
    locations = [
        Path("/Library/Audio/Plug-Ins/CLAP"),
        Path.home() / "Library/Audio/Plug-Ins/CLAP",
    ]
    plugins = []
    for loc in locations:
        if loc.exists():
            for bundle in loc.glob("*.clap"):
                plugins.append(Plugin(
                    name=bundle.stem,
                    format="CLAP",
                    path=bundle,
                ))
    return plugins


def find_au_plugins() -> list[Plugin]:
    """Find Audio Unit plugins."""
    locations = [
        Path("/Library/Audio/Plug-Ins/Components"),
        Path.home() / "Library/Audio/Plug-Ins/Components",
    ]
    plugins = []
    for loc in locations:
        if loc.exists():
            for bundle in loc.glob("*.component"):
                plugins.append(Plugin(
                    name=bundle.stem,
                    format="AU",
                    path=bundle,
                ))
    return plugins


def find_kontakt_libraries() -> list[Plugin]:
    """Find Kontakt libraries by scanning for .nicnt files and known locations."""
    # Standard NI locations + external drives
    locations = [
        Path("/Library/Application Support/Native Instruments"),
        Path("/Users/Shared"),  # Native Access default
        Path.home() / "Documents/Native Instruments",
        Path("/Volumes/External/kontakt_libraries"),  # External drive
    ]
    libraries = []
    seen_names: set[str] = set()

    for loc in locations:
        if not loc.exists():
            continue

        # Find by .nicnt (Player-compatible libraries)
        for nicnt in loc.rglob("*.nicnt"):
            lib_dir = nicnt.parent
            if lib_dir.name not in seen_names:
                seen_names.add(lib_dir.name)
                libraries.append(Plugin(
                    name=lib_dir.name,
                    format="Kontakt",
                    path=lib_dir,
                    vendor="Native Instruments",
                ))

        # Also scan top-level dirs that contain Instruments/*.nki
        if loc.name == "kontakt_libraries" or loc == Path("/Users/Shared"):
            for subdir in loc.iterdir():
                if not subdir.is_dir():
                    continue
                # Check for .nki files anywhere in the library
                nki_files = list(subdir.rglob("*.nki"))
                if nki_files and subdir.name not in seen_names:
                    seen_names.add(subdir.name)
                    libraries.append(Plugin(
                        name=subdir.name,
                        format="Kontakt",
                        path=subdir,
                    ))

    return libraries


def find_ni_registered_products() -> list[Plugin]:
    """Find NI products from installed_products JSON registry."""
    import json

    registry_dir = Path("/Users/Shared/Native Instruments/installed_products")
    products = []

    if registry_dir.exists():
        for json_file in registry_dir.glob("*.json"):
            try:
                data = json.loads(json_file.read_text())
                name = data.get("name", json_file.stem)
                products.append(Plugin(
                    name=name,
                    format="NI-Registry",
                    path=json_file,
                    vendor="Native Instruments",
                ))
            except (json.JSONDecodeError, KeyError):
                pass

    return products


def find_mtron_patches() -> list[Plugin]:
    """Find M-Tron Pro IV patches."""
    patches_dir = Path("/Library/Application Support/GForce/M-Tron Pro IV/Patches")
    patches = []
    if patches_dir.exists():
        for xml_file in patches_dir.glob("*.xml"):
            patches.append(Plugin(
                name=xml_file.stem,
                format="M-Tron Patch",
                path=xml_file,
                vendor="GForce",
            ))
    return patches


def find_mtron_expansions() -> list[Plugin]:
    """Find M-Tron Pro expansion packs (.cpt2 files)."""
    expansion_dir = Path("/Volumes/External/M-Tron Pro Library")
    expansions = []
    if expansion_dir.exists():
        for cpt2_file in expansion_dir.glob("*.cpt2"):
            expansions.append(Plugin(
                name=cpt2_file.stem,
                format="M-Tron Expansion",
                path=cpt2_file,
                vendor="GForce",
            ))
    return expansions


def list_au_via_auval() -> list[str]:
    """Use auval to list registered Audio Units."""
    try:
        result = subprocess.run(
            ["auval", "-a"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Parse output like: aufx dely Avid  -  Avid Delay
        aus = []
        for line in result.stdout.splitlines():
            match = re.match(r"\s*\w{4}\s+\w{4}\s+\w{4}\s+-\s+(.+)", line)
            if match:
                aus.append(match.group(1).strip())
        return aus
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def main():
    import sys

    format_filter = sys.argv[1].upper() if len(sys.argv) > 1 else None

    all_plugins = []

    if not format_filter or format_filter == "VST2":
        all_plugins.extend(find_vst2_plugins())

    if not format_filter or format_filter == "VST3":
        all_plugins.extend(find_vst3_plugins())

    if not format_filter or format_filter == "CLAP":
        all_plugins.extend(find_clap_plugins())

    if not format_filter or format_filter == "AU":
        all_plugins.extend(find_au_plugins())

    if not format_filter or format_filter == "KONTAKT":
        all_plugins.extend(find_kontakt_libraries())

    if not format_filter or format_filter == "NI":
        all_plugins.extend(find_ni_registered_products())

    if not format_filter or format_filter == "MTRON":
        all_plugins.extend(find_mtron_patches())
        all_plugins.extend(find_mtron_expansions())

    # Group by format
    by_format: dict[str, list[Plugin]] = {}
    for p in all_plugins:
        by_format.setdefault(p.format, []).append(p)

    for fmt, plugins in sorted(by_format.items()):
        print(f"\n## {fmt} ({len(plugins)})")
        print("-" * 40)
        for p in sorted(plugins, key=lambda x: x.name.lower()):
            vendor_str = f" [{p.vendor}]" if p.vendor else ""
            print(f"  {p.name}{vendor_str}")

    print(f"\nTotal: {len(all_plugins)} plugins/libraries")


if __name__ == "__main__":
    main()
