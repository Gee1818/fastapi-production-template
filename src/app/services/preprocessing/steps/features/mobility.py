import chess

from app.services.preprocessing.config.feature_engineer_config import (
    FeatureEngineerConfig,
)


def calculate_mobility(
    board: chess.Board | None, config: FeatureEngineerConfig
) -> dict[str, float]:
    if board is None:
        return {
            "white_mobility": 0,
            "black_mobility": 0,
            "mobility_diff": 0,
            "white_weighted_mobility": 0.0,
            "black_weighted_mobility": 0.0,
            "weighted_mobility_diff": 0.0,
        }

    current_turn = board.turn

    if current_turn == chess.WHITE:
        white_legal_moves = board.legal_moves.count()
        board.turn = chess.BLACK
        black_legal_moves = board.legal_moves.count()
        board.turn = chess.WHITE
    else:
        black_legal_moves = board.legal_moves.count()
        board.turn = chess.WHITE
        white_legal_moves = board.legal_moves.count()
        board.turn = chess.BLACK

    white_weighted = _calculate_weighted_mobility_for_white(board, config)
    black_weighted = _calculate_weighted_mobility_for_black(board, config)

    return {
        "white_mobility": white_legal_moves,
        "black_mobility": black_legal_moves,
        "mobility_diff": white_legal_moves - black_legal_moves,
        "white_weighted_mobility": white_weighted,
        "black_weighted_mobility": black_weighted,
        "weighted_mobility_diff": white_weighted - black_weighted,
    }


def _calculate_weighted_mobility_for_white(
    board: chess.Board, config: FeatureEngineerConfig
) -> float:
    weighted_sum = 0.0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.color == chess.WHITE:
            piece_value = config.piece_values[piece.piece_type]
            moves_from_square = sum(
                1 for move in board.legal_moves if move.from_square == square
            )
            weighted_sum += moves_from_square * piece_value

    return weighted_sum


def _calculate_weighted_mobility_for_black(
    board: chess.Board, config: FeatureEngineerConfig
) -> float:
    weighted_sum = 0.0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.color == chess.BLACK:
            piece_value = config.piece_values[piece.piece_type]
            moves_from_square = sum(
                1 for move in board.legal_moves if move.from_square == square
            )
            weighted_sum += moves_from_square * piece_value

    return weighted_sum


def calculate_degrees_of_freedom(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"degrees_of_freedom": 0}

    dof1 = len(list(board.legal_moves)) if board.turn else -len(list(board.legal_moves))
    board.push(chess.Move.null())
    dof2 = len(list(board.legal_moves)) if board.turn else -len(list(board.legal_moves))
    board.pop()
    return {"degrees_of_freedom": dof1 + dof2}
