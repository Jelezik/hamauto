import requests
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HAMAUTO")
        self.geometry("400x700")

        self.is_sending = False  # Флаг для контроля отправки запросов
        
        self.create_widgets()
        
    def create_widgets(self):
        # Bearer token
        tk.Label(self, text="Bearer token:").pack(pady=5)
        self.token_entry = tk.Entry(self, width=50)
        self.token_entry.pack(pady=5)
        
        # Count
        tk.Label(self, text="Count:").pack(pady=5)
        self.count_entry = tk.Entry(self, width=50)
        self.count_entry.pack(pady=5)
        
        # Available Taps
        tk.Label(self, text="Available Taps:").pack(pady=5)
        self.available_taps_entry = tk.Entry(self, width=50)
        self.available_taps_entry.pack(pady=5)
        
        # Interval
        tk.Label(self, text="Интервал в минутах:").pack(pady=5)
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
        
    def send_post_request(self, url, token, data):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=data)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code == 200:
            self.log_text.insert(tk.END, f"{current_time} - Запрос успешно отправлен!\n")
        else:
            self.log_text.insert(tk.END, f"{current_time} - Произошла ошибка: {response.status_code}\n")
            self.log_text.insert(tk.END, f"{response.text}\n")
        self.log_text.see(tk.END)
    
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
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения.")
    
    def send_requests(self, token, count, available_taps, interval, url):
        if not self.is_sending:
            return
        
        timestamp = int(time.mktime(datetime.now().timetuple()))
        data = {
            "count": count,
            "availableTaps": available_taps,
            "timestamp": timestamp
        }
        
        self.send_post_request(url, token, data)
        
        for remaining in range(interval * 60, 0, -1):
            if not self.is_sending:
                self.reset_ui()
                return
            mins, secs = divmod(remaining, 60)
            self.countdown_label.config(text=f"Следующий запрос через: {mins:02d}:{secs:02d}")
            self.update()
            time.sleep(1)
        
        self.send_requests(token, count, available_taps, interval, url)
            
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
        self.log_text.insert(tk.END, "Отправка запросов отменена.\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    app = Application()
    app.mainloop()