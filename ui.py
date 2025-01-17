import tkinter as tk
from tkinter import messagebox
from translations import translations

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HAMAUTO")
        self.geometry("400x750")

        self.icon_path = "appIcon.png"
        self.set_icon(self.icon_path)

        self.is_sending = False  # Флаг для контроля отправки запросов
        self.language = "ru"  # Язык по умолчанию
        self.translations = translations
        self.create_widgets()

    def set_icon(self, icon_path):
        # Метод для установки иконки приложения
        try:
            self.iconphoto(False, tk.PhotoImage(file=icon_path))
        except Exception as e:
            print(f"Не удалось установить иконку: {e}")

    def create_widgets(self):
        # Language Selection
        self.language_frame = tk.Frame(self)
        self.language_frame.pack(pady=5)

        self.russian_button = tk.Button(self.language_frame, text="Русский", command=lambda: self.set_language("ru"))
        self.russian_button.pack(side=tk.LEFT, padx=5)

        self.english_button = tk.Button(self.language_frame, text="English", command=lambda: self.set_language("en"))
        self.english_button.pack(side=tk.LEFT, padx=5)

        # Bearer token
        self.token_label = tk.Label(self, text="Bearer token:")
        self.token_label.pack(pady=5)
        self.token_entry = tk.Entry(self, width=50)
        self.token_entry.pack(pady=5)
        
        # Count
        self.count_label = tk.Label(self, text="Количество кликов:")
        self.count_label.pack(pady=5)
        self.count_entry = tk.Entry(self, width=50)
        self.count_entry.pack(pady=5)
        
        # Available Taps
        self.taps_label = tk.Label(self, text="Доступные клики:")
        self.taps_label.pack(pady=5)
        self.available_taps_entry = tk.Entry(self, width=50)
        self.available_taps_entry.pack(pady=5)
        
        # Interval
        self.interval_label = tk.Label(self, text="Интервал в минутах:")
        self.interval_label.pack(pady=5)
        self.interval_entry = tk.Entry(self, width=50)
        self.interval_entry.pack(pady=5)
        
        # Start Button
        self.start_button = tk.Button(self, text="Начать отправку запросов", command=self.start_sending)
        self.start_button.pack(pady=20)
        
        # Cancel Button
        self.cancel_button = tk.Button(self, text="Отменить отправку запросов", command=self.cancel_sending)
        self.cancel_button.pack(pady=5)
        
        # Countdown Label
        self.countdown_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.countdown_label.pack(pady=10)
        
        # Log Frame
        self.log_frame = tk.Frame(self)
        self.log_frame.pack(pady=20)
        self.log_label = tk.Label(self.log_frame, text="Лог отправки запросов:", font=("Helvetica", 12))
        self.log_label.pack()
        self.log_text = tk.Text(self.log_frame, height=10, width=50)
        self.log_text.pack()

        # Clear Logs Button
        self.clear_logs_button = tk.Button(self.log_frame, text="Очистить логи", command=self.clear_logs)
        self.clear_logs_button.pack(pady=10)

    def clear_logs(self):
        self.log_text.delete('1.0', tk.END)

    def set_language(self, lang):
        self.language = lang
        if lang == "ru":
            self.update_labels("Bearer token:", "Количество кликов:", "Доступные клики:", "Интервал в минутах:", "Начать отправку запросов", "Отменить отправку запросов", "Лог отправки запросов:", "Очистить логи")
        elif lang == "en":
            self.update_labels("Bearer token:", "Count:", "Available Taps:", "Interval in minutes:", "Start Sending Requests", "Cancel Sending Requests", "Request Sending Log:", "Clear Logs")
        
    def get_translation(self, key, **kwargs):
        return self.translations[self.language][key].format(**kwargs)
    
    def update_labels(self, token_text, count_text, taps_text, interval_text, start_button_text, cancel_button_text, log_label_text, clear_logs_text):
        if hasattr(self, 'token_label'):
            self.token_label.config(text=token_text)
        if hasattr(self, 'count_label'):
            self.count_label.config(text=count_text)
        if hasattr(self, 'taps_label'):
            self.taps_label.config(text=taps_text)
        if hasattr(self, 'interval_label'):
            self.interval_label.config(text=interval_text)
        if hasattr(self, 'start_button'):
            self.start_button.config(text=start_button_text)
        if hasattr(self, 'cancel_button'):
            self.cancel_button.config(text=cancel_button_text)
        if hasattr(self, 'log_label'):
            self.log_label.config(text=log_label_text)
        if hasattr(self, 'clear_logs_button'):
            self.clear_logs_button.config(text=clear_logs_text)
        
    def start_sending(self):
        try:
            self.is_sending = True
            token = self.token_entry.get()
            count = int(self.count_entry.get())
            available_taps = int(self.available_taps_entry.get())
            interval = int(self.interval_entry.get())
            
            url = "https://api.hamsterkombatgame.io/clicker/tap"
            
            self.token_entry.config(state='disabled')
            self.count_entry.config(state='disabled')
            self.available_taps_entry.config(state='disabled')
            self.interval_entry.config(state='disabled')
            self.start_button.config(state='disabled')
            
            self.send_requests(token, count, available_taps, interval, url)
        
        except ValueError:
            messagebox.showerror(self.get_translation("error"), self.get_translation("invalid_values"))
    
    def cancel_sending(self):
        self.is_sending = False
        self.reset_ui()

    def reset_ui(self):
        self.token_entry.config(state='normal')
        self.count_entry.config(state='normal')
        self.available_taps_entry.config(state='normal')
        self.interval_entry.config(state='normal')
        self.start_button.config(state='normal')
        self.countdown_label.config(text="")
        self.log_text.insert(tk.END, self.get_translation("cancel_sending"))
        self.log_text.see(tk.END)