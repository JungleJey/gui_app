import gradio as gr
import pandas as pd
import sqlite3 
import os
from sqlalchemy import create_engine 
from sqlalchemy.sql import text
from dotenv import load_dotenv
load_dotenv()

     
# conn = sqlite3.connect('test.db') 
# c = conn.cursor()
# c.execute('''CREATE TABLE my_table(id INTEGER,nome TEXT, cognome TEXT, eta INTEGER, PRIMARY KEY("id" AUTOINCREMENT))''')
# c.execute("INSERT INTO my_table(nome,cognome,eta) VALUES(?,?,?)",("TEST","TEST",33))
# conn.commit()
# conn.close()
password : str = os.getenv('PASSWORD')
db_id : str = os.getenv('DBID')


def insert_data_to_sqlite(nome, cognome, eta):       
    engine = create_engine(url = "{dialect}://{username}.{db_id}:{password}@{host}:{port}/{database}".format(
                            dialect="postgresql",
                            username="postgres",
                            db_id= db_id,
                            password= password,
                            host= "aws-0-eu-central-1.pooler.supabase.com",
                            port= 5432,
                            database= "postgres"
                             ))    
    conn = engine.connect()

    df = pd.DataFrame([[nome,cognome,eta]],Columns["nome","cognome","eta"])   
    df.to_sql("my_test",conn, if_exists="append",index=False)

    print (df)

    conn.commit()
    conn.close()
	
def visualize_data(): 
    engine = create_engine(url = "{dialect}://{username}.{db_id}:{password}@{host}:{port}/{database}".format(
                            dialect="postgresql",
                            username="postgres",
                            db_id= db_id,
                            password= password,
                            host= "aws-0-eu-central-1.pooler.supabase.com",
                            port= 5432,
                            database= "postgres"
                             ))    
    conn = engine.connect()
    df = pd.read_sql_query(text("SELECT *FROM my_test"),conn)
    conn.close()
    return df

insert_interface = gr.Interface(fn=insert_data_to_sqlite,
                                inputs=["text", "text", "number"],
                                outputs=None,
                                title="SQLite Data Insert Interface ",
                                description="Insert data into sqlite",
                                allow_flagging="never",)

visualize_interface = gr.Interface(fn=visualize_data,
                                inputs=None,
                                outputs=gr.Dataframe(visualize_data()),
                                allow_flagging="never",
                                )

app = gr.TabbedInterface(interface_list=[insert_interface,visualize_interface],
                         tab_names = ["Insert","Read"]
                         )
if __name__== "__main__":
     app.launch(share=True)