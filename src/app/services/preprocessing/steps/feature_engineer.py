import io

import chess
import polars as pl
from chess import pgn

from app.services.preprocessing.config.feature_engineer_config import (
    FeatureEngineerConfig,
)


def add_features(df: pl.DataFrame, config: FeatureEngineerConfig) -> pl.DataFrame:
    features_list: list[dict[str, float]] = []

    for moves in df["Moves"]:
        board = _get_board_at_move(moves, config.move_number)

        features: dict[str, float] = {}
        features.update(_calculate_material(board, config))
        features.update(_calculate_attacked_pieces(board, config))
        features.update(_calculate_center_control(board, config))
        features.update(_calculate_castling_rights(board))
        features.update(_calculate_mobility(board, config))
        features.update(_calculate_position_advantage(board))
        features.update(_calculate_center_advantage(board))
        features.update(_calculate_aggression(board))
        features.update(_calculate_pawn_structure(board))
        features.update(_calculate_pieces_protected(board))
        features.update(_calculate_degrees_of_freedom(board))
        features.update(_calculate_opponent_aggression(board))
        features.update(_calculate_piece_positions(board))
        features.update(_calculate_dof_x_material(board, config))

        features_list.append(features)

    features_df = pl.DataFrame(features_list)
    return pl.concat([df, features_df], how="horizontal")


def _get_board_at_move(moves: str, move_number: int) -> chess.Board | None:
    game = pgn.read_game(io.StringIO(moves))
    if game is None:
        return None

    board = game.board()
    move_count = 0

    for move in game.mainline_moves():
        board.push(move)
        move_count += 1
        if move_count == move_number * 2:
            return board

    return board if move_count > 0 else None


def _calculate_material(
    board: chess.Board | None, config: FeatureEngineerConfig
) -> dict[str, int]:
    white_material = 0
    black_material = 0

    if board is None:
        return {"white_material": 0, "black_material": 0, "material_diff": 0}

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = config.piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                white_material += value
            else:
                black_material += value

    return {
        "white_material": white_material,
        "black_material": black_material,
        "material_diff": white_material - black_material,
    }


def _calculate_attacked_pieces(
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


def _calculate_center_control(
    board: chess.Board | None, config: FeatureEngineerConfig
) -> dict[str, int]:
    if board is None:
        return {
            "white_center_pieces": 0,
            "black_center_pieces": 0,
            "white_center_control": 0,
            "black_center_control": 0,
            "center_control_diff": 0,
            "white_extended_control": 0,
            "black_extended_control": 0,
            "extended_control_diff": 0,
        }

    white_center_pieces = 0
    black_center_pieces = 0

    for square in config.center_squares:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                white_center_pieces += 1
            else:
                black_center_pieces += 1

    white_center_attacks = sum(
        1 for sq in config.center_squares if board.is_attacked_by(chess.WHITE, sq)
    )
    black_center_attacks = sum(
        1 for sq in config.center_squares if board.is_attacked_by(chess.BLACK, sq)
    )

    white_extended_attacks = sum(
        1
        for sq in config.extended_center_squares
        if board.is_attacked_by(chess.WHITE, sq)
    )
    black_extended_attacks = sum(
        1
        for sq in config.extended_center_squares
        if board.is_attacked_by(chess.BLACK, sq)
    )

    return {
        "white_center_pieces": white_center_pieces,
        "black_center_pieces": black_center_pieces,
        "white_center_control": white_center_attacks,
        "black_center_control": black_center_attacks,
        "center_control_diff": white_center_attacks - black_center_attacks,
        "white_extended_control": white_extended_attacks,
        "black_extended_control": black_extended_attacks,
        "extended_control_diff": white_extended_attacks - black_extended_attacks,
    }


def _calculate_castling_rights(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {
            "white_can_castle_kingside": 0,
            "white_can_castle_queenside": 0,
            "black_can_castle_kingside": 0,
            "black_can_castle_queenside": 0,
            "white_has_castled": 0,
            "black_has_castled": 0,
            "white_castling_rights_count": 0,
            "black_castling_rights_count": 0,
        }

    white_king_sq = board.king(chess.WHITE)
    black_king_sq = board.king(chess.BLACK)

    white_has_castled = (
        not board.has_castling_rights(chess.WHITE)
        and white_king_sq is not None
        and white_king_sq in {chess.G1, chess.C1}
    )

    black_has_castled = (
        not board.has_castling_rights(chess.BLACK)
        and black_king_sq is not None
        and black_king_sq in {chess.G8, chess.C8}
    )

    return {
        "white_can_castle_kingside": int(
            board.has_kingside_castling_rights(chess.WHITE)
        ),
        "white_can_castle_queenside": int(
            board.has_queenside_castling_rights(chess.WHITE)
        ),
        "black_can_castle_kingside": int(
            board.has_kingside_castling_rights(chess.BLACK)
        ),
        "black_can_castle_queenside": int(
            board.has_queenside_castling_rights(chess.BLACK)
        ),
        "white_has_castled": int(white_has_castled),
        "black_has_castled": int(black_has_castled),
        "white_castling_rights_count": (
            board.has_kingside_castling_rights(chess.WHITE)
            + board.has_queenside_castling_rights(chess.WHITE)
        ),
        "black_castling_rights_count": (
            board.has_kingside_castling_rights(chess.BLACK)
            + board.has_queenside_castling_rights(chess.BLACK)
        ),
    }


def _calculate_mobility(
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


# NEW FEATURES FROM COMMENTED CODE


def _calculate_position_advantage(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"position_advantage": 0}

    w = len([
        x for x in range(64) if board.is_attacked_by(chess.WHITE, chess.SQUARES[x])
    ])
    b = len([
        x for x in range(64) if board.is_attacked_by(chess.BLACK, chess.SQUARES[x])
    ])
    return {"position_advantage": w - b}


def _calculate_center_advantage(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"center_advantage": 0}

    center = [18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45]
    w = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.WHITE, chess.SQUARES[x]) and x in center
    ])
    b = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.BLACK, chess.SQUARES[x]) and x in center
    ])
    return {"center_advantage": w - b}


def _calculate_opponent_aggression(board: chess.Board | None) -> dict[str, int]:
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


def _calculate_degrees_of_freedom(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"degrees_of_freedom": 0}

    dof1 = len(list(board.legal_moves)) if board.turn else -len(list(board.legal_moves))
    board.push(chess.Move.null())
    dof2 = len(list(board.legal_moves)) if board.turn else -len(list(board.legal_moves))
    board.pop()
    return {"degrees_of_freedom": dof1 + dof2}


def _calculate_aggression(board: chess.Board | None) -> dict[str, int]:
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


def _calculate_piece_positions(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {
            "queen_position": 0,
            "knight_position": 0,
            "bishop_position": 0,
            "rook_position": 0,
            "pawn_position": 0,
        }

    def piece_position_score(piece_type: int) -> int:
        w = [
            idx
            for idx, sq in enumerate(chess.SQUARES)
            if (p := board.piece_at(sq)) is not None
            and p.piece_type == piece_type
            and p.color == chess.WHITE
        ]
        b = [
            idx
            for idx, sq in enumerate(chess.SQUARES)
            if (p := board.piece_at(sq)) is not None
            and p.piece_type == piece_type
            and p.color == chess.BLACK
        ]

        w_attacks = sum(len(list(board.attacks(chess.SQUARES[ind]))) for ind in w)
        b_attacks = sum(len(list(board.attacks(chess.SQUARES[ind]))) for ind in b)
        return w_attacks - b_attacks

    return {
        "queen_position": piece_position_score(chess.QUEEN),
        "knight_position": piece_position_score(chess.KNIGHT),
        "bishop_position": piece_position_score(chess.BISHOP),
        "rook_position": piece_position_score(chess.ROOK),
        "pawn_position": piece_position_score(chess.PAWN),
    }


def _calculate_pawn_structure(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"pawn_structure": 0}

    pawn_w = [
        idx
        for idx, sq in enumerate(chess.SQUARES)
        if (p := board.piece_at(sq)) is not None
        and p.piece_type == chess.PAWN
        and p.color == chess.WHITE
    ]
    pawn_b = [
        idx
        for idx, sq in enumerate(chess.SQUARES)
        if (p := board.piece_at(sq)) is not None
        and p.piece_type == chess.PAWN
        and p.color == chess.BLACK
    ]

    w = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.WHITE, chess.SQUARES[x]) and x in pawn_w
    ])
    b = len([
        x
        for x in range(64)
        if board.is_attacked_by(chess.BLACK, chess.SQUARES[x]) and x in pawn_b
    ])
    return {"pawn_structure": w - b}


def _calculate_pieces_protected(board: chess.Board | None) -> dict[str, int]:
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


def _calculate_dof_x_material(
    board: chess.Board | None, config: FeatureEngineerConfig
) -> dict[str, float]:
    if board is None:
        return {"dof_x_material": 0.0}

    scorew = sum(
        config.piece_values[p.piece_type]
        for sq in chess.SQUARES
        if (p := board.piece_at(sq)) and p.color == chess.WHITE
    )
    scoreb = sum(
        config.piece_values[p.piece_type]
        for sq in chess.SQUARES
        if (p := board.piece_at(sq)) and p.color == chess.BLACK
    )

    dof1 = len(list(board.legal_moves)) if board.turn else -len(list(board.legal_moves))
    board.push(chess.Move.null())
    dof2 = len(list(board.legal_moves)) if board.turn else -len(list(board.legal_moves))
    board.pop()

    scorew2 = dof1 * scorew if dof1 > 0 else dof2 * scorew
    scoreb2 = dof1 * scoreb if dof1 < 0 else dof2 * scoreb

    return {"dof_x_material": float(scorew2 - scoreb2)}
