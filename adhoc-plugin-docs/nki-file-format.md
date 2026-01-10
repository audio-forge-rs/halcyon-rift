# NKI File Format (Reverse Engineered)

## Structure

| Offset | Content |
|--------|---------|
| 0x000 | Header (magic bytes, varies by version) |
| 0x00C | "hsin" chunk marker |
| 0x030 | "DSIN" chunk markers (multiple) |
| 0x0C0 | "4KIN" chunk marker |
| 0x180 | Kontakt version (UTF-16LE, length-prefixed) e.g., "5.2.1.6382" or "6.8.0.0" |
| 0x200+ | Metadata block: instrument name, author, library name |
| 0x2D0+ | @field metadata: @color, @devicetypeflags, @soundtype, @tempo, @verl, @verm, @visib |
| 0x400+ | Script data, sample mappings, etc. |

## String Format

Length-prefixed UTF-16LE:
```
[4 bytes: char count (little-endian)]
[N * 2 bytes: UTF-16LE string data]
```

## Extraction Code

```python
def read_utf16le_string(data, offset):
    length = struct.unpack('<I', data[offset:offset+4])[0]
    if length > 200 or length == 0:
        return None
    raw = data[offset+4 : offset+4+(length*2)]
    # Validate: high bytes should be 0 for ASCII
    for i in range(1, len(raw), 2):
        if raw[i] != 0:
            return None
    return raw.decode('utf-16-le')
```

## Extracted Fields

| Field | Detection Method |
|-------|------------------|
| Name | First substantial string after 0x200 |
| Author | Contains "Audio", "Sound", "Instruments", etc. |
| Library | String after author, short, not technical |
| Version | Regex `^\d+\.\d+\.\d+\.\d+$` |
| Categories | Contains "Strings", "Bass", "Piano", etc. |
| Description | Starts with "This ", long text |

## Caveats

- 8Dio files have minimal embedded metadata (use filename instead)
- Older Kontakt versions may have different layouts
- Some files have short ID codes (P79, W06) before real name
- Encrypted/Player-only NKIs may have different structure
