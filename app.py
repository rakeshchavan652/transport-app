import streamlit as st
import pandas as pd
import os
from datetime import datetime

# पानावरील सेटिंग्ज (मोबाईल आणि कॉम्प्युटर दोन्हीसाठी व्यवस्थित दिसण्यासाठी Wide लेआउट)
st.set_page_config(page_title="Shri Kalbhairavnath Transport", page_icon="🚚", layout="wide")

# लॉगिन सिस्टम चेक करणे
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# जर लॉगिन नसेल तर लॉगिन फॉर्म दाखवणे
if not st.session_state.logged_in:
    st.title("🚚 श्री काळभैरवनाथ ट्रान्सポート")
    st.subheader("लॉगिन करा")
    username = st.text_input("युझरनेम (Username)")
    password = st.text_input("पासवर्ड (Password)", type="password")
    if st.button("लॉगिन"):
        if username == "admin" and password == "kalbhairav@123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("चुकीचे युझरनेम किंवा पासवर्ड!")
else:
    # डॅशबोर्ड मेनू (मोबाईलवर डाव्या बाजूला किंवा वरती ३ रेषांवर क्लिक केल्यावर दिसेल)
    st.sidebar.title("🛠️ ट्रान्सपोर्ट मेनू")
    menu = st.sidebar.selectbox("काय करायचे आहे?", ["नवीन LR एंट्री (Data Entry)", "सर्व रेकॉर्ड्स पाहणे (View Data)"])
    
    # एक्सेल फाईलचे नाव (जिथे डेटा सेव्ह होईल)
    EXCEL_FILE = "transport_data.xlsx"
    
    # १. नवीन LR एंट्री फॉर्म
    if menu == "नवीन LR एंट्री (Data Entry)":
        st.header("📝 नवीन लॅपटॉप / LR डेटा एंट्री फॉर्म")
        
        with st.form("lr_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                lr_no = st.text_input("LR नंबर (LR No.)")
                lr_date = st.date_input("तारीख (Date)", datetime.now())
                truck_no = st.text_input("गाडी नंबर (Truck No.)")
                from_loc = st.text_input("कोठून (From)")
                to_loc = st.text_input("कोठे (To)")
            
            with col2:
                description = st.text_input("माल तपशील (Material Description)")
                weight = st.number_input("वजन (Weight in Tons)", min_value=0.0, step=0.1)
                freight = st.number_input("भाडे रक्कम (Total Freight ₹)", min_value=0, step=100)
                advance = st.number_input("अ‍ॅडव्हान्स (Advance Paid ₹)", min_value=0, step=100)
                party_name = st.text_input("पार्टीचे नाव (Party Name)")
            
            submit = st.form_submit_button("डेटा सेव्ह करा (Save Entry)")
            
            if submit:
                if not lr_no or not truck_no:
                    st.error("कृपया LR नंबर आणि गाडी नंबर नक्की टाका!")
                else:
                    new_data = {
                        "LR No": [lr_no],
                        "Date": [lr_date.strftime("%Y-%m-%d")],
                        "Truck No": [truck_no],
                        "From": [from_loc],
                        "To": [to_loc],
                        "Description": [description],
                        "Weight (Tons)": [weight],
                        "Total Freight": [freight],
                        "Advance": [advance],
                        "Balance": [freight - advance],
                        "Party Name": [party_name]
                    }
                    df_new = pd.DataFrame(new_data)
                    
                    if os.path.exists(EXCEL_FILE):
                        df_old = pd.read_excel(EXCEL_FILE)
                        df_final = pd.concat([df_old, df_new], ignore_index=True)
                    else:
                        df_final = df_new
                        
                    df_final.to_excel(EXCEL_FILE, index=False)
                    st.success(f"LR No. {lr_no} चा डेटा यशस्वीरित्या सेव्ह झाला आहे!")
                    
    # २. सर्व रेकॉर्ड्स पाहणे आणि एक्सेल डाऊनलोड करणे
    elif menu == "सर्व रेकॉर्ड्स पाहणे (View Data)":
        st.header("📋 नोंदवलेला सर्व डेटा")
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            st.dataframe(df)
            
            # एक्सेल डाऊनलोड करण्याचे बटण
            with open(EXCEL_FILE, "rb") as f:
                st.download_button(
                    label="📥 एक्सेल फाईल डाऊनलोड करा (Download Excel)",
                    data=f,
                    file_name="Transport_Entries.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("अद्याप कोणताही डेटा नोंदवलेला नाही. कृपया आधी डेटा एंट्री करा.")

    # लॉगआउट बटण
    if st.sidebar.button("ลॉगआउट (Logout)"):
        st.session_state.logged_in = False
        st.rerun()
