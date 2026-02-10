from datetime import datetime
from num2words import num2words
from babel.dates import format_date
from babel.numbers import format_currency

# Formatting Function
def formatdate(date_required=datetime.today(), format="full", lang=None, **kwargs):
    if not date_required:
        return ""

    # Convert string to date object if needed (Odoo date fields are strings)
    if isinstance(date_required, str):
        try:
            # Try parsing as date (YYYY-MM-DD)
            date_required = datetime.strptime(date_required, "%Y-%m-%d").date()
        except ValueError:
            try:
                # Try parsing as datetime (YYYY-MM-DD HH:MM:SS)
                date_required = datetime.strptime(date_required, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return ""

    locale = lang or "en_US"
    return format_date(date_required, format=format, locale=locale, **kwargs)

def spelled_out(number, lang=None, to="cardinal", **kwargs):
    if number is None or number is False:
        return ""
    language = lang or "en_US"
    return num2words(number, lang=language, to=to, **kwargs)

def convert_currency(number, currency_field, locale=None, **kwargs):
    if number is None or number is False or not currency_field:
        return ""
    loc = locale or "en_US"
    return format_currency(number, currency_field.name, locale=loc, **kwargs)