from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side,
)


class ExcelExportService:
    """
    Fitness Controller PRO Excel Export
    """

    def __init__(self):

        self.output_dir = Path("exports/reports")
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_report(self):

        workbook = Workbook()

        dashboard = workbook.active
        dashboard.title = "Dashboard"

        self._create_dashboard_sheet(
            dashboard,
        )

        workbook.create_sheet("Ответы")
        workbook.create_sheet("Питание")
        workbook.create_sheet("Тренировки")
        workbook.create_sheet("Фото")
        workbook.create_sheet("Статистика")

        filename = (
            f"report_{datetime.now():%Y-%m-%d_%H-%M-%S}.xlsx"
        )

        filepath = self.output_dir / filename

        workbook.save(filepath)

        return filepath

    def _create_dashboard_sheet(
        self,
        ws,
    ):

        blue = PatternFill(
            "solid",
            fgColor="305496",
        )

        white_font = Font(
            color="FFFFFF",
            bold=True,
            size=18,
        )

        bold = Font(
            bold=True,
        )

        thin = Side(
            style="thin",
        )

        border = Border(
            left=thin,
            right=thin,
            top=thin,
            bottom=thin,
        )

        ws.merge_cells("A1:D2")

        cell = ws["A1"]

        cell.value = "FITNESS CONTROLLER PRO"

        cell.fill = blue

        cell.font = white_font

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
        )

        ws["A4"] = "Дата"

        ws["B4"] = datetime.now().strftime(
            "%d.%m.%Y"
        )

        rows = [
            ("👥 Пользователей", ""),
            ("✅ Прошли", ""),
            ("❌ Не прошли", ""),
            ("📈 Выполнение", ""),
            ("📷 Фото", ""),
            ("⚖ Средний вес", ""),
        ]

        row = 6

        for title, value in rows:

            ws.cell(
                row=row,
                column=1,
                value=title,
            )

            ws.cell(
                row=row,
                column=2,
                value=value,
            )

            ws.cell(
                row=row,
                column=1,
            ).font = bold

            ws.cell(
                row=row,
                column=1,
            ).border = border

            ws.cell(
                row=row,
                column=2,
            ).border = border

            row += 1

        ws.column_dimensions["A"].width = 32
        ws.column_dimensions["B"].width = 18
        ws.column_dimensions["C"].width = 18
        ws.column_dimensions["D"].width = 18
