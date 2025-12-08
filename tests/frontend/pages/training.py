from io import BytesIO
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from app.frontend.pages.training import training_page


@pytest.fixture
def mock_streamlit():
    """Mock streamlit functions."""
    with patch("app.frontend.pages.training.st") as mock_st:
        # Setup basic mocks
        mock_st.write = Mock()
        mock_st.file_uploader = Mock()
        mock_st.button = Mock()
        mock_st.warning = Mock()
        mock_st.spinner = Mock()
        mock_st.success = Mock()
        mock_st.error = Mock()
        mock_st.dataframe = Mock()

        # Mock spinner as context manager
        mock_spinner = MagicMock()
        mock_spinner.__enter__ = Mock(return_value=mock_spinner)
        mock_spinner.__exit__ = Mock(return_value=False)
        mock_st.spinner.return_value = mock_spinner

        yield mock_st


@pytest.fixture
def mock_requests():
    """Mock requests library."""
    with patch("app.frontend.pages.training.requests") as mock_req:
        yield mock_req


@pytest.fixture
def sample_pgn_file():
    """Create a sample PGN file for testing."""
    content = b"""[Event "Test Game"]
[Site "Test"]
[Date "2025.01.01"]
[Round "1"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]

1. e4 e5 2. Nf3 1-0
"""
    file = BytesIO(content)
    file.name = "test.pgn"
    return file


class TestTrainingPage:
    """Test suite for training_page function."""

    def test_page_initialization(self, mock_streamlit) -> None:
        """Test that page initializes with correct title and description."""
        training_page()

        # Verify page title and description are displayed
        assert mock_streamlit.write.call_count == 2
        mock_streamlit.write.assert_any_call("# Model Training Page")
        mock_streamlit.write.assert_any_call(
            "Upload a PGN file to train the chess game prediction model."
        )

    def test_file_uploader_configuration(self, mock_streamlit) -> None:
        """Test that file uploader is configured correctly."""
        training_page()

        mock_streamlit.file_uploader.assert_called_once_with(
            "Choose a PGN file",
            type=["pgn"],
            help="Upload a chess games file in PGN format",
        )

    def test_button_disabled_when_no_file(self, mock_streamlit) -> None:
        """Test that train button is disabled when no file is uploaded."""
        mock_streamlit.file_uploader.return_value = None
        mock_streamlit.button.return_value = False

        training_page()

        mock_streamlit.button.assert_called_once_with(
            "Train Model", type="primary", disabled=True
        )

    def test_button_enabled_when_file_uploaded(
        self, mock_streamlit, sample_pgn_file
    ) -> None:
        """Test that train button is enabled when file is uploaded."""
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = False

        training_page()

        mock_streamlit.button.assert_called_once_with(
            "Train Model", type="primary", disabled=False
        )

    def test_warning_when_training_without_file(self, mock_streamlit) -> None:
        """Test warning is shown when trying to train without file."""
        mock_streamlit.file_uploader.return_value = None
        mock_streamlit.button.return_value = True

        training_page()

        mock_streamlit.warning.assert_called_once_with("Please upload a file first.")

    def test_successful_training(
        self, mock_streamlit, mock_requests, sample_pgn_file
    ) -> None:
        """Test successful model training flow."""
        # Setup mocks
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = True

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "message": "Model trained successfully",
            "status": "success",
        }
        mock_requests.post.return_value = mock_response

        # Execute
        training_page()

        # Verify API call
        mock_requests.post.assert_called_once()
        call_args = mock_requests.post.call_args
        assert call_args[0][0] == "http://localhost:8000/train/train"
        assert "files" in call_args[1]
        assert call_args[1]["timeout"] == 3000

        # Verify success message
        mock_streamlit.success.assert_called_once_with("✅ Model trained successfully!")

        # Verify dataframe is displayed
        mock_streamlit.dataframe.assert_called_once()

    def test_training_failure(
        self, mock_streamlit, mock_requests, sample_pgn_file
    ) -> None:
        """Test handling of training failure."""
        # Setup mocks
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = True

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Invalid data"}
        mock_requests.post.return_value = mock_response

        # Execute
        training_page()

        # Verify error message
        mock_streamlit.error.assert_called_once_with("❌ Training failed: 400")

        # Verify dataframe is still displayed
        mock_streamlit.dataframe.assert_called_once()

    def test_timeout_error_handling(
        self, mock_streamlit, mock_requests, sample_pgn_file
    ) -> None:
        """Test handling of request timeout."""
        # Setup mocks
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = True
        mock_requests.post.side_effect = requests.exceptions.Timeout()

        # Execute
        training_page()

        # Verify timeout error message
        mock_streamlit.error.assert_called_once_with(
            "❌ Request timed out. The training process is taking too long."
        )

    def test_connection_error_handling(
        self, mock_streamlit, mock_requests, sample_pgn_file
    ) -> None:
        """Test handling of connection error."""
        # Setup mocks
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = True
        mock_requests.post.side_effect = requests.exceptions.ConnectionError()

        # Execute
        training_page()

        # Verify connection error message
        mock_streamlit.error.assert_called_once_with(
            "❌ Could not connect to the API. Make sure the backend is running."
        )

    def test_file_preparation(
        self, mock_streamlit, mock_requests, sample_pgn_file
    ) -> None:
        """Test that file is prepared correctly for upload."""
        # Setup mocks
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = True

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"message": "Success"}
        mock_requests.post.return_value = mock_response

        # Execute
        training_page()

        # Verify file structure in API call
        call_args = mock_requests.post.call_args
        files = call_args[1]["files"]
        assert "file" in files
        file_tuple = files["file"]
        assert file_tuple[0] == "test.pgn"
        assert file_tuple[2] == "application/octet-stream"

    def test_dataframe_creation(
        self, mock_streamlit, mock_requests, sample_pgn_file
    ) -> None:
        """Test that response is properly converted to dataframe."""
        # Setup mocks
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = True

        mock_response = Mock()
        mock_response.ok = True
        test_response = {
            "message": "Model trained successfully",
            "accuracy": 0.95,
            "samples": 1000,
        }
        mock_response.json.return_value = test_response
        mock_requests.post.return_value = mock_response

        # Mock DataFrame to capture creation
        with patch("app.frontend.pages.training.pl.DataFrame") as mock_df:
            mock_df_instance = Mock()
            mock_df.return_value = mock_df_instance

            # Execute
            training_page()

            # Verify DataFrame creation
            mock_df.assert_called_once()
            call_args = mock_df.call_args[0][0]
            assert "Response Key" in call_args
            assert "Value" in call_args
            assert call_args["Response Key"] == list(test_response.keys())

            # Verify dataframe is passed to st.dataframe
            mock_streamlit.dataframe.assert_called_once_with(mock_df_instance)

    def test_spinner_context(
        self, mock_streamlit, mock_requests, sample_pgn_file
    ) -> None:
        """Test that spinner is shown during training."""
        # Setup mocks
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = True

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"message": "Success"}
        mock_requests.post.return_value = mock_response

        # Execute
        training_page()

        # Verify spinner was used
        mock_streamlit.spinner.assert_called_once_with(
            "Training model... This may take a few minutes."
        )

        # Verify spinner context manager was entered
        mock_streamlit.spinner.return_value.__enter__.assert_called_once()

    def test_no_training_when_button_not_clicked(
        self, mock_streamlit, mock_requests, sample_pgn_file
    ) -> None:
        """Test that no training occurs when button is not clicked."""
        # Setup mocks
        mock_streamlit.file_uploader.return_value = sample_pgn_file
        mock_streamlit.button.return_value = False

        # Execute
        training_page()

        # Verify no API call was made
        mock_requests.post.assert_not_called()

        # Verify no messages were shown
        mock_streamlit.success.assert_not_called()
        mock_streamlit.error.assert_not_called()
        mock_streamlit.warning.assert_not_called()
