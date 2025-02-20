import streamlit as st
import pandas as pd

st.title("Truck EIC Qualification App")

st.sidebar.header("Upload Data")
dispatcher_file = st.sidebar.file_uploader("Upload 'The Dispatcher' Excel", type=["xlsx"])
zfnqstate_file = st.sidebar.file_uploader("Upload 'ZFNQState' Excel", type=["xlsx"])

if dispatcher_file and zfnqstate_file:
    dispatcher_df = pd.read_excel(dispatcher_file)
    zfnqstate_df = pd.read_excel(zfnqstate_file)
    
    static_uics = ["WPPTA0", "WPPTB0", "WPPTC0", "WPPTT0", "WPCPD0"]
    
    # Select UIC
    selected_uic = st.selectbox("Select UIC", ["Select UIC"] + static_uics)
    
    if selected_uic != "Select UIC":
        # Filter eligible trucks based on selected UIC
        filtered_trucks = dispatcher_df.copy()
        
        # Select Truck
        selected_truck = st.selectbox("Select Truck", ["Select Truck"] + filtered_trucks["Admin No."].dropna().unique().tolist())
        
        if selected_truck != "Select Truck":
            # Get EIC value for the selected truck
            eic_value = dispatcher_df.loc[dispatcher_df["Admin No."] == selected_truck, "Functional Location"].astype(str).str[:3].values[0]
            
            # Get eligible drivers based on UIC and EIC
            eligible_drivers = zfnqstate_df[(zfnqstate_df["EIC/Abr"].astype(str).str.strip() == str(eic_value).strip()) & (zfnqstate_df["UIC"] == selected_uic)]
            
            driver_options = ["Select Driver"] + eligible_drivers["Name"].dropna().unique().tolist()
            selected_driver = st.selectbox("Select Driver", driver_options)
            
            if selected_driver != "Select Driver":
                personal_number = eligible_drivers.loc[eligible_drivers["Name"] == selected_driver, "ID rel.obj"].values[0]
                st.text_input("Personal Number", personal_number)
    
    # Allow Download of Filtered Data
    if st.button("Download Updated Data"):
        filtered_trucks.to_excel("Updated_Truck_Assignments.xlsx", index=False)
        st.success("Download Ready! Check your files.")
