from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# ---------------CARD---------------------------------------------------------#
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    random_word = current_card["French"]
    canvas.itemconfig(card_language, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_word, fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, func=english_card)


def is_known():
    global current_card, flip_timer
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def english_card():
    # Changing the canvas image
    random_en_word = current_card["English"]
    canvas.itemconfig(card_language, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_en_word, fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


# -------------UI UPSET--------------------------------------------------------#
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=english_card)

# Canvas for Card
canvas = Canvas(width=800, height=526)
card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400, 263, image=card_front_image)
card_language = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)
right_image = PhotoImage(file="images/right.png")
known_button = Button(image=right_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()
window.mainloop()
