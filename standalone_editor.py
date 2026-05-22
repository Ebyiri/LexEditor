
import json
import os
from lxml import etree

HIERARCHY = {
    "Administrative": ["Administrative Organs", "Civil service", "Community Works", "Education", "Election", "Governance", "Health", "Heritage and Tradition", "Immigration", "Partnership", "Sports", "State finance", "State organs", "Urbanisation"],
    "Business": ["Agriculture production", "Animal Production", "Aviation", "Banking", "Capital Market", "Central Security Depository", "Foreign exchange", "Gaming", "Industry", "Insurance", "Intellectual Property", "Investment", "Microfinance", "National Bank of Rwanda", "Organization of commercial Activities", "Telecomunication", "Tourism"],
    "Civil": ["Contracts and Collaterals", "Environment", "Labor", "Liberal Proffessions", "Media and information", "National Resources", "Non-Governmental Organization", "Notary Services", "Persons", "Property"]
}

def generate_docs(elements, doc_name="law_output"):
    json_path = f"{doc_name}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(elements, f, ensure_ascii=False, indent=4)
    
    NS = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
    root = etree.Element("{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}akomaNtoso", nsmap={None: NS["akn"]})
    act = etree.SubElement(root, "act", name="republicOfRwandaLaw")
    body = etree.SubElement(act, "body")
    
    for item in elements:
        container = etree.SubElement(body, "article", eId=item.get('id'))
        heading = etree.SubElement(container, "heading")
        heading.text = item.get('text', {}).get('en', "")
            
    xml_path = f"{doc_name}.xml"
    with open(xml_path, "wb") as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
    print(f"Success! Generated {json_path} and {xml_path}")

if __name__ == '__main__':
    print('--- Rwanda Legal Editor (Hierarchical) ---')
    print("Available Categories:", ", ".join(HIERARCHY.keys()))
    cat = input("Select Category: ")
    art_id = input("Article ID: ")
    en_t = input("English Title: ")
    
    data = [{
        "id": art_id,
        "category": cat,
        "text": {"en": en_t}
    }]
    generate_docs(data)
    input("Done. Press Enter to exit...")
