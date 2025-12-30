import polars as pl
import requests
import streamlit as st

UPLOAD_API_URL = "http://localhost:8000/upload/upload"
TRAIN_API_URL = "http://localhost:8000/train/train"


def training_page() -> None:
    st.write("# Model Training Page")
    st.write("Upload a PGN file and train the chess game prediction model.")

    st.subheader("Step 1: Upload Training Data")
    uploaded_file = st.file_uploader(
        "Choose a PGN file",
        type=["pgn"],
        help="Upload a chess games file in PGN format",
    )

    # Track upload status in session state
    if "upload_complete" not in st.session_state:
        st.session_state.upload_complete = False
    if "upload_result" not in st.session_state:
        st.session_state.upload_result = None

    # Upload button
    if st.button(
        "Upload and Process File",
        type="primary",
        disabled=uploaded_file is None,
        key="upload_btn",
    ):
        if uploaded_file is None:
            st.warning("Please upload a file first.")
            return

        with st.spinner(
            "Uploading and processing file... This may take a few minutes."
        ):
            try:
                # Prepare the file for upload
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "application/octet-stream",
                    )
                }

                response = requests.post(UPLOAD_API_URL, files=files, timeout=3000)
                result = response.json()

                if response.ok:
                    st.session_state.upload_complete = True
                    st.session_state.upload_result = result
                    st.success("✅ File uploaded and processed successfully!")

                    # Display upload results
                    df = pl.DataFrame({
                        "Metric": ["Total Features", "Total Rows"],
                        "Value": [
                            result.get("totalFeatures", "N/A"),
                            result.get("totalRows", "N/A"),
                        ],
                    })
                    st.dataframe(df, use_container_width=True)  # pyright: ignore[reportUnknownMemberType]
                else:
                    st.error(f"❌ Upload failed: {response.status_code}")
                    st.json(result)
                    st.session_state.upload_complete = False

            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The upload process is taking too long.")
                st.session_state.upload_complete = False
            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Could not connect to the API. Make sure the backend is running."
                )
                st.session_state.upload_complete = False

    if st.session_state.upload_complete and st.session_state.upload_result:
        st.info("✓ Training data is ready")

    # Step 2: Train Model
    st.subheader("Step 2: Train Model")

    if not st.session_state.upload_complete:
        st.info("👆 Please upload and process a file first before training.")

    if st.button(
        "Train Model",
        type="primary",
        disabled=not st.session_state.upload_complete,
        key="train_btn",
    ):
        with st.spinner("Training model... This may take a few minutes."):
            try:
                response = requests.post(TRAIN_API_URL, timeout=3000)
                result = response.json()

                if response.ok:
                    st.success("✅ Model trained successfully!")
                    st.json(result)

                else:
                    st.error(f"❌ Training failed: {response.status_code}")
                    st.json(result)

            except requests.exceptions.Timeout:
                st.error(
                    "❌ Request timed out. The training process is taking too long."
                )
            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Could not connect to the API. Make sure the backend is running."
                )

    # Reset button
    if st.session_state.upload_complete:
        st.divider()
        if st.button("Reset and Upload New File", key="reset_btn"):
            st.session_state.upload_complete = False
            st.session_state.upload_result = None
            st.rerun()
