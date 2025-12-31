from collections.abc import Callable

import chess

from app.services.preprocessing.config.feature_engineer_config import (
    FeatureEngineerConfig,
)

from .constants import MID_SQUARE_INDEX, TOTAL_NUM_SQUARES


def _count_squares_attacked_by(
    board: chess.Board,
    color: chess.Color,
    filter_condition: Callable[[int], bool] | None = None,
) -> int:
    return len([
        x
        for x in range(TOTAL_NUM_SQUARES)
        if board.is_attacked_by(color, chess.SQUARES[x])
        and (filter_condition is None or filter_condition(x))
    ])


def calculate_attacked_pieces(
    board: chess.Board | None, config: FeatureEngineerConfig
) -> dict[str, int]:
    if board is None:
        return {
            "white_pieces_attacked": 0,
            "white_attacked_value": 0,
            "black_pieces_attacked": 0,
            "black_attacked_value": 0,
            "attacked_diff": 0,
        }

    def count_attacked_for_color(piece_color: chess.Color) -> tuple[int, int]:
        attacked_count = 0
        attacked_value = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == piece_color:
                is_attacked = board.is_attacked_by(not piece_color, square)
                if is_attacked:
                    attacked_count += 1
                    attacked_value += config.piece_values[piece.piece_type]

        return attacked_count, attacked_value

    white_count, white_value = count_attacked_for_color(chess.WHITE)
    black_count, black_value = count_attacked_for_color(chess.BLACK)

    return {
        "white_pieces_attacked": white_count,
        "white_attacked_value": white_value,
        "black_pieces_attacked": black_count,
        "black_attacked_value": black_value,
        "attacked_diff": black_value - white_value,
    }


def calculate_opponent_aggression(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"opponent_aggression": 0}

    w = _count_squares_attacked_by(board, chess.WHITE, lambda x: x > MID_SQUARE_INDEX)
    b = _count_squares_attacked_by(board, chess.BLACK, lambda x: x < MID_SQUARE_INDEX)

    return {"opponent_aggression": w - b}


def calculate_aggression(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"aggression": 0}

    white_occupied = list(chess.scan_reversed(board.occupied_co[chess.BLACK]))
    black_occupied = list(chess.scan_reversed(board.occupied_co[chess.WHITE]))

    w = _count_squares_attacked_by(board, chess.WHITE, lambda x: x in white_occupied)
    b = _count_squares_attacked_by(board, chess.BLACK, lambda x: x in black_occupied)

    return {"aggression": w - b}


def calculate_pieces_protected(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"pieces_protected": 0}

    def get_piece_squares(color: chess.Color) -> list[int]:
        return [
            idx
            for idx, sq in enumerate(chess.SQUARES)
            if (piece := board.piece_at(sq)) is not None and piece.color == color
        ]

    white_squares = get_piece_squares(chess.WHITE)
    black_squares = get_piece_squares(chess.BLACK)

    w = _count_squares_attacked_by(board, chess.WHITE, lambda x: x in white_squares)
    b = _count_squares_attacked_by(board, chess.BLACK, lambda x: x in black_squares)

    return {"pieces_protected": w - b}
