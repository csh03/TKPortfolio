import tkinter as tk                
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
import user_similarity as sim
import stock_viewer as sv
from yahoo_fin import stock_info

class TkPortfolio(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.label_font = tkfont.Font(family='Microsoft Sans Serif', size=18, weight="bold")
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, page_name):
        '''Show a frame for the given page name'''
        new_frame = page_name(parent=self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)
        
    def switch_stock(self, ticker):
        '''Show a frame for the given page name'''
        new_frame = IndivStockViewer(parent=self,stock=ticker)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)
        
    def quit(self):
        self.destroy()

class StartPage(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        logo_img = ImageTk.PhotoImage(Image.open("Images\logo.png"))
        logo_lbl = tk.Label(self,image=logo_img)
        logo_lbl.image = logo_img
        logo_lbl.pack(side="top", fill="x", pady=10)
        
        button1 = tk.Button(self,fg='#494949',font=parent.label_font,text="Portfolio Creator",bd=4,width=20,height=2,
                            command=lambda: parent.switch_frame(PageTwo))
        button2 = tk.Button(self,fg='#494949',font=parent.label_font,text="Stock Tracker",bd=4,width=20,height=2,
                            command=lambda: parent.switch_frame(StockViewerMain))
        button3 = tk.Button(self,fg='#494949',font=parent.label_font,text="Exit",bd=4,width=20,height=2,
                            command=parent.quit)
        button1.pack()
        button2.pack()
        button3.pack()

class StockViewerMain(tk.Frame):

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        entry_font = tkfont.Font(family='Helvetica', size=14)

        def handle_enter(e):
            entry = stock_entry.get().upper()
            if not sv.stocks[sv.stocks['Symbol'] == entry].empty:
                parent.switch_stock(entry)
            else:
                messagebox.showwarning("Warning","Stock Symbol Not Found!")

        def handle_click(e):
            if stock_entry.get() == default_txt:
                stock_entry.delete(0,tk.END)
            stock_entry.config(foreground='black')

        def handle_key(e):
            recommend = sim.get_autofill(stock_entry.get())
            stock_entry['values'] = recommend

        search_img = ImageTk.PhotoImage(file = "Images\search.png")
        back_button = tk.Button(self, text="<",font=parent.label_font,width=3,height=1,
                   command=lambda: parent.switch_frame(StartPage))
        entry_button = tk.Button(self,image=search_img,bd=0,command=lambda: self.enter_ticker(stock_entry.get().upper()))
        entry_button.image = search_img
        
        ##user input
        stock_entry = ttk.Combobox(self, foreground='grey', values=[],
                                   background='white',width=30, font=entry_font)
        stock_entry.DroppedDown = True

        default_txt = "Search - Example: \"MSFT\""
        stock_entry.insert(0, default_txt)
        stock_entry.config(foreground='grey')
        stock_entry.bind("<Return>", handle_enter)
        stock_entry.bind("<Button-1>", handle_click)
        stock_entry.bind("<KeyRelease>", handle_key)
        ##
        
        back_button.grid(row=0,column=0)
        stock_entry.grid(row=0, column=1, padx=15, columnspan=2)
        entry_button.grid(row=0,column=3)
        tk.Label(self,text="Today's Market Updates",font=entry_font,fg='#575757').grid(row=1,column=1,pady=15)
        for count,val in enumerate(sv.gen_random_8()):
            tmp = self.stockPreview(val,self)
            tmp.subframe.grid(row=count+2,column=1,pady=(15,0),padx=10)
            tmp.update_price()
            
    class stockPreview:
        def __init__(self, stock, instance_main):
            display_font = tkfont.Font(family='Bahnschrift Light', size=18)
            self.stock = stock
            self.subframe = tk.Frame(instance_main)
            self.info = tk.Label(self.subframe,font=display_font,width=15)
            
            ticker = tk.Button(self.subframe,text=self.stock,font=display_font,width=15,
                               command=lambda: instance_main.enter_ticker(self.stock))

            ticker.grid(row=0,column=0)
            self.info.grid(row=0,column=1,padx=15)
            
        def update_price(self):
            self.info.config(text=str(round(stock_info.get_live_price(self.stock),2)))

    def enter_ticker(self,entry):
        if not sv.stocks[sv.stocks['Symbol'] == entry].empty:
            self.parent.switch_stock(entry)
        else:
            messagebox.showwarning("Warning","Stock Symbol Not Found!")

class IndivStockViewer(tk.Frame):

    def __init__(self, parent, stock):
        tk.Frame.__init__(self, parent)
        self.stock = stock

        back_button = tk.Button(self, text=stock,font=parent.label_font,width=3,height=1,
                           command=lambda: parent.switch_frame(StockViewerMain))
        back_button.grid(row=0,column=0)

class PageTwo(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: parent.switch_frame(StartPage))
        button.pack()


if __name__ == "__main__":
    global app
    app = TkPortfolio()
    app.geometry("1280x720")
    app.iconbitmap("Images\icon.ico")
    app.title("TKPortfolio")
    app.mainloop()
