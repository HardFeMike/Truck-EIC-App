
import streamlit as st
import pandas as pd

st.title("Truck EIC Qualification App - Excel View")

st.sidebar.header("Upload Data")
dispatcher_file = st.sidebar.file_uploader("Upload 'The Dispatcher' Excel", type=["xlsx"])
zfnqstate_file = st.sidebar.file_uploader("Upload 'ZFNQState' Excel", type=["xlsx"])

if dispatcher_file and zfnqstate_file:
    dispatcher_df = pd.read_excel(dispatcher_file)
    zfnqstate_df = pd.read_excel(zfnqstate_file)
    
    static_uics = ["WPPTA0", "WPPTB0", "WPPTC0", "WPPTT0", "WPCPD0"]
    
    # Prepare the editable dataframe
    trucks_data = []
    
    for _, row in dispatcher_df.iterrows():
        admin_no = row["Admin No."]
        eic_value = row["Functional Location"][:3] if "Functional Location" in row and isinstance(row["Functional Location"], str) else "UNKNOWN"
        
        # Find eligible drivers
        eligible_drivers = zfnqstate_df[zfnqstate_df["EIC/Abr"].astype(str).str.strip() == str(eic_value).strip()]
        driver_names = eligible_drivers["Name"].tolist()
        driver_names.insert(0, "Select Driver")  # Add default option
        
        # Use the static UIC options
        uic_options = static_uics
        
        # Add row to trucks data
        trucks_data.append({
            "Admin No.": admin_no,
            "EIC": eic_value,
            "Select UIC": "Select UIC",
            "Select Driver": "Select Driver",
            "Available Drivers": driver_names,
            "Personal Number": ""
        })
    
    # Convert to DataFrame for editable table
    trucks_df = pd.DataFrame(trucks_data)
    
    # Display interactive table
    edited_trucks_df = st.data_editor(trucks_df, 
                                      column_config={
                                          "Select UIC": st.column_config.SelectboxColumn("Select UIC", options=static_uics),
                                          "Select Driver": st.column_config.SelectboxColumn("Select Driver", options=trucks_df["Available Drivers"].tolist()),
                                          "Personal Number": st.column_config.TextColumn("Personal Number")
                                      },
                                      hide_index=True)
    
    # Allow Download of Edited Data
    if st.button("Download Updated Data"):
        edited_trucks_df.to_excel("Updated_Truck_Assignments.xlsx", index=False)
        st.success("Download Ready! Check your files.")
