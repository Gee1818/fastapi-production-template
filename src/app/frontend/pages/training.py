import polars as pl
import requests
import streamlit as st
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError, RequestException, Timeout
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.frontend.schemas import TrainResponse, UploadResponse
from app.frontend.settting import FrontendSettings


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


def display_upload_results(result: UploadResponse) -> None:
    df = pl.DataFrame({
        "Metric": ["Message", "Total Features", "Total Rows"],
        "Value": [
            result.message,
            str(result.total_features),
            str(result.total_rows),
        ],
    })
    st.dataframe(df, use_container_width=True)  # pyright: ignore[reportUnknownMemberType]


def display_training_results(result: TrainResponse) -> None:
    df = pl.DataFrame({
        "Metric": ["Message"],
        "Value": [result.message],
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


def upload_file(uploaded_file: UploadedFile) -> UploadResponse:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/octet-stream",
        )
    }

    response = requests.post(FrontendSettings.UPLOAD_API_URL, files=files, timeout=300)
    response.raise_for_status()

    return UploadResponse.model_validate(response.json())


def train_model() -> TrainResponse:
    response = requests.post(FrontendSettings.TRAIN_API_URL, timeout=300)
    response.raise_for_status()

    return TrainResponse.model_validate(response.json())


def handle_file_upload(uploaded_file: UploadedFile) -> None:
    """Handle file upload process with error handling."""
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


def handle_model_training() -> None:
    """Handle model training process with error handling."""
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


def handle_reset() -> None:
    """Reset session state for new upload."""
    st.session_state.upload_complete = False
    st.session_state.upload_result = None
    st.session_state.training_complete = False
    st.session_state.training_result = None
    st.rerun()


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
    if not st.button(
        "Upload and Process File",
        type="primary",
        disabled=uploaded_file is None,
        key="upload_btn",
        use_container_width=True,
    ):
        return

    if uploaded_file is None:
        st.warning("⚠️ Please upload a file first.")
        return

    with st.spinner("⏳ Uploading and processing file... This may take a few minutes."):
        handle_file_upload(uploaded_file)


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

    if not st.button(
        "Train Model",
        type="primary",
        disabled=not st.session_state.upload_complete,
        key="train_btn",
        use_container_width=True,
    ):
        return

    with st.spinner("⏳ Training model... This may take a few minutes."):
        handle_model_training()


def render_reset_section() -> None:
    """Render the reset section to start over with a new file."""
    if not (st.session_state.upload_complete or st.session_state.training_complete):
        return

    st.divider()
    _col1, col2, _col3 = st.columns([1, 2, 1])
    with col2:
        if not st.button(
            "🔄 Reset and Upload New File",
            key="reset_btn",
            use_container_width=True,
        ):
            return

        handle_reset()


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
