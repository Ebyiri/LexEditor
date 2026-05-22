import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from lxml import etree

# Full Rwanda Legal Hierarchy
HIERARCHY = {
    "Administrative": ["Administrative Organs", "Civil service", "Health", "Education", "Immigration"],
    "Business": ["Banking", "Investment", "Telecomunication", "Industry", "Agriculture"],
    "Civil": ["Contracts", "Labor", "Property", "Environment", "Persons"],
    "Criminal": ["Corruption", "CyberCrimes", "Genocide Ideology", "Human Trafficking"],
    "Fundamentals": ["Constitution", "Parliament", "Official Languages"],
    "Judicial": ["Courts", "Prosecution", "Investigation", "Procedures"]
}

def generate_akn_xml(data, filename="law_output"):
    try:
        NS = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
        root = etree.Element("{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}akomaNtoso", nsmap={None: NS["akn"]})
        act = etree.SubElement(root, "act", name="republicOfRwandaLaw")
        meta = etree.SubElement(act, "meta")
        prop = etree.SubElement(meta, "proprietary", source="#rwandaLegalPortal")
        etree.SubElement(prop, "category").text = data.get('category', 'General')
        etree.SubElement(prop, "subCategory").text = data.get('sub_category', 'General')
        body = etree.SubElement(act, "body")
        article = etree.SubElement(body, "article", eId=data.get('id', 'art_1'))
        heading = etree.SubElement(article, "heading")
        for lang in ['en', 'fr', 'rw']:
            span = etree.SubElement(heading, "span", lang=lang)
            span.text = data['titles'].get(lang, "")
        content = etree.SubElement(article, "content")
        for lang in ['en', 'fr', 'rw']:
            p = etree.SubElement(content, "p", lang=lang)
            p.text = data['contents'].get(lang, "")
        with open(f"{filename}.xml", "wb") as f:
            f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
        with open(f"{filename}.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        return str(e)

class LexEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rwanda Legal Editor & Automation Tool")
        self.root.geometry("700x750")
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill="both", expand=True)
        ttk.Label(main_frame, text="Category:").grid(row=1, column=0, sticky="w")
        self.cat_cb = ttk.Combobox(main_frame, values=list(HIERARCHY.keys()), width=30)
        self.cat_cb.grid(row=1, column=1, sticky="w", pady=5)
        self.cat_cb.bind("<<ComboboxSelected>>", self.update_subs)
        ttk.Label(main_frame, text="Sub-Category:").grid(row=2, column=0, sticky="w")
        self.sub_cb = ttk.Combobox(main_frame, width=30)
        self.sub_cb.grid(row=2, column=1, sticky="w", pady=5)
        ttk.Label(main_frame, text="Article ID:").grid(row=3, column=0, sticky="w")
        self.ent_id = ttk.Entry(main_frame, width=33)
        self.ent_id.insert(0, "art_1")
        self.ent_id.grid(row=3, column=1, sticky="w", pady=5)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=20)
        self.lang_fields = {}
        for lang_code, lang_name in [("en", "English"), ("fr", "French"), ("rw", "Kinyarwanda")]:
            frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(frame, text=lang_name)
            ttk.Label(frame, text="Title:").pack(anchor="w")
            t_ent = ttk.Entry(frame, width=80)
            t_ent.pack(pady=5)
            ttk.Label(frame, text="Content:").pack(anchor="w")
            c_txt = scrolledtext.ScrolledText(frame, width=70, height=10)
            c_txt.pack(pady=5)
            self.lang_fields[lang_code] = {"title": t_ent, "content": c_txt}
        btn = tk.Button(main_frame, text="GENERATE PRODUCTION FILES", command=self.submit)
        btn.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

    def update_subs(self, event):
        self.sub_cb['values'] = HIERARCHY.get(self.cat_cb.get(), [])

    def submit(self):
        data = {
            "category": self.cat_cb.get(),
            "sub_category": self.sub_cb.get(),
            "id": self.ent_id.get(),
            "titles": {k: v["title"].get() for k, v in self.lang_fields.items()},
            "contents": {k: v["content"].get("1.0", tk.END).strip() for k, v in self.lang_fields.items()}
        }
        if generate_akn_xml(data) == True:
            messagebox.showinfo("Success", "Generated!")

if __name__ == '__main__':
    root = tk.Tk()
    app = LexEditorApp(root)
    root.mainloop()