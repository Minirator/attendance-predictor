
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Attendance Predictor", layout="centered")
st.title("📊 Week 6 Attendance Predictor")
st.markdown("Upload a file with Student IDs and their current attendance %, then select the current week.")

uploaded_file = st.file_uploader("Upload Excel or CSV", type=["xlsx", "csv"])
current_week = st.selectbox("Select Current Week (1-6)", list(range(1, 7)))

if uploaded_file and current_week:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if 'Student ID' in df.columns and 'Current Attendance %' in df.columns:
        # Ensure percentage is numeric
        df['Current Attendance %'] = pd.to_numeric(df['Current Attendance %'], errors='coerce')
        df.dropna(subset=['Current Attendance %'], inplace=True)

        def calculate_projection(current_pct, week):
            best = ((current_pct * week) + (100 * (6 - week))) / 6
            worst = ((current_pct * week)) / 6
            return round(best, 2), round(worst, 2)

        df['Best Case %'] = df['Current Attendance %'].apply(lambda x: calculate_projection(x, current_week)[0])
        df['Worst Case %'] = df['Current Attendance %'].apply(lambda x: calculate_projection(x, current_week)[1])
        df['Status (Week 6)'] = df['Best Case %'].apply(lambda x: 'PASS' if x >= 85 else 'FAIL')

        st.success("✅ Prediction Complete")
        st.dataframe(df)

        # Download section
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='xlsxwriter')
        st.download_button(
            label="📥 Download Results as Excel",
            data=output.getvalue(),
            file_name="week6_attendance_prediction.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("❌ The file must contain 'Student ID' and 'Current Attendance %' columns.")
