!pip install deep-translator
!pip install pyttsx3
!pip install gTTS

import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator
import pyttsx3
import threading
from gtts import gTTS
import os

# Function to initialize the pyttsx3 engine
def init_engine():
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    return engine

# Initialize TTS engine
engine = init_engine()

# Language options
languages = GoogleTranslator().get_supported_languages()
# gTTS language codes
lang_codes = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bn': 'Bengali', 'ca': 'Catalan', 'cs': 'Czech',
    'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish',
    'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French', 'gu': 'Gujarati', 'hi': 'Hindi',
    'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
    'ja': 'Japanese', 'jw': 'Javanese', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean',
    'la': 'Latin', 'lv': 'Latvian', 'ml': 'Malayalam', 'mr': 'Marathi', 'my': 'Burmese',
    'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese',
    'ro': 'Romanian', 'ru': 'Russian', 'si': 'Sinhala', 'sk': 'Slovak', 'sq': 'Albanian',
    'sr': 'Serbian', 'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil',
    'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
    'vi': 'Vietnamese', 'zh-CN': 'Chinese (Simplified)', 'zh-TW': 'Chinese (Traditional)'
}

# Initialize app
root = tk.Tk()
root.title("Multilingual Translator with Speech")
root.geometry("950x600")
root.config(bg="#d1e7dd")

# Fonts
label_font = ("Arial", 12)
button_font = ("Arial", 12)

# Layout frames
main_frame = tk.Frame(root, bg="#d1e7dd")
main_frame.pack(side="left", padx=10, pady=10)

right_panel = tk.Frame(root, bg="#d1e7dd")
right_panel.pack(side="right", padx=10, pady=10, fill="y")

# -- Main Translation Frame --
source_lang_label = tk.Label(main_frame, text="Source Language:", font=label_font, bg="#d1e7dd")
source_lang_label.grid(row=0, column=0, sticky="w")
source_lang = ttk.Combobox(main_frame, values=languages, width=20, font=label_font)
source_lang.set("english")
source_lang.grid(row=0, column=1, pady=5)

input_label = tk.Label(main_frame, text="Input:", font=label_font, bg="#d1e7dd")
input_label.grid(row=1, column=0, sticky="w")
input_text = tk.Text(main_frame, height=6, width=40, font=("Arial", 12), wrap="word")
input_text.grid(row=1, column=1, pady=5)

read_source_button = tk.Button(main_frame, text="Read Source", font=button_font, command=lambda: read_aloud(True), bg="#4CAF50", fg="white")
read_source_button.grid(row=2, column=1, pady=5)

translate_button = tk.Button(main_frame, text="Translate", font=button_font, command=lambda: translate_text(), bg="#2196F3", fg="white")
translate_button.grid(row=3, column=1, pady=10)

target_lang_label = tk.Label(main_frame, text="Target Language:", font=label_font, bg="#d1e7dd")
target_lang_label.grid(row=4, column=0, sticky="w")
target_lang = ttk.Combobox(main_frame, values=languages, width=20, font=label_font)
target_lang.set("tamil")
target_lang.grid(row=4, column=1, pady=5)

output_label = tk.Label(main_frame, text="Output:", font=label_font, bg="#d1e7dd")
output_label.grid(row=5, column=0, sticky="w")
output_text = tk.Text(main_frame, height=6, width=40, font=("Arial", 12), wrap="word")
output_text.grid(row=5, column=1, pady=5)

read_target_button = tk.Button(main_frame, text="Read Translation", font=button_font, command=lambda: read_aloud(False), bg="#4CAF50", fg="white")
read_target_button.grid(row=6, column=1, pady=5)

save_fav_button = tk.Button(main_frame, text="Save Favorite Pair", font=button_font, command=lambda: save_favorite_pair(), bg="#673AB7", fg="white")
save_fav_button.grid(row=7, column=1, pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12, "italic"), bg="#d1e7dd", fg="black")
status_label.pack(side="bottom", pady=5)

# -- Favorites Panel --
fav_label = tk.Label(right_panel, text="Favorite Pairs", font=label_font, bg="#d1e7dd")
fav_label.pack()
fav_listbox = tk.Listbox(right_panel, width=30, height=6, font=("Arial", 10))
fav_listbox.pack(pady=5)

# -- History Panel --
history_label = tk.Label(right_panel, text="Translation History", font=label_font, bg="#d1e7dd")
history_label.pack(pady=10)
history_listbox = tk.Listbox(right_panel, width=30, height=12, font=("Arial", 10))
history_listbox.pack()

# History and Favorite storage
history_data = {}
fav_pairs = set()

def translate_text():
    src = source_lang.get()
    tgt = target_lang.get()
    text = input_text.get("1.0", tk.END).strip()

    if text:
        try:
            translated = GoogleTranslator(source=src, target=tgt).translate(text)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, translated)
            add_to_history(src, tgt, text, translated)
            status_label.config(text="The translation was successfully done", fg="green")
        except Exception as e:
            status_label.config(text="The target language was not found", fg="red")
    else:
        status_label.config(text="Please enter text to translate", fg="orange")

def read_aloud(is_source=True):
    global engine
    text = input_text.get("1.0", tk.END).strip() if is_source else output_text.get("1.0", tk.END).strip()
    lang = source_lang.get() if is_source else target_lang.get()
    if text:
        engine = init_engine()
        threading.Thread(target=speak, args=(text, lang)).start()

def speak(text, lang):
    gtts_lang = next((code for code, name in lang_codes.items() if name.lower() == lang.lower()), None)
    if not gtts_lang:
        print(f"gTTS does not support the language: {lang}")
        return
    if gtts_lang == "en":
        engine.say(text)
        engine.runAndWait()
    else:
        tts = gTTS(text=text, lang=gtts_lang)
        tts.save("output.mp3")
        os.system("start output.mp3")

def save_favorite_pair():
    pair = (source_lang.get(), target_lang.get())
    if pair not in fav_pairs:
        fav_listbox.insert(tk.END, f"{pair[0]} ➜ {pair[1]}")
        fav_pairs.add(pair)
        status_label.config(text="Favorite pair saved!", fg="purple")

# Favorite pair selection
def on_fav_select(event):
    selection = fav_listbox.curselection()
    if selection:
        selected_text = fav_listbox.get(selection[0])
        src, tgt = selected_text.split(" ➜ ")
        source_lang.set(src)
        target_lang.set(tgt)
        status_label.config(text=f"Favorite pair loaded: {src} ➜ {tgt}", fg="blue")

# History add and select
def add_to_history(src, tgt, original, translated):
    history_entry = f"{src} ➜ {tgt}: {original[:20]}..."
    history_listbox.insert(tk.END, history_entry)
    history_data[history_entry] = (src, tgt, original, translated)

def on_history_select(event):
    selection = history_listbox.curselection()
    if selection:
        selected_text = history_listbox.get(selection[0])
        if selected_text in history_data:
            src, tgt, original, translated = history_data[selected_text]
            source_lang.set(src)
            target_lang.set(tgt)
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, original)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, translated)
            status_label.config(text=f"History loaded: {src} ➜ {tgt}", fg="blue")

# Bind events
fav_listbox.bind("<<ListboxSelect>>", on_fav_select)
history_listbox.bind("<<ListboxSelect>>", on_history_select)

# Start app
root.mainloop()
