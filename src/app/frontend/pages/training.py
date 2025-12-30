"""Training page for the chess game prediction model.

This module provides a two-step workflow for uploading training data
and training the model, with robust error handling and clean UI.
"""

from typing import Any

import polars as pl
import requests
import streamlit as st
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError, RequestException, Timeout
from streamlit.runtime.uploaded_file_manager import UploadedFile

UPLOAD_API_URL = "http://localhost:8000/upload/upload"
TRAIN_API_URL = "http://localhost:8000/train/train"


class APIError(Exception):
    """Custom exception for API-related errors."""


def initialize_session_state() -> None:
    if "upload_complete" not in st.session_state:
        st.session_state.upload_complete = False
    if "upload_result" not in st.session_state:
        st.session_state.upload_result = None
    if "training_complete" not in st.session_state:
        st.session_state.training_complete = False
    if "training_result" not in st.session_state:
        st.session_state.training_result = None


def display_upload_results(result: dict[str, Any]) -> None:
    df = pl.DataFrame({
        "Metric": ["Message", "Total Features", "Total Rows"],
        "Value": [
            str(result.get("message", "N/A")),
            str(result.get("totalFeatures", "N/A")),
            str(result.get("totalRows", "N/A")),
        ],
    })
    st.dataframe(df, use_container_width=True)  # pyright: ignore[reportUnknownMemberType]


def display_training_results(result: dict[str, Any]) -> None:
    df = pl.DataFrame({
        "Metric": list(result.keys()),
        "Value": [str(v) for v in result.values()],
    })
    st.dataframe(df, use_container_width=True)  # pyright: ignore[reportUnknownMemberType]


def handle_api_error(error: RequestException, operation: str) -> None:
    if isinstance(error, Timeout):
        st.error(
            f"❌ Request timed out. The {operation} process is taking too long. "
            "Please try again with a smaller file or check your connection."
        )
    elif isinstance(error, RequestsConnectionError):
        st.error(
            "❌ Could not connect to the API. Please ensure:\n"
            "- The backend server is running\n"
            "- The API is accessible at the configured URL\n"
            "- Your network connection is stable"
        )
    elif isinstance(error, HTTPError):
        st.error(
            f"❌ HTTP error occurred during {operation}: {error}\n"
            "Please check the API logs for more details."
        )
    elif isinstance(error, APIError):
        st.error(f"❌ API error: {error}")
    else:
        st.error(
            f"❌ An unexpected error occurred during {operation}: {type(error).__name__}\n"  # noqa: E501
            f"Details: {error!s}"
        )
        st.exception(error)


def upload_file(uploaded_file: UploadedFile) -> dict[str, Any]:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/octet-stream",
        )
    }

    response = requests.post(UPLOAD_API_URL, files=files, timeout=300)
    response.raise_for_status()

    result: dict[str, Any] = response.json()

    # Validate response structure
    required_keys = {"message", "totalFeatures", "totalRows"}
    if not all(key in result for key in required_keys):
        msg = "Invalid response structure: missing required keys"
        raise APIError(msg)

    return result


def train_model() -> dict[str, Any]:
    response = requests.post(TRAIN_API_URL, timeout=300)
    response.raise_for_status()

    result: dict[str, Any] = response.json()

    # Validate response structure

    return result


def render_upload_section() -> None:
    """Render the file upload section of the page."""
    st.subheader("📤 Step 1: Upload Training Data")

    uploaded_file = st.file_uploader(
        "Choose a PGN file",
        type=["pgn"],
        help="Upload a chess games file in PGN format",
    )

    # Show current upload status
    if st.session_state.upload_complete and st.session_state.upload_result:
        st.success("✅ File uploaded and processed successfully!")
        with st.expander("📊 View Upload Results", expanded=False):
            display_upload_results(st.session_state.upload_result)

    # Upload button
    if st.button(
        "Upload and Process File",
        type="primary",
        disabled=uploaded_file is None,
        key="upload_btn",
        use_container_width=True,
    ):
        if uploaded_file is None:
            st.warning("⚠️ Please upload a file first.")
            return

        with st.spinner(
            "⏳ Uploading and processing file... This may take a few minutes."
        ):
            try:
                result = upload_file(uploaded_file)

                st.session_state.upload_complete = True
                st.session_state.upload_result = result
                st.success("✅ File uploaded and processed successfully!")
                display_upload_results(result)
                st.rerun()

            except RequestException as e:
                handle_api_error(e, "upload")
                st.session_state.upload_complete = False


def render_training_section() -> None:
    """Render the model training section of the page."""
    st.subheader("🎓 Step 2: Train Model")

    if not st.session_state.upload_complete:
        st.info("👆 Please upload and process a file first before training.")
        return

    st.info("✓ Training data is ready. Click below to train the model.")

    # Show previous training results if they exist
    if st.session_state.training_complete and st.session_state.training_result:
        st.success("✅ Model trained successfully!")
        with st.expander("📊 View Training Results", expanded=False):
            display_training_results(st.session_state.training_result)

    if st.button(
        "Train Model",
        type="primary",
        disabled=not st.session_state.upload_complete,
        key="train_btn",
        use_container_width=True,
    ):
        with st.spinner("⏳ Training model... This may take a few minutes."):
            try:
                result = train_model()

                st.session_state.training_complete = True
                st.session_state.training_result = result
                st.success("✅ Model trained successfully!")
                display_training_results(result)
                st.balloons()
                st.rerun()

            except RequestException as e:
                handle_api_error(e, "training")
                st.session_state.training_complete = False


def render_reset_section() -> None:
    """Render the reset section to start over with a new file."""
    if st.session_state.upload_complete or st.session_state.training_complete:
        st.divider()
        _col1, col2, _col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🔄 Reset and Upload New File",
                key="reset_btn",
                use_container_width=True,
            ):
                st.session_state.upload_complete = False
                st.session_state.upload_result = None
                st.session_state.training_complete = False
                st.session_state.training_result = None
                st.rerun()


def training_page() -> None:
    """Main training page function with two-step workflow."""
    # Page header
    st.title("🤖 Model Training")
    st.markdown(
        "Upload a PGN file containing chess games and train the prediction model. "
        "This is a two-step process: first upload and process your data, "
        "then train the model."
    )
    st.divider()

    # Initialize session state
    initialize_session_state()

    # Render sections
    render_upload_section()
    st.divider()
    render_training_section()
    render_reset_section()

    # Add helpful information in sidebar
    with st.sidebar:
        st.subheader("ℹ️ Training Information")  # noqa: RUF001
        st.markdown("""
        **Step 1: Upload**
        - Select a PGN file with chess games
        - File will be validated and processed
        - Features will be extracted

        **Step 2: Train**
        - Model trains on processed data
        - May take several minutes
        - Results displayed upon completion

        **Requirements:**
        - Valid PGN format
        - Rated games (Blitz, Rapid, or Classical)
        - ELO ratings between 1400-2800
        - Minimum 15 moves per game
        """)
