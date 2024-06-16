import tkinter as tk
from tkinter import messagebox
from tkinter import *
from ttkbootstrap import ttk, Style
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
from exercise import *
import os
import random
import time
model = YOLO("best.pt")

# Set the default time for work and break intervals
WORK_TIME = 1 * 60
SHORT_BREAK_TIME = 1 * 60
LONG_BREAK_TIME = 15 * 60

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")  # Adjust size as needed
        self.root.title("Pomodoro Timer")
        self.style = Style(theme="simplex")
        self.style.theme_use()

        self.timer_label = tk.Label(self.root, text="", font=("TkDefaultFont", 40))
        self.timer_label.pack(pady=20)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(self.control_frame, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack()

        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack()

        self.work_time, self.break_time = WORK_TIME, SHORT_BREAK_TIME
        self.is_work_time, self.pomodoros_completed, self.is_runnin, self.drowsy_counter = True, 0, False, 0

        self.root.mainloop()

    def start_timer(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_running = True
        self.update_timer()
        self.run_model()

    def run_model(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            self.show_frame(frame, cap)
        else:
            messagebox.showerror("Error", "Failed to capture video.")
            self.stop_timer()
            return

    def show_frame(self, frame, cap):
        if self.is_running:
            results = model(frame)

            for result in results:
                boxes = result.boxes  # Boxes object for bounding box outputs
                for bbox in boxes.xyxy:
                    # Extracting the coordinates of the top-left and bottom-right corners
                    xmin, ymin, xmax, ymax = bbox
                    # Drawing the bounding box on the frame
                    cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                if len(boxes.xyxy) > 0:
                    if result.names[int(boxes.cls.cpu().numpy()[0])] == 'drowsy':
                        self.drowsy_counter += 1
                        cv2.putText(frame, "", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                        self.stop_timer()
                        # messagebox.showerror("Drowsy detected", "You are drowsy. Take a break!")
                        self.show_message_box("You are drowsy", "meme\\wake_up")

                        answer = messagebox.askyesno("","Would you like to exercise a little to be more awake?")
                        if answer:
                            camera()
                            # messagebox.showerror("","Let's continue studying")
                            self.show_message_box("Let's continue study", "meme/continue")
                        else:
                            # messagebox.showerror("","Let's continue studying")
                            self.show_message_box("Let's continue study", "meme/continue")
                        break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.camera_label.imgtk = imgtk
            self.camera_label.config(image=imgtk)

            if self.is_running and self.is_work_time:
                self.root.after(10, self.show_frame, cap.read()[1], cap)

    def stop_timer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_running = False

    def update_timer(self):
        if self.is_running:
            
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    if self.drowsy_counter >=5: 
                        answer = messagebox.askyesno("","You have many time not focus on study. Do you want a long break to rest your mind")
                        if answer:
                            self.break_time = LONG_BREAK_TIME 
                        else:
                            self.break_time = SHORT_BREAK_TIME
                    else:        
                        self.break_time = LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else SHORT_BREAK_TIME
                        if self.pomodoros_completed % 4 ==0:
                            self.show_message_box("Good job, now take a long break and rest your mind", "meme/congratulations")
                        else:
                            self.show_message_box(f"Take a short break and strech your legs! In this learning progress you have {self.drowsy_counter} times distraction", "meme/relax")
                        # messagebox.showinfo("Great job!" if self.pomodoros_completed % 4 == 0
                        #                     else "Good job!", "Take a long break and rest your mind."
                        #                     if self.pomodoros_completed % 4 == 0
                        #                     else f"Take a short break and strech your legs! In this learning progress you have {self.drowsy_counter} times distraction")
                    
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.is_work_time, self.work_time,self.drowsy_counter = True, WORK_TIME, 0
                    # messagebox.showinfo("Work Time", "Get back to work!")
                    self.show_message_box("Get back to work", "")
            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.root.after(1000, self.update_timer)
    def show_message_box(self,title,src_imgs):
        messagebox = tk.Toplevel(self.root)
        messagebox.title(title)
        files = os.listdir(src_imgs)

        image_files = [file for file in files if file.endswith((".jpg", ".jpeg", ".png"))]
        # Select a random image file
        random_image = random.choice(image_files)
        
        # Construct the full path to the random image
        random_image_path = os.path.join(src_imgs, random_image)
        # Load image
        image = Image.open(random_image_path)
        photo = ImageTk.PhotoImage(image)
        
        # Display image
        label = tk.Label(messagebox, image=photo)
        label.image = photo
        label.pack()
        
        # Add message text
        message = tk.Label(messagebox, text="This is your message.")
        message.pack()
    # PomodoroTimer()
