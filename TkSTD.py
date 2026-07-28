import tkinter as tk
from tkinter import scrolledtext, messagebox, PhotoImage
import socket
import threading
import sys
import os
import sys


# פונקציה שמאתרת את הנתיב הנכון לקובץ (גם ב-EXE וגם ב-Python רגיל)
def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath('.')
  return os.path.join(base_path, relative_path)


def Login_Page():
    log = tk.Tk()
    log.geometry("450x450")
    log.config(bg="#1e1e2e")  # רקע כהה ומודרני
    log.title("Login")

    def add_holder(entry, text):
        entry.insert(0, text)

        def focus(event):
            if entry.get() == text:
                entry.delete(0, tk.END)

        def out_focus(event):
            if entry.get == '':
                entry.insert(0, text)

        entry.bind('<FocusIn>', focus)
        entry.bind('<FocusOut>', out_focus)

    def Check_for_Chat():
        name = username.get().strip()
        passcode = password.get().strip()
        ip = ipadr.get().strip()
        port = portadr.get().strip()
        signs = "!@#$%^&*?_"

        if len(passcode) >= 6 and any(char.upper() for char in passcode) and any(char in signs for char in passcode):
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip,int(port)))
                client.send(name.encode('utf-8'))
                log.destroy()
                Open_Chat(client, name)
            except Exception as e:
                messagebox.showerror("Connection Error", f"The Connect With The Server Has Failed; \n{e}")
        else:
            messagebox.showerror("Login Error!",
                                 "Access Denied! Password requires at least 6 characters, an uppercase letter, and a sign.")

    # מסגרת מרכזית
    log_frm = tk.LabelFrame(log, bg="#2b2b3b", fg="#89b4fa", font=("Segoe UI", 13, "bold"), text=" LOGIN ", bd=0,
                            padx=20, pady=20)
    log_frm.pack(expand=True, pady=20)

    # שם משתמש
    username = tk.Entry(log_frm, font=("Segoe UI", 11), bg="#1e1e2e", fg="#cdd6f4", insertbackground="white",
                        relief="flat", highlightthickness=1, highlightbackground="#45475a")
    username.pack(fill="x", ipady=4, pady=(0, 15))
    add_holder(username,"Enter  Username:")

    # סיסמה
    password = tk.Entry(log_frm, font=("Segue UI", 11), bg="#1e1e2e", fg="#cdd6f4", insertbackground="white",
                        relief="flat", highlightthickness=1, highlightbackground="#45475a")
    password.pack(fill="x", ipady=4, pady=(0, 20))
    add_holder(password,"Your Password:")

    ipadr = tk.Entry(log_frm, font=("Segue UI", 11), bg="#1e1e2e", fg="#cdd6f4", insertbackground="white",
                        relief="flat", highlightthickness=1, highlightbackground="#45475a")
    ipadr.pack( ipady=4, pady=(0, 20))
    add_holder(ipadr,"IP Address:")

    portadr = tk.Entry(log_frm, font=("Segue UI", 11), bg="#1e1e2e", fg="#cdd6f4", insertbackground="white",
                        relief="flat", highlightthickness=1, highlightbackground="#45475a")
    portadr.pack(fill="x", ipady=4, pady=(0, 20))
    add_holder(portadr,"Port:")

    # כפתור התחברות
    logbtn = tk.Button(log_frm, text="Login", bg="#89b4fa", fg="#11111b", font=("Segoe UI", 11, "bold"),
                       activebackground="#b4befe", relief="flat", cursor="hand2", command=Check_for_Chat)
    logbtn.pack(fill="x", ipady=6)

    log.mainloop()


def Open_Chat(client, name):
    root = tk.Tk()
    root.geometry("500x385")
    root.title(f"Chat App - {name}")
    root.config(bg="#1e1e2e")
    try:
        icon_p = resource_path('chat.ico')
        root.iconbitmap(icon_p)
    except Exception as e:
        print(f'Icon error: {e}')

    def receive_messages():
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                info = data.decode('utf-8')
                scrl_txt.configure(state="normal")
                scrl_txt.insert(tk.END, info + '\n\n')
                scrl_txt.configure(state="disabled")
                scrl_txt.see(tk.END)  # גלילה אוטומטית להודעה החדשה
            except:
                break

    def massage_get_info():
        lmt_words = ["password", "low", "secret", "fuck", "shit", "death", "murder", "genocide", "terror", "palestine",
                     "nazi"]
        vals = wrt_forum.get("1.0", tk.END).strip()
        if not vals:
            return

        all_info = vals.split(' ')
        for i in range(len(all_info)):
            if all_info[i].lower().strip(".,?!/") in lmt_words:
                word = all_info[i].lower().strip(".,?!/")
                all_info[i] = all_info[i].replace(word, '*' * len(word))
        vals = " ".join(all_info)
        try:
            client.send(vals.encode('utf-8'))
            wrt_forum.delete(1.0, tk.END)
        except Exception as e:
            messagebox.showerror("Disconnected", "Lost connection to the server!")
            root.destroy()

    # אזור הטקסט הראשי
    scrl_txt = scrolledtext.ScrolledText(root, fg="#cdd6f4", bg="#181825", height=15, width=70, state="disabled",
                                         font=("Segoe UI Emoji", 10), bd=0, highlightthickness=1,
                                         highlightbackground="#45475a")
    scrl_txt.pack(pady=15, padx=15, fill="both", expand=True)

    msg = "😎🫶🏼🫱🏼‍🫲🏼 Access Granted! Welcome to the chat!"
    scrl_txt.configure(state="normal")
    scrl_txt.insert(tk.END, msg + '\n\n')
    scrl_txt.configure(state="disabled")

    # אזור הקלט והכפתור למטה
    input_frm = tk.Frame(root, bg="#1e1e2e")
    input_frm.pack(side="bottom", fill="x", padx=15, pady=15)

    wrt_forum = tk.Text(input_frm, font=("Segoe UI Emoji", 11), bg="#313244", fg="#cdd6f4",
                        insertbackground="white", relief="flat", height=1.5)
    wrt_forum.pack(side="left", fill="x", expand=True, padx=(0, 10))

    # פונקציה לתפיסת מקש Enter בלי ירידת שורה
    def send_on_enter(event):
        massage_get_info()
        return "break"  # מונע מ-Tkinter לרדת שורה בתיבה

    wrt_forum.bind('<Return>', send_on_enter)

    button_send = tk.Button(input_frm, text="Send ➔", width=10, bg="#a6e3a1", fg="#11111b",
                            font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", command=massage_get_info)
    button_send.pack(side="right", ipady=5)

    thr = threading.Thread(target=receive_messages)
    thr.daemon = True
    thr.start()

    root.mainloop()


if __name__ == "__main__":
    Login_Page()