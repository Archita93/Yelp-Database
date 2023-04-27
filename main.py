import pymssql
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime
import login as lg
import uuid
import base64


def createServerConnection(host,user,password,database):
    conection = None
    try: 
        connection = pymssql.connect(host = host ,user = user,
                            password = password,database = database)
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error:'{err}' ")
    return connection

host = 'cypress.csil.sfu.ca'
user = 's_asa410'                
password = '2TtQ4M22nL6bJRqH'
database = 'asa410354'
conn = createServerConnection(host,user,password,database)
cursor = conn.cursor()
   
dataset = []

# Created a main GUI window
root = tkinter.Tk()
root.title('Yelp Database')
root.geometry('900x900')
root.configure(bg = '#ffffff')
root.resizable(0,0)

number = tkinter.IntVar()
number.set(1)
business_tree = tkinter.Frame(root)
users_tree = tkinter.Frame(root)

# Added widgets to the window
greetings_frame = tkinter.Frame(root)
textbox_frame = tkinter.Frame(root)
combobox_frame = tkinter.LabelFrame(root,text = 'How can we help you today?',font = ("Arial",13))
business_frame = tkinter.Frame(root)
bus_info_frame = tkinter.Frame(root)
users_frame = tkinter.Frame(root)
user_info_frame = tkinter.Frame(root)

# Arranging the frames
greetings_frame.pack()
textbox_frame.pack(expand = True) 



greeting_label = tkinter.Label(greetings_frame,text = 'Welcome to the Yelp Database System',bg = '#ffffff',fg = '#333333',font = ("Gabriola",35))
login_label = tkinter.Label(textbox_frame,text = 'Please enter your Login ID to access the Application:',bg = '#ffffff',font = ("Arial",10))
login_entry = tkinter.Entry(textbox_frame,font = ("Arial",12))
login_button = tkinter.Button(textbox_frame,text='Login',bg = '#ffffff',fg = '#333333',font = ("Arial",10),command=lambda:login(login_entry.get(),conn))

business_button = tkinter.Radiobutton(combobox_frame,text='Businesses at Yelp',value = 1,variable = number,
                    bg = '#ffffff',fg = '#333333',font = ("Arial",10),command=lambda:business())
users_button = tkinter.Radiobutton(combobox_frame,text='Find Users and Make Friends',value = 2,variable = number,
                    bg = '#ffffff',fg = '#333333',font = ("Arial",10),command = lambda:users())


# features_frame.pack_forget()
combobox_frame.pack_forget()
business_tree.pack_forget()
users_tree.pack_forget()
business_frame.pack_forget()
users_frame.pack_forget()
bus_info_frame.pack_forget()
user_info_frame.pack_forget()


# Arrange the label
greeting_label.grid(row =0,column =0,sticky = "news")
login_label.grid(row =1,column =0)
login_entry.grid(row =1,column =1)
login_button.grid(row =1,column =2)
business_button.grid(row=2,column=0)
users_button.grid(row=2,column=1)


def login(username,connection):
    lg.validate(username,connection)
    if lg.validate(username,connection) == True:
        textbox_frame.pack_forget()
        combobox_frame.pack(padx=20,pady=10)
        

def business():
    business_frame.pack()
    users_frame.pack_forget()
    users_tree.pack_forget()
    business_tree.pack_forget()
    user_info_frame.pack_forget()

    minstars_label = tkinter.Label(business_frame, text='Least Rating:')
    minstars_text = tkinter.Entry(business_frame)
    maxstars_label = tkinter.Label(business_frame, text='Highest Rating:')
    maxstars_text = tkinter.Entry(business_frame)
    city_label = tkinter.Label(business_frame, text='City:')
    city_text = tkinter.Entry(business_frame)
    name_label = tkinter.Label(business_frame, text='Name:')
    name_text = tkinter.Entry(business_frame)
   
    minstars_label.grid(row=3, column=0)
    minstars_text.grid(row=3, column=1)
    maxstars_label.grid(row=3,column=2)
    maxstars_text.grid(row=3,column=3)
    city_label.grid(row=3, column=4)
    city_text.grid(row=3, column=5)
    name_label.grid(row=3, column=6)
    name_text.grid(row=3, column=7)
    filter_button = tkinter.Button(business_frame,text='Filter',command=lambda:business_filtered(minstars_text.get(),maxstars_text.get(),city_text.get(),name_text.get()))
    filter_button.grid(row = 3,column = 8)
    
    

def business_filtered(minstars,maxstars,city,name):
    columns = ['col0','col1','col2','col3','col4']
    headings = ['ID', 'Name', 'Address','City','Stars']
    dataset = lg.business(minstars,maxstars,city,name,conn)
    button(columns,headings,dataset,business_tree,0)
    

def users():
    users_frame.pack()
    business_frame.pack_forget()
    users_tree.pack_forget()
    business_tree.pack_forget()
    bus_info_frame.pack_forget()

    name_label = tkinter.Label(users_frame, text='Name:')
    name_text = tkinter.Entry(users_frame)
    useful_label = tkinter.Label(users_frame, text='Useful:')
    useful_text = ttk.Combobox(users_frame, value=['yes','no'])
    funny_label = tkinter.Label(users_frame, text='Funny:')
    funny_text = ttk.Combobox(users_frame, value=['yes','no'])
    cool_label = tkinter.Label(users_frame, text='Cool:')
    cool_text = ttk.Combobox(users_frame, value=['yes','no'])

    name_label.grid(row=3, column=0)
    name_text.grid(row=3, column=1)
    useful_label.grid(row=3, column=2)
    useful_text.grid(row=3, column=3)
    funny_label.grid(row=3, column=4)
    funny_text.grid(row=3, column=5)
    cool_label.grid(row=3, column=6)
    cool_text.grid(row=3, column=7)

    filter_button = tkinter.Button(users_frame,text='Filter',command=lambda:users_filtered(name_text.get(),useful_text.get(),funny_text.get(),cool_text.get()))
    filter_button.grid(row = 3,column = 8)
    

def users_filtered(name,useful,funny,cool):
    columns = ['col0','col1','col2','col3','col4','col5']
    headings = ['ID', 'Name', 'Useful(yes/no)','Funny(yes/no)','Cool(yes/no)','Date']
    dataset = lg.users(name,useful,funny,cool,conn)
    button(columns,headings,dataset,users_tree,1)


def double_click_users(event):
    item = event.widget.item(event.widget.selection())
    Id = item['values'][0]
    name = item['values'][1]
    
    result = messagebox.askyesno("Message",f"Do you want to be friends with {name}?")
    if result:
        friends = make_friend(Id)
        if friends == True:
            messagebox.showinfo("Message",f"You are now friends with {name}")
        else:
            messagebox.showinfo("Message",f"You are already friends with {name}")
    else:
        messagebox.showinfo("Message",f"You are not friends with {name}")



def double_click_business(event):
    item = event.widget.item(event.widget.selection())
    Id = item['values'][0]
    name = item['values'][1]

    result = messagebox.askyesno("Message",f"Do you want to write a review for {name}?")
    if result:
        stars = simpledialog.askstring('Rate', 'Rate our business on a five point scale:')
        if stars == None:
            messagebox.showinfo('Message',f"You did not rate {name}.")
        else:
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            write_review(str(login_entry.get()),Id,stars,current_date)
            messagebox.showinfo('Message',f"You rated {name} {stars} stars! Thank you :)")
    else:
        messagebox.showinfo('Message',f"You did not rate {name}.")



def write_review(user_id,business_id,stars,date):
    cursor = conn.cursor()
    uid = uuid.uuid4()
    uid_bytes = uid.bytes
    uid_str = base64.urlsafe_b64encode(uid_bytes).rstrip(b'=').decode('utf-8')
    review_id = uid_str[:22]

    cursor.execute('INSERT INTO dbo.review (review_id,user_id,business_id,stars,date) VALUES (%(review)s,%(username)s,%(business)s,%(stars)s,%(date)s)', {'review':review_id,'username': user_id,'business':str(business_id),'stars':stars,'date':date})
    conn.commit()

    
def make_friend(friend_user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.friendship WHERE user_id = %(username)s AND friend = %(friend)s',{'username': str(login_entry.get()),'friend':str(friend_user_id)})
    result = cursor.fetchone()
    if result:
        return False
    
    # __OdjK-F4MTdHkb8RtDFlQ
    else:
        cursor.execute('INSERT INTO dbo.friendship (user_id,friend) VALUES (%(username)s,%(friend)s)', {'username': str(login_entry.get()),'friend':str(friend_user_id)})
        conn.commit()
        return True
    


def button(columns,headings,dataset,tree_frame,num):
    
    style = ttk.Style()
    style.theme_use('clam')

    tree_frame.pack()
    tree = ttk.Treeview(tree_frame, columns = columns, show = 'headings',height = 30)
    for index,col in enumerate(columns):
        tree.column(col, width = 100, anchor = 'center')
        tree.heading(col, text = headings[index])

        
    scrollbar = ttk.Scrollbar(tree_frame, orient = tkinter.VERTICAL, command = tree.yview)
    tree.configure(yscroll = scrollbar.set)

    tree.grid(row = 4, column = 0)
    scrollbar.grid(row = 4, column = 1)
    
    for index in range(len(dataset)):
        tree.insert('', tkinter.END, values=dataset[index])
    
    if num == 1:
        user_info_frame.pack()
        
        user_info = tkinter.Label(user_info_frame,text = 'Double click on a row to make a friend',bg = '#ffffff',font = ("Arial",10))
        user_info.grid(row = 5,column =1,pady=5)
        tree.bind('<Double-Button-1>', double_click_users)
    elif num == 0:
        bus_info_frame.pack()
        bus_info = tkinter.Label(bus_info_frame,text = 'Double click on a row to write a review',bg = '#ffffff',font = ("Arial",10))
        bus_info.grid(row = 5,column =1,pady=5)
        tree.bind('<Double-Button-1>', double_click_business)

     


root.mainloop()



