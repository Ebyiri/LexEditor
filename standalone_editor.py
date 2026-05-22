
import json
import os
from lxml import etree

def generate_docs(elements, doc_name="law_output"):
    # JSON Generation
    json_path = f"{doc_name}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(elements, f, ensure_ascii=False, indent=4)
    
    # XML Generation (Akoma Ntoso)
    NS = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
    root = etree.Element("{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}akomaNtoso", nsmap={None: NS["akn"]})
    act = etree.SubElement(root, "act", name="republicOfRwandaLaw")
    body = etree.SubElement(act, "body")
    
    for item in elements:
        container = etree.SubElement(body, item.get('type', 'section'), eId=item.get('id', 'item_1'))
        heading = etree.SubElement(container, "heading")
        for lang in ['en', 'fr', 'rw']:
            span = etree.SubElement(heading, "span", lang=lang)
            span.text = item.get('text', {}).get(lang, "")
            
    xml_path = f"{doc_name}.xml"
    with open(xml_path, "wb") as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
    
    print(f"Success! Created {json_path} and {xml_path}")

if __name__ == '__main__':
    print('--- Rwanda Legal Editor CLI ---')
    # Simple CLI interaction for the EXE
    art_id = input("Enter Article ID (e.g., art_1): ") or "art_1"
    en_t = input("English Title: ")
    
    data = [{
        "id": art_id,
        "type": "article",
        "text": {"en": en_t, "fr": "Pending", "rw": "Icyitonderwa"}
    }]
    
    generate_docs(data)
    input("Press Enter to exit...")
