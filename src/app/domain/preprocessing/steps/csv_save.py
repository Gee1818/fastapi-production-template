import polars as pl

from app.settings import Settings


def save_to_csv(df: pl.DataFrame, file_path: str | None = None) -> None:
    save_path = file_path or str(Settings.UPLOAD_DIRECTORY / "train.csv")
    df.write_csv(save_path)
