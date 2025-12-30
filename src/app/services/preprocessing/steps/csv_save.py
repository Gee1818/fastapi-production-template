import polars as pl

from app.settings import Settings

save_path = Settings.UPLOAD_DIRECTORY / "train.csv"


def csv_save(df: pl.DataFrame) -> None:
    df.write_csv(save_path)
