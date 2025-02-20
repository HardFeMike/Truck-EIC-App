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
    uic_list = sorted(set(dispatcher_df["Unit Identification Code"].dropna().unique()).union(static_uics))
    selected_uic = st.selectbox("Select UIC", ["ALL"] + ["Select"] + list(uic_list))
    
    if selected_uic != "Select":
        if selected_uic == "ALL":
            filtered_trucks = dispatcher_df
        else:
            filtered_trucks = dispatcher_df[dispatcher_df["Unit Identification Code"] == selected_uic]
        
        st.write("### Available Trucks:")
        
        for index, row in filtered_trucks.iterrows():
            admin_no = row["Admin No."]
            eic_value = dispatcher_df.loc[dispatcher_df["Admin No."] == admin_no, "EIC/Abr"].values[0] if "EIC/Abr" in dispatcher_df.columns else admin_no
            
            # Debugging Output
            st.write(f"🔍 Checking Truck: {admin_no}")
            st.write(f"🔍 Expected EIC: {eic_value}")
            
            eligible_drivers = zfnqstate_df[(zfnqstate_df["EIC/Abr"] == eic_value) & (zfnqstate_df["Qualification"] == "STANDARD")]
            
            st.write("🔍 Eligible Drivers:")
            st.write(eligible_drivers)
            
            uic_options = ["Select UIC"] + static_uics if not eligible_drivers.empty else ["No UICs Available"]
            selected_driver_uic = st.selectbox(f"Select UIC for Truck {admin_no}", uic_options, key=f"uic_{index}")
            
            if selected_driver_uic != "Select UIC" and selected_driver_uic != "No UICs Available":
                filtered_drivers = eligible_drivers[eligible_drivers["UIC"] == selected_driver_uic]
                
                st.write("🔍 Filtered Drivers Based on UIC:")
                st.write(filtered_drivers)
                
                driver_options = ["Select Driver"] + list(filtered_drivers["Name"].unique()) if not filtered_drivers.empty else ["No Drivers Available"]
                selected_driver = st.selectbox(f"Select Driver for Truck {admin_no}", driver_options, key=f"driver_{index}")
                
                if selected_driver != "Select Driver" and selected_driver != "No Drivers Available":
                    personal_number = filtered_drivers[filtered_drivers["Name"] == selected_driver]["ID rel.obj"].values[0]
                    st.text_input(f"Personal Number for {selected_driver}", personal_number, key=f"personal_{index}")
        
        st.write("### Qualified Personnel:")
        st.dataframe(zfnqstate_df[["Name", "EIC/Abr", "Qualification", "Proficiency"]])
    
    if st.button("Download Filtered Data"):
        filtered_trucks.to_excel("Filtered_Trucks.xlsx", index=False)
        st.success("Download Ready! Check your files.")
