import io

import chess
import polars as pl
from chess import pgn

from app.services.preprocessing.config import FeatureEngineerConfig

from .features import (
    calculate_aggression,
    calculate_attacked_pieces,
    calculate_castling_rights,
    calculate_center_advantage,
    calculate_center_control,
    calculate_degrees_of_freedom,
    calculate_dof_x_material,
    calculate_material,
    calculate_mobility,
    calculate_opponent_aggression,
    calculate_pawn_structure,
    calculate_piece_positions,
    calculate_pieces_protected,
    calculate_position_advantage,
)

MOVES_PER_TURN = 2


def add_features(df: pl.DataFrame, config: FeatureEngineerConfig) -> pl.DataFrame:
    features_list: list[dict[str, float]] = []

    for moves in df["Moves"]:
        board = _get_board_at_move(moves, config.move_number)

        features: dict[str, float] = {}
        features.update(calculate_material(board, config))
        features.update(calculate_attacked_pieces(board, config))
        features.update(calculate_center_control(board, config))
        features.update(calculate_castling_rights(board))
        features.update(calculate_mobility(board, config))
        features.update(calculate_position_advantage(board))
        features.update(calculate_center_advantage(board))
        features.update(calculate_aggression(board))
        features.update(calculate_pawn_structure(board))
        features.update(calculate_pieces_protected(board))
        features.update(calculate_degrees_of_freedom(board))
        features.update(calculate_opponent_aggression(board))
        features.update(calculate_piece_positions(board))
        features.update(calculate_dof_x_material(board, config))

        features_list.append(features)

    features_df = pl.DataFrame(features_list)
    return pl.concat([df, features_df], how="horizontal")


def _get_board_at_move(moves: str, move_number: int) -> chess.Board | None:
    game = pgn.read_game(io.StringIO(moves))
    if game is None:
        return None

    board = game.board()
    move_count = 0
    max_moves = move_number * MOVES_PER_TURN

    for move in game.mainline_moves():
        board.push(move)
        move_count += 1
        if move_count == max_moves:
            return board

    return board if move_count > 0 else None
