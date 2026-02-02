from collections.abc import Sequence

import polars as pl

from app.domain.preprocessing.config import FilterConfig


def apply_filters(df: pl.DataFrame, filter_config: FilterConfig) -> pl.DataFrame:
    df = _filter_by_items_in_list(df, filter_config.terminations, "Termination")
    df = _filter_by_items_in_list(df, filter_config.events, "Event")
    df = _filter_by_elo(df, filter_config.elo_range)
    return _filter_by_move_count(df, filter_config.min_moves)


def _filter_by_elo(df: pl.DataFrame, elo_range: tuple[int, int]) -> pl.DataFrame:
    return df.filter(pl.col("WhiteElo").is_between(elo_range[0], elo_range[1]))


def _filter_by_items_in_list(
    df: pl.DataFrame, items: Sequence[str], target_col: str
) -> pl.DataFrame:
    pattern = "|".join(items)
    return df.filter(pl.col(target_col).str.contains(pattern))


def _filter_by_move_count(df: pl.DataFrame, min_moves: int) -> pl.DataFrame:
    return df.filter(pl.col("NumMoves") >= min_moves)
