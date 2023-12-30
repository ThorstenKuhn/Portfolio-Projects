import sqlite3
from datetime import datetime as dt


class BankDatabase:


    def get_accs_db(self, id):
        conn = sqlite3.connect("Banking\\Bank.db")
        cursor = conn.cursor()
        dataset = []
        dataset, *_ = cursor.execute(f'SELECT ID, Vorname, Nachname, Kapital, Kreditrahmen FROM Accounts WHERE ID = {id}')
        conn.close()
        return dataset


    def update_db(self, own, other, event_, amount, send_name, rec_name):
        
        conn = sqlite3.connect("Banking\\Bank.db")
        cursor = conn.cursor()
        
        # Update Account Balance
        sql_query_upd = []
        sql_query_upd.append(f"UPDATE Accounts SET Kapital = '{own[3]}' WHERE ID = '{own[0]}'")
        sql_query_upd.append(f"UPDATE Accounts SET Kapital = '{other[3]}' WHERE ID = '{other[0]}'")
        for command_ in sql_query_upd:
                cursor.execute(command_)

        # Add Event to History Table
        sql_insert = f'''INSERT INTO History 
                        (SendAccID, RecAccID, Date, Time, Event, Amount, SendName, RecName) 
                      VALUES 
                        ('{own[0]}', '{other[0]}', '{event_[0]}', '{event_[1]}', '{event_[2]}', '{amount}', '{send_name}', '{rec_name}')'''
        cursor.execute(sql_insert)

        conn.commit()
        conn.close()

    def transfer(self, own_id, other_id, amount):
        own = list(self.get_accs_db(own_id))
        other = list(self.get_accs_db(other_id))
        
        if own[3] + own[4] > amount:
            own[3] = (int(own[3]*100) - int(amount*100))/100
            other[3] = (int(other[3]*100) + int(amount*100))/100
            event_ = dt.now().date(), dt.now().time(), f"{own[1]} {own[2]} ({own[0]}) transfered {amount}€ to {other[1]} {other[2]} ({other[0]})"
            self.update_db(own, other, event_, amount, f'{own[1]} {own[2]}' ,f'{other[1]} {other[2]}')
            print("Transfer successfull!")
        else:
            print(f"Insufficient credit to transfer {amount} to {other[1]} {other[2]}.")
            print(f"Transfer amount ({amount}) exceeds credit({own[3]}) and credit limit ({own[4]}).")

    def get_history(self, own_id):
        conn = sqlite3.connect("Banking\\Bank.db")
        cursor = conn.cursor()
        sql = f"SELECT * FROM History WHERE SendAccID = ? OR RecAccID = ?"
        history = cursor.execute(sql, (own_id, own_id)).fetchall()
        conn.close()
        return history
    
if __name__ == "__main__":
    Bank = BankDatabase()
    Bank.transfer('1','2',50)