# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains **Odoo 19.0 modules** for odoo_report_generator.

### Modules

| Module | Version | Description |
|--------|---------|-------------|
| **odoo_report_generator** | 19.0.1.0.0 | Main module |

**License:** LGPL-3

## Development Environment Setup

### Python Environment
- Python virtual environment: `/Users/graph/Documents/Code/odoo/19/venv_19_enterprise/bin/python`
- Odoo source: `/Users/graph/Documents/Code/odoo/odoo-src/odoo/odoo-bin`

### Running Odoo

Start Odoo server with this module:
```bash
/Users/graph/Documents/Code/odoo/19/venv_19_enterprise/bin/python \
  /Users/graph/Documents/Code/odoo/odoo-src/odoo/odoo-bin \
  -c /path/to/config.conf \
  --dev=all
```

Update the module in a specific database:
```bash
/Users/graph/Documents/Code/odoo/19/venv_19_enterprise/bin/python \
  /Users/graph/Documents/Code/odoo/odoo-src/odoo/odoo-bin \
  -c /path/to/config.conf \
  -d <database_name> \
  -u odoo_report_generator
```

### VSCode Debugging

The repository includes debug configurations in `.vscode/launch.json`:
- **"19"** - Launches Odoo with `--dev=all` flag
- **"19 dynamic"** - Prompts for database name and module to update

## Module Architecture

### File Structure

```
odoo_report_generator/
├── __manifest__.py           # Module metadata and dependencies
├── __init__.py               # Python package init
├── models/                   # Python model definitions
│   ├── __init__.py
│   └── model.py              # Main model
├── views/                    # XML view definitions
│   └── views.xml             # List, form, kanban views
└── security/                 # Access rights
    └── ir.model.access.csv
```

## Development Guidelines

### Odoo Standards
- Follow Odoo coding guidelines
- Use proper model inheritance (`_inherit = ['mail.thread', 'mail.activity.mixin']`)
- Module version format: `{odoo_version}.{major}.{minor}.{patch}`

### Code Conventions
- License: LGPL-3
- Python style: Follow PEP 8
- XML formatting: 4-space indentation
- Use `_()` for translatable strings
- Always add `tracking=True` for important fields

### Git Workflow
- Commit message format: `[TAG] odoo_report_generator: Description`
- Common tags: `[ADD]`, `[FIX]`, `[IMP]`, `[REF]`, `[REM]`

## Dependencies

**Required Odoo Modules:**
- `base` - Base Odoo functionality

## Version History

- **19.0.1.0.0** - Initial release
