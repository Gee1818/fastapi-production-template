from pathlib import Path

import polars as pl
from joblib import Memory
from pydantic import BaseModel, ConfigDict, Field
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    train_test_split,  # pyright: ignore[reportUnknownVariableType]
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from app.domain.column_transformer_input import numeric_cols, ohe_cols, ordinal_cols
from app.domain.ml_model import MLModel
from app.domain.preprocessing.steps import split_features_target
from app.domain.transformers import (
    FeatureEngineerTransformer,
    FeatureSelectionTransformer,
    FilterTransformer,
    MappingTransformer,
)
from app.services.helper import save_model
from app.settings import Settings

from .config_model import ModelConfig


class TrainingService(BaseModel):
    model_path: Path = Field(default=Settings.MODEL_PATH)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @staticmethod
    def build_preprocessing_pipeline() -> Pipeline:
        return Pipeline(
            steps=[
                ("filter", FilterTransformer()),
                ("mapping", MappingTransformer()),
                ("feature_engineer", FeatureEngineerTransformer()),
                ("feature_selection", FeatureSelectionTransformer()),
            ],
        )

    @staticmethod
    def build_model_pipeline() -> Pipeline:
        return Pipeline(
            steps=[
                (
                    "column_transformer",
                    ColumnTransformer(
                        transformers=[
                            ("num", StandardScaler(), numeric_cols),
                            (
                                "ord",
                                OrdinalEncoder(
                                    handle_unknown="use_encoded_value", unknown_value=-1
                                ),
                                ordinal_cols,
                            ),
                            (
                                "ohe",
                                OneHotEncoder(
                                    handle_unknown="ignore", sparse_output=False
                                ),
                                ohe_cols,
                            ),
                        ],
                    ),
                ),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=ModelConfig.n_estimators,
                        max_depth=ModelConfig.max_depth,
                        min_samples_leaf=ModelConfig.min_samples_leaf,
                        max_features=ModelConfig.max_features,
                        min_samples_split=ModelConfig.min_samples_split,
                        max_samples=ModelConfig.max_samples,
                        random_state=ModelConfig.random_state,
                    ),
                ),
            ],
            memory=Memory(
                location=str(Settings.MODEL_DIRECTORY / "model_pipeline_cache"),
                verbose=0,
            ),
        )

    def train(self, training_file_path: Path) -> MLModel:
        if not training_file_path.exists():
            raise FileNotFoundError(training_file_path)

        df_raw = pl.read_csv(training_file_path)

        preprocessing = self.build_preprocessing_pipeline()

        df_preprocessed = preprocessing.fit_transform(df_raw)  # pyright: ignore[reportUnknownMemberType]

        X, y = split_features_target(df_preprocessed)  # type: ignore  # noqa: PGH003

        x_train, _x_test, y_train, _y_test = train_test_split(  # pyright: ignore[reportUnknownVariableType]
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        model = self.build_model_pipeline()
        model.fit(x_train, y_train)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

        save_model(model, self.model_path)

        return model
