# Docx Report Generator

The Docx Report Generator is a module that helps you create reports using only a .docx template and Jinja syntax.

This module inspired from [Report Xlsx](https://apps.odoo.com/apps/modules/16.0/report_xlsx).

## Prerequisites

Before installing this module, make sure to install the following libraries:
#### For Python 3.12 and above
- `pip install git+https://github.com/tvuotila/docxcompose.git@hotfix/90 docxtpl htmldocx`
#### Below Python 3.12
- `pip install docxcompose docxtpl htmldocx`

## Usage

For usage instructions, you can refer to the following video: [Link](https://www.youtube.com/watch?v=dZvak8yiD5Q)  
![Video Preview](assets/preview.gif)

Example template use for sale order: [Link](https://github.com/oremacle/docx-report/raw/19.0/ormdoo_docx_report/static/description/example/example.docx)

Documentation on writing syntax in the document: [Link](https://docxtpl.readthedocs.io/en/stable/)

## Field Naming Convention

To call and write the field name, use the following format: `{{docs.field_name}}`, starting with the word "docs".

### Template Syntax Guide

#### 1. Basic Jinja2 Syntax

**Variables:**
```jinja
{{docs.field_name}}
```

**Conditions:**
```jinja
{% if docs.field %}
Content to display
{% endif %}
```

**Loops:**
```jinja
{% for line in docs.order_line %}
{{line.name}} - {{line.quantity}}
{% endfor %}
```

**Important:** For testing subdocuments or objects, use `is not none`:
```jinja
{% if note_subdoc is not none %}
{{p note_subdoc}}
{% endif %}
```

#### 2. Whitespace Control

Use `-` to remove whitespace before or after tags:

```jinja
Conditions:
{% if docs.note %}    ← No dash: keeps "Conditions:" intact
{{p note_subdoc}}
{%- endif %}          ← Dash after: removes space after endif
```

**Warning:** `{%-` removes whitespace **before** the tag, which can remove preceding text!

```jinja
Conditions:
{%- if docs.note %}   ← ❌ Will remove "Conditions:" line!
```

#### 3. Working with HTML Fields (like sale.order.note)

For HTML fields in Odoo, use the pre-processed `note_subdoc` variable:

```jinja
{% if note_subdoc is not none %}
{{p note_subdoc}}
{% endif %}
```

This preserves all HTML formatting: **bold**, *italic*, lists, colors, etc.

**Note:** The `note_subdoc` variable is automatically created for `sale.order.note` field. The HTML is cleaned and converted to a Word subdocument.

### Useful Functions

#### Text & Numbers

- `{{spelled_out(docs.numeric_field)}}`: Spell out numbers
  - Default language: Indonesian (`id_ID`)
  - Change language: `{{spelled_out(docs.amount_total, lang='fr_FR')}}`
  - Example: `1234.56` → `"mille deux cent trente-quatre virgule cinquante-six"`

#### Dates

- `{{formatdate(docs.date_field)}}`: Format dates
  - **Default**: Indonesian (`id_ID`), format `full`
  - **Change language**: `{{formatdate(docs.date_order, lang='fr_FR')}}`
  - **Change format**: `{{formatdate(docs.date_order, format='short', lang='fr_FR')}}`

  Available formats:
  - `short`: `09/02/26`
  - `medium`: `9 févr. 2026`
  - `long`: `9 février 2026`
  - `full`: `dimanche 9 février 2026`

  Common languages:
  - French: `lang='fr_FR'`
  - English (US): `lang='en_US'`
  - Dutch: `lang='nl_NL'`

#### Currency

- `{{convert_currency(docs.monetary_field, docs.currency_id)}}`: Format monetary values
  - Example: `{{convert_currency(docs.amount_total, docs.currency_id)}}`

#### HTML Fields

- `{{parsehtml(docs.html_field)}}`: Convert HTML to plain text (no formatting)
- `{{p html2docx(docs.html_field)}}`: Convert HTML to Word subdocument (preserves formatting)
  - **Note**: Use `{{p note_subdoc}}` for `sale.order.note` field (pre-processed automatically)

#### Images

- `{{render_image(docs.image_field)}}`: Render image in document
  - With size: `{{render_image(docs.image_field, width=50, height=50)}}` (in mm)
- `{{replace_image('dummy_image.jpg', docs.image_field)}}`: Replace placeholder image
- `{{replace_media('dummy_image.jpg', docs.image_field)}}`: Replace media file

#### Rich Text

- `{{r rich_text(docs.text_field)}}`: Display rich text with formatting

#### Subdocuments

- `{{p add_subdoc(docs.docx_binary_field)}}`: Insert another DOCX file as subdocument
- `{{replace_embedded('file_name_in_word', docs.binary_field)}}`: Replace embedded object
- `{{replace_zipname('file_path_in_word', docs.binary_field)}}`: Replace file in document structure

**Note**: Functions with `{{p ...}}` directive insert content as paragraphs/subdocuments.

### Practical Examples

#### Example 1: Customer Address with Conditional Fields

```jinja
{{docs.partner_id.name}}
{{docs.partner_id.street}}
{% if docs.partner_id.street2 %}
{{docs.partner_id.street2}}
{% endif %}
{{docs.partner_id.zip}} {{docs.partner_id.city}}
```

#### Example 2: Date in French with Custom Format

```jinja
Date de commande : {{formatdate(docs.date_order, format='long', lang='fr_FR')}}
```

Output: `Date de commande : 9 février 2026`

#### Example 3: Terms and Conditions (HTML Field)

```jinja
Conditions générales :
{% if note_subdoc is not none %}
{{p note_subdoc}}
{% endif %}
```

This displays the `sale.order.note` HTML field with **full formatting** (bold, lists, colors, etc.).

#### Example 4: Order Lines Loop

```jinja
{% for line in docs.order_line %}
{{line.product_id.name}} - Quantité : {{line.product_uom_qty}} - Prix : {{line.price_unit}} €
{% endfor %}
```

#### Example 5: Conditional Section with Whitespace Control

```jinja
Section title:
{% if docs.client_order_ref %}
Référence client : {{docs.client_order_ref}}
{% endif %}

Next section...
```

**Tip**: Don't use `{%-` at the start if you want to keep the preceding text!

### Automatic Variables

Some variables are **automatically pre-processed** and available in your templates:

#### `note_subdoc` (for `sale.order.note`)

When working with Sale Orders, the `note_subdoc` variable is automatically created from the HTML field `sale.order.note`:

- ✅ **HTML is cleaned** (removes problematic tags like `<script>`, `<style>`)
- ✅ **Converted to Word subdocument** with full formatting preserved
- ✅ **Ready to use** in templates with `{{p note_subdoc}}`

**Usage:**
```jinja
{% if note_subdoc is not none %}
{{p note_subdoc}}
{% endif %}
```

**Important:** Always use `is not none` to test if a subdocument exists, not just `if note_subdoc`.

### Docx Mode

There are three modes for generating `.docx` reports:

1. **composer**: Generate a `.docx` file
2. **zip**: Generate a `.zip` containing the `.docx` file
3. **pdf**: Convert the `.docx` file to PDF using LibreOffice

#### PDF Mode

If you want to use the "pdf" option, ensure that LibreOffice is installed. Then set the LibreOffice path in **Settings** => **Technical** => **Parameters** => **System Parameters**, and search for the key `default_libreoffice_path`. Set the value according to your LibreOffice installation path:

- **Linux**: `/usr/bin/libreoffice`
- **Windows**: `C:\Program Files\LibreOffice\program\soffice.exe`

## Feedback

We welcome any feedback and suggestions, especially for improving this module. Thank you!
