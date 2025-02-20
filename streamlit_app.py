import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")  # Enables full-width layout

st.title("Truck EIC Qualification App")

st.sidebar.header("Upload Data")
dispatcher_file = st.sidebar.file_uploader("Upload 'The Dispatcher' Excel", type=["xlsx"])
zfnqstate_file = st.sidebar.file_uploader("Upload 'ZFNQState' Excel", type=["xlsx"])

if dispatcher_file and zfnqstate_file:
    dispatcher_df = pd.read_excel(dispatcher_file)
    zfnqstate_df = pd.read_excel(zfnqstate_file)
    
    static_uics = ["WPPTA0", "WPPTB0", "WPPTC0", "WPPTT0", "WPCPD0"]
    
    # Display all trucks in a horizontal format with tighter spacing
    st.write("### Available Trucks")
    
    for index, row in dispatcher_df.iterrows():
        eic_value = row["Functional Location"][:3] if isinstance(row["Functional Location"], str) else "UNKNOWN"
        
        with st.container():
            col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1.5], gap="small")  # Reduce column width & spacing
            
            with col1:
                st.write(f"**Truck:** {row['Admin No.']}")
                st.write(f"EIC: {eic_value}")
            
            with col2:
                selected_uic = st.selectbox(f"Select UIC for {row['Admin No.']}", static_uics, key=f"uic_{index}")
            
            with col3:
                eligible_drivers = zfnqstate_df[(zfnqstate_df["EIC/Abr"].astype(str).str.strip() == str(eic_value).strip()) & (zfnqstate_df["UIC"] == selected_uic)]
                driver_options = ["Select Driver"] + eligible_drivers["Name"].dropna().unique().tolist()
                selected_driver = st.selectbox(f"Select Driver for {row['Admin No.']}", driver_options, key=f"driver_{index}")
            
            with col4:
                if selected_driver != "Select Driver":
                    personal_number = eligible_drivers.loc[eligible_drivers["Name"] == selected_driver, "ID rel.obj"].values[0]
                    st.text_input(f"Personal Number for {selected_driver}", personal_number, key=f"personal_{index}")
    
    # Allow Download of Filtered Data
    if st.button("Download Updated Data"):
        dispatcher_df.to_excel("Updated_Truck_Assignments.xlsx", index=False)
        st.success("Download Ready! Check your files.")
