import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import tensorflow as tf

class CameraPreview:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Camera Preview")

        self.vid = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.capture_button = tk.Button(self.window, text="Capture Photo", command=self.capture_image)
        self.capture_button.pack()

        self.update_preview()

    def update_preview(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo
        self.window.after(10, self.update_preview)

    def capture_image(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("camera_capture.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.master.image_captured("camera_capture.jpg")

    def close_preview(self):
        self.vid.release()
        self.window.destroy()

class ImageCaptureApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.model = None
        self.camera_preview = None

        self.canvas = tk.Canvas(window, width=400, height=400)
        self.canvas.pack()

        self.prediction_label = tk.Label(window, text="", font=("Helvetica", 14))
        self.prediction_label.pack()

        self.upload_button = tk.Button(window, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.accuracy_label = tk.Label(window, text="", font=("Helvetica", 12))
        self.accuracy_label.pack()

        self.load_model()

        self.image_path = None

    def load_model(self):
        # Load your model here
        # For example:
        self.model = tf.keras.models.load_model("best_model_2.h5")
        pass

    def show_camera_preview(self):
        if not self.camera_preview:
            self.camera_preview = CameraPreview(self.window)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.display_image_with_predictions()

    def image_captured(self, image_path):
        self.image_path = image_path
        self.display_image_with_predictions()
        self.camera_preview.close_preview()
        self.camera_preview = None

    def display_image_with_predictions(self):
        if self.model and self.image_path:
            image = cv2.imread(self.image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            processed_image = self.preprocess_image(image)
            predictions = self.model.predict(processed_image)
            result, accuracy = self.process_predictions(image.copy(), predictions)
            self.display_image(image)
            self.prediction_label.config(text=result)
            self.accuracy_label.config(text=accuracy)
        else:
            messagebox.showerror("Error", "Model or image not loaded")

    def preprocess_image(self, image):
        processed_image = cv2.resize(image, (224, 224))
        processed_image = np.expand_dims(processed_image, axis=0)
        processed_image = processed_image / 255.0
        return processed_image

    def process_predictions(self, image, predictions):
        class_index = np.argmax(predictions[0])
        classes = ['Healthy','Powdery Mildew','Cedar-Apple Rust']
        accuracy_percentage = predictions[0][class_index] * 100
        if accuracy_percentage > 95:
            result = f"Prediction: {classes[class_index]}"
            accuracy = f"Accuracy: {accuracy_percentage:.2f}%"
        else:
            result = "N/A"
            accuracy = "N/A"
        return result, accuracy

    def display_image(self, image):
        image = cv2.resize(image, (400, 400))
        image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.canvas.image = image

def main():
    root = tk.Tk()
    root.geometry("500x600")
    root.title("Image Recognition App")
    ImageCaptureApp(root, "Image Recognition")
    root.mainloop()

if __name__ == "__main__":
    main()
