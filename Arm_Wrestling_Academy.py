#first lines of the code will be used for the import: I need a library for GUI app and another one for editing the pictures on GUI. Most relevent, I need SQL
import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage, Toplevel, LabelFrame, YView, scrolledtext
import sqlite3
from tkinter.constants import VERTICAL, FALSE
import webbrowser

def login_sql(username, password, email, age):
    db = sqlite3.connect('login.sql') #connecting to a file on PyCharm created automatically and hance the database work
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS login(username TEXT, password TEXT, email TEXT, age TEXT)')
    cursor.execute('INSERT INTO login(username, password, email, age) VALUES(?,?,?,?)',(username, password, email, age))
    db.commit() # gotta make the data updated to the parameters we mentioned
    cursor.execute("SELECT * FROM login WHERE username=? AND password=?", (username, password))
    row = cursor.fetchone()
    if row:
        messagebox.showinfo('Sign In', "Signed In Successfully! \ndon't forget to Login.")
        login_window.destroy()  # added global login_window to be able to destroy login window - login function did not exist I gave it another name for the same thing.
        verify_regist(username, password,email,age) # the homepage will work with the parameters too.
        homepage(username,password,email, age) #Homepage
    else:
        messagebox.showinfo('Invalid Sign In', "Registration fields hadn't been filled properly.")
#Create interactive widgets for the user (goes with func .bind()):
def hover2_on(g):
    g.widget.config(bg='#002366',font=('Ariel',10,'italic','underline'),fg='green')
def hover2_off(e):
    e.widget.config(bg='#002366',font=('Ariel',10,'italic'),fg='green')
def sing_up():
    global login_window # Declare login_window as global - the different name to same func.
    log_window = tk.Tk()
    login_window = log_window #mentioned login_window will now do the same with the log_window
    #at the begging of every window we'd adjust and configure it - before editing the widgets to it.
    log_window.geometry("1310x850")
    log_window.configure(bg="#002366")
    log_window.title("Rani's Login System")
    log_window.resizable(False,False)
    #Main app LABEL
    log_lbl = tk.Label(log_window, text='Register And Submit', font=('Franklin', 22, 'bold'), bg=log_window['bg'], fg='white') # page main label
    log_lbl.grid(row=0, column=2, columnspan=2, pady=10, sticky='new')
    #I'd add a photo to adjust the window in more attractive way for the user:
    log_image = PhotoImage(file=r'C:\Users\ranla\PycharmProjects\proj_images\arm_log.png')
    frame_log_img = tk.LabelFrame(log_window, text='Arm-Wrestling Academy', font=('Times', 18, 'italic', 'bold'), relief='sunken', bd=2, bg=log_window['bg'], fg='white') #'bg=log_window['bg']' used for transparent widgets
    frame_log_img.grid(row=1, column=6, pady=60, padx=10, sticky='ew')
    lbl_img = tk.Label(frame_log_img, image=log_image)
    lbl_img.grid()
    #Now, because I test the homepage and all other windows which come out of it a lot - I will create my self a shortcut of the login. Using a simple button that will take me straight to the homepage, with default values for the sql parameters
    def boss_login():
        log_window.destroy()
        homepage("Rani_theBoss","Rani1234","2027rani.l@ebin.ort.org.il","16 years old")
    boss = tk.Button(log_window,text='FOR BOSS ONLY', bg=log_window['bg'],fg='white',command=boss_login)
    boss.grid(row=2, column=6)
    #Using 1 LabelFrame I'd be able to create an organized place - making it easy to handle for the user
    log_frame = tk.LabelFrame(log_window, text='Sign Up Here', font=('Times', 18, 'italic', 'bold'), relief='sunken', bd=2, height=350, width=450, bg=log_window['bg'], fg='white') #I'll use a lot labelframe just for editing all widgets in a clearer way
    log_frame.grid(row=1, column=2, pady=60, padx=100, sticky='ew')
    #Registration Fields:
    # Username
    name_lbl = tk.Label(log_frame, text="Username:*", bg=log_window['bg'], fg='white', font=('Times', 12))
    name_lbl.grid(row=1, column=0, pady=25, padx=25, sticky='w')
    name_enty = tk.Entry(log_frame, font=('Times', 12), bg=log_window['bg'], fg='white')
    name_enty.grid(row=1, column=1, pady=25, padx=10)
    name_enty.bind('<Return>', lambda event: mail_enty.focus_set()) #Cool keyboard interact for moving frm one entry field to the next one
    # E-mail
    mail_lbl = tk.Label(log_frame, text="E-mail/phone number:", bg=log_window['bg'], fg='white', font=('Times', 11))
    mail_lbl.grid(row=2, column=0, pady=25, padx=25, sticky='w')
    mail_enty = tk.Entry(log_frame, font=('Times', 12), bg=log_window['bg'], fg='white')
    mail_enty.grid(row=2, column=1, padx=10, pady=25)
    mail_enty.bind('<Return>', lambda event: pass_enty.focus_set())
    # User password
    pass_lbl = tk.Label(log_frame, text="Password:*", bg=log_window['bg'], fg='white', font=('Times', 12))
    pass_lbl.grid(row=3, column=0, pady=25, padx=25, sticky='w')
    pass_enty = tk.Entry(log_frame, font=('Times', 12), bg=log_window['bg'], fg='white', show='▪')
    pass_enty.grid(row=3, column=1, pady=25, padx=10)
    pass_enty.bind('<Return>', lambda event: Age_enty.focus_set())
    # User age range
    Age_lbl = tk.Label(log_frame, text="User Age:", bg=log_window['bg'], fg='white', font=('Times', 12))
    Age_lbl.grid(row=4, column=0, pady=50, padx=25, sticky='w')
    Age_enty = ttk.Combobox(log_frame, values=['9-11 years old.', '12-14 years old.', '15-17 years old.', '18+ years old.'])
    Age_enty.grid(row=4, column=1, pady=25, padx=10)
    Age_enty.bind('<Return>', lambda event: agree.focus_set())
    def term_accept(): #The function will provide information for the user about the application he/she would be about to enter
        log_window.withdraw()
        term_page = Toplevel(log_window)
        term_page.title('Terms for login in')
        term_page.geometry('550x500')
        term_page.configure(bg='light gray')
        #scrolling area
        canvas = tk.Canvas(term_page, bg=term_page['bg'], scrollregion=(0, 0, 20, 700))  # Increased scroll region
        canvas.grid(row=0, column=0, sticky='nsew')
        #scrollbox creation, commands and adjust for user comfort
        scroller1 = ttk.Scrollbar(term_page, orient=VERTICAL, command=canvas.yview)
        scroller1.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=scroller1.set)
        term_text = (
            "Welcome to My Arm Wrestling App! Before you sign up, \nhere are couple things you need to know:\n\n"
            "1. About Your Information: When you create an account, \nI'll store your data on the computer using a database. \nThis helps me keep your info organized in \ndifferent files I opened to store it all.\n\n"
            "2. What are you getting into? After signing in, you'd have to confirm again username and password. \nMeaning you should remember your entry fields. \nAfter so, you'll find different sections on the application homepage (called 'label frames') \nthat will cover various arm wrestling topics. \nI really think, you should read it in my opinion that's fascinating.\n\n"
            "3. FeedBack Form: Like in some other web-applications, I've included a feedback form \nwhere you can share your thoughts. You can rate the app or write up your ideas, \nlet me know if the app changed your point of view on the sport. \nFinely, you'd be able to select recommend app or not.\n\n"
            "I hope you'll enjoy learning and experiencing the best of my application!\n"
        )
        container_scrollwindow = tk.Frame(canvas,bg=term_page['bg'])

        trm_lf = tk.LabelFrame(container_scrollwindow, bg=term_page['bg'], fg=term_page['bg'])
        trm_lf.grid(row=0, sticky='w')
        trm_lbl = tk.Label(trm_lf, text=term_text, wraplength=470, font=('Georgian', 11), bg=term_page['bg'], fg='black', justify=tk.LEFT)  #put it all into a label
        trm_lbl.grid(row=0, column=0, pady=10, padx=40)
        app_name = tk.LabelFrame(container_scrollwindow, bg=term_page['bg'], fg=term_page['bg'])
        app_name.grid(row=1)
        tk.Label(app_name, text="©Arm-Wrestling Academy | May 2025", font=('Georgia',11), fg='black', bg=term_page['bg']).grid(padx=150, pady=30)
        def back_to_sing():
            log_window.deiconify()
            term_page.destroy()
        tk.Button(container_scrollwindow, bg='green', fg='white',text='Back to sign-up page', font=('Helvetica',11,'italic'),relief='sunken', command=back_to_sing).grid(row=2,padx=180)
        #justify final parameters in the canvas
        canvas.create_window((0, 0), window=container_scrollwindow, anchor=tk.NW)
        term_page.grid_rowconfigure(0, weight=1)
        term_page.grid_columnconfigure(0, weight=1)
    terms = tk.Button(log_frame,text='terms', bg=log_window['bg'],fg='green',font=('Ariel',10,'italic'),bd=0,relief='flat',command=term_accept)
    terms.grid(row=5,column=1,sticky='w',pady=10)
    terms.bind('<Enter>', hover2_on)
    terms.bind('<Leave>',hover2_off)
    # Agree to terms
    term_var = tk.StringVar() #A boolean that check state of checkbutton, did the user confirm reading all terms?
    agree = tk.Checkbutton(log_frame, text='I read and accept all written terms*', font=('Ariel', 10, 'italic'), bg=log_window['bg'],fg='red',relief='flat', variable=term_var, onvalue='on', offvalue='off')
    agree.grid(row=5, column=0)
    term_var.set('off')
    necessary = tk.Label(log_frame,text='■ You must fill the fields with *!',font=('Times',11),bg=log_window['bg'],fg='red')# message for the user to fill the most important entries
    necessary.grid(row=6,sticky='w')
    def submit_login():
        #that's the base of the code - here we'll get the information of the user and connect it to the sql parameters
        username = name_enty.get()
        password = pass_enty.get()
        email = mail_enty.get()
        age = Age_enty.get()
        accept_terms = term_var.get()
        #The user can't get in without the necessary information and a minimum of 6 characters in the password
        if not username or not password or accept_terms == 'off': #Stringvar is a system checks if the checkbutton filled or not
            messagebox.showerror('Login Invalid',"You can't login with blanked necessary entry fields...")
            return
        elif len(password) < 6:
            messagebox.showerror('Invalid Pass' , "The password must have at least 6 characters")
            return
        login_sql(username,password,email,age) # here ends-up the roll of the signup and I'd save the data for the next functions (verification, homepage, feedback form)
    btn_lbl = tk.Button(log_window, text='Sign-up', bg=log_window['bg'], fg='white', height=2, width=12, command=submit_login, relief= 'sunken') # changed to submit_login.
    btn_lbl.grid(row=2, column=2, sticky='s')
    mention = tk.Label(log_window, text="©Arm-Wrestling Academy | May 2025", font=('Helvetica', 9, 'italic'), fg='white', bg=log_window['bg'])
    mention.grid(padx=500, columnspan=14, sticky='s')
    log_window.mainloop()

def verify_regist(username,password,email,age):
    rgist = tk.Tk()
    rgist.geometry('500x500')
    rgist.configure(bg='#002366')
    rgist.title('Confirm Login')
    rgist.resizable(False,False)
    #Window's title
    log_text = tk.Label(rgist, text="Confirm Your Register:", font=('Arial',14,'bold','underline'),bg=rgist['bg'],fg='white')
    log_text.grid(row=0, padx=150,sticky='n')
    login_labelframe = tk.LabelFrame(rgist,text='Confirm Register',bg=rgist['bg'],fg='white')
    login_labelframe.grid(row=1,padx=20,pady=10)
    #Verification of necessary fields:
    #Confirm username
    confirm_user = tk.Label(login_labelframe, text='Confirm Username: ', font=('Georgie',11,'bold'),fg='white',bg=rgist['bg'])
    confirm_user.grid(row=0,column=0,pady=20)
    entry_user= tk.Entry(login_labelframe, font=('Georgie',11), bg=rgist['bg'], fg='white')
    entry_user.grid(row=0,column=1,pady=20)
    entry_user.bind('<Return>', lambda event: entry_pass.focus_set())
    #confirm password
    confirm_pass = tk.Label(login_labelframe, text='Confirm Password: ', font=('Georgie',11,'bold'),fg='white',bg=rgist['bg'])
    confirm_pass.grid(row=1,column=0,pady=20)
    entry_pass= tk.Entry(login_labelframe, font=('Georgie',11),fg='white', bg=rgist['bg'],show='▪')
    entry_pass.grid(row=1,column=1,pady=20)

    def verify_credentials(*args):
        username_verify = entry_user.get()
        pass_verify = entry_pass.get()
        #Check verification:
        if not username_verify or not pass_verify:
            messagebox.showwarning('Verification',"Can't let your in with empty necessary fields!")
            return
        if username_verify != username or pass_verify != password:
            messagebox.showwarning('Verification',"Username or Password don't match your profile info..")
            return
        db = sqlite3.connect('login.sql')  # Open sql file with all 'login' stored info
        cursor = db.cursor()
        cursor.execute("SELECT * FROM login WHERE username=? AND password=?", (username, password))
        row = cursor.fetchone()
        db.close()
        if row:
            messagebox.showinfo('Login', 'Logged In Successfully!')
            rgist.destroy()
            homepage(row[0], row[1], row[2], row[3])  # using row as an array
        else:
            messagebox.showerror('Login Failed', 'Invalid username/pass or empty fields.')
    login_btn = tk.Button(login_labelframe, text='Login', bg=rgist['bg'], fg='white', height=2, width=10, command=verify_credentials)
    login_btn.grid(row=2, column=0, columnspan=2, pady=20)
    login_btn.bind('<Return>', lambda event: verify_credentials())
    rgist.mainloop()
def on_hover(a):
    a.widget.config(bg='black',font=('Times',9,'underline','bold','italic'),fg='light blue')
def off_hover(b):
    b.widget.config(bg='black',font=('Times',9,'italic'), fg='light blue')
def activate_profile(p):
    p.widget.config(font=('Georgia',12,'italic','bold', 'underline'),bg='#002366',fg='white')
def shut_profile(r):
    r.widget.config(font=('Georgia',12,'italic','bold'),bg='#002366',fg='white')
def homepage(username,password,email,age):
    root = tk.Tk()
    root.geometry("1330x850")
    root.configure(bg="#002366")
    root.resizable(False,False)
    root.title("Rani's MainApp Project")

    icon_img = PhotoImage(file=r"C:\Users\ranla\PycharmProjects\proj_images\Cyber10th - 1.png") # On its default next to the title we'd see a blue pan presenting Tkinter-Icon, but now I replaced it with a photo of MY app icon
    root.iconphoto(False, icon_img)
    #Main window title:
    wel_label = tk.Label(root, text="Welcome To My Arm-Wrestling Application!", font=('Georgie', 20,'bold','underline'), bg=root['bg'], fg="white")
    wel_label.grid(row=0, column=1,sticky='ew')
    style = ttk.Style() # adjust title for ttk frame (info)
    style.configure('Info.TFrame', background='black', borderwidth=5)
    #main Frames: each one leads to a different page. Each pege will contain a button for the user to come back to the main page.
    #Profile information Label Frame
    Profile = LabelFrame(root, bg=root['bg'], width=350, height=50,relief='groove')
    Profile.grid(row=2,column=3,sticky='sw')
    def display_info():
        disif = Toplevel(root)
        disif.geometry('400x300')
        disif.configure(bg='gray')
        display_disif = tk.LabelFrame(disif, text="User Profile", bg=disif['bg'], fg='white', height=250, width=200)
        display_disif.grid(padx=50, pady=20, sticky="nsew")  # added sticky parameter
        s_pass = tk.BooleanVar(value=False) # for making the pass on its default invisible
        #Added icon-images for password visibility
        closed = PhotoImage(file=r"C:\Users\ranla\PycharmProjects\proj_images\closed.png")
        opened = PhotoImage(file=r"C:\Users\ranla\PycharmProjects\proj_images\opened.png")
        def tog_pass(): # with a click of a button pass will be visible entirely
            s_pass.set(not s_pass.get())
            update_prof()

        def update_prof(): # will update the variables of the profile page according to values from 'login.sql'
            pass_display = '▪'*len(password) # hide pass
            eye_state = closed # set eye state
            if s_pass.get(): #If button pressed:
                pass_display = password # show pass
                eye_state=opened # change eye-state
            # Unnecessary fields display:
            email_disp = email if email else "Blank" #display only if exist
            age_disp = age if age else "Blank" #same as email parameter
            prof_text = (f"Username: {username}\n\n"
                         f"Password: {pass_display}\n\n"
                         f"Age: {age_disp}\n\n"
                         f"Email/Number: {email_disp}")
            prof_lbl.config(text=prof_text) #add text in label
            tog_btn.config(image=eye_state) # image button update according to eye state

        prof_lbl = tk.Label(display_disif, text="", font=('Georgian', 11), bg=disif['bg'], fg='white', justify=tk.LEFT) # display the profile data
        prof_lbl.grid(row=0, column=0, pady=10, padx=10, sticky='w')
        tog_btn = tk.Button(display_disif, image=closed, bg=disif['bg'], fg='cyan', relief='groove', command=tog_pass, bd=0)
        tog_btn.grid(row=0, column=2, pady=5,sticky='e')
        update_prof()

    prof_img = PhotoImage(file=r"C:\Users\ranla\PycharmProjects\proj_images\profile_logo.png")
    img_lbl = tk.Label(Profile,image=prof_img)
    img_lbl.grid(row=0,column=0,sticky='w')
    prof_btn = tk.Button(Profile, text='Your Profile Information', font=('Georgia',12,'italic','bold'),bg=root['bg'],fg='white',relief='flat', command=display_info)
    prof_btn.grid(row=0,sticky='e',padx=75)
    prof_btn.bind('<Enter>', activate_profile)
    prof_btn.bind('<Leave>', shut_profile)

    #FeedBack Display
    feedback_lf = tk.LabelFrame(root, text="Your FeedBack:", font=('George',11,'bold'), bg=root['bg'], fg='white', width=500, height= 220)
    feedback_lf.grid(row=1,column=1,padx=70)
    feed_lbl = tk.Label(feedback_lf, text="Nothing yet",font=('Georgia',11), bg=root['bg'],fg='white', justify=tk.LEFT,wraplength=450)
    feed_lbl.grid()
    #Technique
    Technique = tk.LabelFrame(root, bg='black', width=350, height=250, relief='groove')
    Technique.grid(row=1, column=0, pady=10, padx=5, sticky='nw')
    Tech_label = tk.Label(Technique, text="Arm-Wrestling Technique", font=('Arial',15,'bold'), bg='black',fg='cyan3')
    Tech_label.grid(row=1, column=0,pady=10 ,padx=5 , sticky='ew')
    Tech_area = tk.LabelFrame(Technique, bg='black', bd=2, relief='sunken', width=330, height=170)
    Tech_area.grid(row=2, column=0, padx=10, pady=10)
    tech_lbl = tk.Label(Tech_area,text='Would you want to learn secret \ntechniques to beat everyone in seconds?', bg='black',fg='white',font=('Georgian',11,'italic'))
    tech_lbl.grid(pady=50,padx=30)
    #Here we opened the Top In The Sport page
    def tech_arms():
        techs = tk.Toplevel(root)
        techs.geometry('600x700')
        techs.configure(bg='#002366')
        techs.title("Learn to pin in 3 seconds")
        techs.resizable(False, False)

        lbl_techs = tk.Label(techs,text="Master the basic techniques in the sport", font=('Times', 14, "bold",'underline'),bg=techs['bg'], fg='white')
        lbl_techs.grid(row=0,padx=150)
        various = tk.LabelFrame(techs, text="Various Techniques", bg='black',fg='white',width=400,height=400)
        various.grid(row=1)
        #top-roll
        toproll_labelf = tk.LabelFrame(various, bg=techs['bg'], text='TOP-ROLL', fg='white')
        toproll_labelf.grid(column=0, row=0, pady=10)
        toproll_txt = ("The toproll (or toprolling) is an outside arm wrestling style \ncharacterized by pronating the hand and forearm\n"
                       "to apply wrist pressure on the opponent, \nwhile pulling back and sideways to control the opponent's hand.")
        top_roll = tk.Label(toproll_labelf, text=toproll_txt, fg='white',bg=techs['bg'], font=('Franklin',11,'italic'), justify=tk.LEFT)
        top_roll.grid(row=0,padx=40,pady=5)
        #hook
        hook_labelf = tk.LabelFrame(various,bg=techs['bg'], text='HOOK', fg='white')
        hook_labelf.grid(column=0, row=1, pady=10)
        hook_txt = ("The hook is an inside pulling technique in armwrestling. \n"
                    "It involves supinating your hand and cupping your wrist "
                    "aiming to secure\n a grip inside your opponent's hand."
                    "Maintain a tight angle \nbetween your forearm and bicep to maximize leverage.\n"
                    "Once this position is established, \napply side pressure to pull your opponent's"
                    "hand towards the pin pad.\n A strong hook relies on wrist flexion, supination control, and lat strength.")
        hook = tk.Label(hook_labelf, text=hook_txt, font=('Franklin',11,'italic'),bg=techs['bg'],fg='white',justify = tk.LEFT)
        hook.grid(padx=10,pady=10)
        #press
        press_labelf = tk.LabelFrame(various, bg=techs['bg'],fg='white',text='PRESS')
        press_labelf.grid(column=0,row=2,pady=5)
        press_txt = ("The press is a techniqe in which you mostly use your"
                     "tricep and forearm.\n We have couple of forms for these techniques:\n"
                     "hook form with supination and flop press \nin which you sacrifice your wrist and using your fingers.\n"
                     "For keeping the advantage on the table, \nyou'd use your body weight maintaining height. ")
        press = tk.Label(press_labelf, text=press_txt, font=('Franklin',11,'italic'),bg=techs['bg'],fg='white',justify=tk.LEFT)
        press.grid(padx=10,pady=10)
        # Added link for a youtube video explaining mentioned techniques.
        links = tk.LabelFrame(techs,text='Links',bg=techs['bg'],fg='white',width=400,height=150)
        links.grid(row=2)
        techs_link = tk.Label(links, text="Technique Features Arm-Wrestling - Real Link", cursor='hand2',fg='cyan3',font=('Georgie',10,'underline'), bg=techs['bg'], justify= tk.LEFT)
        techs_link.grid(pady=10,padx=100)
        techs_link.bind('<Button-1>', lambda x: webbrowser.open_new('https://www.youtube.com/watch?v=WxI66b1zaqg'))
        def back_home():
            techs.destroy()
        to_homepage = tk.Button(techs, bg=techs['bg'],text="Back To Home",fg= 'white', font=('Franklin',11,'bold'), command = back_home)
        to_homepage.grid(row=3,sticky='s',pady=30)
        techs.mainloop()

    tech_btn = tk.Button(Tech_area, text='click me...',bd=0,bg='black',fg='light blue',font=('Times',9,'italic'), command=tech_arms)
    tech_btn.grid(sticky='se')
    tech_btn.bind('<Enter>',on_hover)
    tech_btn.bind('<Leave>',off_hover)

    #Top Arm-Wrestlers
    Top_ArmWrestlers = tk.LabelFrame(root, bg='black', width=350, height=250, relief='groove')
    Top_ArmWrestlers.grid(row=1, column=3, pady=10, padx=5,sticky='nw')
    Tech_label = tk.Label(Top_ArmWrestlers, text="Top Strongest In The Sport", font=('Arial',15,'bold'), bg='black',fg='cyan3')
    Tech_label.grid(row=1, column=0,pady=10 ,padx=5 , sticky='ew')
    top_area = tk.LabelFrame(Top_ArmWrestlers, bg='black', bd=2, relief='sunken', width=330, height=170)
    top_area.grid(row=2, column=0, padx=8, pady=10)
    top_lbl = tk.Label(top_area,text='Would you wanna get known with the \ntop in the sport?', bg='black',fg='white',font=('Georgian',11,'italic'))
    top_lbl.grid(pady=50,padx=50)
    #Here we opened the Top In The Sport page
    def top_arms():
        top_s = tk.Toplevel(root)
        top_s.geometry('1300x700')
        top_s.configure(bg='#002366')
        top_s.resizable(False,False)
        best_lbl = tk.Label(top_s, text="Left And Right Strongest Arm-Wrestlers Board", font=('Franklin',14,'underline','bold'), bg=top_s['bg'], fg='white')
        best_lbl.grid(column=1,sticky='n')
        # Split the screen to two boards, left-handed and right-handed:
        #TOP10_LEFT
        best_left = tk.LabelFrame(top_s, bg="black", fg='white', text='Best On The Left', width=300, height=450, font=('Franklin', 12, 'bold'))
        best_left.grid(column=0, row=0, sticky='wsn', pady=50, padx=10)
        # Vitalii Laletin
        vitalii_frame = tk.LabelFrame(best_left, text="1", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        vitalii_frame.grid(row=0, pady=5,sticky='ew')
        vitalii_label = tk.Label(vitalii_frame, text="1. Vitalii Laletin", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        vitalii_label.grid(column=1, padx=100)
        # Artyum Morozov
        artyum_frame = tk.LabelFrame(best_left, text="2", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        artyum_frame.grid(row=1, pady=5,sticky='ew')
        artyum_label = tk.Label(artyum_frame, text="2. Artyum Morozov", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        artyum_label.grid(column=1,padx=100)
        # David
        david_frame = tk.LabelFrame(best_left, text="3", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        david_frame.grid(row=2, pady=5,sticky='ew')
        david_label = tk.Label(david_frame, text="3. David Dadikyan", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        david_label.grid(column = 1,padx=100)
        # Alex
        alex_frame = tk.LabelFrame(best_left, text="4", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        alex_frame.grid(row=3, pady=5,sticky='ew')
        alex_label = tk.Label(alex_frame, text="4. Alex Kurdecha", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        alex_label.grid(column=1,padx=100)
        # Aalizhan
        aalizhan_frame = tk.LabelFrame(best_left, text="5", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        aalizhan_frame.grid(row=4, pady=5,sticky='ew')
        aalizhan_label = tk.Label(aalizhan_frame, text="5. Alizhan Muratov", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        aalizhan_label.grid(column=1,padx=100)
        # Ivan
        ivan_frame = tk.LabelFrame(best_left, text="6", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        ivan_frame.grid(row=5, pady=5,sticky='ew')
        ivan_label = tk.Label(ivan_frame, text="6. Ivan Matyushenko", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        ivan_label.grid(column=1,padx=100)
        # Kamil
        kamil_frame = tk.LabelFrame(best_left, text="7", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        kamil_frame.grid(row=6, pady=5,sticky='ew')
        kamil_label = tk.Label(kamil_frame, text="7. Kamil Jablonski", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        kamil_label.grid(column=1,padx=100)
        # Tobias
        tobias_frame = tk.LabelFrame(best_left, text="8", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        tobias_frame.grid(row=7, pady=5,sticky='ew')
        tobias_label = tk.Label(tobias_frame, text="8. Tobias Sporrong", bg=top_s['bg'], fg='white',font=('Arial', 12, 'bold'))
        tobias_label.grid(column=1,padx=100)
        # Georgi
        georgi_frame = tk.LabelFrame(best_left, text="9", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        georgi_frame.grid(row=8, pady=5,sticky='ew')
        georgi_label = tk.Label(georgi_frame, text="9. Georgi Dzeranov", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        georgi_label.grid(column=1,padx=100)
        # Wanger
        wanger_frame = tk.LabelFrame(best_left, text="10", bg=top_s['bg'], fg='white', font=('Arial', 10),width=300)
        wanger_frame.grid(row=9, pady=5, sticky='ew')
        wanger_label = tk.Label(wanger_frame, text="10. Wanger Bortolato", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        wanger_label.grid(column=1,padx=100)

        #TOP10_RIGHT
        best_right = tk.LabelFrame(top_s,bg="black",fg='white',text='Best On The Right', width=300, height=450, font=('Franklin',12,'bold'))
        best_right.grid(column=2,row=0,pady=50,sticky='esn',padx=10)
        #Levan
        levan_frame = tk.LabelFrame(best_right, text="1", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        levan_frame.grid(row=0, pady=5, sticky='ew')
        levan_label = tk.Label(levan_frame, text="1. Levan Saginashvili", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        levan_label.grid(column=0, padx=100)
        #Devon
        devon_frame = tk.LabelFrame(best_right, text="2", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        devon_frame.grid(row=1, pady=5, sticky='ew')
        devon_label = tk.Label(devon_frame, text="2. Devon Larratt", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        devon_label.grid(column=0, padx=100)
        #Ermes
        ermes_frame = tk.LabelFrame(best_right, text="3", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        ermes_frame.grid(row=2, pady=5, sticky='ew')
        ermes_label = tk.Label(ermes_frame, text="3. Ermes Gasparini", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        ermes_label.grid(column=0, padx=100)
        #Jerry
        jerry_frame = tk.LabelFrame(best_right, text="4", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        jerry_frame.grid(row=3, pady=5, sticky='ew')
        jerry_label = tk.Label(jerry_frame, text="4. Jerry Cadorette", bg=top_s['bg'], fg='white',  font=('Arial', 12, 'bold'))
        jerry_label.grid(column=0, padx=100)
        #Michael
        michael_frame = tk.LabelFrame(best_right, text="5", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        michael_frame.grid(row=4, pady=5, sticky='ew')
        michael_label = tk.Label(michael_frame, text="5. Michael Todd", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        michael_label.grid(column=0, padx=100)
        #Genadi
        genadi_frame = tk.LabelFrame(best_right, text="6", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        genadi_frame.grid(row=5, pady=5, sticky='ew')
        genadi_label = tk.Label(genadi_frame, text="6. Genadi Kvikvinia", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        genadi_label.grid(column=0, padx=100)
        #Alex
        alex_right_frame = tk.LabelFrame(best_right, text="7", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        alex_right_frame.grid(row=6, pady=5, sticky='ew')
        alex_right_label = tk.Label(alex_right_frame, text="7. Alex Kurdecha", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        alex_right_label.grid(column=0, padx=100)
        # 8. Georgi Tsvetkov
        georgi_right_frame = tk.LabelFrame(best_right, text="8", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        georgi_right_frame.grid(row=7, pady=5, sticky='ew')
        georgi_right_label = tk.Label(georgi_right_frame, text="8. Georgi Tsvetkov", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        georgi_right_label.grid(column=0, padx=100)
        # 9. Vitalii Laletin
        vitalii_right_frame = tk.LabelFrame(best_right, text="9", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        vitalii_right_frame.grid(row=8, pady=5, sticky='ew')
        vitalii_right_label = tk.Label(vitalii_right_frame, text="9. Vitalii Laletin", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        vitalii_right_label.grid(column=0, padx=100)
        # 10. Artyum Morozov
        artyum_right_frame = tk.LabelFrame(best_right, text="10", bg=top_s['bg'], fg='white', font=('Arial', 10), width=300)
        artyum_right_frame.grid(row=9, pady=5, sticky='ew')
        artyum_right_label = tk.Label(artyum_right_frame, text="10. Artyum Morozov", bg=top_s['bg'], fg='white', font=('Arial', 12, 'bold'))
        artyum_right_label.grid(column=0, padx=100)
        def back_home():
            top_s.destroy()
            root.deiconify()
        to_homepage = tk.Button(top_s, bg=top_s['bg'],text="Back To Home",fg= 'white', font=('Franklin',11,'bold'), command = back_home)
        to_homepage.grid(column=1,row=3,sticky='s')
        top_s.mainloop()

    top_btn = tk.Button(top_area, text='click me...',bd=0,bg='black',fg='light blue',font=('Times',9,'italic'), command=top_arms)
    top_btn.grid(sticky='se')
    top_btn.bind('<Enter>',on_hover)
    top_btn.bind('<Leave>',off_hover)

    #Arm-Wrestling Deeper explanation
    Explain = tk.LabelFrame(root, bg='black', width=350, height=250, relief='groove')
    Explain.grid(row=2, column=0 ,pady=10, padx=5,sticky='sw')
    Tech_label = tk.Label(Explain, text="Deeper Explanation Of The Sport", font=('Arial',15,'bold'), bg='black',fg='cyan3')
    Tech_label.grid(row=1, column=0,pady=10 ,padx=5 , sticky='ew')
    explain_area = tk.LabelFrame(Explain, bg='black', bd=2, relief='sunken', width=330, height=170)
    explain_area.grid(row=2, column=0, padx=10, pady=10)
    exp_lbl = tk.Label(explain_area,text='Would you like to learn deeper about the sport?', bg='black',fg='white',font=('Georgian',11,'italic'))
    exp_lbl.grid(row=0, pady=50,padx=10)
    #Here we opened a new page getting the user with the sport
    def learn_more():
        learn = tk.Toplevel(root)
        learn.geometry('800x800')
        learn.configure(bg='#002366')
        learn.resizable(False,False)
        learn_lbl = tk.Label(learn, text='About The Arm Wrestling Sport:', font=('Franklin',14,'underline','bold'),bg=learn['bg'],fg='white')
        learn_lbl.grid(row=0,padx=160,sticky='n')
        #Background info and what is the sport:
        learnlf = tk.LabelFrame(learn, text='Explanation of the sport',bg=learn['bg'],height=500, width=550, fg='white')
        learnlf.grid(padx=50,row=1, pady=50)
        in_short_text=("Arm-Wrestling is a sport that got known by the middle of the 20th century. \n"
                       "Because of the fact most people didn't see it \nas a real sport(and a lot yet doubt it) we only know \n"
                       "the first recorded competition was in US,California 1952."
                       "Most people look at arm wrestling with their sense,\n the biggest guy at the table wins..\n "
                       "Actually, this is far from truth, \narm wrestling is a complex, very technical sport.\n "
                       "Requiring years of training and learning \ndifferent techniques including wrist perfecting positioning.\n"
                       "Honestly, some athletes like to present it like Chess.\n"
                       "For being successful in arm wrestling,\nyou need a combination of arm strength and technique.\n"
                       "In a different episode you'll learn various techniques.")
        learntext= tk.Label(learnlf, text=in_short_text, font=('Franklin',11,'italic'),bg=learn['bg'],fg='white',justify=tk.LEFT)
        learntext.grid(row=0)
        #My connection to the arm-wrestling world.
        myexp = tk.LabelFrame(learn,text='Me&Sport', height=70,width=500,bg=learn['bg'],fg='white')
        myexp.grid(padx=50,row=2,sticky='sew')
        my_text = ("Last summer I injured my right shoulder leading me \nto leave the Calisthenics world "
                   "and Capoeira, \nwhich was a platform that have been beside me \nsince I was 4 years old."
                   "I did not want it to stop me, \nI chose a sport in which I can grow with only one hand\n"
                   "Which lead me into the Arm-wrestling world.\nAs a result, I chose to do my project about it.\n"
                   "I want to add a link for my favorite arm-wrestler explanation about the sport.\n A person which is also a great influencer in the sport.")
        myexp_lbl = tk.Label(myexp,text=my_text, font=('Franklin',11,'italic'), bg=learn['bg'],fg='white',justify=tk.LEFT)
        myexp_lbl.grid(padx=5)
        links = tk.LabelFrame(learn,text='Links',fg = 'white', bg= learn['bg'],height=120,width=550)
        links.grid(row=3,pady=30)
        devon_exp= tk.Button(links, text="One of the greatest influencers in the the sport about Arm-Wrestling",
                          bg=learn['bg'], fg='cyan3', cursor='hand2',font=('Georgie',10,'underline',), justify=tk.LEFT, bd=0)
        devon_exp.grid(padx=120,pady=25)
        devon_exp.bind('<Button-1>', lambda x: webbrowser.open_new('https://www.youtube.com/watch?v=WxmEyqxtL1Y'))
        def back_home():
            learn.destroy()
            root.deiconify()
        to_homepage = tk.Button(learn, bg=learn['bg'],text="Back To Home",fg= 'white', font=('Franklin',11,'bold'), command = back_home)
        to_homepage.grid(row=4,sticky='s', pady=15)
        learn.mainloop()

    exp_btn = tk.Button(explain_area, text='Learn more...',bd=0,bg='black',fg='light blue',font=('Times',9,'italic'), command=learn_more)
    exp_btn.grid(column=0,sticky='se')
    exp_btn.bind('<Enter>',on_hover)
    exp_btn.bind('<Leave>',off_hover)
    # Footer - info Frame
    info = ttk.Frame(root, style='Info.TFrame', width=1100, height=200)
    info.grid(row=4, column=0, columnspan=4, sticky="sew", pady=(50, 0))
    # Configure grid weights to help with centering:
    for i in range(12):  # Increase range to include all columns
        info.grid_columnconfigure(i, weight=1)
    label1 = tk.Label(info, image=icon_img) # app-icon display
    label1.grid(row=0, column=0, pady=10, padx=10, sticky='w')
    label2 = tk.Label(info, text="About The Site:", font=('Arial', 12, 'bold'), bg='black', fg='white')
    label2.grid(row=0, column=1, pady=1, sticky='nw')
    # a little about my experience building the app
    footer_txt = ("I built the application from passover until Shavuot and it went pretty well.\n"
                  "Definitely upgraded my abilities in Python and Tkinter library!")
    info2 = tk.Label(info, text=footer_txt, font=('Helvetica', 11, 'italic'), bg='black', fg='white')
    info2.grid(row=0, column=1, padx=1, sticky='w')
    # Center the copyright mention by spanning multiple columns
    mention = tk.Label(info, text="©Arm-Wrestling Academy | May 2025", font=('Helvetica', 9, 'italic'), fg='white', bg='black')
    mention.grid(row=1, column=0, columnspan=12, sticky='s')  # Changed to row 1 and spanning all column
    comment_lf = tk.LabelFrame(info, text='Add Comments here', relief='sunken', bg='black', width=350, height=100, font=('Times', 10, 'italic'), fg='cyan')
    comment_lf.grid(row=0, column=2, sticky='e')
    comment_label= tk.Label(comment_lf,text='For More Information: 050-696-5688',font=('Times', 9, 'italic','underline'),bg='black',fg='white')
    comment_label.grid(row=0,column=0,sticky='new',padx=20,pady=15)

    def feed_sql(rate,perspective,comment,recommend): #Sql for storing the collected data out of the feedback form
        db_1 = sqlite3.connect('feedback.sql')
        cursor = db_1.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS feedback(rate INTEGER, comment TEXT, perspective INTEGER, recommend TEXT)')
        cursor.execute('INSERT INTO feedback(rate,comment,perspective,recommend) VALUES(?,?,?,?)',(rate,comment,perspective,recommend))
        db_1.commit()
        cursor.execute("SELECT * FROM feedback WHERE rate=? AND comment=? AND perspective=? AND recommend=?", (rate,comment,perspective,recommend))
        row_feed = cursor.fetchone()
        db_1.close()
        return row_feed
    def update_feed(rate,perspective,comment,recommend):
        # Update sql parameters
        feed_txt = (f"Rate of experience: \t\t{rate}/10\n"
               f"Impact of the content: \t{perspective}/10\n"
               f"Your thoughts&Ideas: \t\t\n{comment}"
               f"Do you currently recommend it?       {recommend}.\n")
        feed_lbl.config(text=feed_txt) #configure the label of the feedback accordingly
    def FeedBack(username,password,email,age):
        feed = Toplevel(root)
        feed.geometry('1000x800')
        feed.configure(bg='#002366')
        feed.resizable(False,False)
        global rate #Set all parameters global for using them through 3 functions
        global comment
        global perspective
        global recommend
        #welcome to window
        feed_lbl = tk.Label(feed,text="Feedback!", font=('New Time Orlin',20,'bold','underline'),bg=feed['bg'],fg='white')
        feed_lbl.grid(column=0,padx=300,sticky='n')
        #Form Frame
        feed_fl = tk.LabelFrame(feed, text='Feedback Form', font=('Times', 12, 'italic', 'bold'), bg=feed["bg"], fg='white',height=350, width=600)
        feed_fl.grid(column=0,row=1,pady=50,sticky='ns')
        #Username:
        lbl_feed = tk.Label(feed_fl, text=f"Username: \t\t{username}", font=('Franklin',11, 'bold'), bg=feed['bg'],fg='white')
        lbl_feed.grid(row=0, pady=25,sticky='n')
        #new frame which will contain more of advances widgets keeping it all organized
        overall = tk.LabelFrame(feed_fl, text='Over All Experience', bg= 'black', fg='white')
        overall.grid(row=1, columnspan=5,column=0, padx=50, pady=10)
        #rate
        rate_lf = tk.LabelFrame(overall, bg=feed['bg'], fg='white')
        rate_lf.grid(row=0,padx=1,pady=1,sticky='ew')
        tk.Label(rate_lf, text="1. Rate The Over-All App Experience: ", font=('George',11,'underline'),bg=feed['bg'],fg='white').grid(row=0,column=0,sticky='w')
        satisfaction = tk.IntVar(value=3)
        Overall_scale = tk.Scale(rate_lf, from_= 1, to=10, orient=tk.HORIZONTAL,bg='black',fg='white', length=250, label="Rate Your App Experience:", variable=satisfaction)
        Overall_scale.grid(row=0, column=1,pady=30,padx=120)
        #Comments --> scrolled text
        comment_lf = tk.LabelFrame(overall, bg=feed['bg'], fg='white')
        comment_lf.grid(row=1,padx=1,pady=1,sticky='ew')
        comment_label = tk.Label(comment_lf, text="2. I will be happy to hear your thoughts/suggestions:", font=('George', 11, 'underline'), bg=feed['bg'], fg='white')
        comment_label.grid(row=0, sticky='w')
        comments = scrolledtext.ScrolledText(comment_lf, wrap=tk.WORD,bg=feed['bg'],fg='white', font=('George',11,'italic'), width=70, height=6)
        comments.grid(row=1, sticky='e',pady=15,padx=2.5)
        #perspective
        app_effect_lf = tk.LabelFrame(overall, bg=feed['bg'], fg='white')
        app_effect_lf.grid(row=2,padx=1,pady=1,sticky='ew')
        tk.Label(app_effect_lf, text="3. Did it change your perspective about Arm-Wrestling?", font=('George',11,'underline'), bg=feed['bg'], fg='white').grid(row=0, column=0, sticky='w')
        fun = tk.IntVar(value=5)
        fun_scale = tk.Scale(app_effect_lf, from_= 1, to=10, orient=tk.HORIZONTAL,bg='black',fg='white', length=250, label="1=Absolutely Not  10=Yeah, Of course!", variable=fun)
        fun_scale.grid(row=0, column=1,padx=100,pady=30,sticky='e')
        #Radio_button --> recommend
        recommendation_lf = tk.LabelFrame(overall, bg=feed['bg'], fg='white')
        recommendation_lf.grid(row=3,padx=1,pady=1,sticky='ew')
        recommendation = tk.Label(recommendation_lf, text="4. Would you recommend using this app?", font=('George',11,'underline'), bg=feed['bg'], fg='white')
        recommendation.grid(row=0, column=0, sticky='w', pady=10)
        options = ["I Do Recommend","I Don't Recommend"]
        radio_val = tk.IntVar()
        # radio_val.set(1)
        return_val_string = ""
        def active_radio():
            global return_val_string
            if radio_val.get() == 0:
                return_val_string = "I Do Recommend"
            elif radio_val.get() == 1:
                return_val_string = "I Don't Recommend"
            # No other option.
        for i in range(len(options)):
            radio_btn = tk.Radiobutton(recommendation_lf, text=options[i], bg=feed['bg'],fg='red', font=('George', 11),variable=radio_val, value = i, command=active_radio)
            radio_btn.grid(row=0, column=(i+1), pady=10)
        #Submition
        def back_to_home():
            rate = satisfaction.get()
            comment = comments.get('1.0', tk.END)
            perspective = fun.get()
            recommend = options[radio_val.get()]
            if not rate or not comment or not perspective or not recommend:
                messagebox.showwarning('FeedBack', "Empty fields.. You have to fill all before submission")
                return
            data_kept = feed_sql(rate, perspective, comment, recommend)
            if data_kept:
                messagebox.showinfo('FeedBack',"I appreciate your feedback!")
                update_feed(rate, perspective, comment, recommend)
                feed.withdraw()
        to_homepage = tk.Button(feed, text="Submit Feedback", font=('George',11,'bold'), bg=feed['bg'], fg='white',command= lambda: back_to_home(), relief='sunken')
        to_homepage.grid(row=2,sticky='s',padx=10)
        feed.mainloop()
    comment_btn = tk.Button(comment_lf,text='Feedback Form',font=('Times',9,'italic'),fg='light blue',bg='black', command=lambda: FeedBack(username,password,email,age), bd=0)
    comment_btn.grid(row=1,column=1,sticky='s',padx=20,pady=10)
    comment_btn.bind('<Enter>', on_hover)
    comment_btn.bind('<Leave>', off_hover)

    root.mainloop() # end of homepage function
if __name__ == "__main__":
    sing_up() # at the very begging as expected I'd want to take data and store it