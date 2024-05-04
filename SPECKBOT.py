import tkinter as tk
from transformers import pipeline

class TextToDashApp:
    def __init__(self, master):
        self.master = master
        master.title("Text to Dash Points")
        master.geometry("800x600")
        master.configure(bg='black')
        
        self.text_entry = tk.Text(master, height=20, width=70, bg='gray', fg='white')
        self.text_entry.pack()

        self.dash_button = tk.Button(master, text="Generate Dashes", command=self.generate_dashes, bg='gray', fg='white')
        self.dash_button.pack()

        self.dash_output = tk.Text(master, height=20, width=70, state=tk.DISABLED, bg='gray', fg='white')
        self.dash_output.pack()

    @staticmethod
    def generate_key_points(text):
        summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="pt")

        # Generate summary using abstractive summarization
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

        return summary.split(". ")

    @staticmethod
    def post_process(key_points):
        # Remove empty strings and leading/trailing whitespace
        key_points = [point.strip() for point in key_points if point.strip()]
        
        return key_points

    def generate_dashes(self):
        input_text = self.text_entry.get("1.0", tk.END).strip()

        if not input_text:
            return

        # Generate key points
        key_points = self.generate_key_points(input_text)

        # Post-process key points
        key_points = self.post_process(key_points)

        # Display processed key points
        self.dash_output.config(state=tk.NORMAL)
        self.dash_output.delete("1.0", tk.END)
        for i, point in enumerate(key_points, start=1):
            self.dash_output.insert(tk.END, f"{i}. {point}\n")
        self.dash_output.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToDashApp(root)
    root.mainloop()
