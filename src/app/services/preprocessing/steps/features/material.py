import chess

from app.services.preprocessing.config import FeatureEngineerConfig


def calculate_material(
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


def calculate_dof_x_material(
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
