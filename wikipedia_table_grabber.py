from tkinter import *
from tkinter import ttk
import pandas as pd
from bs4 import BeautifulSoup
from pandastable import Table, TableModel
import requests

def source_get(url_arg):
    source = requests.get(url_arg).content
    code = BeautifulSoup(source, 'lxml')
    return code

def calculate(*args):
    try:
        url_in = url.get()
        file_in = file_name.get()
        
        source_code = source_get(url_in)    
        info = source_code.find("table", class_="wikitable")
            
        data = pd.read_html(str(info))[0]
                       
        return data
    except ValueError:
        pass

def save_to_csv(*args):
    dataframe = calculate()
    dataframe.to_csv(f"/your/folder/{file_name.get()}.csv", index = False, encoding = 'utf-8')
    return


class TableFrame(ttk.Frame):
        
    def __init__(self, master):
        ttk.Frame.__init__(self,master)
        f= ttk.Frame(master)
        f.grid(column=1,row=0)
        
        df = calculate()
        self.table = pt = Table(f, dataframe=df)
        pt.show()
        
        return

def show_data(*args):
    display_frame = TableFrame(root)
    return

root = Tk()

mainframe = ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0,row=0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

url = StringVar()
ttk.Label(mainframe,text="URL").grid(column=2,row=2)
url_input = ttk.Entry(mainframe, textvariable = url).grid(column=2,row=3)

file_name = StringVar()
ttk.Label(mainframe, text = "File name").grid(column=2,row=4)
file_name_input = ttk.Entry(mainframe, textvariable = file_name).grid(column=2,row=5)

ttk.Button(mainframe, text = "Get Tables", command = show_data).grid(column=3,row=3)
ttk.Button(mainframe, text = "Save as CSV", command = save_to_csv).grid(column=3,row=5)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
