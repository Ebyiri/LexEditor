
import json
import tkinter as tk
from tkinter import ttk, messagebox
from lxml import etree

HIERARCHY = {
    "Administrative": ["Administrative Organs", "Civil service", "Education", "Health"],
    "Business": ["Banking", "Industry", "Investment", "Telecomunication"],
    "Civil": ["Contracts", "Environment", "Labor", "Property"],
    "Criminal": ["Corruption", "CyberCrimes", "Genocide Ideology"],
    "Fundamentals": ["Constitution", "Parliament", "Official Languages"]
}

def generate_docs(elements, doc_name="law_output"):
    try:
        NS = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
        root = etree.Element("{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}akomaNtoso", nsmap={None: NS["akn"]})
        act = etree.SubElement(root, "act", name="republicOfRwandaLaw")
        body = etree.SubElement(act, "body")
        for item in elements:
            container = etree.SubElement(body, "article", eId=item.get('id'))
            heading = etree.SubElement(container, "heading")
            heading.text = item.get('text', {}).get('en', "")
        
        with open(f"{doc_name}.xml", "wb") as f:
            f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
        return True
    except Exception as e:
        return str(e)

def run_gui():
    root = tk.Tk()
    root.title("Rwanda Legal Editor v2.0")
    root.geometry("450x350")

    tk.Label(root, text="Select Law Category:", font=('Arial', 10, 'bold')).pack(pady=5)
    cat_combo = ttk.Combobox(root, values=list(HIERARCHY.keys()), width=40)
    cat_combo.pack(pady=5)

    tk.Label(root, text="Article ID (e.g., art_1):").pack(pady=2)
    ent_id = tk.Entry(root, width=43)
    ent_id.pack(pady=5)

    tk.Label(root, text="English Title / Heading:").pack(pady=2)
    ent_title = tk.Entry(root, width=43)
    ent_title.pack(pady=5)

    def on_submit():
        if not cat_combo.get() or not ent_id.get():
            messagebox.showwarning("Input Error", "Please fill in the Category and Article ID.")
            return
            
        data = [{
            "id": ent_id.get(),
            "category": cat_combo.get(),
            "text": {"en": ent_title.get()}
        }]
        res = generate_docs(data)
        if res == True:
            messagebox.showinfo("Success", f"Files generated successfully!\nCheck your folder for law_output.xml")
        else:
            messagebox.showerror("Error", f"Failed: {res}")

    tk.Button(root, text="Generate Akoma Ntoso XML", command=on_submit, bg="#2e7d32", fg="white", font=('Arial', 10, 'bold')).pack(pady=20)
    
    tk.Label(root, text="Status: Ready", fg="gray").pack(side="bottom", pady=5)
    root.mainloop()

if __name__ == '__main__':
    run_gui()
