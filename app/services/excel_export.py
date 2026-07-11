from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.report_generator import ReportGeneratorService


class ExcelExportService:
    """
    Excel report generator.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        self.generator = ReportGeneratorService(
            session,
        )

        self.output_dir = Path(
            "exports/reports"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def create_report(
        self,
        report_date: date | None = None,
    ) -> Path:
        """
        Create Excel report.
        """

        if report_date is None:
            report_date = date.today()

        workbook = Workbook()

        dashboard = workbook.active
        dashboard.title = "Dashboard"

        answers_sheet = workbook.create_sheet(
            "Ответы"
        )

        workbook.create_sheet("Питание")
        workbook.create_sheet("Тренировки")
        workbook.create_sheet("Фото")
        workbook.create_sheet("Статистика")

        dashboard_data = await self.generator.dashboard(
            report_date,
        )

        answers = await self.generator.answers(
            report_date,
        )

        self._fill_dashboard(
            dashboard,
            dashboard_data,
        )

        self._fill_answers(
            answers_sheet,
            answers,
        )

        filename = (
            f"report_{report_date}.xlsx"
        )

        filepath = self.output_dir / filename

        workbook.save(filepath)

        return filepath

    # =====================================================
    # DASHBOARD
    # =====================================================

    def _fill_dashboard(
        self,
        ws,
        data,
    ):

        blue = PatternFill(
            "solid",
            fgColor="305496",
        )

        white = Font(
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

        cell.font = white

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
        )

        ws["A4"] = "Дата"

        ws["B4"] = data["date"].strftime(
            "%d.%m.%Y"
        )

        rows = [
            (
                "👥 Пользователей",
                data["total_users"],
            ),
            (
                "✅ Прошли",
                data["completed"],
            ),
            (
                "❌ Не прошли",
                data["not_completed"],
            ),
            (
                "📈 Выполнение",
                f"{data['percent']}%",
            ),
            (
                "📷 Фото",
                data["photos"],
            ),
            (
                "⚖ Средний вес",
                f"{data['average_weight']} кг",
            ),
        ]

        row = 6

        for title, value in rows:

            ws.cell(
                row=row,
                column=1,
                value=title,
            ).font = bold

            ws.cell(
                row=row,
                column=2,
                value=value,
            )

            ws.cell(
                row=row,
                column=1,
            ).border = border

            ws.cell(
                row=row,
                column=2,
            ).border = border

            row += 1

        ws.column_dimensions["A"].width = 30
        ws.column_dimensions["B"].width = 20

    # =====================================================
    # ANSWERS
    # =====================================================

    def _fill_answers(
        self,
        ws,
        rows,
    ):
    """
    Fill worksheet with answers.
    """

    headers = [
        "Пользователь",
        "Дата",
        "Вопрос",
        "Ответ",
        "Фото",
        "Есть фото",
    ]

    header_fill = PatternFill(
        fill_type="solid",
        fgColor="305496",
    )

    header_font = Font(
        bold=True,
        color="FFFFFF",
    )

    yes_fill = PatternFill(
        fill_type="solid",
        fgColor="C6EFCE",
    )

    no_fill = PatternFill(
        fill_type="solid",
        fgColor="FFC7CE",
    )

    for col, title in enumerate(
        headers,
        start=1,
    ):

        cell = ws.cell(
            row=1,
            column=col,
            value=title,
        )

        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
        )

    row = 2

    for item in rows:

        ws.cell(
            row=row,
            column=1,
            value=item["user"],
        )

        ws.cell(
            row=row,
            column=2,
            value=item["date"],
        )

        ws.cell(
            row=row,
            column=3,
            value=item["question"],
        )

        ws.cell(
            row=row,
            column=4,
            value=item["answer"],
        )

        ws.cell(
            row=row,
            column=5,
            value=item["photos"],
        )

        photo_cell = ws.cell(
            row=row,
            column=6,
        )

        if item["photos"] > 0:

            photo_cell.value = "✅"

            photo_cell.fill = yes_fill

        else:

            photo_cell.value = "❌"

            photo_cell.fill = no_fill

        row += 1

    ws.freeze_panes = "A2"

    ws.auto_filter.ref = ws.dimensions

    widths = {
        "A": 28,
        "B": 15,
        "C": 40,
        "D": 45,
        "E": 10,
        "F": 12,
    }

    for column, width in widths.items():

        ws.column_dimensions[
            column
        ].width = width
