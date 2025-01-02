import tkinter as tk
from tkinter import ttk
import requests

class TextTranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Text Translator")
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for text input
        label1 = tk.Label(self.root, text="Enter text to translate:")
        label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry = tk.Entry(self.root, width=50)
        self.entry.grid(row=0, column=1, padx=10, pady=10)

        # Source language selection
        label2 = tk.Label(self.root, text="Choose source language:")
        label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.source_lang = ttk.Combobox(self.root, values=["en", "es", "fr", "vi", "ja", "zh"])
        self.source_lang.set("en")
        self.source_lang.grid(row=1, column=1, padx=10, pady=10)

        # Target language selection
        label3 = tk.Label(self.root, text="Choose target language:")
        label3.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.target_lang = ttk.Combobox(self.root, values=["en", "es", "fr", "vi", "ja", "zh"])
        self.target_lang.set("vi")
        self.target_lang.grid(row=2, column=1, padx=10, pady=10)

        # Translate button
        translate_button = tk.Button(self.root, text="Translate", command=self.translate_text)
        translate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Label to display result
        self.result_label = tk.Label(self.root, text="Translated text will appear here.", wraplength=400)
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def translate_text(self):
        # Replace with your API key
        api_key = "AIzaSyB1qupyzNgJMrej3hRAnKdaxk0JRqdcF_c"
        text_to_translate = self.entry.get()

        # API URL and parameters
        url = f"https://translation.googleapis.com/language/translate/v2"
        params = {
            'q': text_to_translate,
            'source': self.source_lang.get(),
            'target': self.target_lang.get(),
            'key': api_key
        }

        try:
            # Sending the request
            response = requests.post(url, params=params)
            response_data = response.json()

            # Extract translated text
            translated_text = response_data['data']['translations'][0]['translatedText']
            self.result_label.config(text=translated_text)
        except Exception as e:
            # Handle errors gracefully
            self.result_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextTranslatorApp(root)
    root.mainloop()


