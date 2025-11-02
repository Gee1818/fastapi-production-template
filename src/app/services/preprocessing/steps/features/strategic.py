import chess


def calculate_castling_rights(board: chess.Board | None) -> dict[str, int]:
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


def calculate_pawn_structure(board: chess.Board | None) -> dict[str, int]:
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
