"""Extract the original diagram forms from the renewed report, without screenshots."""
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter, PageObject
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject, RectangleObject
import pymupdf

ROOT = Path(__file__).resolve().parent.parent
REPORT = 'To_the_Era_of_Agentic_Embodied_Intelligence_renew.pdf'
DIAGRAMS = [
    ('framework', 4, '/Im4', 'figure/framework-renew.pdf', (7, 13, 1022.5, 520)),
    ('action-model', 16, '/Im10', 'figure/action-model-renew.pdf', (3, 3, 1080.5, 604.5)),
]


def main():
    reader = PdfReader(ROOT / REPORT)
    sources_path = ROOT / 'assets/figures/sources.json'
    records = json.loads(sources_path.read_text())
    digest = hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest()
    for ident, number, name, derived, bounds in DIAGRAMS:
        form = reader.pages[number - 1]['/Resources']['/XObject'][name].get_object()
        assert form['/Subtype'] == '/Form' and not form.get('/Matrix'), 'Unexpected source transform'
        writer = PdfWriter()
        page = PageObject.create_blank_page(width=1, height=1)
        page[NameObject('/MediaBox')] = RectangleObject(form['/BBox'])
        page[NameObject('/CropBox')] = RectangleObject(form['/BBox'])
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/XObject'): DictionaryObject({NameObject('/Original'): form})})
        stream = DecodedStreamObject()
        stream.set_data(b'q /Original Do Q')
        page[NameObject('/Contents')] = stream
        writer.add_page(page)
        writer.write(ROOT / derived)
        with pymupdf.open(ROOT / derived) as source:
            canvas = pymupdf.open()
            clip = pymupdf.Rect(bounds)
            target = canvas.new_page(width=clip.width, height=clip.height)
            target.show_pdf_page(target.rect, source, 0, clip=clip)
            (ROOT / f'assets/figures/{ident}.svg').write_text(target.get_svg_image(text_as_path=True))
            canvas.close()
        record = next(row for row in records if row['id'] == ident)
        record.update(source=REPORT, page=number, derived_source=derived,
                      source_sha256=digest, source_form=name, clip=list(bounds))
        print(f'{ident}: report page {number}, original form → {derived}')
    sources_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
