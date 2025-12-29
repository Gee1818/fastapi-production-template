from pathlib import Path

import polars as pl
import pytest
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from app.services.training import TrainingService


def test_train_with_nonexistent_file_fails(
    test_model_path: Path,
) -> None:

    service = TrainingService(model_path=test_model_path)
    nonexistent_path = Path("/nonexistent/path/train.csv")

    with pytest.raises(FileNotFoundError) as exc_info:
        service.train(nonexistent_path)

    assert f"Training file not found at {nonexistent_path}" in str(exc_info.value)


def test_train_success_with_valid_csv(
    sample_train_csv_file: Path,
    test_model_path: Path,
) -> None:
    """Test successful training with valid CSV data."""
    # Arrange
    service = TrainingService(model_path=test_model_path)

    # Act
    model = service.train(sample_train_csv_file)

    # Assert
    assert model is not None
    assert test_model_path.exists()
    assert hasattr(model, "predict")
    assert hasattr(model, "fit")


def test_train_creates_model_file(
    sample_train_csv_file: Path,
    test_model_path: Path,
) -> None:
    """Test that training creates a model file on disk."""
    # Arrange
    service = TrainingService(model_path=test_model_path)
    assert not test_model_path.exists()

    # Act
    service.train(sample_train_csv_file)

    # Assert
    assert test_model_path.exists()
    assert test_model_path.stat().st_size > 0


def test_train_with_invalid_csv_structure_fails(
    test_train_csv_path: Path,
    test_model_path: Path,
) -> None:
    """Test that training fails with invalid CSV structure."""
    # Arrange
    service = TrainingService(model_path=test_model_path)

    # Create invalid CSV (missing required columns)
    invalid_df = pl.DataFrame({
        "Event": ["Blitz"],
        "Result": [1],
    })
    invalid_df.write_csv(test_train_csv_path)

    # Act & Assert
    with pytest.raises(Exception):  # Will raise KeyError or similar
        service.train(test_train_csv_path)


def test_train_overwrites_existing_model(
    sample_train_csv_file: Path,
    test_model_path: Path,
) -> None:
    """Test that training overwrites existing model file."""
    # Arrange
    service = TrainingService(model_path=test_model_path)

    # First training
    model1 = service.train(sample_train_csv_file)
    first_size = test_model_path.stat().st_size

    # Act - Second training
    model2 = service.train(sample_train_csv_file)
    second_size = test_model_path.stat().st_size

    # Assert
    assert model1 is not None
    assert model2 is not None
    assert test_model_path.exists()
    # Size might vary slightly but should be similar
    assert abs(first_size - second_size) < first_size * 0.1


def test_build_pipeline_structure() -> None:

    numeric_cols = ["white_material", "black_material"]
    ordinal_cols = ["ECO", "Opening"]
    ohe_cols = ["Event", "TimeControl"]

    # Act
    pipeline = TrainingService.build_pipeline(
        numeric_cols=numeric_cols,
        ordinal_cols=ordinal_cols,
        ohe_cols=ohe_cols,
    )

    # Assert
    assert isinstance(pipeline, Pipeline)
    assert len(pipeline.steps) == 2

    # Check preprocessor step
    preprocessor_name, preprocessor = pipeline.steps[0]
    assert preprocessor_name == "preprocessor"
    assert isinstance(preprocessor, ColumnTransformer)

    # Check transformers in ColumnTransformer
    transformers = dict(preprocessor.transformers)
    assert "num" in transformers
    assert "ord" in transformers
    assert "ohe" in transformers

    # Check transformer types
    assert isinstance(transformers["num"][0], StandardScaler)
    assert isinstance(transformers["ord"][0], OrdinalEncoder)
    assert isinstance(transformers["ohe"][0], OneHotEncoder)

    # Check classifier step
    classifier_name, classifier = pipeline.steps[1]
    assert classifier_name == "classifier"
    assert isinstance(classifier, RandomForestClassifier)


def test_build_pipeline_with_correct_columns() -> None:
    numeric_cols = ["col1", "col2"]
    ordinal_cols = ["col3"]
    ohe_cols = ["col4", "col5"]

    # Act
    pipeline = TrainingService.build_pipeline(
        numeric_cols=numeric_cols,
        ordinal_cols=ordinal_cols,
        ohe_cols=ohe_cols,
    )

    # Assert
    preprocessor = pipeline.steps[0][1]
    transformers = {
        name: (transformer, cols)
        for name, transformer, cols in preprocessor.transformers
    }

    # Check column assignments
    assert transformers["num"][1] == numeric_cols
    assert transformers["ord"][1] == ordinal_cols
    assert transformers["ohe"][1] == ohe_cols


def test_trained_model_can_predict(
    sample_train_csv_file: Path,
    test_model_path: Path,
) -> None:
    """Test that trained model can make predictions."""
    service = TrainingService(model_path=test_model_path)
    model = service.train(sample_train_csv_file)

    df = pl.read_csv(sample_train_csv_file)
    X = df.drop("Result")

    # Act
    predictions = model.predict(X[:1])

    # Assert
    assert predictions is not None
    assert len(predictions) == 1
    assert predictions[0] in {-1, 0, 1}


def test_build_pipeline_random_forest_parameters() -> None:
    """Test that RandomForestClassifier has correct parameters."""
    numeric_cols = ["col1"]
    ordinal_cols = ["col2"]
    ohe_cols = ["col3"]

    pipeline = TrainingService.build_pipeline(
        numeric_cols=numeric_cols,
        ordinal_cols=ordinal_cols,
        ohe_cols=ohe_cols,
    )

    # Assert
    classifier = pipeline.steps[1][1]
    assert classifier.n_estimators == 100
    assert classifier.max_depth == 10
    assert classifier.min_samples_leaf == 2
    assert classifier.max_features == "sqrt"
    assert classifier.min_samples_split == 80
    assert classifier.max_samples == 0.5
    assert classifier.random_state == 42
