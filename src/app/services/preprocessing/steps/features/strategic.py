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

    def get_pawn_squares(color: chess.Color) -> list[int]:
        return [
            idx
            for idx, sq in enumerate(chess.SQUARES)
            if (piece := board.piece_at(sq)) is not None
            and piece.piece_type == chess.PAWN
            and piece.color == color
        ]

    def count_attacked_pawns(color: chess.Color, pawn_squares: list[int]) -> int:
        return len([
            x
            for x in range(64)
            if board.is_attacked_by(color, chess.SQUARES[x]) and x in pawn_squares
        ])

    pawn_w = get_pawn_squares(chess.WHITE)
    pawn_b = get_pawn_squares(chess.BLACK)

    w = count_attacked_pawns(chess.WHITE, pawn_w)
    b = count_attacked_pawns(chess.BLACK, pawn_b)

    return {"pawn_structure": w - b}
