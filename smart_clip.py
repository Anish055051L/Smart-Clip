import os
import sys
import threading
import time
import tkinter as tk
from PIL import Image
import customtkinter as ctk
import pyperclip
import keyboard

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SmartClipApp:
    def __init__(self):
        self.history = []
        self.last_clipboard = ""
        self.window_open = False
        self.win = None
        self.lock = threading.Lock()
        
        self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.monitor_thread.start()
        
        try:
            keyboard.add_hotkey('ctrl+shift+x', self.toggle_hud)
        except Exception:
            pass

    def classify_snippet(self, text):
        t_lower = text.strip().lower()
        
        if t_lower.startswith("http://") or t_lower.startswith("https://") or t_lower.startswith("www."):
            return "Link", "#0ea5e9"
            
        if any(kw in text for kw in ["def ", "import ", "print(", "class ", "self.", "lambda "]) and ("\n" in text or ":" in text):
            return "Python", "#8b5cf6"
            
        if any(kw in t_lower for kw in ["#include", "std::", "cout", "cin", "printf(", "scanf(", "int main(", "vector<", "nullptr", "iostream"]) or (text.endswith(";") and "int " in t_lower):
            return "C++ / C", "#f97316"
            
        if any(kw in text for kw in ["public class", "private void", "system.out.println", "public static void main", "import java."]):
            return "Java", "#ea580c"
            
        if any(kw in text for kw in ["fn main(", "let mut ", "println!", "pub fn ", "String::from", "match "]) and "->" in text:
            return "Rust", "#b45309"
            
        if any(kw in text for kw in ["console.log", "const ", "let ", "document.getElementById", "=>", "function(", "import React"]) or ("async function" in text):
            return "JavaScript", "#eab308"
            
        if t_lower.startswith("<!doctype html") or ("<html" in t_lower and "</html>" in t_lower) or ("<div" in t_lower and "</div>" in t_lower):
            return "HTML", "#db2777"
            
        if "{" in text and "}" in text and any(prop in t_lower for prop in ["color:", "background:", "margin:", "padding:", "font-size:", "display:"]):
            return "CSS", "#06b6d4"
            
        if any(kw in t_lower for kw in ["select ", "insert into", "update ", "delete from", "drop table", "create table"]):
            return "SQL", "#f59e0b"
            
        if t_lower.startswith("pip install") or t_lower.startswith("git ") or t_lower.startswith("sudo ") or t_lower.startswith("apt ") or "npm i " in t_lower or t_lower.startswith("cd "):
            return "Bash Code", "#10b981"
            
        if any(err in t_lower for err in ["error:", "exception:", "traceback", "warning:", "[info]", "[status]"]):
            return "Log", "#ef4444"
            
        if (text.strip().startswith("{") and text.strip().endswith("}")) or (text.strip().startswith("[") and text.strip().endswith("]")):
            return "JSON", "#6366f1"
            
        return "Plain Text", "#3b82f6"

    def get_title(self, text):
        clean_text = text.strip().replace("\n", " ")
        words = clean_text.split()
        if len(words) > 2:
            return f"{words[0]} {words[1]}..."
        elif len(words) > 0:
            return clean_text
        return "Empty Clip"

    def monitor_clipboard(self):
        while True:
            try:
                current = pyperclip.paste()
                if current and current != self.last_clipboard:
                    self.last_clipboard = current
                    if current in self.history:
                        self.history.remove(current)
                    self.history.insert(0, current)
                    if len(self.history) > 50:
                        self.history.pop()
            except Exception:
                pass
            time.sleep(0.4)

    def toggle_hud(self):
        with self.lock:
            if self.window_open and self.win is not None:
                try:
                    self.win.after(0, self.win.destroy)
                except Exception:
                    pass
                self.window_open = False
                self.win = None
            else:
                if not self.window_open:
                    self.window_open = True
                    threading.Thread(target=self.show_hud_window, daemon=True).start()

    def show_hud_window(self):
        try:
            win = ctk.CTk()
            with self.lock:
                self.win = win
            
            win.title("Smart Clip")
            win.geometry("380x480")
            win.configure(fg_color="#0b0f19")
            win.attributes("-topmost", True)

            icon_path = "smart_clip_icon.png"
            if os.path.exists(icon_path):
                try:
                    win.iconphoto(False, tk.PhotoImage(file=icon_path))
                except Exception:
                    pass

            header_frame = ctk.CTkFrame(win, fg_color="transparent")
            header_frame.pack(fill=tk.X, padx=14, pady=(12, 4))

            title_label = ctk.CTkLabel(header_frame, text="Smart Clip", font=("Segoe UI", 18, "bold"), text_color="#38bdf8")
            title_label.pack(side=tk.LEFT)

            search_var = ctk.StringVar(master=win)

            def manual_refresh():
                search_var.set("")
                populate_cards()

            refresh_btn = ctk.CTkButton(
                header_frame, 
                text="🔄 Refresh", 
                command=manual_refresh,
                width=75,
                height=26,
                corner_radius=8,
                fg_color="#1e293b",
                hover_color="#334155",
                text_color="#38bdf8",
                font=("Segoe UI", 11, "bold")
            )
            refresh_btn.pack(side=tk.RIGHT)

            search_entry = ctk.CTkEntry(
                win, 
                textvariable=search_var, 
                placeholder_text="🔍 Search clips...", 
                height=36, 
                corner_radius=10,
                fg_color="#1e293b",
                border_color="#334155",
                text_color="#f8fafc",
                placeholder_text_color="#64748b",
                font=("Segoe UI", 11)
            )
            search_entry.pack(fill=tk.X, padx=14, pady=8)
            search_entry.focus()

            scroll_frame = ctk.CTkScrollableFrame(
                win, 
                fg_color="transparent", 
                corner_radius=10,
                scrollbar_button_color="#334155",
                scrollbar_button_hover_color="#475569"
            )
            scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

            def copy_and_close(text):
                pyperclip.copy(text)
                with self.lock:
                    try:
                        win.destroy()
                    except Exception:
                        pass
                    self.window_open = False
                    self.win = None

            def populate_cards(query=""):
                for widget in scroll_frame.winfo_children():
                    widget.destroy()

                filtered_items = [
                    item for item in self.history 
                    if not query or query.lower() in item.lower()
                ]

                if not filtered_items:
                    empty_lbl = ctk.CTkLabel(scroll_frame, text="No clips found.", font=("Segoe UI", 12), text_color="#64748b")
                    empty_lbl.pack(pady=30)
                    return

                for idx, item in enumerate(filtered_items):
                    ctype, badge_color = self.classify_snippet(item)
                    card_title = self.get_title(item)

                    card = ctk.CTkFrame(
                        scroll_frame, 
                        fg_color="#111827", 
                        corner_radius=10,
                        border_width=1,
                        border_color="#1f2937"
                    )
                    card.pack(fill=tk.X, padx=4, pady=5)

                    card_header = ctk.CTkFrame(card, fg_color="transparent", height=24)
                    card_header.pack(fill=tk.X, padx=10, pady=(6, 2))

                    title_lbl = ctk.CTkLabel(card_header, text=card_title, font=("Segoe UI", 12, "bold"), text_color="#f3f4f6")
                    title_lbl.pack(side=tk.LEFT)

                    badge_lbl = ctk.CTkLabel(
                        card_header, 
                        text=f" {ctype} ", 
                        font=("Segoe UI", 9, "bold"), 
                        text_color=badge_color,
                        fg_color="#1f2937",
                        corner_radius=5
                    )
                    badge_lbl.pack(side=tk.RIGHT)

                    preview_text = item.strip()
                    if len(preview_text) > 120:
                        preview_text = preview_text[:120] + "..."

                    body_lbl = ctk.CTkLabel(
                        card, 
                        text=preview_text, 
                        font=("Consolas", 10), 
                        text_color="#9ca3af",
                        justify=tk.LEFT,
                        anchor="w"
                    )
                    body_lbl.pack(fill=tk.X, padx=10, pady=(0, 8))

                    def make_click_handler(txt=item):
                        return lambda e: copy_and_close(txt)

                    card.bind("<Button-1>", make_click_handler())
                    title_lbl.bind("<Button-1>", make_click_handler())
                    body_lbl.bind("<Button-1>", make_click_handler())

            populate_cards()

            def on_search(*args):
                populate_cards(search_var.get())

            search_var.trace_add("write", on_search)

            def on_escape(event):
                with self.lock:
                    try:
                        win.destroy()
                    except Exception:
                        pass
                    self.window_open = False
                    self.win = None

            def quit_app():
                try:
                    win.destroy()
                except Exception:
                    pass
                os._exit(0)

            win.bind("<Escape>", on_escape)
            win.protocol("WM_DELETE_WINDOW", quit_app)

            win.mainloop()
        except Exception:
            pass
        finally:
            with self.lock:
                self.window_open = False
                self.win = None

if __name__ == "__main__":
    app = SmartClipApp()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
