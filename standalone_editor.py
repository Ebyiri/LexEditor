import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from lxml import etree
from datetime import datetime

# Complete Production Hierarchy
HIERARCHY = {
    "Administrative": ["Administrative Organs", "Civil service", "Education", "Election", "Governance", "Health", "Immigration"],
    "Business": ["Banking", "Capital Market", "Gaming", "Industry", "Insurance", "Investment", "Telecomunication", "Tourism"],
    "Civil": ["Contracts and Collaterals", "Environment", "Labor", "Media", "National Resources", "Property"],
    "Criminal": ["Corruption", "CyberCrimes", "Data Protection", "Genocide Ideology", "Human Trafficking", "Terrorism"],
    "Fundamentals": ["Constitution", "Parliament", "Political Organizations", "Official Languages"],
    "Judicial": ["Correctional Services", "Courts", "Investigation", "Legal Assistance", "Prosecution"],
    "Security": ["Security Activities", "Security Organs and Staff"]
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
        self.root.title("Rwanda Legal Editor Pro v2.0")
        self.root.geometry("800x850")
        self.root.configure(bg="#f0f0f0")

        # Styling
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Header.TLabel", font=('Helvetica', 16, 'bold'), foreground="#2c3e50")
        
        # Header
        header_frame = ttk.Frame(root, padding="20")
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="🇷🇼 Rwanda Legal Automation Dashboard", style="Header.TLabel").pack(side="left")
        
        main_container = ttk.Frame(root, padding="20")
        main_container.pack(fill="both", expand=True)

        # Section 1: Classification
        class_frame = ttk.LabelFrame(main_container, text=" Law Classification & Metadata ", padding="15")
        class_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(class_frame, text="Domain Category:").grid(row=0, column=0, sticky="w", padx=5)
        self.cat_cb = ttk.Combobox(class_frame, values=list(HIERARCHY.keys()), width=40, state="readonly")
        self.cat_cb.grid(row=0, column=1, sticky="w", pady=5)
        self.cat_cb.bind("<<ComboboxSelected>>", self.update_subs)

        ttk.Label(class_frame, text="Sub-Category:").grid(row=1, column=0, sticky="w", padx=5)
        self.sub_cb = ttk.Combobox(class_frame, width=40, state="readonly")
        self.sub_cb.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(class_frame, text="Technical ID (eId):").grid(row=2, column=0, sticky="w", padx=5)
        self.ent_id = ttk.Entry(class_frame, width=43)
        self.ent_id.insert(0, "art_section_1")
        self.ent_id.grid(row=2, column=1, sticky="w", pady=5)

        # Section 2: Trilingual Content
        content_frame = ttk.LabelFrame(main_container, text=" Multilingual Legislative Content ", padding="10")
        content_frame.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)

        self.lang_fields = {}
        for code, name, color in [("en", "English", "#003366"), ("fr", "French", "#660000"), ("rw", "Kinyarwanda", "#006633")]:
            f = ttk.Frame(self.notebook, padding=15)
            self.notebook.add(f, text=f" {name} ")
            
            ttk.Label(f, text="Official Title / Heading:", font=('Arial', 9, 'bold')).pack(anchor="w")
            t_ent = ttk.Entry(f, width=90, font=('Arial', 10))
            t_ent.pack(pady=(5, 15), ipady=3)
            
            ttk.Label(f, text="Legislative Text / Content:", font=('Arial', 9, 'bold')).pack(anchor="w")
            c_txt = scrolledtext.ScrolledText(f, width=80, height=12, font=('Verdana', 10), undo=True)
            c_txt.pack(pady=5, fill="both", expand=True)
            self.lang_fields[code] = {"title": t_ent, "content": c_txt}

        # Action Bar
        self.status_var = tk.StringVar(value="Ready to generate legal artifacts...")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w", padding=(5, 2))
        status_bar.pack(side="bottom", fill="x")

        btn_frame = ttk.Frame(main_container, padding="10")
        btn_frame.pack(fill="x")
        
        self.gen_btn = tk.Button(btn_frame, text="🚀 GENERATE PRODUCTION-READY XML & JSON", 
                                 bg="#27ae60", fg="white", font=('Arial', 11, 'bold'), 
                                 relief="flat", command=self.submit, cursor="hand2")
        self.gen_btn.pack(fill="x", ipady=10)

    def update_subs(self, event):
        self.sub_cb['values'] = HIERARCHY.get(self.cat_cb.get(), [])
        self.sub_cb.set("")

    def submit(self):
        if not self.cat_cb.get():
            messagebox.showwarning("Input Required", "Please select a Law Category first.")
            return

        data = {
            "category": self.cat_cb.get(),
            "sub_category": self.sub_cb.get(),
            "id": self.ent_id.get(),
            "titles": {k: v["title"].get() for k, v in self.lang_fields.items()},
            "contents": {k: v["content"].get("1.0", tk.END).strip() for k, v in self.lang_fields.items()},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.status_var.set("Generating files...")
        result = generate_akn_xml(data)
        
        if result == True:
            self.status_var.set(f"Successfully generated at {datetime.now().strftime('%H:%M:%S')}")
            messagebox.showinfo("Success", "Akoma Ntoso 3.0 XML and JSON maps generated successfully!")
        else:
            messagebox.showerror("Pipeline Error", f"Failed to generate files: {result}")

if __name__ == '__main__':
    root = tk.Tk()
    app = LexEditorApp(root)
    root.mainloop()