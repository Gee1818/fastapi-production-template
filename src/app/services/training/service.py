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

from app.domain.ml_model import MLModel
from app.domain.preprocessing.steps import split_features_target
from app.services.helper import save_model
from app.settings import Settings

from .config_model import ModelConfig


class TrainingService(BaseModel):
    model_path: Path = Field(default=Settings.MODEL_PATH)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @staticmethod
    def build_pipeline(
        numeric_cols: list[str],
        ordinal_cols: list[str],
        ohe_cols: list[str],
    ) -> Pipeline:
        preprocessing_pipeline = ColumnTransformer(
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
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                    ohe_cols,
                ),
            ],
        )

        memory = Memory(
            location=str(Settings.MODEL_DIRECTORY / "pipeline_cache"), verbose=0
        )

        return Pipeline(
            steps=[
                ("preprocessor", preprocessing_pipeline),
                (
                    "classifier",
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
            memory=memory,
        )

    def train(self, training_file_path: Path) -> MLModel:

        if not training_file_path.exists():
            raise FileNotFoundError(training_file_path)
        df = pl.read_csv(training_file_path)

        X, y = split_features_target(df)

        ohe_cols = ["Event", "TimeControl", "Termination"]

        ordinal_cols = ["ECO", "Opening"]

        numeric_cols = list(set(X.columns) - set(ohe_cols) - set(ordinal_cols))

        pipeline = self.build_pipeline(
            numeric_cols=numeric_cols,
            ordinal_cols=ordinal_cols,
            ohe_cols=ohe_cols,
        )

        X_train, X_test, y_train, _y_test = train_test_split(  # pyright: ignore[reportUnknownVariableType]
            X, y, test_size=0.2, random_state=42, stratify=y
        )  # pyright: ignore[reportUnknownVariableType]
        pipeline.fit(X_train, y_train)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
        save_model(pipeline, self.model_path)
        pipeline.predict(X_test)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

        return pipeline
