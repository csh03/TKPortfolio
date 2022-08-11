# For reading stock data from yahoo
import pandas_datareader.data as web

# For time stamps
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import tkinter as tk
import ttk
import seaborn as sns
sns.set_style('darkgrid')

root = tk.Tk()
endtime = datetime.now()
start = datetime(endtime.year-1,endtime.month,endtime.day)

test = web.DataReader('TSLA','yahoo',start,endtime)

lf = ttk.Labelframe(root, text='Plot Area')
lf.grid(row=0, column=0, sticky='nwes', padx=3, pady=3)

fig = Figure(figsize=(12,4), dpi=100)

ax = fig.add_subplot(111)
ax.set_ylim([500,1500])

sns.lineplot(x='Date',y='Adj Close',data=test,ax=ax)

canvas = FigureCanvasTkAgg(fig, master=lf)
canvas.get_tk_widget().grid(row=0, column=0)

root.mainloop()
