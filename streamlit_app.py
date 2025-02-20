import streamlit as st
import pandas as pd

st.title("Truck EIC Qualification App")

st.sidebar.header("Upload Data")
dispatcher_file = st.sidebar.file_uploader("Upload 'The Dispatcher' Excel", type=["xlsx"])
zfnqstate_file = st.sidebar.file_uploader("Upload 'ZFNQState' Excel", type=["xlsx"])

if dispatcher_file and zfnqstate_file:
    dispatcher_df = pd.read_excel(dispatcher_file)
    zfnqstate_df = pd.read_excel(zfnqstate_file)
    
    uic_list = dispatcher_df["Unit Identification Code"].dropna().unique()
    selected_uic = st.selectbox("Select UIC", ["Select"] + list(uic_list))
    
    if selected_uic != "Select":
        filtered_trucks = dispatcher_df[dispatcher_df["Unit Identification Code"] == selected_uic]
        st.write("### Available Trucks:")
        
        # Create a dropdown for each truck to select a qualified driver
        for index, row in filtered_trucks.iterrows():
            eic_code = row["Admin No."]
            eligible_drivers = zfnqstate_df[(zfnqstate_df["EIC/Abr"] == eic_code) & (zfnqstate_df["Qualification"] == "STANDARD")]
            
            driver_options = ["Select Driver"] + list(eligible_drivers["Name"].unique())
            selected_driver = st.selectbox(f"Select Driver for {row['Material Description']} ({row['Model number']})", driver_options, key=f"driver_{index}")
        
        st.write("### Qualified Personnel:")
        st.dataframe(zfnqstate_df[["Name", "EIC/Abr", "Qualification", "Proficiency"]])
    
    if st.button("Download Filtered Data"):
        filtered_trucks.to_excel("Filtered_Trucks.xlsx", index=False)
        st.success("Download Ready! Check your files.")
