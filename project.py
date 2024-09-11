import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import os


MOOD_JOURNAL_FILE = 'mood_journal.csv'
MEDICAL_DIAGNOSIS_FILE = 'medical_diagnosis.csv'


for file in [MOOD_JOURNAL_FILE, MEDICAL_DIAGNOSIS_FILE]:
    if not os.path.isfile(file):
        pd.DataFrame(columns=['Date', 'Mood', 'Notes']).to_csv(file, index=False)

class MoodTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Tracker")

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        
        self.tab_control = ttk.Notebook(self.main_frame)
        self.create_mood_tab()
        self.create_journal_tab()
        self.create_medical_tab()
        self.create_calendar_tab()
        self.create_settings_tab()
        self.create_exercise_tab()
        self.tab_control.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_mood_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text='Mood Graph')

        
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


        self.update_mood_graph(pd.DataFrame({
            'Date': [datetime.date.today() - datetime.timedelta(days=i) for i in range(10)],
            'Mood': [i % 5 + 1 for i in range(10)]
        }))

    def update_mood_graph(self, data):
        self.ax.clear()
        self.ax.plot(pd.to_datetime(data['Date']), data['Mood'], marker='o')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Mood')
        self.ax.set_title('Mood Over Time')
        self.canvas.draw()

    def create_journal_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text='Mood Journal')

        self.journal_text = tk.Text(tab, wrap=tk.WORD, height=15)
        self.journal_text.pack(fill=tk.BOTH, expand=True)

        self.save_button = ttk.Button(tab, text="Save Journal Entry", command=self.save_journal_entry)
        self.save_button.pack()

    def save_journal_entry(self):
        text = self.journal_text.get("1.0", tk.END).strip()
        if text:
            date = datetime.date.today().strftime("%Y-%m-%d")
            df = pd.read_csv(MOOD_JOURNAL_FILE)
            new_entry = pd.DataFrame([[date, 'Neutral', text]], columns=['Date', 'Mood', 'Notes'])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(MOOD_JOURNAL_FILE, index=False)
            messagebox.showinfo("Success", "Journal entry saved.")
        else:
            messagebox.showwarning("Warning", "Journal entry is empty.")

    def create_medical_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text='Medical Diagnosis')

        self.medical_text = tk.Text(tab, wrap=tk.WORD, height=15)
        self.medical_text.pack(fill=tk.BOTH, expand=True)

        self.save_medical_button = ttk.Button(tab, text="Save Medical Diagnosis", command=self.save_medical_diagnosis)
        self.save_medical_button.pack()

    def save_medical_diagnosis(self):
        text = self.medical_text.get("1.0", tk.END).strip()
        if text:
            date = datetime.date.today().strftime("%Y-%m-%d")
            df = pd.read_csv(MEDICAL_DIAGNOSIS_FILE)
            new_entry = pd.DataFrame([[date, text]], columns=['Date', 'Diagnosis'])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(MEDICAL_DIAGNOSIS_FILE, index=False)
            messagebox.showinfo("Success", "Medical diagnosis saved.")
        else:
            messagebox.showwarning("Warning", "Medical diagnosis entry is empty.")

    def create_calendar_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text='Calendar')
        

    def create_settings_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text='Settings/Goals')
        

    def create_exercise_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text='Exercises')
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodTrackerApp(root)
    root.mainloop()
