import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import tensorflow as tf
import time
import serial  


def open_plant_status_window():
    global plant_status_window  # Declare plant_status_window as global variable
    plant_status_window = tk.Toplevel(root)
    plant_status_window.title("Plant Status")
    plant_status_window.geometry("800x500")

    # Initialize current state
    current_state = None

    # Create labels to display the sensor data
    title_label = tk.Label(plant_status_window, text="Smart Agri-System Monitoring and Management", font=('Times New Roman', 20, "bold"))
    title_label.pack()

    # Labels for temperature, humidity, and moisture
    temperature_label = tk.Label(plant_status_window, text="Temperature: ", font=('Times New Roman', 17))
    temperature_label.place(x=100, y=50)

    humidity_label = tk.Label(plant_status_window, text="Humidity: ", font=('Times New Roman', 17))
    humidity_label.place(x=300, y=50)

    moisture_label = tk.Label(plant_status_window, text="Moisture: ", font=('Times New Roman', 17))
    moisture_label.place(x=500, y=50)

    # Initial labels
    #moisture_sensor_label = tk.Label(plant_status_window, text="Moisture Sensor State: ", font=('Times New Roman', 15))
    #moisture_sensor_label.place(x=100, y=110)

    moisture_state1_label = tk.Label(plant_status_window)
    moisture_state1_label.place(x=100, y=110)

    moisture_state2_label = tk.Label(plant_status_window)
    moisture_state2_label.place(x=100, y=110)

    moisture_state3_label = tk.Label(plant_status_window)
    moisture_state3_label.place(x=100, y=110)

    pump1_label = tk.Label(plant_status_window)
    pump1_label.place(x=100, y=150)

    pump2_label = tk.Label(plant_status_window)
    pump2_label.place(x=100, y=150)

    pump3_label = tk.Label(plant_status_window)
    pump3_label.place(x=100, y=150)

    # Functions to change labels based on state button clicked
    def clear_labels():
        moisture_state1_label.config(text="")
        pump1_label.config(text="")
        moisture_state2_label.config(text="")
        pump2_label.config(text="")
        moisture_state3_label.config(text="")
        pump3_label.config(text="")

    def state1():
        clear_labels()
        moisture_state1_label.config(text="Moisture Sensor 1 State: ", font=('Arial', 15))
        pump1_label.config(text="Pump 1 State:", font=('Arial', 15))
        global current_state
        current_state = 1

    def state2():
        clear_labels()
        moisture_state2_label.config(text="Moisture Sensor 2 State: ", font=('Arial', 15))
        pump2_label.config(text="Pump 2 State:", font=('Arial', 15))
        global current_state
        current_state = 2

    def state3():
        clear_labels()
        moisture_state3_label.config(text="Moisture Sensor 3 State: ", font=('Arial', 15))
        pump3_label.config(text="Pump 3 State:", font=('Arial', 15))
        global current_state
        current_state = 3

    # Create state buttons
    state1_button = tk.Button(plant_status_window, text="State 1", command=state1)
    state1_button.place(x=100, y=200)

    state2_button = tk.Button(plant_status_window, text="State 2", command=state2)
    state2_button.place(x=250, y=200)

    state3_button = tk.Button(plant_status_window, text="State 3", command=state3)
    state3_button.place(x=400, y=200)

    def update_sensor_data():
    # Open the serial port to communicate with the Arduino
        ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace '/dev/ttyUSB0' with your Arduino's serial port

    # Read the sensor data from the Arduino
    sensor_data = ser.readline().decode().strip()

    # Split the received data into individual values
    temperature, humidity, moisture = sensor_data.split(',')

    # Update the labels with the new sensor data
    temperature_label.config(text="Temperature: " + temperature + "°C")
    humidity_label.config(text="Humidity: " + humidity + "%")
    moisture_label.config(text="Soil Moisture: " + moisture + "%")

    # Determine moisture state based on moisture percentage
    moisture_percentage = float(moisture)
    if 0 <= moisture_percentage <= 20:
        moisture_state1 = "No water detected!"
    elif 20 < moisture_percentage <= 50:
        moisture_state1 = "Low soil moisture detected!"
    else:
        moisture_state1 = "Soil moisture between desired states"
        moisture_state1_label.config(text="Moisture State: " + moisture_state1)

    # Close the serial port
    ser.close()

    # Schedule the function to run again after 1 second
    root.after(1000, update_sensor_data)

# Call the function to start updating the sensor data
    update_sensor_data()


def open_upload_window():
    upload_window = tk.Toplevel(root)
    upload_window.title("Upload Image")
    upload_window.geometry("500x600")
    ImageCaptureApp(upload_window, "Image Recognition")

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

    def open_upload_window(self):
        upload_window = tk.Toplevel(self.window)
        upload_window.title("Upload Image")
        upload_window.geometry("400x300")

        upload_button = tk.Button(upload_window, text="Upload Image", command=self.upload_image)
        upload_button.pack(pady=10)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.display_image_with_predictions()

    def image_captured(self, image_path):
        self.image_path = image_path
        self.display_image_with_predictions()
        if self.camera_preview:
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
        if accuracy_percentage > 80:
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
    global root
    root = tk.Tk()
    root.title("Plant Monitoring App")
    root.geometry("300x150")

    plant_status_button = tk.Button(root, text="Plant Status", command=open_plant_status_window)
    plant_status_button.pack(pady=10)

    upload_image_button = tk.Button(root, text="Upload Image for Recognition", command=open_upload_window)
    upload_image_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
        
