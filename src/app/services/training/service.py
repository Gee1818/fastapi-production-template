import logging
from pathlib import Path
from typing import cast

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
from app.domain.transformers import (
    FeatureEngineerTransformer,
    FeatureSelectionTransformer,
    FilterTransformer,
    MappingTransformer,
)
from app.services.helper import save_model
from app.settings import Settings

from .config_model import ModelConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger(__name__)


class TrainingService(BaseModel):
    model_path: Path = Field(default=Settings.MODEL_PATH)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @staticmethod
    def build_data_cleaning_pipeline() -> Pipeline:
        return Pipeline(
            steps=[
                ("filter", FilterTransformer()),
                ("mapping", MappingTransformer()),
                (
                    "feature_engineer",
                    FeatureEngineerTransformer(),
                ),
                (
                    "feature_selection",
                    FeatureSelectionTransformer(),
                ),
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
            memory=Memory(
                location=str(Settings.MODEL_DIRECTORY / "pipeline_cache"),
                verbose=0,
            ),
        )

    def train(self, training_file_path: Path) -> MLModel:
        if not training_file_path.exists():
            raise FileNotFoundError(training_file_path)

        df = pl.read_csv(training_file_path)
        logger.info("Loaded training data from %s", training_file_path)

        pipeline = self.build_data_cleaning_pipeline()

        x = df
        for _name, step in pipeline.steps[:-1]:
            x = step.fit_transform(x)

        feature_selection = cast(
            "FeatureSelectionTransformer", pipeline.named_steps["feature_selection"]
        )
        y: pl.Series = feature_selection.target_  # type: ignore[assignment]

        X_train, X_test, y_train, _y_test = train_test_split(  # pyright: ignore[reportUnknownVariableType]
            x, y, test_size=0.2, random_state=42, stratify=y
        )

        pipeline.named_steps["classifier"].fit(X_train, y_train)  # pyright: ignore[reportUnknownMemberType]

        save_model(pipeline, self.model_path)

        _preds = pipeline.named_steps["classifier"].predict(X_test)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        return pipeline
