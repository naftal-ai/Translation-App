import tkinter as tk
from data.translate import get_translation

class TranslationDialog:
    def __init__(self, root):
        self.root = root
        self.root.title("Translation App")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f8ff")

        # Input Section
        input_frame = tk.Frame(root, bg="#f0f8ff", padx=10, pady=10)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Enter a word:", font=("Helvetica", 14), bg="#f0f8ff").pack(side="left", padx=(0, 10))

        self.input_entry = tk.Entry(input_frame, width=30, font=("Helvetica", 14))
        self.input_entry.pack(side="left", padx=(0, 10))
        self.input_entry.bind("<Return>", lambda event: self.translate())

        search_button = tk.Button(input_frame, text="Translate", command=self.translate, font=("Helvetica", 14), bg="#4682b4", fg="white", relief="raised", padx=10, pady=5)
        search_button.pack(side="left")

        # Results Section
        self.results_frame = tk.Frame(root, bg="#f0f8ff", padx=10, pady=10)
        self.results_frame.pack(fill="both", expand=True)

        tk.Label(self.results_frame, text="Results:", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(anchor="w")

        # Scrollable Container
        self.canvas = tk.Canvas(self.results_frame, bg="#f0f8ff")
        self.scrollbar = tk.Scrollbar(self.results_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f8ff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind arrow keys for scrolling
        self.canvas.bind_all("<Up>", lambda event: self.scroll_canvas("up"))
        self.canvas.bind_all("<Down>", lambda event: self.scroll_canvas("down"))

    def scroll_canvas(self, direction):
        if direction == "up":
            self.canvas.yview_scroll(-1, "units")
        elif direction == "down":
            self.canvas.yview_scroll(1, "units")

    def translate(self):
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Get translations
        word = self.input_entry.get().strip()
        if not word:
            tk.Label(self.scrollable_frame, text="Please enter a word to translate.", font=("Helvetica", 14), bg="#f0f8ff").pack(anchor="w")
            return

        results = get_translation(word)  # Fetch translations using the provided function

        if not results:
            tk.Label(self.scrollable_frame, text="No results found.", font=("Helvetica", 14), bg="#f0f8ff").pack(anchor="w")
            return

        for result in results:
            self.display_result(result)

    def display_result(self, word_obj):
        result_frame = tk.Frame(self.scrollable_frame, relief="solid", borderwidth=2, bg="#ffffff", padx=10, pady=10)
        result_frame.pack(fill="x", pady=10)

        tk.Label(result_frame, text=f"Word: {word_obj.en_word}", font=("Helvetica", 14, "bold"), bg="#ffffff").pack(anchor="w")
        tk.Label(result_frame, text=f"Part of Speech: {word_obj.part_of_speech}", font=("Helvetica", 14), bg="#ffffff").pack(anchor="w")
        tk.Label(result_frame, text=f"Translation: {word_obj.translation}", font=("Helvetica", 16, "bold"), fg="#4682b4", bg="#ffffff").pack(anchor="w", pady=5)

        if word_obj.inflections:
            inflections = ", ".join(word_obj.inflections)
            tk.Label(result_frame, text=f"Inflections: {inflections}", font=("Helvetica", 14), bg="#ffffff").pack(anchor="w")

        if word_obj.examples:
            for example in word_obj.examples:
                tk.Label(result_frame, text=f"Example: {example}", font=("Helvetica", 14, "italic"), bg="#ffffff").pack(anchor="w")

        if word_obj.audio_path:
            play_button = tk.Button(result_frame, text="Play", command=lambda: word_obj.play_word(), font=("Helvetica", 12), bg="#4682b4", fg="white", relief="raised", padx=10, pady=5)
            play_button.pack(anchor="w", pady=5)



def run_dialog():
    root = tk.Tk()
    TranslationDialog(root)
    root.mainloop()

if __name__ == "__main__":
    run_dialog()
