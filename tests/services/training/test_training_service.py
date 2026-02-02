from pathlib import Path

import polars as pl
import pytest

from app.services.training import TrainingService


def test_train_with_nonexistent_file_fails(test_model_path: Path) -> None:
    service = TrainingService(model_path=test_model_path)
    nonexistent_path = Path("/nonexistent/path/train.csv")

    with pytest.raises(FileNotFoundError) as exc_info:
        service.train(nonexistent_path)

    assert str(nonexistent_path) in str(exc_info.value)


def test_train_success_with_valid_csv(
    sample_train_csv_file: Path,
    test_model_path: Path,
) -> None:
    service = TrainingService(model_path=test_model_path)

    model = service.train(sample_train_csv_file)

    assert model is not None
    assert test_model_path.exists()
    assert hasattr(model, "predict")
    assert hasattr(model, "fit")


def test_train_creates_model_file(
    sample_train_csv_file: Path,
    test_model_path: Path,
) -> None:
    service = TrainingService(model_path=test_model_path)
    assert not test_model_path.exists()

    service.train(sample_train_csv_file)

    assert test_model_path.exists()
    assert test_model_path.stat().st_size > 0


def test_train_overwrites_existing_model(
    sample_train_csv_file: Path,
    test_model_path: Path,
) -> None:
    service = TrainingService(model_path=test_model_path)

    model1 = service.train(sample_train_csv_file)
    first_size = test_model_path.stat().st_size

    model2 = service.train(sample_train_csv_file)
    second_size = test_model_path.stat().st_size

    assert model1 is not None
    assert model2 is not None
    assert test_model_path.exists()
    assert abs(first_size - second_size) < first_size * 0.1


def test_trained_model_can_predict(
    sample_train_csv_file: Path,
    test_model_path: Path,
) -> None:
    # Arrange
    service = TrainingService(model_path=test_model_path)
    model = service.train(sample_train_csv_file)

    # Load the CSV to get feature structure
    df = pl.read_csv(sample_train_csv_file)
    X = df.drop("Result")

    predictions = model.predict(X[:1])  # type: ignore[arg-type]

    # Assert
    assert predictions is not None
    assert len(predictions) == 1
    assert predictions[0] in {-1, 0, 1}
