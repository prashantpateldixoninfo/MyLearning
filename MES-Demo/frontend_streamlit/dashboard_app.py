import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# Page config
st.set_page_config(page_title="MES Dashboard", layout="wide")
st.title("📊 MES Dashboard – Test Results")

# Load data from backend
try:
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    response = requests.get(f"{API_URL}/dashboard")
    data = response.json()
except Exception as e:
    st.error(f"Failed to connect to MES backend: {e}")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(data)

if df.empty:
    st.warning("No test results yet.")
else:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp", ascending=False)

    # Unique options
    result_options = ["All"] + sorted(df["result"].unique())
    test_type_options = ["All"] + sorted(df["test_type"].unique())

    # Layout: main content + filter panel
    main_col, filter_col = st.columns([4, 1])  # Wider table, narrow filters

    with filter_col:
        st.markdown("### 🔍 Filters")

        # Reset logic (must run before widgets are rendered)
        if "reset_trigger" not in st.session_state:
            st.session_state.reset_trigger = False

        if st.session_state.reset_trigger:
            st.session_state.selected_result = "All"
            st.session_state.selected_test_type = "All"
            st.session_state.reset_trigger = False  # Reset flag

        # Initialize filters if not already
        if "selected_result" not in st.session_state:
            st.session_state.selected_result = "All"
        if "selected_test_type" not in st.session_state:
            st.session_state.selected_test_type = "All"

        # Filter widgets
        selected_result = st.selectbox("Result", result_options, key="selected_result")
        selected_test_type = st.selectbox("Test Type", test_type_options, key="selected_test_type")

        # Reset button sets the reset_trigger flag and reruns app
        if st.button("🔄 Reset Filters"):
            st.session_state.reset_trigger = True
            st.experimental_rerun()


    # Apply filters
    filtered_df = df.copy()
    if st.session_state.selected_result != "All":
        filtered_df = filtered_df[filtered_df["result"] == st.session_state.selected_result]
    if st.session_state.selected_test_type != "All":
        filtered_df = filtered_df[filtered_df["test_type"] == st.session_state.selected_test_type]

    # Colored row styling
    def color_rows(row):
        if row["result"] == "PASS":
            return ["background-color: #d4edda"] * len(row)
        elif row["result"] == "FAIL":
            return ["background-color: #f8d7da"] * len(row)
        return [""] * len(row)

    # Display table
    main_col.subheader("🧪 Filtered Test Results")
    styled_df = filtered_df.style.apply(color_rows, axis=1)
    main_col.dataframe(styled_df, use_container_width=True)

    # Summary Charts
    st.subheader("📈 Test Result Summary")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        result_counts = filtered_df["result"].value_counts().reset_index()
        result_counts.columns = ["Result", "Count"]
        fig_result = px.bar(
            result_counts, x="Result", y="Count", color="Result",
            color_discrete_map={"PASS": "green", "FAIL": "red"},
            title="Test Result Distribution"
        )
        st.plotly_chart(fig_result, use_container_width=True)

    with chart_col2:
        test_counts = filtered_df["test_type"].value_counts().reset_index()
        test_counts.columns = ["Test Type", "Count"]
        fig_test = px.bar(
            test_counts, x="Test Type", y="Count",
            title="Test Type Distribution",
            color_discrete_sequence=["skyblue"]
        )
        st.plotly_chart(fig_test, use_container_width=True)
