import sys
import traceback
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import threading
import app.backend.assistant_api as assistant_api
import llama_runner

# Resolve paths correctly for PyInstaller bundles
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# --- Configuration (placeholders only) ---
# These MUST be set in your environment or .env file before running
API_URL = os.getenv("SPINDLE_API_URL")       # e.g., "YOUR_API_ENDPOINT_HERE"
WELCOME_MESSAGE = os.getenv("SPINDLE_WELCOME", "Hi, I'm Spindle, your AI network crawling assistant.")
LOG_PATH = os.getenv("SPINDLE_LOG", "YOUR_LOG_PATH_HERE")  # e.g., "./spindle_log.txt"
ICON_PATH = os.getenv("SPINDLE_ICON", "YOUR_ICON_PATH_HERE")  # e.g., "./assets/spindlechatbot.png"

try:
    # Log startup
    with open(LOG_PATH, "w") as f:
        f.write("Spindle started launcher.py\n")

    class ChatApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("spindleAI")
            self.geometry("600x700")
            self.configure(bg="#f2f2f2")

            # Bot icon loaded from assets folder
            self.bot_icon = ImageTk.PhotoImage(
                Image.open(resource_path(ICON_PATH)).resize((40, 40))
            )

            self.create_widgets()
            self.after(500, lambda: self.add_bot_message(WELCOME_MESSAGE))

            # Start local servers in background threads
            threading.Thread(target=llama_runner.start_llama_server, daemon=True).start()
            threading.Thread(target=assistant_api.start_api, daemon=True).start()

        def create_widgets(self):
            """Create chat UI: scrollable chat area + input box"""
            self.chat_frame = tk.Frame(self, bg="#f2f2f2")
            self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.canvas = tk.Canvas(self.chat_frame, bg="#f2f2f2", highlightthickness=0)
            self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
            self.scrollable_frame = tk.Frame(self.canvas, bg="#f2f2f2")

            self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")

            # Input field + send button
            self.input_frame = tk.Frame(self, bg="#ffffff", bd=1)
            self.input_frame.pack(fill=tk.X, padx=10, pady=10)

            self.entry = tk.Entry(self.input_frame, font=("Helvetica", 14))
            self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
            self.entry.bind("<Return>", lambda event: self.on_send())

            self.send_button = tk.Button(self.input_frame, text="Send", command=self.on_send)
            self.send_button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)

        def add_user_message(self, text):
            """Show user’s message in green bubble on right"""
            msg = tk.Label(self.scrollable_frame, text=text, bg="#d1e7dd", wraplength=400, justify="right",
                           font=("Helvetica", 13), padx=10, pady=6, anchor="e")
            msg.pack(anchor="e", pady=5, padx=10)
            self.canvas.yview_moveto(1.0)

        def add_bot_message(self, text):
            """Show bot’s message with icon on left"""
            frame = tk.Frame(self.scrollable_frame, bg="#f2f2f2")
            icon = tk.Label(frame, image=self.bot_icon, bg="#f2f2f2")
            icon.pack(side="left", padx=(0, 5))
            msg = tk.Label(frame, text=text, bg="#e2e3e5", wraplength=400, justify="left",
                           font=("Helvetica", 13), padx=10, pady=6, anchor="w")
            msg.pack(side="left")
            frame.pack(anchor="w", pady=5, padx=10)
            self.canvas.yview_moveto(1.0)

        def add_typing_indicator(self):
            """Temporary 'Spindle is thinking...' label"""
            self.typing_label = tk.Label(self.scrollable_frame, text="Spindle is thinking...", bg="#f2f2f2", font=("Helvetica", 11, "italic"))
            self.typing_label.pack(anchor="w", pady=5, padx=10)
            self.canvas.yview_moveto(1.0)

        def remove_typing_indicator(self):
            if hasattr(self, 'typing_label'):
                self.typing_label.destroy()

        def on_send(self):
            """Handle send button / Enter key"""
            user_text = self.entry.get().strip()
            if not user_text:
                return
            self.entry.delete(0, tk.END)
            self.add_user_message(user_text)
            self.add_typing_indicator()
            threading.Thread(target=self.get_bot_response, args=(user_text,), daemon=True).start()

        def get_bot_response(self, user_text):
            """Call backend API and show response"""
            try:
                if not API_URL:
                    raise ValueError("SPINDLE_API_URL not set. Please configure it in your environment.")
                res = requests.post(API_URL, json={"message": user_text})
                reply = res.json().get("response", "Sorry, something went wrong.")
            except Exception as e:
                reply = f"Error: {e}"
            self.after(0, lambda: [self.remove_typing_indicator(), self.add_bot_message(reply)])

    if __name__ == "__main__":
        app = ChatApp()
        app.mainloop()

except Exception:
    # Log crash
    with open(LOG_PATH, "a") as f:
        f.write("Spindle crashed:\n")
        traceback.print_exc(file=f)
    sys.exit(1)
