import tkinter as tk                
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
import user_similarity as sim
import stock_viewer as sv

# For Visualization
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure
import seaborn as sns
sns.set_style('darkgrid')

class TkPortfolio(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.label_font = tkfont.Font(family='Bahnschrift', size=18)
        self._frame = None
        #self.switch_frame(StartPage)
        self.switch_stock("NVDA")
    
    def switch_frame(self, page_name):
        self.update_idletasks()
        
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
        entry_font = tkfont.Font(family='Bahnschrift Light', size=16)
        entry_font_bold = tkfont.Font(family='Bahnschrift Light', size=16, weight='bold')

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
        refresh_button = tk.Button(self,text="Refresh",font=entry_font,command=lambda: parent.switch_frame(StockViewerMain))
        entry_button.image = search_img
        
        #user input
        stock_entry = ttk.Combobox(self, foreground='grey', values=[],
                                   background='white',width=30, font=entry_font)
        default_txt = "Search - Example: \"MSFT\""
        stock_entry.insert(0, default_txt)
        stock_entry.config(foreground='grey')
        stock_entry.bind("<Return>", handle_enter)
        stock_entry.bind("<Button-1>", handle_click)
        stock_entry.bind("<KeyRelease>", handle_key)
        ##

        #DOW Jones and SPY graphs
        timeframes = ["1d","1w","1m","1y","5y"]
        
        sp500 = tk.Frame(self, width=500, height=300)
        spy_current = tk.Label(sp500, text = "S & P 500 (SPY) " + "%.2f" % sv.get_current('SPY') + " USD", font=entry_font)
        spy_change = tk.Label(sp500, font=entry_font)
        config_updates(spy_change,sv.get_pct_change('SPY'))
        
        spy_current.grid(row=0,column=0,padx=(30,0),columnspan=3)
        spy_change.grid(row=0,column=3,padx=(0,30),columnspan=2)
        tk.Button(sp500,text="1d",width=15,command=lambda: update_graph("1d",'SPY',sp500,5.5,2.2,1,0,1,5)).grid(row=2,column=0,pady=(15,0))
        tk.Button(sp500,text="1w",width=15,command=lambda: update_graph("1w",'SPY',sp500,5.5,2.2,1,0,1,5)).grid(row=2,column=1,pady=(15,0))
        tk.Button(sp500,text="1m",width=15,command=lambda: update_graph("1m",'SPY',sp500,5.5,2.2,1,0,1,5)).grid(row=2,column=2,pady=(15,0))
        tk.Button(sp500,text="1y",width=15,command=lambda: update_graph("1y",'SPY',sp500,5.5,2.2,1,0,1,5)).grid(row=2,column=3,pady=(15,0))
        tk.Button(sp500,text="5y",width=15,command=lambda: update_graph("5y",'SPY',sp500,5.5,2.2,1,0,1,5)).grid(row=2,column=4,pady=(15,0))

        dia = tk.Frame(self, width=500, height=300)
        dia_current = tk.Label(dia, text = "Dow Jones (DIA) " + "%.2f" % sv.get_current('DIA') + " USD", font=entry_font)
        dia_change = tk.Label(dia, font=entry_font)
        config_updates(dia_change,sv.get_pct_change('DIA'))
        
        dia_current.grid(row=0,column=0,padx=(30,0),columnspan=3)
        dia_change.grid(row=0,column=3,padx=(0,30),columnspan=2)
        tk.Button(dia,text="1d",width=15,command=lambda: update_graph("1d",'DIA',dia,5.5,2.2,1,0,1,5)).grid(row=2,column=0,pady=(15,0))
        tk.Button(dia,text="1w",width=15,command=lambda: update_graph("1w",'DIA',dia,5.5,2.2,1,0,1,5)).grid(row=2,column=1,pady=(15,0))
        tk.Button(dia,text="1m",width=15,command=lambda: update_graph("1m",'DIA',dia,5.5,2.2,1,0,1,5)).grid(row=2,column=2,pady=(15,0))
        tk.Button(dia,text="1y",width=15,command=lambda: update_graph("1y",'DIA',dia,5.5,2.2,1,0,1,5)).grid(row=2,column=3,pady=(15,0))
        tk.Button(dia,text="5y",width=15,command=lambda: update_graph("5y",'DIA',dia,5.5,2.2,1,0,1,5)).grid(row=2,column=4,pady=(15,0))

        update_graph("1y","SPY",sp500,5.5,2.2,1,0,1,5)
        update_graph("1y","DIA",dia,5.5,2.2,1,0,1,5)
        
        #blit items on screen
        back_button.grid(row=0,column=0)
        stock_entry.grid(row=0, column=1,columnspan=2,padx=(25,0))
        entry_button.grid(row=0,column=3,padx=(30,0))
        refresh_button.grid(row=0,column=4,padx=(30,0))
        tk.Label(self,text="Today's Market Updates",font=entry_font_bold,fg='#575757').grid(row=1,column=1,pady=(20,15),columnspan=4)
        sp500.grid(row=0,column=5, padx=(20,0), pady=(25,0), rowspan=5)
        dia.grid(row=5,column=5, padx=(20,0), pady=(25,0), rowspan=5)
        
        for count,val in enumerate(sv.gen_random_8()):
            tmp = self.stockPreview(val,self)
            tmp.subframe.grid(row=count+2,column=1,pady=(15,0),padx=10,columnspan=4)
            tmp.update_price()
            
    class stockPreview:
        def __init__(self, stock, instance_main):
            display_font = tkfont.Font(family='Bahnschrift Light', size=18)
            display_font_small = tkfont.Font(family='Bahnschrift Light', size=15)
            self.stock = stock
            self.subframe = tk.Frame(instance_main)
            self.current = tk.Label(self.subframe,font=display_font_small,width=15)
            self.change = tk.Label(self.subframe,font=display_font_small,width=15)
            self.main = instance_main
            
            ticker = tk.Button(self.subframe,text=self.stock,font=display_font,width=13,
                               command=lambda: instance_main.enter_ticker(self.stock))

            ticker.grid(row=0,column=0)
            self.current.grid(row=0,column=1,padx=(15,0))
            self.change.grid(row=0,column=2)
            
        def update_price(self):
            self.current.config(text="%.2f" % sv.get_current(self.stock) + "  USD")
            pct_change = sv.get_pct_change(self.stock)
            config_updates(self.change,pct_change)
            
    def enter_ticker(self,entry):
        if not sv.stocks[sv.stocks['Symbol'] == entry].empty:
            self.parent.switch_stock(entry)
        else:
            messagebox.showwarning("Warning","Stock Symbol Not Found!")

class IndivStockViewer(tk.Frame):

    def __init__(self, parent, stock):
        tk.Frame.__init__(self, parent)
        title_font = tkfont.Font(family='Helvetica Neue', weight='bold',size=26)
        small_font = tkfont.Font(family='Helvetica Neue', weight='bold',size=18)
        lbl_font = tkfont.Font(family='Bahnschrift Light', size=14)
        lbl_small = tkfont.Font(family='Bahnschrift Light', size=12)
        
        self.stock = stock
        self.current = tk.Label(self, text = sv.get_current(self.stock), font=title_font, fg="#444444")
        self.change = tk.Label(self,font=small_font)
        info_frame = tk.Frame(self, width=400, height=550, bg="black")
        graph_frame = tk.Frame(self, width=500, height=550)
        profile_frame = tk.Frame(self, width=460, height=210)
        financials_frame = tk.Frame(self, width=200, height=210)

        back_button = tk.Button(self, text="<",font=parent.label_font,width=3,height=1,
                           command=lambda: parent.switch_frame(StockViewerMain))

        stock_info = sv.get_stock_info(self.stock)

        stock_symbol = tk.Label(self, text=stock_info['shortName'] + " (" + self.stock + ")",font=title_font, fg="#444444")
        refresh_button = tk.Button(self,text="Refresh",font=lbl_font,command=lambda: parent.switch_stock(self.stock))

        back_button.place(relx=0,rely=0)
        stock_symbol.place(x=80,y=7)
        refresh_button.place(x=1180,y=10)
        self.current.place(x=80,y=70)
        self.change.place(x=300,y=75)
        info_frame.place(x=80,y=140)
        graph_frame.place(x=500,y=25)
        financials_frame.place(x=550,y=480)
        profile_frame.place(x=770,y=480)

        #graph frame
        update_graph('1y',self.stock,graph_frame,8,4,0,0,1,7)
        tk.Label(graph_frame,text="",width=15).grid(row=1,column=0,pady=(15,0))
        tk.Button(graph_frame,text="1d",width=15,command=lambda: update_graph("1d",self.stock,graph_frame,8,4,0,0,1,7)).grid(row=1,column=1)
        tk.Button(graph_frame,text="1w",width=15,command=lambda: update_graph("1w",self.stock,graph_frame,8,4,0,0,1,7)).grid(row=1,column=2)
        tk.Button(graph_frame,text="1m",width=15,command=lambda: update_graph("1m",self.stock,graph_frame,8,4,0,0,1,7)).grid(row=1,column=3)
        tk.Button(graph_frame,text="1y",width=15,command=lambda: update_graph("1y",self.stock,graph_frame,8,4,0,0,1,7)).grid(row=1,column=4)
        tk.Button(graph_frame,text="5y",width=15,command=lambda: update_graph("5y",self.stock,graph_frame,8,4,0,0,1,7)).grid(row=1,column=5)
        tk.Label(graph_frame,text="",width=15).grid(row=1,column=6,pady=(15,0))

        #profile_frame
        tk.Label(profile_frame,text="Company Profile",font=lbl_font).place(x=0,y=0)
        tk.Label(profile_frame,text="Sector: " + stock_info['sector'],font=lbl_small).place(x=0,y=60)
        tk.Label(profile_frame,text="Country: " + stock_info['country'],font=lbl_small).place(x=0,y=85)
        tk.Label(profile_frame,text="Address: " + stock_info['address1'],font=lbl_small).place(x=0,y=110)
        tk.Label(profile_frame,text="Website: " + stock_info['website'],font=lbl_small).place(x=0,y=135)
        tk.Label(profile_frame,text="Full-Time Employees: " + str(stock_info['fullTimeEmployees']),font=lbl_small).place(x=0,y=160)

        #financials_frame
        tk.Label(financials_frame,text="Financials",font=lbl_font).grid(row=0,column=0)
        tk.Button(financials_frame,text="Income Statement",font=lbl_small,width=15).grid(row=1,column=0,pady=(25,0))
        tk.Button(financials_frame,text="Balance Sheet",font=lbl_small,width=15).grid(row=2,column=0,pady=15)
        tk.Button(financials_frame,text="Cash Flow",font=lbl_small,width=15).grid(row=3,column=0)
        
        self.update_price()

    def update_price(self):
        self.current.config(text="%.2f" % sv.get_current(self.stock) + "  USD")
        pct_change = sv.get_pct_change(self.stock)
        config_updates(self.change,pct_change)

class PageTwo(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: parent.switch_frame(StartPage))
        button.pack()

def get_graph(timeframe,index,frame,figx,figy):
    tmp = Figure(figsize=(figx,figy),dpi=100)
    tmp.patch.set_facecolor('#F0F0F0')
    tmp_ax = tmp.add_subplot(111)

    info_df = sv.get_historical_data(index,timeframe)
    plot = sns.lineplot(x='timestamp',y='close',lw=0.8,data=info_df,ax=tmp_ax)
    plot.set(xlabel=None,ylabel=None)
    return FigureCanvasTkAgg(tmp, master=frame)

def update_graph(timeframe,index,frame,figx,figy,row,col,rowsp,colsp):
    new_canvas = get_graph(timeframe,index,frame,figx,figy)
    new_canvas.draw()
    new_canvas.get_tk_widget().grid(row=row,column=col,rowspan=rowsp,columnspan=colsp)

def config_updates(label,vals):
    if(vals[0] < 0):
        label.config(text=str(vals[0]) + " (" + str(vals[1]) + "%)" + " ▼")
        label.config(fg="#EF2D2D")
    elif(vals[0] > 0):         
        label.config(text="+" + str(vals[0]) + " (" + str(vals[1]) + "%)" + " ▲")
        label.config(fg="#27D224")
    else:
        label.config(text="+0.00 (0.00%)")
        label.config(fg="#27D224")

if __name__ == "__main__":
    global app
    app = TkPortfolio()
    
    app.geometry("1280x720")
    app.iconbitmap("Images\icon.ico")
    app.title("TKPortfolio")
    app.resizable(False, False)
    app.mainloop()
