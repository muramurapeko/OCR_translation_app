# ui/controls.py
import tkinter as tk
from tkinter import ttk
import sys
import sys
import os
from unittest import result
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tkinter as tk
from tkinter import ttk
import threading
import time
from core.screen_capture import select_screen_area
from PIL import ImageGrab
# import pytesseract
# import easyocr
import numpy as np
from paddleocr import PaddleOCR
class ControlsFrame(tk.Frame):
    def __init__(self, master=None, on_area_selected=None, on_toggle_capture=None, on_frequency_change=None, on_ocr_result=None):
        super().__init__(master)

        # 🟢 Préchargement de EasyOCR Reader
        
        print("[INFO] Initializing EasyOCR reader...")
        language_list = ['ch_sim']
        # 🔁 Preload OCR readers once to reduce latency
        self.easyocr_reader = None
        self.paddleocr_reader = None
        
        


        self.on_area_selected = on_area_selected
        self.on_toggle_capture = on_toggle_capture
        self.on_frequency_change = on_frequency_change
        self.on_ocr_result = on_ocr_result  # Callback pour l'affichage OCR

        self.selected_bbox = None  # Zone sélectionnée

        self.capture_continuous = False
        self.capture_thread = None
        self.capture_interval = 2.0  # Intervalle de capture

        self.pack(fill="x", padx=10, pady=5)

        # Bouton de sélection de zone
        self.select_btn = ttk.Button(self, text="📷 Sélectionner une portion de l'écran", command=self.handle_select)
        self.select_btn.pack(side="left", padx=5)

        # Toggle capture continue
        self.capture_var = tk.BooleanVar()
        self.toggle_btn = ttk.Checkbutton(self, text="Capture continue", variable=self.capture_var,
                                          command=self.handle_toggle)
        self.toggle_btn.pack(side="left", padx=5)

        # Slider fréquence de capture
        self.freq_value = tk.DoubleVar(value=self.capture_interval)
        self.freq_label = ttk.Label(self, text=f"Fréquence : {self.freq_value.get():.1f} s")
        self.freq_label.pack(side="left", padx=(20, 5))
        self.freq_slider = ttk.Scale(self, from_=0.5, to=10, variable=self.freq_value,
                                     orient="horizontal", command=self.handle_freq_change)
        self.freq_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def handle_select(self):
        # Réinitialiser la zone avant la nouvelle sélection
        self.selected_bbox = None
        
        def callback(bbox):
            print("Zone sélectionnée :", bbox)
            self.selected_bbox = bbox  # Mettre à jour la zone sélectionnée
            if self.on_area_selected:
                self.on_area_selected(bbox)
            self.process_ocr_on_selected_area(bbox)  # Traiter l'OCR immédiatement après la sélection

        select_screen_area(callback)

    
    def handle_toggle(self):
        self.capture_continuous = self.capture_var.get()  # Capture continue
        if self.capture_continuous:
            self.start_capture_thread()
        else:
            self.stop_capture_thread()

        if self.on_toggle_capture:
            self.on_toggle_capture(self.capture_continuous)

    def handle_freq_change(self, val):
        self.capture_interval = float(val)
        self.freq_label.config(text=f"Fréquence : {self.capture_interval:.1f} s")
        if self.on_frequency_change:
            self.on_frequency_change(self.capture_interval)



    def process_ocr_on_selected_area(self, bbox, language="ch_sim+eng", ocr_tool="paddleocr"):
        try:
            screenshot = ImageGrab.grab(bbox)
            np_img = np.array(screenshot)

            text = ""
            start_time = time.time()

            if ocr_tool == "tesseract":
                text = pytesseract.image_to_string(screenshot, lang=language)

            elif ocr_tool == "easyocr":
                if self.easyocr_reader is None:
                    langs = language.split("+")
                    self.easyocr_reader = easyocr.Reader(langs)
                results = self.easyocr_reader.readtext(np_img, detail=0)
                text = " ".join(results)

            elif ocr_tool == "paddleocr":
                if self.paddleocr_reader is None:
                    self.paddleocr_reader = PaddleOCR(use_textline_orientation=True, lang='ch')  # 'ch' includes simplified + English
                results = self.paddleocr_reader.predict(np_img)
                # text_lines = [line[1][0] for line in results[0]]
                # text = " ".join(text_lines)
                result = results[0]
                text_lines = result["rec_texts"]
                text = " ".join(text_lines)

                print(f"[DEBUG] PaddleOCR raw results: {text}")

            else:
                raise ValueError("Unsupported OCR tool")

            end_time = time.time()
            print(f"[INFO] OCR with {ocr_tool} took {end_time - start_time:.2f}s")
            if self.on_ocr_result:
                self.on_ocr_result(text)

        except Exception as e:
            print(f"[ERROR] OCR failed: {e}")
            if self.on_ocr_result:
                self.on_ocr_result("Erreur lors de l'OCR")

            if self.on_ocr_result:
                self.on_ocr_result(text)  # Envoi du texte OCR au callback
        
        except Exception as e:
            print(f"Erreur lors de l'OCR : {e}")
            if self.on_ocr_result:
                self.on_ocr_result("Erreur lors de l'OCR")


    def capture_loop(self):
        while self.capture_continuous:
            time.sleep(self.capture_interval)
            if self.selected_bbox:
                self.process_ocr_on_selected_area(self.selected_bbox)


    def start_capture_thread(self):
        if not self.capture_thread or not self.capture_thread.is_alive():
            self.capture_thread = threading.Thread(target=self.capture_loop, daemon=True)
            self.capture_thread.start()

    def stop_capture_thread(self):
        self.capture_continuous = False
        # Do NOT join here; just let the thread finish by itself



# Test local
if __name__ == "__main__":
    def fake_bbox(bbox):
        print("BBox sélectionnée :", bbox)

    def fake_toggle(val):
        print("Capture continue :", val)

    def fake_freq(val):
        print("Fréquence mise à jour :", val)

    def display_ocr_result(text):
        print("OCR Result:", text)

    root = tk.Tk()
    root.title("Test UI - Controls")

    ControlsFrame(root, on_area_selected=fake_bbox, on_toggle_capture=fake_toggle, on_frequency_change=fake_freq, on_ocr_result=display_ocr_result)

    root.mainloop()