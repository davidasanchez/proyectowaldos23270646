import tkinter as tk
from login import LoginWindow

def main():
    app = tk.Tk()
    app.title("Punto de Venta")
    app.geometry("900x600")  
    LoginWindow(app)
    app.mainloop()

if __name__ == "__main__":
    main()