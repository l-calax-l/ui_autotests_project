from pathlib import Path

import pandas as pd


class ExcelDataReader:
    """Читает тестовые данные из Excel — каждый лист = отдельная страница."""

    def __init__(self, file_path: str = None):
        if file_path is None:
            file_path = Path(__file__).parent / "test_data.xlsx"
        self.file_path = file_path

    def _read_sheet(self, sheet_name: str, is_valid: bool) -> list[dict]:
        """Читает лист, фильтрует по is_valid, убирает колонку is_valid из результата."""
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, keep_default_na=False)

        mask = (
            df["is_valid"].astype(str).str.strip().str.lower() == str(is_valid).lower()
        )
        filtered = df[mask].drop(columns=["is_valid"])

        return filtered.to_dict(orient="records")

    # RegPage
    def get_reg_page_valid(self) -> list[dict]:
        return self._read_sheet("reg_page", True)

    def get_reg_page_invalid(self) -> list[dict]:
        return self._read_sheet("reg_page", False)

    # BankLogin
    def get_bank_login_valid(self) -> list[dict]:
        return self._read_sheet("bank_login", True)

    def get_bank_login_invalid(self) -> list[dict]:
        return self._read_sheet("bank_login", False)

    # Manager
    def get_manager_valid(self) -> list[dict]:
        return self._read_sheet("manager", True)

    def get_manager_invalid(self) -> list[dict]:
        return self._read_sheet("manager", False)
