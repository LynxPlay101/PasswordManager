from tkinter import messagebox
from tkinter import *

from sql.ManagedPassword import ManagedPassword
from sql.ManagedPasswordDao import ManagedPasswordDao

import validators as validators
import sql.ManagedPassword as mP


class PasswordManagerGui:
    dao: ManagedPasswordDao = None
    screen: Tk

    def __init__(self, dao: ManagedPasswordDao):
        self.dao = dao

        self.screen = Tk()
        self.screen.geometry("600x450+650+150")
        self.screen.title("Password Manager")
        self.screen.configure(background="#d9d9d9")

        self.add_button = Button(self.screen)
        self.add_button.place(relx=0.25, rely=0.78, height=33, width=136)
        self.add_button.configure(pady="0")
        self.add_button.configure(text='''Add''')
        self.add_button.config(command=self.save)

        self.delete_button = Button(self.screen)
        self.delete_button.place(relx=0.72, rely=0.9, height=33, width=145)
        self.delete_button.configure(pady="0")
        self.delete_button.configure(text='''Delete url''')
        self.delete_button.config(command=self.delete)

        self.url_list = Listbox(self.screen)
        self.url_list.place(relx=0.72, rely=0.04, relheight=0.86, relwidth=0.24)
        self.url_list.configure(width=144)
        self.url_list.bind("<Double-Button-1>", self.on_list_select)

        self.url_label = Label(self.screen)
        self.url_label.place(relx=0.05, rely=0.13, height=26, width=32)
        self.url_label.configure(text='''URL''')

        self.username_label = Label(self.screen)
        self.username_label.place(relx=0.05, rely=0.29, height=26, width=72)
        self.username_label.configure(text='''Username''')

        self.password_label = Label(self.screen)
        self.password_label.place(relx=0.05, rely=0.42, height=26, width=68)
        self.password_label.configure(text='''Password''')

        self.url_text = Text(self.screen)
        self.url_text.place(relx=0.2, rely=0.13, relheight=0.05, relwidth=0.4)
        self.url_text.configure(wrap=WORD)

        self.username_text = Text(self.screen)
        self.username_text.place(relx=0.2, rely=0.29, relheight=0.05, relwidth=0.4)
        self.username_text.configure(wrap=WORD)

        self.password_text = Text(self.screen)
        self.password_text.place(relx=0.2, rely=0.42, relheight=0.05, relwidth=0.4)
        self.password_text.configure(wrap=WORD)

        self.screen.bind_class("Text", "<Tab>", focus_next_window)
        self.screen.bind_class("Text", "<Return>", self.save_from_event)

        self.dao.all()
        self.update_list()
        pass

    def save(self):
        url: str = self.url_text.get("1.0", END)
        url = url.strip()
        if len(url) < 1:
            messagebox.showerror("Missing information", "No url was provided")
            return

        if not url.startswith("http"):
            url = "http://" + url

        if not validators.url(url):
            messagebox.showerror("Not an URL", "The provided url %s is not a url" % url)
            return

        user: str = self.username_text.get("1.0", END)
        user = user.strip()

        password: str = self.password_text.get("1.0", END)
        password = password.strip()

        if len(user) < 1:
            messagebox.showerror("Missing field", "No username was provided")
            return
        if len(password) < 1:
            messagebox.showerror("Missing field", "No password was provided")
            return

        entry = mP.new(url, user, password)
        exiting = self.dao.get(url)
        if exiting is not None and exiting.equals(entry):
            messagebox.showinfo("No change detected", "The provided data is equal to the currently stored on")
            return

        if exiting is not None and exiting.url == entry.url:
            choice = messagebox.askyesno("Changing values", (
                    "The url %s already exists and will be changed\n" % entry.url +
                    "%s -> %s\n" % (exiting.username, entry.username) +
                    "%s -> %s\n" % (exiting.password, entry.password)
            ))
            if not choice:
                return

        self.dao.store(entry)
        self.update_list()

        self.clear_text_fields()
        pass

    def clear_text_fields(self):
        self.url_text.delete("1.0", END)
        self.username_text.delete("1.0", END)
        self.password_text.delete("1.0", END)

    def save_from_event(self, event):
        if event is not None:
            self.save()

    def delete(self):
        selection = self.url_list.curselection()
        if len(selection) < 1:
            return

        url = self.url_list.get(selection[0])
        password = self.dao.get(url)
        if password is None:
            messagebox.showerror("Database error", "Could not find the url %s in the database. Removing.." % url)
            self.dao.remove(url)
            self.update_list()
            return

        if messagebox.askyesno("Delete URL", "Are you sure you want to delete %s" % url):
            self.dao.remove(url)
            self.update_list()
        pass

    def update_list(self):
        self.url_list.delete(0, self.url_list.size())

        index = 0
        for x in self.dao.get_cache():
            self.url_list.insert(index, x.url)
            index += 1
        pass

    def on_list_select(self, event):
        w = event.widget
        if len(w.curselection()) < 1:
            return

        index = int(w.curselection()[0])
        value = w.get(index)

        url: str = value

        entry = self.dao.lookup_cache(url)
        if entry is None:
            entry = self.dao.get(url)
        if entry is None:
            messagebox.showerror("Database error", "Could not find the url %s in the database. Removing.." % url)
            self.dao.remove(url)
            self.update_list()
            return

        self.clear_text_fields()
        self.url_text.insert(END, entry.url)
        self.username_text.insert(END, entry.username)
        self.password_text.insert(END, entry.password)
        pass


pass


def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return "break"
    pass


pass
