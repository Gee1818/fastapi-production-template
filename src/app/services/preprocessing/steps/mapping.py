import polars as pl

from app.services.preprocessing.config import MappingConfig


def apply_mappings(df: pl.DataFrame, config: MappingConfig) -> pl.DataFrame:
    df = _map_result(df, config.result_map)
    return _map_event(df, config.event_map)


def _map_result(df: pl.DataFrame, mapping: dict[str, int]) -> pl.DataFrame:
    return df.with_columns(
        pl.col("Result").map_elements(mapping.get, return_dtype=pl.Int8)
    )


def _map_event(df: pl.DataFrame, mapping: dict[str, str]) -> pl.DataFrame:
    return df.with_columns(
        pl.col("Event").map_elements(mapping.get, return_dtype=pl.Utf8)
    )
