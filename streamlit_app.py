import streamlit as st
import pandas as pd

# Set page title and layout
st.set_page_config(page_title="Truck EIC Qualification App", layout="wide")

st.title("🚛 Truck EIC Qualification App")
st.markdown("---")

st.sidebar.header("📂 Upload Data")
dispatcher_file = st.sidebar.file_uploader("Upload 'The Dispatcher' Excel", type=["xlsx"])
zfnqstate_file = st.sidebar.file_uploader("Upload 'ZFNQState' Excel", type=["xlsx"])

if dispatcher_file and zfnqstate_file:
    dispatcher_df = pd.read_excel(dispatcher_file)
    zfnqstate_df = pd.read_excel(zfnqstate_file)
    
    st.sidebar.markdown("### 🔍 Select UIC")
    uic_list = dispatcher_df["Unit Identification Code"].dropna().unique()
    selected_uic = st.sidebar.selectbox("Select UIC", ["Select"] + list(uic_list))
    
    if selected_uic != "Select":
        filtered_trucks = dispatcher_df[dispatcher_df["Unit Identification Code"] == selected_uic]
        eic_list = filtered_trucks["Admin No."].unique()
        qualified_personnel = zfnqstate_df[zfnqstate_df["EIC/Abr"].isin(eic_list)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚚 Available Trucks")
            st.dataframe(filtered_trucks[["Admin No.", "Material Description", "Model number"]].style.set_properties(**{'background-color': '#f9f9f9', 'border': '1px solid black'}))
        
        with col2:
            st.subheader("👷‍♂️ Qualified Personnel")
            st.dataframe(qualified_personnel[["Name", "EIC/Abr", "Qualification", "Proficiency"]].style.set_properties(**{'background-color': '#f9f9f9', 'border': '1px solid black'}))
        
        st.markdown("---")
        
        st.subheader("📥 Download Filtered Data")
        if st.button("Download Trucks Data", key="trucks"):
            filtered_trucks.to_excel("Filtered_Trucks.xlsx", index=False)
            st.success("✅ Download Ready! Check your files.")
