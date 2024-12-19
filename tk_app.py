import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import subprocess
from datetime import datetime
import pytz
import threading

def run_speedtest():
    try:
        result = subprocess.run(["speedtest", "--json"], capture_output=True, text=True)
        return {"data": json.loads(result.stdout)}
    except Exception as e:
        return {"error": f"Speedtest CLI error: {str(e)}"}

def convert_to_local_time(utc_time, timezone):
    try:
        utc_datetime = datetime.fromisoformat(utc_time.replace("Z", "+00:00"))
        local_tz = pytz.timezone(timezone)
        local_datetime = utc_datetime.astimezone(local_tz)
        return local_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception as e:
        return f"Error converting time: {str(e)}"

class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("500x500")
        self.root.configure(bg="#2e2e2e")
        self.root.resizable(False, False)

        self.title_label = tk.Label(root, text="Internet Speed Test", font=("Helvetica", 18, "bold"), fg="#ffffff", bg="#2e2e2e")
        self.title_label.pack(pady=30)

        self.test_button = tk.Button(root, text="Start Test", command=self.start_test, font=("Helvetica", 14, "bold"), fg="#ffffff", bg="#1db954", width=15, height=2, relief="flat",cursor="hand2")
        self.test_button.pack(pady=20)

        self.result_label = tk.Label(root, text="Results will appear here", font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#2e2e2e", justify="left")
        self.result_label.pack(pady=20)

        self.loading_label = tk.Label(root, text="Please wait...", font=("Helvetica", 12, "italic"), fg="#ffffff", bg="#2e2e2e")
        self.loading_label.pack_forget()

        self.spinner = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")
        self.spinner.pack(pady=20)
        self.spinner.pack_forget()

    def start_test(self):
        self.test_button.config(state=tk.DISABLED)
        self.loading_label.pack(pady=20)
        self.spinner.pack_forget()
        self.spinner.start()

        test_thread = threading.Thread(target=self.run_test)
        test_thread.start()

    def run_test(self):
        result = run_speedtest()
        if "error" in result:
            self.root.after(0, lambda: self.show_error(result["error"]))
            return

        data = result["data"]
        timezone = pytz.timezone('UTC')
        data["timestamp"] = convert_to_local_time(data["timestamp"], timezone.zone)
        ds = ""
        us = ""
        results_text = (
            f"Download Speed: {data['download'] / 1_000_000:.2f} Mbps\n"
            f"Upload Speed: {data['upload'] / 1_000_000:.2f} Mbps\n"
            f"Ping: {data['ping']} ms\n"
            f"Server Name: {data['server']['name']}\n"
            f"Server Location: {data['server']['country']}\n"
            f"Server Host: {data['server']['host']}\n"
            f"Timestamp: {data['timestamp']}\n"
            f"Client IP: {data['client']['ip']}\n"
            f"ISP: {data['client']['isp']}\n"
        )

        self.root.after(0, lambda: self.show_results(results_text))

    def show_results(self, results_text):
        self.result_label.config(text=results_text)
        self.loading_label.pack_forget()
        self.spinner.stop()
        self.spinner.pack_forget() 
        self.test_button.config(state=tk.NORMAL)

    def show_error(self, error):
        self.result_label.config(text="Error occurred while testing.")
        self.loading_label.pack_forget()
        self.spinner.stop()
        self.spinner.pack_forget() 
        self.test_button.config(state=tk.NORMAL)
        messagebox.showerror("Error", error)

def main():
    root = tk.Tk()
    root.attributes("-topmost", True)
    app = SpeedTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
