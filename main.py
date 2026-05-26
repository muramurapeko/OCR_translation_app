import tkinter as tk
import time
from ui.controls import ControlsFrame
from ui.ocr_display import OCRDisplayFrame
from ui.translation_display import TranslationDisplayFrame
from core.translator3 import translate_text

class OCRTranslationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OCR + Traduction Tool")
        self.geometry("800x600")

        # Composants UI
        self.ocr_display = OCRDisplayFrame(self)
        self.translation_display = TranslationDisplayFrame(self)

        self.controls = ControlsFrame(
            self,
            on_area_selected=self.on_area_selected,
            on_toggle_capture=self.on_toggle_capture,
            on_frequency_change=self.on_frequency_change,
            on_ocr_result=self.update_ocr_text
        )

        # Texte OCR temporaire
        self.last_ocr_text = ""

    def on_area_selected(self, bbox):
        print("[INFO] Zone sélectionnée :", bbox)

    def on_toggle_capture(self, is_active):
        print("[INFO] Capture continue :", is_active)

    def on_frequency_change(self, interval):
        print("[INFO] Fréquence de capture :", interval)

    def update_ocr_text(self, text):
        self.last_ocr_text = text.strip()
        self.ocr_display.update_text(self.last_ocr_text)
        self.update_translation()

    def update_translation(self):
        if self.last_ocr_text:
            # Time the translation process
            start_time = time.time()
            translated = translate_text(self.last_ocr_text, target_language="chinese")
            end_time = time.time()
            translation_duration = end_time - start_time

            print(f"[INFO] Translation took {translation_duration:.4f} seconds")

            self.translation_display.update_translation(translated)


if __name__ == "__main__":
    app = OCRTranslationApp()
    app.mainloop()
