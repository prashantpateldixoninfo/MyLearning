import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
import os

st.set_page_config(page_title="MES Dashboard", layout="wide")
st.title("📊 MES Dashboard – Test Results")

# --- ✅ Dynamic backend hostname via env ---
API_URL = os.getenv("API_URL", "http://localhost:8000")

# --- ✅ Retry logic in case backend isn't up yet ---
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

data = None
error = None

for attempt in range(MAX_RETRIES):
    try:
        response = requests.get(f"{API_URL}/dashboard", timeout=3)
        data = response.json()
        break
    except Exception as e:
        error = str(e)
        time.sleep(RETRY_DELAY)

# --- Display result or fallback error ---
if data:
    df = pd.DataFrame(data)
    if df.empty:
        st.warning("No test results yet.")
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values(by="timestamp", ascending=False)

        # Unique dropdown options
        result_options = ["All"] + sorted(df["result"].unique())
        test_type_options = ["All"] + sorted(df["test_type"].unique())

        # Layout: main content + filter panel
        main_col, filter_col = st.columns([4, 1])

        with filter_col:
            st.markdown("### 🔍 Filters")

            # Initialize/reset logic
            if "reset_trigger" not in st.session_state:
                st.session_state.reset_trigger = False
            if st.session_state.reset_trigger:
                st.session_state.selected_result = "All"
                st.session_state.selected_test_type = "All"
                st.session_state.reset_trigger = False

            if "selected_result" not in st.session_state:
                st.session_state.selected_result = "All"
            if "selected_test_type" not in st.session_state:
                st.session_state.selected_test_type = "All"

            selected_result = st.selectbox("Result", result_options, key="selected_result")
            selected_test_type = st.selectbox("Test Type", test_type_options, key="selected_test_type")

            if st.button("🔄 Reset Filters"):
                st.session_state.reset_trigger = True
                st.experimental_rerun()

        # --- Apply filters
        filtered_df = df.copy()
        if st.session_state.selected_result != "All":
            filtered_df = filtered_df[filtered_df["result"] == st.session_state.selected_result]
        if st.session_state.selected_test_type != "All":
            filtered_df = filtered_df[filtered_df["test_type"] == st.session_state.selected_test_type]

        # --- Add emoji-based PASS/FAIL status column
        def render_status(row):
            if row["result"] == "PASS":
                return "🟢 PASS"
            elif row["result"] == "FAIL":
                return "🔴 FAIL"
            return row["result"]

        filtered_df["Status"] = filtered_df.apply(render_status, axis=1)
        filtered_df = filtered_df.drop(columns=["result"])

        # --- Show results table
        main_col.subheader("🧪 Filtered Test Results")
        main_col.dataframe(filtered_df, use_container_width=True)

        # --- Summary Charts
        st.subheader("📈 Test Result Summary")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            result_counts = df["result"].value_counts().reset_index()
            result_counts.columns = ["Result", "Count"]
            fig_result = px.bar(
                result_counts, x="Result", y="Count", color="Result",
                color_discrete_map={"PASS": "green", "FAIL": "red"},
                title="Test Result Distribution"
            )
            st.plotly_chart(fig_result, use_container_width=True)

        with chart_col2:
            test_counts = df["test_type"].value_counts().reset_index()
            test_counts.columns = ["Test Type", "Count"]
            fig_test = px.bar(
                test_counts, x="Test Type", y="Count",
                title="Test Type Distribution",
                color_discrete_sequence=["skyblue"]
            )
            st.plotly_chart(fig_test, use_container_width=True)
else:
    st.error(f"❌ Failed to connect to backend after {MAX_RETRIES} attempts:\n\n{error}")
