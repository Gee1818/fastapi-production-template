import chess

from app.services.preprocessing.config.feature_engineer_config import (
    FeatureEngineerConfig,
)


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

    white_attacked_count = 0
    white_attacked_value = 0
    black_attacked_count = 0
    black_attacked_value = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            is_attacked = board.is_attacked_by(not piece.color, square)

            if is_attacked:
                piece_value = config.piece_values[piece.piece_type]

                if piece.color == chess.WHITE:
                    white_attacked_count += 1
                    white_attacked_value += piece_value
                else:
                    black_attacked_count += 1
                    black_attacked_value += piece_value

    return {
        "white_pieces_attacked": white_attacked_count,
        "white_attacked_value": white_attacked_value,
        "black_pieces_attacked": black_attacked_count,
        "black_attacked_value": black_attacked_value,
        "attacked_diff": black_attacked_value - white_attacked_value,
    }


def calculate_opponent_aggression(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"opponent_aggression": 0}

    MID_SQUARE_INDEX = 31

    w = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.WHITE, chess.SQUARES[x]) and x > MID_SQUARE_INDEX
    ])
    b = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.BLACK, chess.SQUARES[x]) and x < MID_SQUARE_INDEX
    ])
    return {"opponent_aggression": w - b}


def calculate_aggression(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"aggression": 0}

    w = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.WHITE, chess.SQUARES[x])
        and x in list(chess.scan_reversed(board.occupied_co[chess.BLACK]))
    ])
    b = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.BLACK, chess.SQUARES[x])
        and x in list(chess.scan_reversed(board.occupied_co[chess.WHITE]))
    ])
    return {"aggression": w - b}


def calculate_pieces_protected(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"pieces_protected": 0}

    all_w = [
        idx
        for idx, sq in enumerate(chess.SQUARES)
        if (p := board.piece_at(sq)) is not None and p.color == chess.WHITE
    ]
    all_b = [
        idx
        for idx, sq in enumerate(chess.SQUARES)
        if (p := board.piece_at(sq)) is not None and p.color == chess.BLACK
    ]

    w = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.WHITE, chess.SQUARES[x]) and x in all_w
    ])
    b = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.BLACK, chess.SQUARES[x]) and x in all_b
    ])
    return {"pieces_protected": w - b}
