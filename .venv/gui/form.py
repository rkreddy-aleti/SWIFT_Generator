import tkinter as tk
from tkinter import ttk, messagebox
from generator.mt54x import generate_mt54x
from generator.mt548 import generate_mt548
from generator.mt54y import generate_mt54y

class SwiftMessageForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SWIFT Message Generator")

        self.message_type = tk.StringVar()
        self.fields = {}

        self._build_form()

    def _build_form(self):
        ttk.Label(self.root, text="Select Message Type:").grid(row=0, column=0, sticky="w")
        msg_type = ttk.Combobox(self.root, textvariable=self.message_type)
        msg_type["values"] = ("MT54x", "MT548", "MT54Y")
        msg_type.grid(row=0, column=1)
        msg_type.bind("<<ComboboxSelected>>", self._build_fields)

        self.fields_frame = ttk.Frame(self.root)
        self.fields_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        generate_btn = ttk.Button(self.root, text="Generate", command=self._generate)
        generate_btn.grid(row=2, column=0, columnspan=2)

    def _build_fields(self, event=None):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        self.fields.clear()

        fields_list = {
            "MT54x": ["Transaction Ref", "Trade Date", "Settlement Date", "ISIN", "Quantity"],
            "MT548": ["Transaction Ref", "Status", "Processing Time"],
            "MT54Y": ["Related Ref", "Narrative"]
        }

        selected_type = self.message_type.get()
        for idx, field in enumerate(fields_list[selected_type]):
            ttk.Label(self.fields_frame, text=field + ":").grid(row=idx, column=0, sticky="w")
            entry = ttk.Entry(self.fields_frame)
            entry.grid(row=idx, column=1)
            self.fields[field] = entry

    def _generate(self):
        data = {k: v.get() for k, v in self.fields.items()}
        msg_type = self.message_type.get()

        if not all(data.values()):
            messagebox.showerror("Missing Fields", "Please fill all fields")
            return

        if msg_type == "MT54x":
            message = generate_mt54x(data)
        elif msg_type == "MT548":
            message = generate_mt548(data)
        elif msg_type == "MT54Y":
            message = generate_mt54y(data)

        with open(f"{msg_type}_output.txt", "w") as f:
            f.write(message)

        messagebox.showinfo("Success", f"{msg_type} message generated!")

    def run(self):
        self.root.mainloop()
