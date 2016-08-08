from psycopg2 import *
import pandas.io.sql as sql
from sqlalchemy import create_engine

#establishes connection to the default postgres database
con = connect(dbname='postgres', user='adriano', host='localhost', password='pasta')
#create database for the project
cur = con.cursor()
#this allows creating the database with psycopg2, by isolating transactions
con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur.execute("CREATE DATABASE brexit;")
#no password specified as it is the default one in my system
conn = connect("dbname=brexit user=adriano")

cur = conn.cursor()

'''using sqlalchemy to write data in database on localhost, columns with '(,),%' 
are renamed as this causes problems in tranferring the data'''

engine = create_engine("postgresql://adriano:pasta@localhost:5432/brexit")

all_data.rename(columns={'UK Independence Party (UKIP)': 'UKIP', 'Respect (George Galloway)':'Respect', 
	'2015conf %':'2015 conf', '% Turnout':'Turnout'}).to_sql('records', engine)
#check database is fine
cur.execute("SELECT * FROM records;")

cur.fetchone()
