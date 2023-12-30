

import tkinter as tk
from tkinter import messagebox
import BankDatenbank

class BankingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking App")
        self.master.geometry("310x180")
        self.master.eval('tk::PlaceWindow . center')
        self.Bank = BankDatenbank.BankDatabase()
        offset_column = 80
        offset_row = 60

        # Label für Begrüßung
        self.label = tk.Label(master, text="Willkommen bei der Banking App ihres Vertrauens!")
        self.label.place(anchor= 'n', x=offset_column + 75, y=10)

        # Eingabe für Zielkontonummer
        self.to_account_label = tk.Label(master, text="Kontonummer Empfänger:")
        self.to_account_label.place(anchor='n', x= offset_column, y=offset_row)
        self.to_account_entry = tk.Entry(master)
        self.to_account_entry.place(anchor='n', x=offset_column, y= offset_row + 20)

        # Eingabe für eigene Kontonummer
        self.from_account_label = tk.Label(master, text="Ihre Kontonummer:")
        self.from_account_label.place(anchor='n', x=offset_column +150, y=60)
        self.from_account_entry = tk.Entry(master)
        self.from_account_entry.place(anchor='n', x=offset_column +150, y=80)

        # Eingabe für Betrag der Überweisung
        self.amount_label = tk.Label(master, text="Betrag:")
        self.amount_label.place(anchor='n', x=offset_column, y = 100)
        self.amount_entry = tk.Entry(master)
        self.amount_entry.place(anchor='n', x=offset_column, y= 120)

        # Button für Überweisung
        self.transfer_button = tk.Button(master, text="Überweisen", command= lambda: self.transfer())
        self.transfer_button.place(anchor='n', x= offset_column, y= offset_row + 85)

        # Button für Kontoauszug
        self.statement_button = tk.Button(master, text="Kontoauszug", command= lambda: self.show_statement_window(self.from_account_entry.get()))
        self.statement_button.place(anchor='n', x= offset_column+ 150, y=offset_row+ 85)

        # Button für Kontostandabfrage
        self.balance_button = tk.Button(master, text="Kontostand abrufen", command= lambda: self.get_balance())
        self.balance_button.place(anchor='n', x= offset_column+ 150, y= offset_row+ 50)

    def transfer(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Fehler", "Betrag muss positiv sein")
                return
            from_account = self.Bank.get_accs_db(int(self.from_account_entry.get()))
            to_account = self.Bank.get_accs_db(int(self.to_account_entry.get()))
            
        except ValueError:
            messagebox.showerror("Fehler", "Ungültige Eingabe")
            return
        
        asked = messagebox.askyesno(message=f'Sure to transfer {amount} to {to_account[0]}?\nNew account balance: {from_account[3]-amount}')
        if asked:
            self.Bank.transfer(from_account[0], to_account[0], amount)


    def get_balance(self):
        id = str(self.from_account_entry.get())
        value = self.Bank.get_accs_db(id)
        messagebox.showinfo(message=f'Kontostand: {value[3]:,}\nKreditrahmen: {value[4]:,}', title=f'Kontostand für {id}')
        

    def show_statement_window(self, own_id = 1):
        # Get History from DB
        history_list = self.Bank.get_history(own_id)
        if history_list != []:
            # New Window for History
            statement_window = tk.Toplevel(self.master)
            statement_window.title("Kontoauszug")
            statement_window.geometry("+%d+%d" % (self.master.winfo_rootx()/1.25, self.master.winfo_rooty()/1.25))
            
            # Text Widget for output
            self.output_text = tk.Text(statement_window, height=10, width=50)
            self.output_text.pack()
        
            entry_width = 0
            entry_text = ''
            self.output_text.delete(1.0, tk.END) 
            # Write History into variable    
            for index in range(len(history_list)):
                event_ = history_list[index]
                event_text = ""
                
                if index == 0 or event_[3] != history_list[index -1][3]:
                    event_text = f"\n{event_[3]}"
                event_text += f"\n    {event_[5]}"
                
                if len(str(event_text)) > entry_width:
                    entry_width = len(str(event_text))
                entry_text += event_text
            # Write variable into empty Text Widget
            self.output_text.insert(tk.END, entry_text.lstrip("\n"))
            self.output_text.config(width=entry_width, height=index+5)
            statement_window.update_idletasks()
        else:
            messagebox.showwarning(message='Kein Bankverlauf zu dieser Kontonummer gefunden.')
        
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()


