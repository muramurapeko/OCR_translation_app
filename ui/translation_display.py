import tkinter as tk
from tkinter import scrolledtext

class TranslationDisplayFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=10, pady=5)

        # Label
        self.label = tk.Label(self, text="🌐 Traduction / LLM Output :", anchor="w", font=("Arial", 12, "bold"))
        self.label.pack(fill="x")

        # Zone de texte scrollable
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10)
        self.text_area.pack(fill="both", expand=True)
        self.text_area.configure(state="disabled")

    def update_translation(self, text):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state="disabled")


# Test local
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test - Translation Output")

    frame = TranslationDisplayFrame(root)
    frame.update_translation("Ceci est la traduction automatique du texte OCR...")

    root.mainloop()
