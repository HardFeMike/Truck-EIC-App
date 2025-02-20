import streamlit as st
import pandas as pd

st.title("Truck EIC Qualification App")

st.sidebar.header("Upload Data")
dispatcher_file = st.sidebar.file_uploader("Upload 'The Dispatcher' Excel", type=["xlsx"])
zfnqstate_file = st.sidebar.file_uploader("Upload 'ZFNQState' Excel", type=["xlsx"])

if dispatcher_file and zfnqstate_file:
    dispatcher_df = pd.read_excel(dispatcher_file)
    zfnqstate_df = pd.read_excel(zfnqstate_file)
    
    # Ensure column names are correct
    required_columns_dispatcher = ["Unit Identification Code", "Admin No."]
    required_columns_zfnq = ["UIC", "EIC/Abr", "Name", "Qualification", "ID rel.obj"]
    
    if not all(col in dispatcher_df.columns for col in required_columns_dispatcher):
        st.error("Error: Missing required columns in 'The Dispatcher' file.")
    elif not all(col in zfnqstate_df.columns for col in required_columns_zfnq):
        st.error("Error: Missing required columns in 'ZFNQState' file.")
    else:
        uic_list = dispatcher_df["Unit Identification Code"].dropna().unique()
        selected_uic = st.selectbox("Select UIC", ["Select"] + list(uic_list))
        
        if selected_uic != "Select":
            filtered_trucks = dispatcher_df[dispatcher_df["Unit Identification Code"] == selected_uic]
            st.write("### Available Trucks:")
            
            for index, row in filtered_trucks.iterrows():
                admin_no = row["Admin No."]
                eligible_drivers = zfnqstate_df[(zfnqstate_df["EIC/Abr"] == admin_no) & (zfnqstate_df["Qualification"].str.upper() == "STANDARD")]
                
                if eligible_drivers.empty:
                    st.warning(f"No qualified drivers available for Truck {admin_no}")
                else:
                    uic_options = ["Select UIC"] + list(eligible_drivers["UIC"].dropna().unique())
                    selected_driver_uic = st.selectbox(f"Select UIC for Truck {admin_no}", uic_options, key=f"uic_{index}")
                    
                    if selected_driver_uic != "Select UIC":
                        filtered_drivers = eligible_drivers[eligible_drivers["UIC"] == selected_driver_uic]
                        driver_options = ["Select Driver"] + list(filtered_drivers["Name"].unique())
                        selected_driver = st.selectbox(f"Select Driver for Truck {admin_no}", driver_options, key=f"driver_{index}")
                        
                        if selected_driver != "Select Driver":
                            personal_number = filtered_drivers[filtered_drivers["Name"] == selected_driver]["ID rel.obj"].values[0]
                            st.text_input(f"Personal Number for {selected_driver}", personal_number, key=f"personal_{index}")
            
            st.write("### Qualified Personnel:")
            st.dataframe(zfnqstate_df[["Name", "EIC/Abr", "Qualification", "Proficiency"]])
        
        if st.button("Download Filtered Data"):
            filtered_trucks.to_excel("Filtered_Trucks.xlsx", index=False)
            st.success("Download Ready! Check your files.")
