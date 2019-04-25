import pymapd

create_stmt_ = '''CREATE TABLE msft_stocks (
    timestamp_ TIMESTAMP(3), 
    price_ DOUBLE);'''

load_stmt_ = '''COPY msft_stocks FROM 
    's3://wamsi-trading/msft/msft.tar.gz';'''

def load_data():
    
    try:

        con = pymapd.connect(user='mapd',
                    password='HyperInteractive',
                    host='localhost',
                    dbname='mapd',
                    port=6274,
                    protocol='binary')
        print(con)
        con.execute(create_stmt_)
        con.execute(load_stmt_)
        con.close()

        print("Data loaded successfully.")

    except Exception as e:
        raise RuntimeError("Error importing data.\n {}".format(e))

if __name__ == "__main__":
    load_data()
