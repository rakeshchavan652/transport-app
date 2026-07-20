import streamlit as st
import pandas as pd
import os

# पानावरील सेटिंग्ज
st.set_page_config(page_title="Shri Kalbhairavnath Transport", page_icon="🚚", layout="centered")

# लॉगिन सिस्टम चेक करणे
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# जर लॉगिन नसेल तर लॉगिन फॉर्म दाखवणे
if not st.session_state.logged_in:
    st.title("🚚 श्री काळभैरवनाथ ट्रान्सपोर्ट")
    st.subheader("लॉगिन करा")
    
    username = st.text_input("युझरनेम (Username)")
    password = st.text_input("पासवर्ड (Password)", type="password")
    
    if st.button("लॉगिन"):
        if username == "admin" and password == "kalbhairav@123":
            st.session_state.logged_in = True
            st.success("लॉगिन यशस्वी!")
            st.rerun()
        else:
            st.error("चुकीचे युझरनेम किंवा पासवर्ड!")
            
# लॉगिन झाल्यावर दिसणारा डॅशबोर्ड
else:
    st.title("📊 श्री काळभैरवनाथ ट्रान्सपोर्ट डॅशボード")
    st.write("तुमचे अ‍ॅप आता यशस्वीरित्या सुरू झाले आहे! इथून पुढे तुम्ही तुमचे काम करू शकता.")
    
    if st.button("लॉगआउट"):
        st.session_state.logged_in = False
        st.rerun()

