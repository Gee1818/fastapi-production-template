import io
import re

import polars as pl
from chess import pgn
from fastapi import UploadFile


def read_file(file: UploadFile) -> pl.DataFrame:
    # Read file content
    content = file.file.read().decode("utf-8")

    # Parse PGN text
    games = _parse_pgn(content)

    df = pl.DataFrame(games)

    # Drop BlackTitle column if it exists
    if "BlackTitle" in df.columns:
        df = df.drop("BlackTitle")

    df = _apply_schema(df)

    df = _fill_nulls(df)

    return _add_move_count(df)


def _parse_pgn(pgn_text: str) -> list[dict[str, str]]:
    games: list[dict[str, str]] = []
    game_blocks = re.split(r"\n\n(?=\[Event)", pgn_text.strip())

    for block in game_blocks:
        if not block.strip():
            continue

        game_data = _parse_game_block(block)
        if game_data:
            games.append(game_data)

    return games


def _parse_game_block(block: str) -> dict[str, str] | None:
    # Extract headers
    headers = re.findall(r'\[(\w+)\s+"([^"]*)"\]', block)
    game_data: dict[str, str] = dict(headers)

    # Extract moves
    moves_match = re.search(
        r"\]\n\n(.+?)(?:\s+(?:1-0|0-1|1/2-1/2|\*))?$", block, re.DOTALL
    )

    if moves_match:
        moves_text = moves_match.group(1).strip()
        # Remove comments in curly braces
        moves_clean = re.sub(r"\{[^}]*\}", "", moves_text)
        # Normalize whitespace
        moves_clean = re.sub(r"\s+", " ", moves_clean).strip()
        game_data["Moves"] = moves_clean
    else:
        game_data["Moves"] = ""

    return game_data or None


def _apply_schema(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("WhiteElo").cast(pl.Int64), pl.col("BlackElo").cast(pl.Int64)
    )


def _fill_nulls(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("WhiteRatingDiff").fill_null(pl.lit(0)),
        pl.col("BlackRatingDiff").fill_null(pl.lit(0)),
    )


def _count_moves(moves: str) -> int:
    game = pgn.read_game(io.StringIO(moves))
    if game is None:
        return 0
    return sum(1 for _ in game.mainline_moves()) // 2


def _add_move_count(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("Moves")
        .map_elements(_count_moves, return_dtype=pl.Int64)
        .alias("NumMoves")
    )
