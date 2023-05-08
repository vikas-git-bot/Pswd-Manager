from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    symbols = ['!', '@', '#', '$', '%', '&', '*', '(', ')']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_lists = password_letters + password_numbers + password_symbols
    shuffle(password_lists)

    password = "".join(password_lists)
    pass_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    w = web_entry.get().title()
    e = email_entry.get()
    p = pass_entry.get()

    new_data = {
        w: {
            "email": e,
            "password": p,
        }
    }
    if len(w) == 0 or len(p) == 0:
        messagebox.showerror(title="Oops!", message="Make sure you haven't left any empty fields")
    else:
        try:
            with open("data.json") as df:
                # reading old data load() return converting json data into dict
                data = json.load(df)
        except FileNotFoundError:
            with open("data.json", "w") as df:
                json.dump(new_data, df, indent=4)
        else:
            # update old data with new data
            data.update(new_data)  # using data.update() over json.update()

            with open("data.json", "w") as df:
                # saving the updated data
                json.dump(data, df, indent=4)
        finally:
            web_entry.delete(0, END)
            pass_entry.delete(0, END)


# ----------------------------Find Password ------------------------------- #
def find_password():
    w = web_entry.get().title()
    try:
        with open("data.json") as df:
            data = json.load(df)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data found")
    else:
        if w in data:
            email = data[w]["email"]
            password = data[w]["password"]
            messagebox.showinfo(title=w, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details of {w} exits")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="lock.png")
canvas.create_image(120, 105, image=logo_img)
canvas.grid(row=0, column=1)

web_label = Label(text="Website", fg="Blue")
web_label.grid(row=1, column=0)
email_label = Label(text="Email", fg="Blue")
email_label.grid(row=2, column=0)
password_label = Label(text="Password", fg="Blue")
password_label.grid(row=3, column=0)

web_entry = Entry(width=21)
web_entry.focus()
web_entry.grid(row=1, column=1)
email_entry = Entry(width=40)
email_entry.insert(0, "vicky.singhk09@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)
pass_entry = Entry(width=21)
pass_entry.grid(row=3, column=1)

password_gen_button = Button(text="Generate Password", command=generate_password)
password_gen_button.grid(row=3, column=2)
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
add_button = Button(text="Add", width=40, command=save)
add_button.grid(row=4, column=1, columnspan=2)
window.mainloop()