import TkPortfolio as tkp

if __name__ == "__main__":
    global app
    app = tkp.TkPortfolio()
    
    app.geometry("1280x720")
    app.iconbitmap("Images\icon.ico")
    app.title("TKPortfolio")
    app.resizable(False, False)
    app.mainloop()
