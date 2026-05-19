from PIL import ImageGrab
import tkinter as tk
import ctypes

# Function to get the DPI scaling factor
def get_dpi_scaling_factor():
    # Call GetScaleFactorForDevice with device index 0 (primary monitor)
    scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
    return scale_factor

def select_screen_area(callback=None):
    class Selector:
        def __init__(self):
            self.start_x = None
            self.start_y = None
            self.rect = None
            self.dpi_scaling_factor = get_dpi_scaling_factor()  # Get the DPI scaling factor

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
            # Capture the starting point in the canvas coordinates
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

        def on_move_press(self, event):
            # Capture the current point while moving the mouse and update rectangle
            cur_x = self.canvas.canvasx(event.x)
            cur_y = self.canvas.canvasy(event.y)
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

        def on_button_release(self, event):
            # Get the final coordinates after mouse release
            end_x = self.canvas.canvasx(event.x)
            end_y = self.canvas.canvasy(event.y)
            self.root.destroy()

            # Adjust coordinates based on the DPI scaling factor for external use
            x1 = min(self.start_x, end_x)
            y1 = min(self.start_y, end_y)
            x2 = max(self.start_x, end_x)
            y2 = max(self.start_y, end_y)

            # Apply the DPI scaling factor when passing the coordinates to the callback
            scaled_bbox = (int(x1 * self.dpi_scaling_factor), int(y1 * self.dpi_scaling_factor),
                           int(x2 * self.dpi_scaling_factor), int(y2 * self.dpi_scaling_factor))

            if callback:
                callback(scaled_bbox)

    Selector()

# Test local
if __name__ == "__main__":
    def fake_bbox(bbox):
        print("BBox sélectionnée :", bbox)

    select_screen_area(fake_bbox)
