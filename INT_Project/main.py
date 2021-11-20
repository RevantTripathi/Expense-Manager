from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector as sql


l = []


def open_home():
    def create_database_if_not_found():

        def create_account_table():

            c = sql.connect(host="localhost", database='expense_manager', username="root", passwd="AT06bh@$")
            c_cur = c.cursor()
            c_cur.execute(
                "CREATE TABLE account_list (SR int AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Email VARCHAR(255), acc_type VARCHAR(40), income int(10))")
            c.commit()
            c_cur.close()
            c.close()

        s = sql.connect(host="localhost", username="root", passwd="AT06bh@$")
        cur = s.cursor()
        cur.execute("SHOW DATABASES")
        j = 0
        for i in cur:
            if (i[0] == "expense_manager"):
                j = 1
                break
        if (j == 1):
            return
        else:
            cur.execute("create database expense_manager")
            s.commit()
            create_account_table()
            cur.close()
            s.close()

    home = Tk()
    home.geometry("1100x700")
    home.title("Expense Manager")

    create_database_if_not_found()

    head = Label(home, text="Expense Manager", font=("Arial", 50), bg="#F2CC8F", fg="purple", relief="ridge",
                 borderwidth=5)
    head.place(relx=0.5, rely=0.03, anchor=N)

    def add_acc_win():

        window = Toplevel()
        window.title("Expense Manager")
        window.geometry('500x550')
        window.title("Expense Manager")
        window.maxsize(500, 550)

        def act():
            global l

            c = sql.connect(host="localhost", database='expense_manager', username="root", passwd="AT06bh@$")
            c_cur = c.cursor()
            name = b1.get()
            email = c1.get()
            t_ype = clicked.get()
            In = f1.get()

            c_cur.execute(
                "insert into account_list(Name,Email,acc_type,income) values('{}','{}','{}',{})".format(name, email,
                                                                                                        t_ype, In))
            c_cur.execute(
                "create table {}(SR INT PRIMARY KEY AUTO_INCREMENT,TITLE VARCHAR(100),TYPE VARCHAR(20),SENT_TO_RECIEVED_FROM VARCHAR(100),COST INT,d_ate DATE)".format(
                    name))
            c.commit()
            c_cur.close()
            c.close()
            fetch_acc_list()
            create_option()
            list_box(fetch_acc_list())
            window.destroy()

        def rgb_hack(rgb):
            return "#%02x%02x%02x" % rgb

        window.configure(bg=rgb_hack((237, 208, 159)));
        doo = Label(window, text="New Registration", font=("Serif", 18, "bold"), bg=rgb_hack((237, 208, 159)))
        doo.place(x=160, y=18)
        b = Label(window, text="Name", font=("Serif", 9))
        b.place(x=130, y=110)
        c = Label(window, text="Email Id", font=("Serif", 9))
        c.place(x=130, y=150)
        e = Label(window, text="Type", font=("Serif", 9))
        e.place(x=130, y=230)
        f = Label(window, text="Income (Monthly)", font=("Serif", 9))
        f.place(x=130, y=270)

        b1 = Entry(window)
        b1.place(x=250, y=110)
        c1 = Entry(window)
        c1.place(x=250, y=150)
        f1 = Entry(window)
        f1.place(x=250, y=270)

        clicked = StringVar(window)
        clicked.set("SELECT")  # for default selection

        drop = OptionMenu(window, clicked, "Single", "Family")
        drop.place(x=250, y=230)

        bt = Button(window, text="Submit", bd="5", height=1, width=12, font=("Serif", 11), command=act)
        bt.place(x=195, y=320)

        window.mainloop()

    new_acc = Button(home, text="Add account", bg="#F2CC8F", font=("Arial", 18), command=add_acc_win)
    new_acc.place(relx=0.65, rely=0.19)

    open_head = Label(home, text="Select Accounts :", bg="#F2CC8F", fg="purple", font=("Arial", 20))
    open_head.place(relx=0.5, rely=0.3)

    acc_list = LabelFrame(home, padx=20, pady=20, bg="#F2CC8F", width=60)

    def fetch_acc_list():
        l = []
        w = 0
        s = sql.connect(host="localhost", username="root", passwd="AT06bh@$", database="expense_manager")
        s_cur = s.cursor()
        s_cur.execute("select * from account_list")

        for i in s_cur.fetchall():
            l.append(i[1])
            w += 1

        s_cur.close()
        s.close()
        return l

    def list_box(l):
        listbox = Listbox(acc_list, font=("Arial", 17), bg="#F2CC8F", width=30)
        for i in range(len(l)):
            listbox.insert(0, l[i])
        listbox.pack()
        scroll = ttk.Scrollbar(acc_list, orient=VERTICAL)
        listbox.config(yscrollcommand=scroll)
        scroll.config(command=listbox.yview)
        scroll.pack(fill=Y, side=RIGHT)

    list_box(fetch_acc_list())

    open_select = LabelFrame(home, padx=20, pady=20, bg="#F2CC8F", text="select account", font=("Arial", 14))

    l_list = []
    f = StringVar()
    f.set("select")

    def create_option():
        l_list = fetch_acc_list()
        if (l_list == []):
            l_list.append("none")
        account = OptionMenu(open_select, f, *l_list)
        account.config(font=("Arial", 14), bg="#F2CC8F")
        account.grid(row=0, column=0, pady=15, padx=10)

    create_option()

    def dashboard_select():
        home.destroy()
        s = sql.connect(host="localhost", username="root", passwd="AT06bh@$", database="expense_manager")
        s_cur = s.cursor()
        s_cur.execute("select * from account_list")

        for i in s_cur.fetchall():
            if (f.get() == i[1]):
                open_dashboard(i)
                break
        s_cur.close()
        s.close()

    open_b = Button(open_select, text=" Open ", font=("Arial", 14), bg="#F2CC8F", command=dashboard_select)
    open_b.grid(row=1, column=0)

    open_select.place(relx=0.6, rely=0.4)

    acc_head = Label(home, text="Existing Accounts :", bg="#F2CC8F", fg="purple", font=("Arial", 20))
    acc_head.place(relx=0.1, rely=0.3)

    acc_list.place(relx=0.1, rely=0.4)

    fetch_acc_list()
    home.configure(bg="#F2CC8F")
    home.mainloop()


def open_dashboard(j):
    dashboard = Tk()
    dashboard.geometry("1100x700")
    dashboard.title("Expense Manager")

    head = Label(dashboard, text="Dashboard", font=("Arial", 50), bg="#F2CC8F", fg="purple", relief="ridge",
                 borderwidth=5)
    head.place(relx=0.5, rely=0.03, anchor=N)

    def button_analysis_clicked():
        dashboard.destroy()
        account_analysis(j[1], j)

    button_analysis = Button(dashboard, text="Account Analysis", bg="#F2CC8F", font=("Arial", 18),
                             command=button_analysis_clicked)
    button_analysis.place(relx=0.3, rely=0.3)

    def button_transaction_clicked():
        dashboard.destroy()
        open_transaction(j, j[1])

    button_transaction = Button(dashboard, text="Transactions", bg="#F2CC8F", font=("Arial", 18),
                                command=button_transaction_clicked)
    button_transaction.place(relx=0.3, rely=0.2)

    def button_switch_clicked():
        dashboard.destroy()
        open_home()

    button_switch = Button(dashboard, text="Switch account", bg="#F2CC8F", font=("Arial", 18),
                           command=button_switch_clicked)
    button_switch.place(relx=0.5, rely=0.2)

    info = LabelFrame(dashboard, text="Account Info : ", bg="#F2CC8F", fg="purple", font=("Arial", 25))

    name = Label(info, text=j[1], bg="#F2CC8F", font=("Arial", 20))
    name.grid(row=0, column=0, padx=10, pady=15, sticky="W")

    Type = Label(info, text=j[4], bg="#F2CC8F", font=("Arial", 20))
    Type.grid(row=1, column=0, padx=10, pady=15, sticky="W")

    salary = Label(info, text=j[5], bg="#F2CC8F", font=("Arial", 20))
    salary.grid(row=2, column=0, padx=10, pady=15, sticky="W")

    email = Label(info, text=j[2], bg="#F2CC8F", font=("Arial", 20))
    email.grid(row=3, column=0, padx=10, pady=15, sticky="W")

    info.place(relx=0.3, rely=0.4)

    dashboard.configure(bg="#F2CC8F")
    dashboard.mainloop()


def open_transaction(tt, t):
    transaction = Tk()
    transaction.geometry("1100x700")
    transaction.title("Expense Manager")

    head = Label(transaction, text="Transactions", font=("Arial", 50), bg="#F2CC8F", fg="purple", relief="ridge",
                 borderwidth=5)
    head.place(relx=0.5, rely=0.03, anchor=N)

    def button_dashboard_clicked():
        transaction.destroy()
        open_dashboard(tt)

    button_dashboard = Button(transaction, text="Back to dashboard", bg="#F2CC8F", font=("Arial", 18),
                              command=button_dashboard_clicked)
    button_dashboard.place(relx=0.3, rely=0.2)

    def add_trans():
        trans_desc = Toplevel()
        trans_desc.geometry("700x700")
        trans_desc.title("Transaction Info")

        head = Label(trans_desc, text="Transaction details", font=("Arial", 30), bg="#F2CC8F", fg="purple",
                     relief="ridge", borderwidth=5)
        head.place(relx=0.5, rely=0.03, anchor=N)

        details = LabelFrame(trans_desc, text="Enter details ", bg="#F2CC8F", fg="purple", font=("Arial", 20), padx=10,
                             pady=10)

        tr = Label(details, text=" Title- ", font=("Arial", 18), bg="#F2CC8F")
        tr.grid(row=0, column=0, sticky="w", pady=10)

        te = Entry(details, font=("Arial", 18), width=20)
        te.grid(row=0, column=1, sticky="w", columnspan=3, pady=10)

        ty = Label(details, text=" Type:- ", font=("Arial", 18), bg="#F2CC8F")
        ty.grid(row=1, column=0, sticky="w")

        trans_type = ["Entertainment", "Essentials", "investment", "Gift", "Income"]

        var_trans_type = StringVar()

        k = 1

        for i in trans_type:
            r = Radiobutton(details, text=i, value=i, variable=var_trans_type, bg="#F2CC8F", font=("Arial", 18))
            r.grid(row=k, column=1, sticky="w", columnspan=3)
            r.select()
            k += 1

        to = Label(details, text=" Sent to/\nReceived from:- ", font=("Arial", 18), bg="#F2CC8F")
        to.grid(row=6, column=0, sticky="w", pady=10)

        toe = Entry(details, font=("Arial", 18), width=20)
        toe.grid(row=6, column=1, sticky="w", columnspan=3, pady=10)

        date = Label(details, text=" Date :-\n(DD-MM-YYYY) ", font=("Arial", 18), bg="#F2CC8F")
        date.grid(row=7, column=0, sticky="w", pady=10)

        de = Entry(details, font=("Arial", 18), width=2)
        de.grid(row=7, column=1, sticky="w", pady=10)

        me = Entry(details, font=("Arial", 18), width=2)
        me.grid(row=7, column=2, sticky="w", pady=10)

        ye = Entry(details, font=("Arial", 18), width=4)
        ye.grid(row=7, column=3, sticky="w", pady=10)

        cos = Label(details, text=" Cost(Rs.):- ", font=("Arial", 18), bg="#F2CC8F")
        cos.grid(row=8, column=0, sticky="w", pady=10)

        ce = Entry(details, font=("Arial", 18), width=8)
        ce.grid(row=8, column=1, sticky="w", columnspan=3, pady=10)

        details.place(relx=0.15, rely=0.14)

        def verify_trans():
            ti = te.get()
            Type = var_trans_type.get()
            source = toe.get()
            day = de.get()
            mon = me.get()
            yea = ye.get()
            amt = int(ce.get())
            s = sql.connect(host="localhost", username="root", passwd="AT06bh@$", database="expense_manager")
            cur = s.cursor()
            cur.execute(
                "insert into {}(TITLE,TYPE,SENT_TO_RECIEVED_FROM,COST,d_ate) values('{}','{}','{}',{},'{}')".format(t,
                                                                                                                    ti,
                                                                                                                    Type,
                                                                                                                    source,
                                                                                                                    amt,
                                                                                                                    yea + "-" + mon + "-" + day))
            s.commit()
            trans_desc.destroy()

        submit = Button(trans_desc, text=" Add Transaction ", font=("Arial", 18), bg="#F2CC8F", command=verify_trans)
        submit.place(relx=0.36, rely=0.9)

        trans_desc.configure(bg="#F2CC8F")
        trans_desc.mainloop()

    button_add = Button(transaction, text="Add Transaction", bg="#F2CC8F", font=("Arial", 18), command=add_trans)
    button_add.place(relx=0.55, rely=0.2)

    see_t = LabelFrame(transaction, text="See Transactions : ", bg="#F2CC8F", fg="purple", font=("Arial", 25), padx=20,
                       pady=20)

    select = Label(see_t, text="Select the month and year of transactions: ", bg="#F2CC8F", font=("Arial", 20))
    select.grid(row=0, column=0, padx=10, pady=15, sticky="W", columnspan=5)

    transaction_month = {"January": 1, "Febraury": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
                         "August": 8, "September": 9,
                         "October": 10, "November": 11, "December": 12}
    var_month1 = StringVar()
    var_month1.set("January")

    months = OptionMenu(see_t, var_month1, *transaction_month.keys())
    months.config(font=("Arial", 14), bg="#F2CC8F")
    months.grid(row=0, column=5, pady=15, padx=10)

    year = Entry(see_t, width=4, font=("Arial", 14))
    year.insert(END, '2021')
    year.grid(row=0, column=6, ipadx=5, ipady=5)

    def get_transactions(*args):

        y = int(year.get())
        m = transaction_month[var_month1.get()]

        s = sql.connect(host="localhost", username="root", passwd="AT06bh@$", database="expense_manager")
        cur = s.cursor()
        dst = (str(y) + "-" + str(m) + "-01")
        den = (str(y) + "-" + str(m + 1) + "-01")
        cur.execute(
            "select TITLE,TYPE,SENT_TO_RECIEVED_FROM,COST,d_ate from {} where d_ate>='{}' and d_ate<'{}' order by d_ate".format(
                t, dst, den))
        data = cur.fetchall()

        tran_table = Toplevel()
        tran_table.title("Transaction Info")

        col1 = Listbox(tran_table, width=20)
        col2 = Listbox(tran_table, width=15)
        col3 = Listbox(tran_table, width=30)
        col4 = Listbox(tran_table, width=20)
        col5 = Listbox(tran_table, width=20)

        col1.insert(END, "Title")
        col2.insert(END, "Type")
        col3.insert(END, "Source/destination")
        col4.insert(END, "Amount")
        col5.insert(END, "Date")

        col1.insert(END, " ")
        col2.insert(END, " ")
        col3.insert(END, " ")
        col4.insert(END, " ")
        col5.insert(END, " ")

        for i in data:
            col1.insert(END, i[0])
            col2.insert(END, i[1])
            col3.insert(END, i[2])
            col4.insert(END, i[3])
            col5.insert(END, i[4])
        col1.grid(row=0, column=0, pady=20, padx=5)
        col2.grid(row=0, column=1, pady=20, padx=5)
        col3.grid(row=0, column=2, pady=20, padx=5)
        col4.grid(row=0, column=3, pady=20, padx=5)
        col5.grid(row=0, column=4, pady=20, padx=5)

        cur.close()
        s.close()

        tran_table.configure(bg="#F2CC8F")
        tran_table.mainloop()

    b = Button(see_t, text="see transactions", font=("Arial", 14), bg="#F2CC8F", command=get_transactions)
    b.grid(row=1, column=5)

    see_t.place(relx=0.15, rely=0.3)

    transaction.configure(bg="#F2CC8F")
    transaction.mainloop()


def account_analysis(t, tt):
    analysis = Tk()
    analysis.geometry("1100x700")
    analysis.title("Expense Manager")

    head = Label(analysis, text="Account Analysis", font=("Arial", 50), bg="#F2CC8F", fg="purple", relief="ridge",
                 borderwidth=5)
    head.place(relx=0.5, rely=0.03, anchor=N)

    def back():
        analysis.destroy()
        open_dashboard(tt)

    button_back = Button(analysis, text="Back to dashboard", bg="#F2CC8F", font=("Arial", 18), command=back)
    button_back.place(relx=0.6, rely=0.5)

    select_mon = LabelFrame(analysis, text="Select month for analysis ", bg="#F2CC8F", fg="purple", font=("Arial", 20),
                            padx=20, pady=20)

    select = Label(select_mon, text="Select the month and year for summary: ", bg="#F2CC8F", font=("Arial", 15))
    select.grid(row=0, column=0, padx=10, pady=15, sticky="W", columnspan=5)

    months_list = {"January": 1, "Febraury": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                   "September": 9,
                   "October": 10, "November": 11, "December": 12}
    var_month1 = StringVar()
    var_month1.set("January")

    months = OptionMenu(select_mon, var_month1, *months_list.keys())
    months.config(font=("Arial", 14), bg="#F2CC8F")
    months.grid(row=0, column=5, pady=15, padx=10)

    year = Entry(select_mon, width=4, font=("Arial", 14))
    year.insert(END, '2021')
    year.grid(row=0, column=6, ipadx=5, ipady=5)

    def fetch_details():

        y = int(year.get())
        m = months_list[str(var_month1.get())]

        dst = (str(y) + "-" + str(m) + "-01")
        den = (str(y) + "-" + str(m + 1) + "-01")

        s = sql.connect(host="localhost", username="root", passwd="AT06bh@$", database="expense_manager")
        cur = s.cursor()

        cur.execute("select sum(COST) from {} where TYPE='Income' and d_ate>='{}' and d_ate<'{}'".format(t, dst, den))
        income = cur.fetchall()[0][0]

        cur.execute(
            "select sum(COST) from {} where TYPE='Entertainment' and d_ate>='{}' and d_ate<'{}'".format(t, dst, den))
        entertainment = cur.fetchall()[0][0]

        cur.execute(
            "select sum(COST) from {} where TYPE='Essentials' and d_ate>='{}' and d_ate<'{}'".format(t, dst, den))
        essentials = cur.fetchall()[0][0]

        cur.execute(
            "select sum(COST) from {} where TYPE='investments' and d_ate>='{}' and d_ate<'{}'".format(t, dst, den))
        investment = cur.fetchall()[0][0]

        cur.execute("select sum(COST) from {} where TYPE='Gift' and d_ate>='{}' and d_ate<'{}'".format(t, dst, den))
        gift = cur.fetchall()[0][0]

        if (income == None):
            income = 0
        if (entertainment == None):
            entertainment = 0
        if (essentials == None):
            essentials = 0
        if (investment == None):
            investment = 0
        if (gift == None):
            gift = 0

        total = int(essentials) + int(entertainment) + int(gift) + int(investment)

        details = LabelFrame(analysis, bg="#F2CC8F", fg="purple", font=("Arial", 20), padx=8, pady=8)

        ex_enter = Label(details, text="Expenses of entertainment : " + str(entertainment), bg="#F2CC8F",
                         font=("Arial", 14))
        ex_enter.grid(row=1, column=0, padx=10, pady=15, sticky="W")

        ex_essen = Label(details, text="Expenses of essentials : " + str(essentials), bg="#F2CC8F", font=("Arial", 14))
        ex_essen.grid(row=2, column=0, padx=10, pady=15, sticky="W")

        ex_gift = Label(details, text="Expenses of gifts : " + str(gift), bg="#F2CC8F", font=("Arial", 14))
        ex_gift.grid(row=3, column=0, padx=10, pady=15, sticky="W")

        inc = Label(details, text="Total Income : " + str(income), bg="#F2CC8F", font=("Arial", 14))
        inc.grid(row=0, column=0, padx=10, pady=15, sticky="W")

        ex_inv = Label(details, text="Expenses on investments : " + str(investment), bg="#F2CC8F", font=("Arial", 14))
        ex_inv.grid(row=4, column=0, padx=10, pady=15, sticky="W")

        ex_tot = Label(details, text="Total expenses : " + str(total), bg="#F2CC8F", font=("Arial", 14))
        ex_tot.grid(row=5, column=0, padx=10, pady=15, sticky="W")

        details.place(relx=0.2, rely=0.45)

        cur.close()
        s.close()

    show = Button(select_mon, text="see expenses", font=("Arial", 14), bg="#F2CC8F", command=fetch_details)
    show.grid(row=1, column=5)

    select_mon.place(relx=0.2, rely=0.19)

    analysis.configure(bg="#F2CC8F")
    analysis.mainloop()


open_home()
