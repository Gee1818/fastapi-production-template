import chess

from app.services.preprocessing.config import FeatureEngineerConfig

TOTAL_BOARD_SQUARES = 64


def calculate_center_control(
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


def calculate_position_advantage(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"position_advantage": 0}

    w = len([
        x
        for x in range(TOTAL_BOARD_SQUARES)
        if board.is_attacked_by(chess.WHITE, chess.SQUARES[x])
    ])
    b = len([
        x
        for x in range(TOTAL_BOARD_SQUARES)
        if board.is_attacked_by(chess.BLACK, chess.SQUARES[x])
    ])
    return {"position_advantage": w - b}


def calculate_center_advantage(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {"center_advantage": 0}

    center = [18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45]
    w = len([
        x
        for x in range(TOTAL_BOARD_SQUARES)
        if board.is_attacked_by(chess.WHITE, chess.SQUARES[x]) and x in center
    ])
    b = len([
        x
        for x in range(TOTAL_BOARD_SQUARES)
        if board.is_attacked_by(chess.BLACK, chess.SQUARES[x]) and x in center
    ])
    return {"center_advantage": w - b}


def calculate_piece_positions(board: chess.Board | None) -> dict[str, int]:
    if board is None:
        return {
            "queen_position": 0,
            "knight_position": 0,
            "bishop_position": 0,
            "rook_position": 0,
            "pawn_position": 0,
        }

    def piece_position_score(piece_type: int) -> int:
        def attacks_by(color: chess.Color) -> int:
            return sum(
                len(list(board.attacks(sq)))
                for sq in chess.SQUARES
                if (piece := board.piece_at(sq))
                and piece.piece_type == piece_type
                and piece.color == color
            )

        return attacks_by(chess.WHITE) - attacks_by(chess.BLACK)

    return {
        "queen_position": piece_position_score(chess.QUEEN),
        "knight_position": piece_position_score(chess.KNIGHT),
        "bishop_position": piece_position_score(chess.BISHOP),
        "rook_position": piece_position_score(chess.ROOK),
        "pawn_position": piece_position_score(chess.PAWN),
    }
