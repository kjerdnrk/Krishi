import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("best.pt")

# Target classes
trigger_classes = {
    "Healthy", "Leaf Curl", "Septoria Leaf Spot", "Verticulum Wilt", "Leaf Blight",
    "Healthy Maize", "Leaf Blight Maize", "Leaf Spot", "Streak Virus", "Grasshopper", "Fall Armyworm"
}

# Bright & aesthetic farming colors
BG_MAIN = "#f1f1f1"       # very light grey
CARD_BG = "#ffffff"       
HEADER_BG = "#43aa8b"     
FOOTER_BG = "#2d6a4f"     
ACCENT_GREEN = "#52b788"  
ACCENT_YELLOW = "#ffd60a" 
ACCENT_RED = "#e63946"    
TEXT_DARK = "#1b4332"     
TEXT_MUTED = "#555555"

class ModernButton(tk.Button):
    def __init__(self, parent, **kwargs):
        self.hover_bg = kwargs.pop('hover_bg', "#40916c")
        default_config = {
            'font': ('Segoe UI', 12, 'bold'),
            'relief': 'flat',
            'bd': 0,
            'cursor': 'hand2',
            'padx': 18,
            'pady': 10
        }
        default_config.update(kwargs)
        super().__init__(parent, **default_config)
        self.default_bg = default_config.get('bg', ACCENT_GREEN)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    def _on_enter(self, event):
        self.config(bg=self.hover_bg)
    def _on_leave(self, event):
        self.config(bg=self.default_bg)

class StatusCard(tk.Frame):
    def __init__(self, parent, title, icon="", bg_color=CARD_BG):
        super().__init__(parent, bg=bg_color, relief='ridge', bd=2)

        title_label = tk.Label(
            self, text=f"{icon} {title}",
            font=('Segoe UI', 13, 'bold'),
            fg=ACCENT_GREEN, bg=bg_color, pady=6
        )
        title_label.pack(fill="x", padx=12, pady=(8, 0))

        self.value_label = tk.Label(
            self, font=('Segoe UI', 14, 'bold'),
            bg=bg_color, fg=TEXT_DARK, pady=10
        )
        self.value_label.pack(fill="x", padx=12, pady=(0, 12))

    def update_status(self, text, color=TEXT_DARK):
        self.value_label.config(text=text, fg=color)

class KrishiRakshakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 Krishi Rakshak - AI Pesticide Sprayer")
        self.root.state("zoomed")   
        self.root.configure(bg=BG_MAIN)

        self.root.grid_rowconfigure(1, weight=1)
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)

        self.create_header()
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()
        self.create_controls()
        self.create_footer()

        self.cap = None
        self.running = False

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=HEADER_BG, height=90)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        header_frame.grid_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🌱 Krishi Rakshak - AI Pesticide Sprayer",
            font=("Segoe UI", 30, "bold"),
            fg="white", bg=HEADER_BG
        )
        title_label.pack(expand=True, pady=(12, 2))

        subtitle_label = tk.Label(
            header_frame,
            text="AI-Powered Real-time Plant Disease Detection & Smart Spraying",
            font=("Segoe UI", 13),
            fg="#e6f2e9", bg=HEADER_BG
        )
        subtitle_label.pack()

    def create_left_panel(self):
        left_frame = tk.Frame(self.root, bg=BG_MAIN)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.detection_card = StatusCard(left_frame, "Current Detection", "🔍")
        self.detection_card.pack(fill="both", expand=True, pady=(0, 12))
        self.detection_card.update_status("Waiting for input...", TEXT_MUTED)

        self.disease_info_card = StatusCard(left_frame, "Disease Information", "🦠")
        self.disease_info_card.pack(fill="both", expand=True)
        self.disease_info_card.update_status("No Disease detected", TEXT_MUTED)

    def create_center_panel(self):
        video_frame = tk.Frame(self.root, bg=CARD_BG, relief='solid', bd=3)
        video_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        video_frame.grid_rowconfigure(1, weight=1)
        video_frame.grid_columnconfigure(0, weight=1)

        video_header = tk.Label(
            video_frame,
            text="📹 Live Camera Feed",
            font=("Segoe UI", 18, "bold"),
            fg=ACCENT_GREEN, bg=CARD_BG
        )
        video_header.grid(row=0, column=0, pady=(10, 8))

        self.video_label = tk.Label(
            video_frame,
            bg=BG_MAIN,
            text="📷\n\nCamera feed will appear here\n\nClick 'Start Detection' to begin",
            font=("Segoe UI", 14),
            fg=TEXT_MUTED,
            justify="center"
        )
        self.video_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 12))

    def create_right_panel(self):
        right_frame = tk.Frame(self.root, bg=BG_MAIN)
        right_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.system_status_card = StatusCard(right_frame, "System Status", "🔧")
        self.system_status_card.pack(fill="both", expand=True, pady=(0, 12))
        self.system_status_card.update_status("System Ready", ACCENT_GREEN)

        stats_card = StatusCard(right_frame, "Supported Diseases", "📊")
        stats_card.pack(fill="both", expand=True, pady=(0, 12))

        diseases_text = (
            "• Healthy\n• Leaf Curl\n• Septoria Leaf Spot\n• Verticulum Wilt\n"
            "• Leaf Blight\n• Healthy Maize\n• Leaf Blight Maize\n"
            "• Leaf Spot\n• Streak Virus\n• Grasshopper\n• Fall Armyworm"
        )
        stats_card.update_status(diseases_text, TEXT_DARK)

        self.severity_card = tk.Frame(right_frame, bg=CARD_BG, relief='ridge', bd=2)
        self.severity_card.pack(fill="both", expand=True)

        severity_label = tk.Label(
            self.severity_card, text="Severity Level 📉",
            font=('Segoe UI', 13, 'bold'),
            fg=ACCENT_GREEN, bg=CARD_BG, pady=6
        )
        severity_label.pack(fill="x", padx=12, pady=(8, 0))

        self.severity_bar = ttk.Progressbar(
            self.severity_card, orient="horizontal",
            mode="determinate", length=200
        )
        self.severity_bar.pack(pady=15, padx=20, fill="x")

        self.severity_value = tk.Label(
            self.severity_card, text="0%", font=('Segoe UI', 12, 'bold'),
            bg=CARD_BG, fg=TEXT_DARK
        )
        self.severity_value.pack(pady=(0, 12))

    def create_controls(self):
        control_frame = tk.Frame(self.root, bg=BG_MAIN, height=70)
        control_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        control_frame.grid_propagate(False)

        button_container = tk.Frame(control_frame, bg=BG_MAIN)
        button_container.pack(expand=True)

        self.start_button = ModernButton(
            button_container,
            text="▶  Start Detection",
            command=self.start_detection,
            bg=ACCENT_GREEN,
            hover_bg="#2d6a4f",
            fg="white",
            width=20
        )
        self.start_button.pack(side="left", padx=20)

        self.stop_button = ModernButton(
            button_container,
            text="⏹  Stop Detection",
            command=self.stop_detection,
            bg=ACCENT_RED,
            hover_bg="#9d0208",
            fg="white",
            width=20
        )
        self.stop_button.pack(side="left")

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg=FOOTER_BG, height=45)
        footer_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        footer_frame.grid_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text="🤖 Powered by YOLO AI | Real-time Plant Disease Recognition | Version 1.0",
            font=("Segoe UI", 10),
            fg="white", bg=FOOTER_BG
        )
        footer_label.pack(expand=True)

    def start_detection(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Could not access camera.")
            self.running = False
            return

        self.system_status_card.update_status("🔴 Detection Active", ACCENT_RED)
        self.detection_card.update_status("Scanning for Disease...", ACCENT_YELLOW)
        self.update_frame()

    def stop_detection(self):
        self.running = False
        if self.cap:
            self.cap.release()

        self.video_label.config(
            image='', text="📷\n\nCamera feed stopped\n\nClick 'Start Detection' to begin",
            fg=TEXT_MUTED
        )

        self.system_status_card.update_status("System Ready", ACCENT_GREEN)
        self.detection_card.update_status("Detection Stopped", ACCENT_RED)
        self.disease_info_card.update_status("No Disease detected", TEXT_MUTED)

        self.severity_bar['value'] = 0
        self.severity_value.config(text="0%")

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.root.after(10, self.update_frame)
            return

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(img, verbose=False)

        probs = results[0].probs.data.tolist()
        names = results[0].names

        pred_class = results[0].probs.top1
        confidence = probs[pred_class] * 100
        self.severity_bar['value'] = confidence
        self.severity_value.config(text=f"{confidence:.2f}%")

        # Overlay only detected classes (>0 probability)
        y0, dy = 20, 18
        j = 0
        for i, p in enumerate(probs):
            if p > 0:
                text_line = f"{names[i]} {p:.2f}"
                y = y0 + j * dy
                cv2.putText(frame, text_line, (5, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (34, 139, 34), 1)
                j += 1

        class_name = names[pred_class]
        if class_name in trigger_classes:
            if class_name == "Healthy Maize":
                self.detection_card.update_status(f"✅ {class_name} Detected", ACCENT_GREEN)
                self.disease_info_card.update_status(f"{class_name}", ACCENT_GREEN)
            else:
                self.detection_card.update_status(f"⚠ {class_name} Detected", ACCENT_YELLOW)
                self.disease_info_card.update_status(f"{class_name} - Motor Pump Started \n Spraying for 3 Seconds", ACCENT_GREEN)
        else:
            self.detection_card.update_status("🔍 Scanning...", ACCENT_YELLOW)
            self.disease_info_card.update_status("No recognized Disease", TEXT_MUTED)

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (720, 500))
        img_pil = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.video_label.imgtk = img_pil
        self.video_label.configure(image=img_pil, text="")

        self.root.after(10, self.update_frame)


if __name__ == "__main__":
    root = tk.Tk()
    app = KrishiRakshakApp(root)
    root.mainloop()
