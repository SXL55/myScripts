import pandas as pd
import sqlite3

filename = 'systeminfo'

conn = sqlite3.connect(filename+'.db')

database = pd.read_excel(filename+'.xlsx')

database.to_sql(name = filename, con = conn, if_exists='append')