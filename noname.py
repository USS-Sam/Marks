import streamlit as st
import pandas as pd
import sqlite3
def ex(a):
   con = sqlite3.connect("marks.db")
   cur = con.cursor()
   c = '''SELECT EXISTS(SELECT 1 FROM CSS WHERE Name = ?)'''
   cur.execute(c,(a,))
   k = cur.fetchone()[0]
   con.close()
   return k
if "NA" not in st.session_state:
   st.session_state["NA"] = ""
st.title ("12TH B1 SARATHA CS BOYS")
tab1,tab2, tab3 = st.tabs(["Dashboard and Enter Marks","Change The Entered Data","Marks Search"])
if "authenticated" not in st.session_state:
  st.session_state["authenticated"] = False
if "au" not in st.session_state:
  st.session_state["au"] = False   
with tab1:
  st.header("DASHBOARD")
  st.write("To be filled in the future")
  st.header("Enter Your Marks")
  with st.form("Myform1",clear_on_submit = True):
    if st.form_submit_button("Refresh", key = 'btn6'):
       st.rerun()
    if not st.session_state["authenticated"]:
       Pa = st.text_input("Enter Your Password", placeholder="Note: Ask The Admins", key = "pw1")
       if st.form_submit_button ("Enter Password", key="btn1"):
         if Pa == "CSB":
            st.session_state["authenticated"] = True
            st.rerun()  
         else:
            st.warning("Your Password Is Incorrect")
    if st.session_state["authenticated"]:
        N = st.text_input("Enter Your Name", key = 'un')
        I = st.text_input("Enter Your RollNo [Optional]", key = 'rn')
        M = st.text_input("Enter Your Mobile Number [Optional]", key = 'mn')
        Ma = st.text_input("Enter Your Marks", key = 'm')
        if st.form_submit_button("Submit Report"):
          if N and Ma:
            con= sqlite3.connect("marks.db")
            cur = con.cursor()
            cur.execute('''INSERT INTO CSS (RollNo, Name, Mobile, Marks) VALUES (?,?,?,?)''',(I,N,M,Ma))
            con.commit()
            con.close()
            st.success("Insert Successful")
          else:
            st.warning("Please Fill Out Mandatory Columns[Name,Marks]")
with tab2:
    st.header("Change The Entered Data")       
    if not st.session_state["authenticated"]:
       Pa = st.text_input("Enter Your Password", placeholder="Note: Ask The Admins", key = "pw2")
       if st.button("Enter Password", key="btn2"):
         if Pa == "CSB":
            st.session_state["authenticated"] = True
            st.rerun()  
         else:
            st.warning("Your Password Is Incorrect")
    if st.session_state["authenticated"]:
       con = sqlite3.connect("marks.db")
       cur = con.cursor()
       if not st.session_state["au"]:
        Na = st.text_input("Enter The Person's Name", placeholder="e.g.: Abc, Xyz,.....")
        if st.button("Submit"):
          if ex(Na):
             st.session_state["au"] = True
             st.session_state["NA"] = Na
          else:
             st.session_state["au"] = False
       if st.session_state["au"]:
         q = '''SELECT * FROM CSS WHERE Name = ?'''
         d = pd.read_sql_query(q,con,params= [st.session_state["NA"]])
         if not d.empty:
            OI = d.iloc[0,1 ]
            OM = d.iloc[0,3]
            OMa = d.iloc[0,4]
            st.info(f"Modifying the record for: {st.session_state["NA"]}")
            NI = st.text_input("Enter The New RollNo", value = OI)
            NM = st.text_input("Enter The New Mobile Number", value = OM)
            NMa = st.text_input("Enter The New Marks", value = OMa)
            if st.button ("Save Changes",key = "SC"):
               uq = '''UPDATE CSS SET RollNo = ?, Mobile = ?, Marks = ? WHERE Name = ?'''
               cur.execute(uq,(NI,NM,NMa,st.session_state["NA"]))
               st.success(f'Record of {st.session_state["NA"]} is updated!')
               con.commit()
               con.close()
            if st.button("Change Another Record"):
               st.session_state["au"] = False
               st.session_state["NA"] = ""
               st.rerun()
         else:
          st.error("Name Not Found/Not Inserted Yet")
          con.commit()
          con.close()
          if st.button("Refresh"):
             st.session_state["au"] = False
             st.rerun()
       st.header("Delete a Record")
       DN = st.text_input("Enter The Name Of Student Record To Be Deleted", placeholder="e.g.: Abc, Xyz,...")
       if st.button("Delete"):
         if ex (DN):
           con = sqlite3.connect("marks.db")
           cur = con.cursor()
           cur.execute('''DELETE FROM CSS WHERE Name = ?''', (DN,))
           st.success(f"Record Successfully Removed: {DN}")
           con.commit()
           con.close()
         else:
          st.error("Please Enter a Valid Name")
          con.commit()
          con.close()
with tab3:
    st.header("Marks and Ranks")
    sq = st.text_input("Who are you looking for?", placeholder = "e.g.: Abc, Xyz,...")
    if st.button("Refresh", key='btn7'):
       st.rerun()
    con = sqlite3.connect("marks.db")
    if sq:
      q = '''SELECT RollNo, Name, Mobile, Marks FROM CSS WHERE Name LIKE ?'''
      d = pd.read_sql_query(q,con, params = (f'%{sq}%',) )
      st.dataframe(d)
    else:
      d = pd.read_sql_query('''SELECT * FROM CSS''',con)
      st.dataframe(d)
    con.close()