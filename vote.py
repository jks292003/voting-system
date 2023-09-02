import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import sqlite3 as sqltor
import matplotlib.pyplot as plt
conn=sqltor.connect('main.db')
cursor=conn.cursor() 
cursor.execute("""CREATE TABLE IF NOT EXISTS poll
                    (name)""")

def pollpage(): 
     def proceed():
        chose=choose.get()
        print(chose)
        command='update polling set votes=votes+1 where name=?'
        pd.execute(command,(chose,))
        pd.commit()
        messagebox.showinfo('Success!','You have voted')
     choose=StringVar()
     names=[]
     pd=sqltor.connect(plname+'.db') 
     pcursor=pd.cursor() 
     pcursor.execute('select name from polling')
     data=pcursor.fetchall()
     for i in range(len(data)):
         data1=data[i]
         ndata=data1[0]
         names.append(ndata)
     print(names)
     ppage=Toplevel()
     ppage.geometry('300x300')
     ppage.title('Poll')
     ppage['bg'] = '#FF6347'

     Label(ppage,text='Vote for any one person!',bg='#ff6347').grid(row=1,column=3)
     for i in range(len(names)):
         Radiobutton(ppage,text=names[i],value=names[i],variable=choose,bg='#ff6347').grid(row=2+i,column=1)
     Button(ppage,text='Vote',command=proceed,bg="#008b8b").grid(row=2+i+1,column=2)


def polls(): 
    def proceed():
        global plname
        plname=psel.get()
        if plname=='-select-':
            return messagebox.showerror('Error','select poll')
        else:
            mpolls.destroy()
            pollpage()
    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames=['-select-']
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)
    psel=StringVar()
    mpolls=Toplevel()
    mpolls.geometry('270x200')
    mpolls.title('Voting Program')
    mpolls['bg'] = '#FF6347'
    Label(mpolls,text='Select Poll',font='Helvetica 12 bold',bg='#ff6347').grid(row=1,column=3)
    select=ttk.Combobox(mpolls,values=pollnames,state='readonly',textvariable=psel)
    select.grid(row=2,column=3)
    select.current(0)
    Button(mpolls,text='Proceed',command=proceed,bg="#008b8b").grid(row=2,column=4)



def create():
    def proceed():
        global pcursor
        pname=name.get() 
        can=cname.get()  
        if pname=='':
            return messagebox.showerror('Error','Enter poll name')
        elif can=='':
            return messagebox.showerror('Error','Enter candidates')
        else:
            candidates=can.split(',') 
            command='insert into poll (name) values (?);'
            cursor.execute(command,(pname,))
            conn.commit()
            pd=sqltor.connect(pname+'.db') 
            pcursor=pd.cursor() 
            pcursor.execute("""CREATE TABLE IF NOT EXISTS polling
                 (name TEXT,votes INTEGER)""")
            for i in range(len(candidates)):
                command='insert into polling (name,votes) values (?, ?)'
                data=(candidates[i],0)
                pcursor.execute(command,data)
                pd.commit()
            pd.close()
            messagebox.showinfo('Success!','Poll Created')
            cr.destroy()

    name=StringVar()
    cname=StringVar()
    cr=Toplevel()
    cr.geometry('500x400')
    cr.title('Create a new poll')
    cr['bg'] = '#FF6347'
    Label(cr,text='Enter Details',font='Helvetica 12 bold',bg='#ff6347').grid(row=1,column=2)
    Label(cr,text='Enter Poll name: ',bg='#ff6347').grid(row=2,column=1)
    Entry(cr,width=45,textvariable=name).grid(row=2,column=2) #poll name
    Label(cr,text='(eg: captain elections)',bg='#ff6347').place(x=354,y=25)
    Label(cr,text='Enter Candidates: ',bg='#ff6347').grid(row=3,column=1)
    Entry(cr,width=45,textvariable=cname).grid(row=3,column=2) #candidate name
    Label(cr,text='Note: Enter the candidate names one by one by putting commas',bg='#ff6347').grid(row=4,column=2)
    Label(cr,text='eg: candidate1,candidate2,candidate3....',bg='#ff6347').grid(row=5,column=2)
    Button(cr,text='Proceed',command=proceed,bg="#008b8b").grid(row=6,column=2)
def selpl(): #pollresults
    def results():
        sel=sele.get()  #selected option
        if sel=='-select-':
            return messagebox.showerror('Error','Select Poll')
        else:
            pl.destroy()
            def project():
                names=[]
                votes=[]
                for i in range(len(r)):
                    data=r[i]
                    names.append(data[0])
                    votes.append(data[1])
                    plt.title('Poll Result')
                plt.pie(votes,labels=names,autopct='%1.1f%%',shadow=True,startangle=140)
                plt.axis('equal')
                plt.show()

            res=Toplevel()
            res.geometry('300x300')
            res.title('Results!')
            res['bg'] = '#FF6347'
            Label(res,text='Here is the Result!',font='Helvetica 12 bold',bg='#ff6347').grid(row=1,column=2)
            con=sqltor.connect(sel+'.db')
            pcursor=con.cursor()
            pcursor.execute('select * from polling')
            r=pcursor.fetchall() 
            for i in range(len(r)):
                data=r[i]
                Label(res,text=data[0]+': '+str(data[1])+' votes',bg='#ff6347').grid(row=2+i,column=1)
            Button(res,text='Project Results',command=project,bg="#008b8b").grid(row=2+i+1,column=2)


    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames=['-select-']
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)
    sele=StringVar()
    pl=Toplevel()
    pl.geometry('300x200')
    pl.title('Voting System')
    pl['bg'] = '#FF6347'
    Label(pl,text='Select Poll',font='Helvetica 12 bold',bg='#ff6347').grid(row=1,column=2)
    sel=ttk.Combobox(pl,values=pollnames,state='readonly',textvariable=sele)
    sel.grid(row=2,column=1)
    sel.current(0)
    Button(pl,text='Get Results',command=results,bg="#008b8b").grid(row=2,column=2)



home=Tk()
home.geometry('400x400')
home.title('Voting Program')
home['bg'] = '#FF6347'
Label(home,text='voting program made in python',font='Helvetica 12 bold',bg='#ff6347').grid(row=1,column=10)
Label(home,text='                             ',font='Helvetica 12 bold',bg='#ff6347').grid(row=2,column=10)
Button(home,text='Create new Poll +',width=50,bg="#008b8b",command=create).grid(row=4,column=10)
Button(home,text='My Polls',width=50,bg="#008b8b",command=polls).grid(row=5,column=10)
Button(home,text='Poll Results',width=50,bg="#008b8b",command=selpl).grid(row=6,column=10)
home.mainloop()
