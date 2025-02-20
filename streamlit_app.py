import streamlit as st
import pandas as pd

# Upload Excel files
st.title("Truck EIC Qualification App")

st.sidebar.header("Upload Data")
dispatcher_file = st.sidebar.file_uploader("Upload 'The Dispatcher' Excel", type=["xlsx"])
zfnqstate_file = st.sidebar.file_uploader("Upload 'ZFNQState' Excel", type=["xlsx"])

if dispatcher_file and zfnqstate_file:
    dispatcher_df = pd.read_excel(dispatcher_file)
    zfnqstate_df = pd.read_excel(zfnqstate_file)
    
    # Select UIC
    uic_list = dispatcher_df["Unit Identification Code"].dropna().unique()
    selected_uic = st.selectbox("Select UIC", ["Select"] + list(uic_list))
    
    if selected_uic != "Select":
        # Filter trucks by UIC
        filtered_trucks = dispatcher_df[dispatcher_df["Unit Identification Code"] == selected_uic]
        st.write("### Available Trucks:")
        st.dataframe(filtered_trucks[["Admin No.", "Material Description", "Model number"]])
        
        # Match EIC personnel
        eic_list = filtered_trucks["Admin No."].unique()
        qualified_personnel = zfnqstate_df[zfnqstate_df["EIC/Abr"].isin(eic_list)]
        
        st.write("### Qualified Personnel:")
        st.dataframe(qualified_personnel[["Name", "EIC/Abr", "Qualification", "Proficiency"]])
    
    # Option to download filtered results
    if st.button("Download Filtered Data"):
        filtered_trucks.to_excel("Filtered_Trucks.xlsx", index=False)
        st.success("Download Ready! Check your files.")