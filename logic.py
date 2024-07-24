import requests
import time
from datetime import datetime
import tkinter as tk

class RequestHandler:
    def __init__(self, app):
        self.app = app

    def send_post_request(self, url, token, data):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=data)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code == 200:
            self.app.log_text.insert(tk.END, self.app.get_translation("request_success", current_time=current_time))
        else:
            self.app.log_text.insert(tk.END, self.app.get_translation("request_error", current_time=current_time, response_status=response.status_code))
            self.app.log_text.insert(tk.END, f"{response.text}\n")
        self.app.log_text.see(tk.END)

    def send_requests(self, token, count, available_taps, interval, url):
        if not self.app.is_sending:
            return
        
        timestamp = int(time.mktime(datetime.now().timetuple()))
        data = {
            "count": count,
            "availableTaps": available_taps,
            "timestamp": timestamp
        }
        
        self.send_post_request(url, token, data)
        
        for remaining in range(interval * 60, 0, -1):
            if not self.app.is_sending:
                self.app.reset_ui()
                return
            mins, secs = divmod(remaining, 60)
            self.app.countdown_label.config(text=self.app.get_translation("next_request", mins=mins, secs=secs))
            self.app.update()
            time.sleep(1)
        
        self.send_requests(token, count, available_taps, interval, url)