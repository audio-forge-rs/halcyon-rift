# M-Tron Pro IV Patch Format

## Locations

| Type | Path |
|------|------|
| Patches (metadata) | `/Library/Application Support/GForce/M-Tron Pro IV/Patches/*.xml` |
| Samples (encrypted) | `/Volumes/External/M-Tron Pro Library/*.cpt2` |

## XML Structure

```xml
<metadata
  name="Hammond C3 Clean Basic"
  author="GForce Software"
  collection="The Streetly Tapes Vol 3"
  category="Organs"
  types="Basic,"
  timbres="Deep,Dark,"
  cpt="The_Streetly_Tapes Vol_3"/>
```

## Available Fields

| Field | Example |
|-------|---------|
| name | Hammond C3 Clean Basic |
| author | GForce Software, Dave Spiers |
| collection | The Streetly Tapes Vol 3 |
| category | Organs, Strings, Voices, Keys |
| types | Basic, Wide, Dynamic |
| timbres | Deep, Dark, Warm, Bright |
| cpt | Links to .cpt2 sample file |

## Quick Extraction

```bash
# One-liner to extract all patch names
grep -h "metadata" /Library/Application\ Support/GForce/M-Tron\ Pro\ IV/Patches/*.xml | \
  sed 's/.*name="\([^"]*\)".*/\1/'
```

## Python Extraction

```python
import xml.etree.ElementTree as ET
import glob

for xml_file in glob.glob('/Library/Application Support/GForce/M-Tron Pro IV/Patches/*.xml'):
    tree = ET.parse(xml_file)
    meta = tree.find('.//metadata')
    if meta is not None:
        print(f"Name: {meta.get('name')}")
        print(f"Author: {meta.get('author')}")
        print(f"Category: {meta.get('category')}")
        print(f"Collection: {meta.get('collection')}")
```

## .cpt2 Files

Encrypted/proprietary sample containers. No metadata extractable - just binary audio data referenced by the XML patches via the `cpt` attribute.

## Summary

| Format | Parseable | Method |
|--------|-----------|--------|
| .xml patches | Yes | Standard XML parsing |
| .cpt2 samples | No | Encrypted binary |
