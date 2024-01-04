import tkinter as tk
import base64
import hashlib
import Bank_db_API

#==========================
'''
For simplicity are all passwords "pass"
For Testing, use one of the following IBANs to Login.
DE63932837445071501532
DE74674473839747110623
DE75679135975291093937
'''
#==========================



class BankingApp():
    
    '''init for window and widgets (designer)'''
    def __init__(self, master, acc_id):
        
        self.acc_id = acc_id
        self.Bank = Bank_db_API.BankDatabase()
        offset_column = 80
        offset_row = 50
        
        # Banking window
        self.master = master
        self.master.title('Banking App')
        self.master.geometry('310x180')
        x = app.master.winfo_x() - 310/4
        y = app.master.winfo_y()
        self.master.geometry('+%d+%d' %(x,y))
        
        # Label für Begrüßung
        self.label = tk.Label(master, text= 'Welcome to the Banking App of your Trust!')
        self.label.place(anchor= 'n', x=offset_column + 75, y=10)

        # Eingabe für Zielkontonummer
        self.to_account_label = tk.Label(master, text='Acc No receiver:')
        self.to_account_label.place(anchor='n', x= offset_column, y=offset_row)
        self.to_account_entry = tk.Entry(master)
        self.to_account_entry.place(anchor='n', x=offset_column, y= offset_row + 20)

        # Eingabe für Betrag der Überweisung
        self.amount_label = tk.Label(master, text='Amount:')
        self.amount_label.place(anchor='n', x=offset_column, y = offset_row + 40)
        self.amount_entry = tk.Entry(master)
        self.amount_entry.place(anchor='n', x=offset_column, y= offset_row+ 60)

        # Button für Überweisung
        self.transfer_button = tk.Button(master, text='Transfer', command= lambda: self.transfer())
        self.transfer_button.place(anchor='n', x= offset_column, y= offset_row+ 85)

        # Button für Kontostandabfrage
        self.balance_button = tk.Button(master, text='Show Balance', command= lambda: self.get_balance())
        self.balance_button.place(anchor='n', x= offset_column+ 150, y= offset_row+ 10)
        
        # Button für Kontoauszug
        self.statement_button = tk.Button(master, text='Acc. History', command= self.show_statement_window)
        self.statement_button.place(anchor='n', x= offset_column+ 150, y=offset_row+ 50)
        
        # Button für Logout
        self.balance_button = tk.Button(master, text='Logout', command= lambda: master.destroy())
        self.balance_button.place(anchor='n', x= offset_column+ 150, y= offset_row+ 85)
        
        
    '''Method to transfer money'''
    def transfer(self):
        
        # try handling user input
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                tk.messagebox.showerror('Error', 'Amount must be positive!')
                return
            from_account = self.Bank.get_accs_db(self.acc_id)
            to_account = self.Bank.get_accs_db(self.to_account_entry.get())
            
        # Catch invalid user entry
        except ValueError:
            tk.messagebox.showerror('Error', 'Invalid Entry')
            return
        
        # check if accound no is not own
        if from_account == to_account:
            return
        
        # ask user to check transfer and process transfer
        elif tk.messagebox.askyesno(message=f'Sure to transfer {amount} to {to_account[0]}?\nNew account balance: {from_account[3]-amount}'):
            self.Bank.transfer(from_account[0], to_account[0], amount)


    '''Method to show account balance'''
    def get_balance(self):
        balance, credit = self.Bank.get_accs_db(self.acc_id)[3:5]
        tk.messagebox.showinfo(message=f'{self.acc_id}\nBalance: {balance:,}\nCredit frame: {credit:,}', title='Account balance')
        
        
    '''Method to show history'''
    def show_statement_window(self):
        
        # Get History from DB
        history_list = self.Bank.get_history(self.acc_id)
        if history_list != []:
            
            # New Window for History
            statement_window = tk.Toplevel(self.master)
            statement_window.grab_set()
            statement_window.title('Account History')
            statement_window.geometry('+%d+%d' % (self.master.winfo_rootx()/1.25, self.master.winfo_rooty()/1.25))
            statement_window.resizable(False, False)
            
            # Scrollbar for Text Widget
            self.scrollbar = tk.Scrollbar(statement_window, orient='vertical')
            self.scrollbar.pack(side='right',fill='y')
            
            # Text Widget for output
            self.output_text = tk.Text(statement_window, height=30, width=50, yscrollcommand=self.scrollbar.set)
            self.output_text.pack(side='left')
            self.output_text.focus()
            self.scrollbar.config(command=self.output_text.yview)
            
            # Write History into variable
            event_text = ''
            for index in range(len(history_list)):
                event_ = history_list[index]
                
                # Write if new date
                if index == 0 or event_[3] != history_list[index -1][3]:
                    event_text += f'\n{event_[3]}\n'
                
                amount = str(event_[5])
                send_iban = event_[1]
                send_name = event_[6]
                rec_iban = event_[2]
                rec_name = event_[7]
                
                # Check if sent or received
                if self.acc_id == str(history_list[index][1]): 
                    event_text += f'\n    {rec_name}\n    {rec_iban}'+' '*(40-len(amount)-len(rec_iban))+f'-{amount}\n'
                else:
                    event_text += f'\n    {send_name}\n    {send_iban}'+' '*(40-len(amount)-len(send_iban))+f'+{amount}\n'
                
            # Write variable into Text Widget
            self.output_text.insert(tk.END, event_text.lstrip('\n'))
            self.output_text.config(state=tk.DISABLED)
        else:
            tk.messagebox.showerror(message='No account history found for that account number.')


'''Login Window'''
class Login():
    
    def __init__(self, master):
        
        # Login window
        self.master = master
        self.master.title('Banking')
        self.master.eval('tk::PlaceWindow . center')
        self.master.geometry('160x150')
        self.Bank = Bank_db_API.BankDatabase()
        
        x_offset = 80
        y_offset = 20
        
        # Eingabe Kontonummer
        self.account_id = tk.Label(master, text='Your Acc No:')
        self.account_id.place(anchor='n', x= x_offset, y= y_offset+ 0)
        self.account_id_entry = tk.Entry(master)
        self.account_id_entry.place(anchor='n', x= x_offset, y=y_offset+20, width = 150)
    
        # Eingabe Passwort
        self.account_pw = tk.Label(master, text='Password:')
        self.account_pw.place(anchor='n', x= x_offset, y= y_offset+ 40)
        self.account_pw_entry = tk.Entry(master, show='*')
        self.account_pw_entry.place(anchor='n', x= x_offset, y= y_offset+ 60)
        
        # Login Button
        self.btn_login = tk.Button(master, text='Login', command=self.login_try)
        self.btn_login.place(anchor='n', x= x_offset, y= y_offset+ 80)
        
        
    '''Method validatin login'''
    def login_try(self):
        
        id = self.account_id_entry.get()
        acc_data = self.Bank.get_accs_db(id)
        
        if acc_data == []:
            return # return if there is no account with that ID/IBAN
        
        # get salt and hashed password
        decoded_data = base64.b64decode(acc_data[5].encode('utf-8'))
        salt = decoded_data[:32]
        key = decoded_data[32:]
        password = self.account_pw_entry.get()
        
        # if login is valid, open banking window
        if key == hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000):
            root = tk.Toplevel()
            BankingApp(root, id)
            root.grab_set()
        else:
            tk.messagebox.showerror(message='Wrong password.')
        

if __name__ == '__main__':
    root = tk.Tk()
    app = Login(root)
    root.mainloop()