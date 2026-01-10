#!/usr/bin/env python3
"""
Parse M-Tron Pro IV patch files to extract metadata.

Patches are plain XML with a <metadata> element containing all info.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass, field


PATCHES_DIR = Path("/Library/Application Support/GForce/M-Tron Pro IV/Patches")


@dataclass
class MTronPatch:
    path: Path
    name: str
    author: str | None = None
    collection: str | None = None
    category: str | None = None
    types: list[str] = field(default_factory=list)
    timbres: list[str] = field(default_factory=list)
    cpt: str | None = None  # Reference to .cpt2 sample file


def parse_patch(filepath: Path) -> MTronPatch | None:
    """Parse an M-Tron patch XML file."""
    try:
        tree = ET.parse(filepath)
        meta = tree.find('.//metadata')

        if meta is None:
            return None

        # Parse comma-separated lists
        types_str = meta.get('types', '')
        types = [t.strip() for t in types_str.split(',') if t.strip()]

        timbres_str = meta.get('timbres', '')
        timbres = [t.strip() for t in timbres_str.split(',') if t.strip()]

        return MTronPatch(
            path=filepath,
            name=meta.get('name', filepath.stem),
            author=meta.get('author'),
            collection=meta.get('collection'),
            category=meta.get('category'),
            types=types,
            timbres=timbres,
            cpt=meta.get('cpt'),
        )
    except ET.ParseError:
        return None


def find_all_patches() -> list[MTronPatch]:
    """Find and parse all M-Tron patches."""
    patches = []

    if not PATCHES_DIR.exists():
        return patches

    for xml_file in PATCHES_DIR.glob("*.xml"):
        patch = parse_patch(xml_file)
        if patch:
            patches.append(patch)

    return sorted(patches, key=lambda p: p.name.lower())


def main():
    import sys

    patches = find_all_patches()

    if not patches:
        print(f"No patches found in {PATCHES_DIR}")
        sys.exit(1)

    # Filter by category if provided
    category_filter = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if category_filter:
        patches = [p for p in patches if p.category and category_filter in p.category.lower()]
        print(f"Patches in category '{category_filter}':\n")

    # Group by collection
    by_collection: dict[str, list[MTronPatch]] = {}
    for p in patches:
        collection = p.collection or "Unknown"
        by_collection.setdefault(collection, []).append(p)

    for collection, collection_patches in sorted(by_collection.items()):
        print(f"\n## {collection} ({len(collection_patches)})")
        print("-" * 50)

        # Group by category within collection
        by_category: dict[str, list[MTronPatch]] = {}
        for p in collection_patches:
            cat = p.category or "Uncategorized"
            by_category.setdefault(cat, []).append(p)

        for category, cat_patches in sorted(by_category.items()):
            print(f"\n  [{category}]")
            for p in sorted(cat_patches, key=lambda x: x.name):
                types_str = f" ({', '.join(p.types)})" if p.types else ""
                print(f"    {p.name}{types_str}")

    print(f"\n\nTotal: {len(patches)} patches")

    # Show stats
    all_categories = set(p.category for p in patches if p.category)
    all_timbres = set(t for p in patches for t in p.timbres)
    print(f"Categories: {', '.join(sorted(all_categories))}")
    print(f"Timbres: {', '.join(sorted(all_timbres))}")


if __name__ == "__main__":
    main()
