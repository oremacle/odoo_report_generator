from io import BytesIO
from base64 import b64decode
from datetime import datetime
from docx import Document
from docx.shared import Mm
from docxtpl import InlineImage, RichText
from bs4 import BeautifulSoup
from num2words import num2words
from babel.dates import format_date
from babel.numbers import format_currency
from htmldocx import HtmlToDocx

# Partial Function
def render_image(tpl, imgb64, width=None, height=None):
    width = Mm(width) if width else None
    height = Mm(height) if height else None
        
    if not imgb64:
        return ''

    image_stream = BytesIO(b64decode(imgb64))
    return InlineImage(
        tpl, image_descriptor=image_stream, width=width, height=height
    )
    
def render_html_as_subdoc(tpl, html_code=None):
    if not (
        isinstance(html_code, str)
        and bool(BeautifulSoup(html_code, "html.parser").find())
    ):
        return ""

    temp = BytesIO()
    desc_document = Document()
    new_parser = HtmlToDocx()
    new_parser.add_html_to_document(html_code, desc_document)
    desc_document.save(temp)
    temp.seek(0)
    return tpl.new_subdoc(temp)


def add_new_subdoc(tpl, docx_file):
    if docx_file:
        return tpl.new_subdoc(BytesIO(b64decode(docx_file)))
    
    return tpl.new_subdoc()


def replace_image(tpl, dummy_pic, imgb64):
    if not imgb64:
        return ''

    tpl.replace_pic(dummy_pic, BytesIO(b64decode(imgb64)))
    return ''

def replace_media(tpl, dummy_pic, imgb64):
    if not imgb64:
        return ''

    tpl.replace_media(dummy_pic, BytesIO(b64decode(imgb64)))
    return ''

def replace_embedded(tpl, dummy_embeed, file_b64):
    if not file_b64:
        return ''

    tpl.replace_embedded(dummy_embeed, BytesIO(b64decode(file_b64)))
    return ''

def replace_zipname(tpl, embedded_object_path, file_b64):
    if not file_b64:
        return ''

    tpl.replace_zipname(embedded_object_path, BytesIO(b64decode(file_b64)))
    return ''

# Formatting Function
def parse_html(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def formatdate(date_required=datetime.today(), format="full", lang=None, **kwargs):
    from datetime import date, time

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

    # Verify it's a valid date/datetime/time object before formatting
    if not isinstance(date_required, (date, datetime, time)):
        # If it's not a valid type, return empty string to avoid error
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

def format_abs(number):
    return abs(number)

def rich_text(text, **kwargs):
    if not text:
        return ""
    
    return RichText(text, **kwargs)