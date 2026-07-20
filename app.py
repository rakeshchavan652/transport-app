import streamlit as st
import pandas as pd
import os
from datetime import datetime

# पानावरील सेटिंग्ज
st.set_page_config(page_title="Shri Kalbhairavnath Transport", page_icon="🚚", layout="wide")

# लॉगिन सिस्टम
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🚚 श्री काळभैरवनाथ ट्रान्सपोर्ट")
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
    # डॅशबोर्ड मेनू
    st.sidebar.title("🛠️ ट्रान्सपोर्ट मेनू")
    menu = st.sidebar.selectbox("काय करायचे आहे?", [
        "नवीन LR एंट्री (Data Entry)", 
        "LR एडिट करा (Edit LR)",
        "LR प्रिंट करा (Print Bill)", 
        "सर्व रेकॉर्ड्स पाहणे (View Data)"
    ])
    
    EXCEL_FILE = "transport_data.xlsx"
    
    # १. नवीन LR एंट्री फॉर्म
    if menu == "नवीन LR एंट्री (Data Entry)":
        st.header("📝 नवीन लॅपटॉप / LR डेटा एंट्री फॉर्म")
        
        with st.form("lr_form", clear_on_submit=True):
            st.markdown("### 🔹 बेसिक बिल माहिती")
            c1, c2, c3 = st.columns(3)
            with c1:
                lr_no = st.text_input("LR नंबर (उदा. SKT/26/001)")
                lr_date = st.date_input("तारीख (Date)", datetime.now())
            with c2:
                vehicle_no = st.text_input("गाडी नंबर (Vehicle No.)")
            with c3:
                driver_phone = st.text_input("ड्रायव्हर फोन नंबर")

            c4, c5 = st.columns(2)
            with c4:
                from_loc = st.text_input("कोठून (From)")
            with c5:
                to_loc = st.text_input("कोठे (To)")

            st.markdown("---")
            st.markdown("### 🔹 पार्टीचे तपशील (Sender & Receiver)")
            c6, c7 = st.columns(2)
            with c6:
                consignor = st.text_input("CONSIGNOR (माल पाठवणारा - M/S)")
                consignor_gst = st.text_input("Consignor GSTIN")
            with c7:
                consignee = st.text_input("CONSIGNEE (माल मिळणारा - M/S)")
                consignee_gst = st.text_input("Consignee GSTIN")

            st.markdown("---")
            st.markdown("### 🔹 मालाचा तपशील (Goods Details)")
            c8, c9, c10, c11 = st.columns(4)
            with c8:
                pkgs = st.number_input("नग (NO. OF PKGS)", min_value=0, step=1)
            with c9:
                description = st.text_input("माल तपशील (Description of Goods)")
            with c10:
                actual_wt = st.number_input("अ‍ॅक्चुअल वजन (Actual Wt. Tons)", min_value=0.0, step=0.01)
                charged_wt = st.number_input("चार्ज केलेले वजन (Charged Wt. Tons)", min_value=0.0, step=0.01)
            with c11:
                rate_basis = st.text_input("भाडे दर (Rate Basis)")

            st.markdown("---")
            st.markdown("### 🔹 भाडे आणि पेमेंट अटी (Freight & Payment)")
            c12, c13 = st.columns(2)
            with c12:
                payment_term = st.radio("FREIGHT PAYMENT TERMS (पेमेंट अट)", ["PAID", "TO PAY", "TO BE BILLED (TBB)"])
            with c13:
                basic_freight = st.number_input("BASIC FREIGHT (₹)", min_value=0, step=100)
                hamali = st.number_input("HAMALI / LOADING (₹)", min_value=0, step=50)
                statistical = st.number_input("STATISTICAL / OTHER (₹)", min_value=0, step=10)
                total_amount = basic_freight + hamali + statistical
                st.write(f"**एकूण रक्कम (TOTAL AMOUNT): ₹ {total_amount}**")

            submit = st.form_submit_button("डेटा सेव्ह करा (Save LR Entry)")
            
            if submit:
                if not lr_no or not vehicle_no:
                    st.error("कृपया LR नंबर आणि गाडी नंबर नक्की टाका!")
                else:
                    new_data = {
                        "LR No": [lr_no], "Date": [lr_date.strftime("%Y-%m-%d")], "Vehicle No": [vehicle_no], "Driver Phone": [driver_phone],
                        "From": [from_loc], "To": [to_loc], "Consignor": [consignor], "Consignor GSTIN": [consignor_gst],
                        "Consignee": [consignee], "Consignee GSTIN": [consignee_gst], "Pkgs": [pkgs], "Description": [description],
                        "Actual Wt": [actual_wt], "Charged Wt": [charged_wt], "Rate Basis": [rate_basis], "Payment Term": [payment_term],
                        "Basic Freight": [basic_freight], "Hamali": [hamali], "Statistical": [statistical], "Total Amount": [total_amount]
                    }
                    df_new = pd.DataFrame(new_data)
                    if os.path.exists(EXCEL_FILE):
                        df_old = pd.read_excel(EXCEL_FILE)
                        # डबल एंट्री टाळण्यासाठी जुना नंबर असेल तर आधी तो डिलीट करू
                        if lr_no in df_old["LR No"].values:
                            df_old = df_old[df_old["LR No"] != lr_no]
                        df_final = pd.concat([df_old, df_new], ignore_index=True)
                    else:
                        df_final = df_new
                    df_final.to_excel(EXCEL_FILE, index=False)
                    st.success(f"LR No. {lr_no} यशस्वीरित्या सेव्ह झाला आहे!")

    # २. LR एडिट करण्याचा नवीन विभाग
    elif menu == "LR एडिट करा (Edit LR)":
        st.header("✏️ जुनी LR एंट्री एडिट / दुरुस्त करा")
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            edit_lr = st.selectbox("दुरुस्त करण्यासाठी LR नंबर निवडा", df["LR No"].unique())
            
            if edit_lr:
                # निवडलेल्या LR चा जुना डेटा शोधणे
                idx = df[df["LR No"] == edit_lr].index[0]
                row = df.loc[idx]
                
                with st.form("edit_form"):
                    st.markdown(f"### 📍 LR नंबर: {edit_lr} चा डेटा एडिट करत आहात")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        e_date_str = str(row['Date'])
                        try:
                            e_date = datetime.strptime(e_date_str, "%Y-%m-%d")
                        except:
                            e_date = datetime.now()
                        new_date = st.date_input("तारीख बदलणे", e_date)
                    with c2:
                        new_vehicle = st.text_input("गाडी नंबर बदलणे", str(row['Vehicle No']))
                    with c3:
                        new_driver = st.text_input("ड्रायव्हर फोन बदलणे", str(row['Driver Phone']) if pd.notna(row['Driver Phone']) else "")

                    c4, c5 = st.columns(2)
                    with c4:
                        new_from = st.text_input("कोठून (From)", str(row['From']))
                    with c5:
                        new_to = st.text_input("कोठे (To)", str(row['To']))

                    st.markdown("---")
                    c6, c7 = st.columns(2)
                    with c6:
                        new_consignor = st.text_input("CONSIGNOR M/S", str(row['Consignor']))
                        new_consignor_gst = st.text_input("Consignor GSTIN", str(row['Consignor GSTIN']) if pd.notna(row['Consignor GSTIN']) else "")
                    with c7:
                        new_consignee = st.text_input("CONSIGNEE M/S", str(row['Consignee']))
                        new_consignee_gst = st.text_input("Consignee GSTIN", str(row['Consignee GSTIN']) if pd.notna(row['Consignee GSTIN']) else "")

                    st.markdown("---")
                    c8, c9, c10, c11 = st.columns(4)
                    with c8:
                        new_pkgs = st.number_input("नग (PKGS)", min_value=0, value=int(row['Pkgs']) if pd.notna(row['Pkgs']) else 0)
                    with c9:
                        new_desc = st.text_input("माल तपशील", str(row['Description']))
                    with c10:
                        new_act_wt = st.number_input("Actual Wt.", min_value=0.0, value=float(row['Actual Wt']) if pd.notna(row['Actual Wt']) else 0.0)
                        new_chg_wt = st.number_input("Charged Wt.", min_value=0.0, value=float(row['Charged Wt']) if pd.notna(row['Charged Wt']) else 0.0)
                    with c11:
                        new_basis = st.text_input("Rate Basis", str(row['Rate Basis']) if pd.notna(row['Rate Basis']) else "")

                    st.markdown("---")
                    c12, c13 = st.columns(2)
                    with c12:
                        # जुनी व्हॅल्यू सिलेक्ट ठेवणे
                        t_list = ["PAID", "TO PAY", "TO BE BILLED (TBB)"]
                        try:
                            t_idx = t_list.index(str(row['Payment Term']))
                        except:
                            t_idx = 0
                        new_term = st.radio("पेमेंट अट बदला", t_list, index=t_idx)
                    with c13:
                        new_basic = st.number_input("BASIC FREIGHT (₹)", min_value=0, value=int(row['Basic Freight']) if pd.notna(row['Basic Freight']) else 0)
                        new_hamali = st.number_input("HAMALI / LOADING (₹)", min_value=0, value=int(row['Hamali']) if pd.notna(row['Hamali']) else 0)
                        new_stat = st.number_input("STATISTICAL / OTHER (₹)", min_value=0, value=int(row['Statistical']) if pd.notna(row['Statistical']) else 0)
                        new_total = new_basic + new_hamali + new_stat
                        st.write(f"**नवीन एकूण रक्कम: ₹ {new_total}**")

                    update_submit = st.form_submit_button("🔄 डेटा अपडेट करा (Update LR)")
                    
                    if update_submit:
                        df.loc[idx, "Date"] = new_date.strftime("%Y-%m-%d")
                        df.loc[idx, "Vehicle No"] = new_vehicle
                        df.loc[idx, "Driver Phone"] = new_driver
                        df.loc[idx, "From"] = new_from
                        df.loc[idx, "To"] = new_to
                        df.loc[idx, "Consignor"] = new_consignor
                        df.loc[idx, "Consignor GSTIN"] = new_consignor_gst
                        df.loc[idx, "Consignee"] = new_consignee
                        df.loc[idx, "Consignee GSTIN"] = new_consignee_gst
                        df.loc[idx, "Pkgs"] = new_pkgs
                        df.loc[idx, "Description"] = new_desc
                        df.loc[idx, "Actual Wt"] = new_act_wt
                        df.loc[idx, "Charged Wt"] = new_chg_wt
                        df.loc[idx, "Rate Basis"] = new_basis
                        df.loc[idx, "Payment Term"] = new_term
                        df.loc[idx, "Basic Freight"] = new_basic
                        df.loc[idx, "Hamali"] = new_hamali
                        df.loc[idx, "Statistical"] = new_stat
                        df.loc[idx, "Total Amount"] = new_total
                        
                        df.to_excel(EXCEL_FILE, index=False)
                        st.success(f"LR No. {edit_lr} चा डेटा यशस्वीरित्या अपडेट झाला आहे!")
                        st.rerun()
        else:
            st.warning("अद्याप कोणताही डेटा नाही, आधी नवीन एंट्री करा.")

    # ३. पावती प्रिंट करण्याचा विभाग
    elif menu == "LR प्रिंट करा (Print Bill)":
        st.header("🖨️ लॅपटॉप पावती प्रिंटर")
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            search_lr = st.selectbox("प्रिंट करण्यासाठी LR नंबर निवडा", df["LR No"].unique())
            
            if search_lr:
                row = df[df["LR No"] == search_lr].iloc[0]
                
                bill_html = f"""
                <div style="border: 3px double #f39c12; padding: 20px; font-family: Arial, sans-serif; background-color: #fff; color: #000; max-width: 800px; margin: auto;">
                    <div style="text-align: center; border-bottom: 2px solid #f39c12; padding-bottom: 10px;">
                        <span style="float: right; text-align: right; font-size: 12px; font-weight: bold;">
                            Booking Contacts:<br>9623903901<br>9763995328<br>9527260445
                        </span>
                        <h1 style="color: #d35400; margin: 0; font-size: 28px; font-weight: bold; text-align: left;">SHRI KALBHAIRAVNATH TRANSPORT</h1>
                        <p style="text-align: left; margin: 5px 0; font-weight: bold; font-size: 13px; letter-spacing: 1px;">FLEET OWNERS & TRANSPORT CONTRACTORS</p>
                        <p style="text-align: left; margin: 0; font-size: 12px;"><b>Regd. Office:</b> Mantarwadi, Uruli Devachi, Tal-Haveli, Dist-Pune 412308</p>
                        <div style="background-color: #000; color: #fff; display: inline-block; padding: 4px 10px; font-size: 12px; font-weight: bold; margin-top: 5px; float: right;">GSTIN / ID: 27BKEPC5674H1Z3</div>
                        <div style="clear: both;"></div>
                    </div>
                    
                    <div style="background-color: #ffaa44; text-align: center; font-weight: bold; padding: 5px; margin: 10px 0; font-size: 16px; border: 1px solid #d35400;">
                        GOODS FORWARDING / LORRY RECEIPT (L.R.)
                    </div>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 10px;" border="1">
                        <tr>
                            <td style="padding: 5px; width: 33%;"><b>L.R. NO:</b> {row['LR No']}</td>
                            <td style="padding: 5px; width: 33%;"><b>DATE:</b> {row['Date']}</td>
                            <td style="padding: 5px; width: 34%;"><b>VEHICLE NO:</b> {row['Vehicle No']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px;"><b>FROM:</b> {row['From']}</td>
                            <td style="padding: 5px;"><b>TO:</b> {row['To']}</td>
                            <td style="padding: 5px;"><b>DRIVER PHONE:</b> {row['Driver Phone'] if pd.notna(row['Driver Phone']) else ''}</td>
                        </tr>
                    </table>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 10px;" border="1">
                        <tr style="background-color: #ffaa44; font-weight: bold; text-align: center;">
                            <td style="width: 50%; padding: 3px;">CONSIGNOR (SENDER DETAILS)</td>
                            <td style="width: 50%; padding: 3px;">CONSIGNEE (RECEIVER DETAILS)</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; height: 60px; vertical-align: top;"><b>M/S:</b> {row['Consignor']}<br><br><b>GSTIN:</b> {row['Consignor GSTIN'] if pd.notna(row['Consignor GSTIN']) else ''}</td>
                            <td style="padding: 8px; height: 60px; vertical-align: top;"><b>M/S:</b> {row['Consignee']}<br><br><b>GSTIN:</b> {row['Consignee GSTIN'] if pd.notna(row['Consignee GSTIN']) else ''}</td>
                        </tr>
                    </table>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: center;" border="1">
                        <tr style="background-color: #f2f2f2; font-weight: bold;">
                            <td style="padding: 5px; width: 10%;">NO. OF PKGS</td>
                            <td style="padding: 5px; width: 45%;">DESCRIPTION OF GOODS (SAID TO CONTAIN)</td>
                            <td style="padding: 5px; width: 15%;">ACTUAL WT.</td>
                            <td style="padding: 5px; width: 15%;">CHARGED WT.</td>
                            <td style="padding: 5px; width: 15%;">RATE BASIS</td>
                        </tr>
                        <tr style="height: 120px; vertical-align: top;">
                            <td style="padding: 5px;"><br>{row['Pkgs']}</td>
                            <td style="padding: 5px; text-align: left;"><br>{row['Description']}</td>
                            <td style="padding: 5px;"><br>{row['Actual Wt']} Tons</td>
                            <td style="padding: 5px;"><br>{row['Charged Wt']} Tons</td>
                            <td style="padding: 5px;"><br>{row['Rate Basis'] if pd.notna(row['Rate Basis']) else ''}</td>
                        </tr>
                        <tr style="background-color: #fff8ee; font-weight: bold;">
                            <td style="padding: 5px;">TOTAL</td>
                            <td style="padding: 5px;"></td>
                            <td style="padding: 5px;"></td>
                            <td style="padding: 5px;"></td>
                            <td style="padding: 5px;"></td>
                        </tr>
                    </table>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 10px;" border="1">
                        <tr>
                            <td style="width: 50%; padding: 10px; vertical-align: top;">
                                <b>FREIGHT PAYMENT TERMS:</b><br><br>
                                <span style="border: 1px solid #000; padding: 2px 8px; font-weight: bold; background-color: #eee;">
                                    {row['Payment Term']}
                                </span>
                            </td>
                            <td style="width: 50%; padding: 0;">
                                <table style="width: 100%; border-collapse: collapse;" border="1">
                                    <tr><td style="padding: 4px; width: 60%;"><b>BASIC FREIGHT:</b></td><td style="padding: 4px; text-align: right;">₹ {row['Basic Freight']}</td></tr>
                                    <tr><td style="padding: 4px;"><b>HAMALI / LOADING:</b></td><td style="padding: 4px; text-align: right;">₹ {row['Hamali']}</td></tr>
                                    <tr><td style="padding: 4px;"><b>STATISTICAL / OTHER:</b></td><td style="padding: 4px; text-align: right;">₹ {row['Statistical']}</td></tr>
                                    <tr style="background-color: #fff8ee; font-weight: bold;"><td style="padding: 4px;"><b>TOTAL AMOUNT:</b></td><td style="padding: 4px; text-align: right;">₹ {row['Total Amount']}</td></tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    
                    <p style="font-size: 9px; color: #555; margin: 8px 0; line-height: 1.2;">
                        <b>Terms of Carriage:</b> 1. Goods are carried at Owner's risk... 2. The company is not liable for structural leakage... 3. Unloading must be processed immediately... 4. All jurisdictions are restricted to Pune courts.
                    </p>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 11px; text-align: center; margin-top: 15px;" border="1">
                        <tr style="height: 50px; vertical-align: bottom;">
                            <td style="width: 33%; padding-bottom: 5px;">Consignee's Stamp & Sign</td>
                            <td style="width: 33%; padding-bottom: 5px;">Driver's Signature/Thumb</td>
                            <td style="width: 34%; padding-bottom: 5px; font-size: 10px;">For SHRI KALBHAIRAVNATH TRANSPORT<br><br><br><b>Authorized Signature</b></td>
                        </tr>
                    </table>
                </div>
                """
                st.markdown(bill_html, unsafe_allow_html=True)
                st.info("💡 टीप: ही पावती प्रिंट करण्यासाठी तुमच्या मोबाईलमध्ये स्क्रीनशॉट काढा किंवा कॉम्प्युटरवरून Ctrl + P दाबून PDF म्हणून सेव्ह करा!")
        else:
            st.warning("अद्याप कोणताही डेटा नोंदवलेला नाही.")

    # ४. सर्व डेटा पाहणे
    elif menu == "सर्व रेकॉर्ड्स पाहणे (View Data)":
        st.header("📋 नोंदवलेला सर्व डेटा")
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            st.dataframe(df)
            with open(EXCEL_FILE, "rb") as f:
                st.download_button(label="📥 एक्सेल फाईल डाऊनलोड करा", data=f, file_name="Transport_Entries.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.warning("अद्याप कोणताही डेटा नाही.")

    if st.sidebar.button("लॉगआउट (Logout)"):
        st.session_state.logged_in = False
        st.rerun()
