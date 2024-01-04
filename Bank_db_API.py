import sqlite3
from datetime import datetime as dt


class BankDatabase:

    '''Method to get main dataset of one account'''
    def get_accs_db(self, id):
        
        conn = sqlite3.connect("Banking/Bank.db")
        cursor = conn.cursor()
        dataset = []
        
        # try to get account dataset
        try:
            dataset, *_ = cursor.execute(f"SELECT ID, Vorname, Nachname, Kapital, Kreditrahmen, Token FROM Accounts WHERE ID = '{id}'")
        except ValueError:
            print("No Data found to that Account ID: " + id)
        conn.close()
        return dataset


    '''Update DB with a valid transfer'''
    def update_db(self, own, other, date_, time_, amount, send_name, rec_name):
        
        conn = sqlite3.connect("Banking/Bank.db")
        cursor = conn.cursor()
        
        # Update account balances
        sql_query_upd = []
        sql_query_upd.append(f"UPDATE Accounts SET Kapital = '{own[3]}' WHERE ID = '{own[0]}'")
        sql_query_upd.append(f"UPDATE Accounts SET Kapital = '{other[3]}' WHERE ID = '{other[0]}'")
        for command_ in sql_query_upd:
                cursor.execute(command_)

        # Add event to History table
        sql_insert = f'''INSERT INTO History 
                            (SendAccID, RecAccID, Date, Time, Amount, SendName, RecName) 
                        VALUES 
                            ('{own[0]}', '{other[0]}', '{date_}', '{time_}', '{amount:.2f}', '{send_name}', '{rec_name}')'''
        cursor.execute(sql_insert)
        conn.commit()
        conn.close()


    '''Method dealing and checking the transfer'''
    def transfer(self, own_id, other_id, amount):
        
        #Account datasets
        own = list(self.get_accs_db(own_id))
        other = list(self.get_accs_db(other_id))
        
        #check if enough balance for transfer
        if own[3] + own[4] > amount:
            own[3] = (int(own[3]*100) - int(amount*100))/100
            other[3] = (int(other[3]*100) + int(amount*100))/100
            date_, time_ = dt.now().date(), dt.now().time()
            
            # update transfer to db
            self.update_db(own, other, date_, time_ , amount, f'{own[1]} {own[2]}' ,f'{other[1]} {other[2]}')
            print("Transfer successfull!")
        else:
            print(f"Insufficient credit to transfer {amount} to {other[1]} {other[2]}.")
            print(f"Transfer amount ({amount}) exceeds balance({own[3]}) and credit limit ({own[4]}).")


    '''Method to get History of an account'''
    def get_history(self, own_id):
        
        conn = sqlite3.connect("Banking/Bank.db")
        cursor = conn.cursor()
        
        # Get Events account involved sending or receiving end
        sql = f"SELECT * FROM History WHERE SendAccID = ? OR RecAccID = ? ORDER BY ID DESC"
        history = cursor.execute(sql, (own_id, own_id)).fetchall()
        conn.close()
        return history