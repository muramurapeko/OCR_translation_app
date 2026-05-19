import tkinter as tk
from PIL import ImageGrab, Image
import pytesseract
import pyautogui

# Spécifie le chemin de tesseract si ce n'est pas dans le PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class ScreenOCR:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.configure(bg='black')

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.root.mainloop()

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_move_press(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        self.root.destroy()

        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        text = pytesseract.image_to_string(image, lang='chi_sim')

        self.show_text(text)

    def show_text(self, text):
        result_window = tk.Tk()
        result_window.title("Résultat OCR")

        text_box = tk.Text(result_window, wrap="word", font=("Arial", 12))
        text_box.insert("1.0", text)
        text_box.pack(fill=tk.BOTH, expand=True)

        result_window.mainloop()

if __name__ == "__main__":
    ScreenOCR()
