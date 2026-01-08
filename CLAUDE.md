# CLAUDE.md

Guide for AI assistants working on this project.

## Project Overview

Halcyon Rift is a music production automation toolkit for Bitwig Studio on macOS. It provides CLI tools and scripts for managing plugins, presets, and OSC communication.

## Repository Structure

```
halcyon-rift/
├── DrivenByMoss/            # Git submodule - OSC controller for Bitwig (our fork)
├── cli/                     # Polished CLI tools with argparse commands
│   ├── bwpreset.py          # Bitwig preset operations
│   ├── osc.py               # OSC communication with Bitwig
│   ├── kontakt.py           # Kontakt library management
│   ├── m-tron.py            # M-Tron patch management
│   └── plugin.py            # Plugin discovery
├── adhoc-*/                 # Learning/exploration directories
│   ├── adhoc-*-docs/        # Markdown documentation
│   └── adhoc-*-scripts/     # Experimental Python scripts
```

### adhoc vs cli

- **adhoc-\*** directories are for messy exploration, learning, one-offs
- **cli/** contains polished tools distilled from adhoc learnings

## Key Technical Details

### Bitwig Presets (.bwpreset)

- Binary format with header indicating encryption
- Header `0004` = factory presets (encrypted, unreadable)
- Header `0002` = user presets (unencrypted, parseable)
- Metadata is filesystem-based: folder name = device, filename = preset name
- Tool: [bwEdit-Python](https://github.com/jaxter184/bwEdit-Python) for user presets

### macOS Plugin Locations

| Format | Path |
|--------|------|
| VST2 | `/Library/Audio/Plug-Ins/VST/` |
| VST3 | `/Library/Audio/Plug-Ins/VST3/` |
| CLAP | `/Library/Audio/Plug-Ins/CLAP/` |
| AU | `/Library/Audio/Plug-Ins/Components/` |

### Kontakt Libraries

- Native Access default: `/Users/Shared/`
- External drive: `/Volumes/External/kontakt_libraries/`
- Registry: `/Users/Shared/Native Instruments/installed_products/*.json`
- Player-compatible libraries have `.nicnt` file

### M-Tron Pro IV

- Patches: `/Library/Application Support/GForce/M-Tron Pro IV/Patches/*.xml` (parseable XML)
- Expansions: `/Volumes/External/M-Tron Pro Library/*.cpt2`

### DrivenByMoss (Submodule)

Our fork at `audio-forge-rs/DrivenByMoss`. Build with Maven:
```bash
cd DrivenByMoss
mvn clean package -Dbitwig.extension.directory=target
cp target/DrivenByMoss-*.jar ~/Documents/Bitwig\ Studio/Extensions/DrivenByMoss.bwextension
```

## Commands

Run adhoc discovery scripts:
```bash
python adhoc-plugin-scripts/discover_plugins.py [VST2|VST3|CLAP|AU|KONTAKT|MTRON]
python adhoc-bwpreset-scripts/discover_presets.py [device-filter]
```

## Code Style

- Python 3.11+ with type hints
- Use `pathlib.Path` for filesystem operations
- CLI tools use argparse with subcommands
- Prefer dataclasses for structured data
