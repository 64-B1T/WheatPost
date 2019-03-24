import tkinter as tk
from tkinter import filedialog
import connection_broker as cb
import os

ssh = None
username = ""
password = ""

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None

        self.title("Wheatpaste")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)

        self.geometry("+{}+{}".format(positionRight, positionDown))

        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        banner = tk.Label(self, text="Welcome to Wheatpaste!")
        banner.grid(row=0, columnspan=2)

        tk.Label(self, text="Username").grid(row=1, padx=5, pady=5)
        username_entry = tk.Entry(self)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        username_entry.focus_set()

        tk.Label(self, text="Password").grid(row=2, padx=5, pady=5)
        password_entry = tk.Entry(self, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        def login():
            global ssh, username, password

            username = username_entry.get()
            password = password_entry.get()

            if not username:
                banner.configure(text="Enter username")
                return
            if not password:
                banner.configure(text="Enter password")
                return

            message, ssh = cb.login(username, password)

            banner.configure(text=message)

            if ssh:
                master.switch_frame(OptionsPage)

        def make_user():
            global ssh

            username = username_entry.get()
            password = password_entry.get()

            if not username:
                banner.configure(text="Enter username")
                return
            if not password:
                banner.configure(text="Enter password")
                return

            result = cb.create_user(ssh, username, password)

            if result == 1:
                # User could not be created
                banner.configure(text="User could not be created")
                return
            else:
                # User was created
                banner.configure(text="User was created")
                return

        tk.Button(self, text="Create User", command=make_user).grid(row=3, padx=15)
        tk.Button(self, text="Login", width=8, command=login).grid(row=3, column=1, padx=15, pady=5)

class OptionsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global ssh, username

        tk.Label(self, text="Welcome %s!" % username, font="Helvetica 9 bold").grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Mount folder or share with users?").grid(row=1, column=1, padx=5, pady=5)

        def logout():
            global ssh
            cb.close(ssh)
            ssh = None
            master.switch_frame(LoginPage)

        tk.Button(self, text="Mount", command=lambda: master.switch_frame(MountPage)).grid(row=2, padx=15)
        tk.Button(self, text="Share", width=8, command=lambda: master.switch_frame(SharePage)).grid(row=2, column=1, padx=15, pady=5)
        tk.Button(self, text="Logout", width=8, command=logout).grid(row=2, column=2, padx=15, pady=5)

class MountPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        banner = tk.Label(self, text=" ")
        banner.grid(row=0, columnspan=3, padx=5, pady=5)

        tk.Label(self, text="Choose a folder to mount").grid(row=1, columnspan=3, padx=5, pady=5)
        folder = tk.Label(self, text=" ")
        folder.grid(row=2, columnspan=3, padx=5, pady=5)

        def get_folder():
            f = filedialog.askdirectory(title='Choose a folder')
            folder.configure(text=f)

        def mount():
            global ssh, username, password
            nonlocal folder
            folder_name = folder.cget("text")
            print(folder_name)
            result = cb.mount(username, password, folder_name)
            banner.configure(text=result)

        tk.Button(self, text="Browse", command=get_folder).grid(row=3, padx=15)
        tk.Button(self, text="Mount", command=mount, width=8).grid(row=3, column=1, padx=15, pady=5)
        tk.Button(self, text="Back", width=8, command=lambda: master.switch_frame(OptionsPage)).grid(row=3, column=2, padx=15, pady=5)

class SharePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        vals = cb.get_users(ssh)
        user_var = tk.StringVar()
        user_var.set(vals[0])
        files = []

        tk.Label(self, text=" ").grid(row=0, columnspan=4, padx=5, pady=5)
        tk.Label(self, text="Choose a user to share with").grid(row=1, columnspan=4, padx=5, pady=5)
        users = tk.OptionMenu(self, user_var, *vals)
        users.grid(row=2, columnspan=4, padx=5, pady=5)

        tk.Label(self, text="Choose files to share").grid(row=3, columnspan=4, padx=5, pady=5)

        s = tk.Scrollbar(self)
        s.grid(row=4, column=3, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        t = tk.Text(self, height=4)
        t.grid(row=4, columnspan=3, padx=5, pady=5)
        s.config(command=t.yview)
        t.config(yscrollcommand=s.set)

        def get_files():
            nonlocal files
            files = filedialog.askopenfilenames(parent=self, title='Choose files')
            print(files)
            for file in self.tk.splitlist(files):
                t.insert(tk.END, file + "\n")

        def send_files()


        tk.Button(self, text="Browse", command=get_files).grid(row=5, padx=15)
        tk.Button(self, text="Send", width=8).grid(row=5, column=1, padx=15, pady=5)
        tk.Button(self, text="Back", width=8, command=lambda: master.switch_frame(OptionsPage)).grid(row=5, column=2, columnspan=2, padx=15, pady=5)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
