import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time

class ImageCaptureApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(window, text="Take Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def close_window(self):
        self.vid.__del__()
        self.window.destroy()

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def open_camera():
    camera_window = tk.Toplevel(root)
    ImageCaptureApp(camera_window, "Image Capture")

# Create the main window
root = tk.Tk()
root.geometry("800x500")
root.title("Arduino Sensor Data")

# Create labels to display the sensor data
title_label = tk.Label(root, text="Smart Agri-System Monitoring and Management", font=('Times New Roman', 20, "bold"))
title_label.pack()

temperature_label = tk.Label(root, text="Temperature: ", font=('Times New Roman', 17))
temperature_label.place(x=100, y=50)

humidity_label = tk.Label(root, text="Humidity: ", font=('Times New Roman', 17))
humidity_label.place(x=300, y=50)

moisture_label = tk.Label(root, text="Moisture: ", font=('Times New Roman', 17))
moisture_label.place(x=500, y=50)

moisture_state1_label = tk.Label(root, text="Moisture Sensor 1 State: ", font=('Times New Roman', 15))
moisture_state1_label.place(x=100, y=110)

moisture_state2_label = tk.Label(root, text="Moisture Sensor 2 State: ", font=('Times New Roman', 15))
moisture_state2_label.place(x=100, y=180)

moisture_state3_label = tk.Label(root, text="Moisture Sensor 3 State: ", font=('Times New Roman', 15))
moisture_state3_label.place(x=100, y=250)

pump_state1_label = tk.Label(root, text="Pump 1 State:", font=('Arial', 13))
pump_state1_label.place(x=100, y=340)

pump_state2_label = tk.Label(root, text="Pump 2 State:", font=('Arial', 13))
pump_state2_label.place(x=300, y=340)

pump_state3_label = tk.Label(root, text="Pump 3 State:", font=('Arial', 13))
pump_state3_label.place(x=500, y=340)

# Create the button to open the camera
camera_button = tk.Button(root, font=('Times New Roman', 12, "bold"), text="Open Camera", command=open_camera)
camera_button.place(x=300, y=420)

"""# Function to update the sensor data
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
update_sensor_data() """

# Run the Tkinter event loop
root.mainloop()
