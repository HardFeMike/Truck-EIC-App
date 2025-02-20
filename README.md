# Truck-EIC-App

# Truck EIC Qualification App

This is a **Streamlit web app** that allows users to:
- Upload **'The Dispatcher'** and **'ZFNQState'** Excel files
- Select **UIC from a dropdown**
- View **filtered trucks and qualified personnel**
- Download the results

## 🚀 How to Run the App Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/Truck-EIC-App.git
   cd Truck-EIC-App
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App**:
   ```bash
   streamlit run streamlit_app.py
   ```

## 🌍 Deployment to Streamlit Cloud

1. Push this repo to **GitHub**.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Select **New App** → Connect your GitHub repo.
4. Choose `streamlit_app.py` as the main file.
5. Click **Deploy** and get a public URL!

🔗 **Live Demo**: [Try the App](https://your-app-url.streamlit.app)

## 📂 File Structure
```
/Truck-EIC-App
│── streamlit_app.py    # Main app script
│── requirements.txt    # Dependencies
│── README.md           # Instructions
```

## 🖼 Example Screenshots
![App Screenshot](link_to_screenshot.png)

## ✅ Features & Future Enhancements
- [x] File Upload & Filtering
- [x] Dropdown UIC Selection
- [x] Export Filtered Results
- [ ] Add Authentication (Login System)
- [ ] Store Data in a Database

## 🤝 Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit changes (`git commit -m "Added new feature"`)
4. Push to GitHub (`git push origin feature-branch`)
5. Submit a Pull Request 🚀

## 🛠 Troubleshooting
- **Error: ModuleNotFoundError: No module named 'streamlit'**
  - Run: `pip install -r requirements.txt`
- **App Not Running on Streamlit Cloud?**
  - Ensure all files are committed and your `streamlit_app.py` is correctly set as the main script.

---
Built with ❤️ using Streamlit & Pandas.
