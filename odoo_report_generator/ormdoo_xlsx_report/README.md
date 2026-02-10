# XLSX Report Generator

The XLSX Report Generator is a module that helps you create reports using only a .xlsx template and Jinja syntax.

This module inspired from [Report Xlsx](https://apps.odoo.com/apps/modules/16.0/report_xlsx).

## Prerequisites

Before installing this module, make sure to install the following libraries:

- `pip install xlsxtpl`

## Usage

For usage instructions, you can refer to the following video: [Link](https://youtu.be/-mpE5AaSJhw)
![Video Preview](assets/preview.gif)

Example Template: [Link](https://github.com/oremacle/xlsx-report/raw/19.0/ormdoo_xlsx_report/static/description/example/example.xlsx)
Example Template with Image: [Link](https://github.com/oremacle/xlsx-report/raw/19.0/ormdoo_xlsx_report/static/description/example/example_with_picture.xlsx)

Documentation on xlsxtpl syntax: [Link](https://pypi.org/project/xlsxtpl/)

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

#### 2. Working with Multiple Sheets

When your Excel template has multiple sheets, each sheet is rendered independently with the same context:

```jinja
Sheet 1: Order Summary
{{docs.name}} - {{docs.amount_total}}

Sheet 2: Order Lines
{% for line in docs.order_line %}
{{line.product_id.name}}
{% endfor %}
```

**Note:** All sheets in your template will be included in the output. The variable `sheet_name` and `tpl_idx` are automatically available to identify the current sheet.

#### 3. Special Cell Values

**Non-string values ({% xv %}):**
Use this to insert values that Excel should treat as numbers/dates, not strings:

```jinja
{% xv docs.amount_total %}        ← Excel number (can use in formulas)
{% xv docs.date_order %}           ← Excel date (can format as date)
{{docs.amount_total}}              ← String "1234.56" (text)
```

**Checkbox ({% yn %}):**
Returns a checkmark based on boolean condition:

```jinja
{% yn docs.invoiced %}              ← ✓ or empty based on True/False
```

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
  - `full`: `lundi 10 février 2026`

  Common languages:
  - French: `lang='fr_FR'`
  - English (US): `lang='en_US'`
  - Dutch: `lang='nl_NL'`

#### Currency

- `{{convert_currency(docs.monetary_field, docs.currency_id)}}`: Format monetary values
  - Example: `{{convert_currency(docs.amount_total, docs.currency_id)}}`
  - With locale: `{{convert_currency(docs.amount_total, docs.currency_id, locale='fr_FR')}}`

#### Images

**Insert image (fit to cell):**
```jinja
{% insert_img docs.image_field %}
```
The image is resized to fit within the cell boundaries.

**Insert image (cell fits image):**
```jinja
{% insert_img_cell docs.image_field %}
```
The cell is resized to match the image dimensions.

**Insert image with custom size:**
```jinja
{% insert_img_cell docs.image_field, width=200, height=200 %}
```
Specify width and height in pixels.

**Replace placeholder image:**
```jinja
{% img docs.image_field %}
```
Replaces a dummy image in your template with the actual image field.

![Replace Image Syntax](assets/assets/replace_image.png)

**Note:**
- Images support **WebP format** (automatically converted to PNG)
- Images are automatically decoded from base64 Odoo format
- All image fields must be Odoo `Binary` or `Image` field types

### Practical Examples

#### Example 1: Customer Address Table

```
| Field          | Value                      |
|----------------|----------------------------|
| Customer       | {{docs.partner_id.name}}   |
| Street         | {{docs.partner_id.street}} |
| City           | {{docs.partner_id.city}}   |
| Postal Code    | {{docs.partner_id.zip}}    |
```

#### Example 2: Order Lines with Loop

```
| Product                    | Qty                      | Price                 | Subtotal                        |
|----------------------------|--------------------------|---------------------- |---------------------------------|
{% for line in docs.order_line %}
| {{line.product_id.name}}   | {% xv line.product_uom_qty %} | {% xv line.price_unit %} | {% xv line.price_subtotal %} |
{% endfor %}
|                            |                          | **Total:**            | {% xv docs.amount_total %}      |
```

**Tips:**
- Use `{% xv ... %}` for numeric values so Excel can calculate formulas
- The loop will create one row per order line

#### Example 3: Conditional Content

```jinja
Order: {{docs.name}}
Date: {{formatdate(docs.date_order, format='long', lang='fr_FR')}}

{% if docs.client_order_ref %}
Customer Reference: {{docs.client_order_ref}}
{% endif %}

{% if docs.payment_term_id %}
Payment Terms: {{docs.payment_term_id.name}}
{% endif %}
```

#### Example 4: Date Formatting

```jinja
Order Date (full): {{formatdate(docs.date_order, format='full', lang='fr_FR')}}
Order Date (short): {{formatdate(docs.date_order, format='short', lang='fr_FR')}}

Delivery Date: {{formatdate(docs.commitment_date, format='medium', lang='fr_FR')}}
```

Output:
```
Order Date (full): lundi 10 février 2026
Order Date (short): 10/02/26
Delivery Date: 10 févr. 2026
```

#### Example 5: Product Images in Cells

```
| Product                    | Image                                      | Price                 |
|----------------------------|--------------------------------------------|-----------------------|
{% for line in docs.order_line %}
| {{line.product_id.name}}   | {% insert_img_cell line.product_id.image_128, width=80, height=80 %} | {% xv line.price_unit %} |
{% endfor %}
```

### Automatic Variables

Some variables are **automatically available** in your templates:

- `docs`: The current Odoo record (e.g., sale.order object)
- `data`: Data passed from wizard or context
- `company`: Current company (`self.env.company`)
- `lang`: Current language (default: `id_ID`)
- `sysdate`: Current system date/time
- `sheet_name`: Name of the current sheet being rendered
- `tpl_idx`: Index of the current sheet (0-based)

**Usage:**
```jinja
Generated on: {{formatdate(sysdate, format='full', lang='fr_FR')}}
Company: {{company.name}}
Current Sheet: {{sheet_name}}
```

### Multi-Record Reports

When you generate a report for multiple records (e.g., select 3 sale orders and print), the module automatically:

1. **Single record** → Generates a single `.xlsx` file
2. **Multiple records** → Generates a `.zip` file containing one `.xlsx` per record

The filename for each record is determined by the `print_report_name` configuration.

**Example filename configuration:**
```python
print_report_name = "'Order %s' % object.name if object.name else ''"
```

Results in: `Order SO001.xlsx`, `Order SO002.xlsx`, etc.

## Configuration

### Creating a Report

1. Go to **Settings** → **Technical** → **XLSX Report**
2. Click **Create**
3. Fill in:
   - **Report Name**: Display name (e.g., "Sale Order Report")
   - **Report Code**: Technical code (e.g., `sale.order.xlsx`)
   - **Model**: Select the Odoo model (e.g., `sale.order`)
   - **Field Name**: Field to use for filename (e.g., `name`)
   - **Prefix**: Optional prefix for filename (e.g., "Order_")
   - **Report XLSX Template**: Upload your `.xlsx` template file
4. Click **Save** then **Publish**

The report will now appear in the **Print** menu for that model.

### Report States

- **Draft**: Report is being configured (editable)
- **Published**: Report is active and available in Print menu (read-only)

To modify a published report, click **Unpublish**, make changes, then **Publish** again.

## Technical Notes

### Language Default

The default language for date and number formatting is **Indonesian (`id_ID`)**. To change:

```jinja
{{formatdate(docs.date_order, lang='fr_FR')}}
{{spelled_out(docs.amount_total, lang='fr_FR')}}
{{convert_currency(docs.amount_total, docs.currency_id, locale='fr_FR')}}
```

### Image Format Support

Supported formats:
- PNG, JPEG, BMP, GIF
- **WebP** (automatically converted to PNG)

Images are decoded from Odoo's base64 format automatically.

### Excel Functions

You can use Excel formulas in your template. Use `{% xv %}` to insert cell references:

```
| A                        | B                       | C                    |
|--------------------------|-------------------------|----------------------|
| Product                  | Quantity                | Price                |
| {{line.product_id.name}} | {% xv line.product_uom_qty %} | {% xv line.price_unit %} |
| Total:                   | =SUM(B2:B10)            | =SUM(C2:C10)         |
```

### Debugging Tips

1. **Test with simple templates first**: Start with basic `{{docs.name}}` to ensure everything works
2. **Check field names**: Use Odoo's developer mode to verify exact field names
3. **Use conditions for optional fields**: Wrap optional fields in `{% if %}` blocks
4. **Language issues**: Always specify `lang` parameter if dates appear in wrong language
5. **Image not showing**: Ensure the field is a Binary/Image field and contains data

## Feedback

We welcome any feedback and suggestions, especially for improving this module. Thank you!
