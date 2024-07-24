import requests
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Post Request Sender")
        self.geometry("400x400")
        
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
        
    def send_post_request(self, url, token, data):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print('Запрос успешно отправлен!')
        else:
            print(f'Произошла ошибка: {response.status_code}')
            print(response.text)
    
    def start_sending(self):
        try:
            token = self.token_entry.get()
            count = int(self.count_entry.get())
            available_taps = int(self.available_taps_entry.get())
            interval = int(self.interval_entry.get())
            
            url = "https://api.hamsterkombatgame.io/clicker/tap"
            
            while True:
                timestamp = int(time.mktime(datetime.now().timetuple()))
                data = {
                    "count": count,
                    "availableTaps": available_taps,
                    "timestamp": timestamp
                }
                
                self.send_post_request(url, token, data)
                time.sleep(interval * 60)
        
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()