from collections.abc import Sequence

import polars as pl

from app.services.preprocessing.config.filter_config import FilterConfig


class GameFilter:
    @staticmethod
    def apply_filters(df: pl.DataFrame, filter_config: FilterConfig) -> pl.DataFrame:
        df = GameFilter._filter_by_items_in_list(
            df, filter_config.terminations, "Termination"
        )
        df = GameFilter._filter_by_items_in_list(df, filter_config.events, "Event")
        df = GameFilter._filter_by_elo(df, filter_config.elo_range)
        return GameFilter._filter_by_move_count(df, filter_config.min_moves)

    @staticmethod
    def _filter_by_elo(df: pl.DataFrame, elo_range: tuple[int, int]) -> pl.DataFrame:
        return df.filter(pl.col("WhiteElo").is_between(elo_range[0], elo_range[1]))

    @staticmethod
    def _filter_by_items_in_list(
        df: pl.DataFrame, items: Sequence[str], target_col: str
    ) -> pl.DataFrame:
        pattern = "|".join(items)
        return df.filter(pl.col(target_col).str.contains(pattern))

    @staticmethod
    def _filter_by_move_count(df: pl.DataFrame, min_moves: int) -> pl.DataFrame:
        return df.filter(pl.col("NumMoves") >= min_moves)
