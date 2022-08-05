import tkinter as tk                
from tkinter import font as tkfont
from tkinter import ttk
from PIL import ImageTk,Image
#import stock_viewer as sv

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
        tk.Frame.__init__(self, parent)
        entry_font = tkfont.Font(family='Helvetica', size=14)

        def handle_focus_in(_):
            stock_entry.delete(0, tk.END)
            stock_entry.config(foreground='black')

        def handle_focus_out(_):
            stock_entry.delete(0, tk.END)
            stock_entry.config(foreground='grey')
            stock_entry.insert(0, "Example: MSFT")

        def handle_enter(txt):
            parent.switch_stock(stock_entry.get())

        def enter_ticker(ticker):
            parent.switch_stock(ticker)

        search_img = ImageTk.PhotoImage(file = "Images\search.png")
        entry = tk.StringVar()

        stock_entry = ttk.Combobox(self, textvariable=entry, foreground='grey',
                                   background='white',width=30, font=entry_font)
        back_button = tk.Button(self, text="<",font=parent.label_font,width=3,height=1,
                   command=lambda: parent.switch_frame(StartPage))
        entry_button = tk.Button(self,image=search_img,bd=0,command=lambda: enter_ticker(stock_entry.get()))
        entry_button.image = search_img

        back_button.grid(row=0,column=0)
        stock_entry.grid(row=0, column=1, padx=15, columnspan=2)
        entry_button.grid(row=0,column=3)
        
        stock_entry.set("Example: NVDA")
        stock_entry.bind("<FocusIn>", handle_focus_in)
        stock_entry.bind("<FocusOut>", handle_focus_out)
        stock_entry.bind("<Return>", handle_enter)

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
