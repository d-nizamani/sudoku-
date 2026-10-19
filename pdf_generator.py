from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors


def draw_text(pdf, x, y, text, font="Helvetica", size=10):
    pdf.setFont(font, size)
    pdf.drawString(x, y, text)


def draw_centered(pdf, x, y, text, font="Helvetica", size=10):
    pdf.setFont(font, size)
    pdf.drawCentredString(x, y, text)


def draw_grid(pdf, grid, x, y, size):
    cell = size / 9

    for i in range(10):
        pdf.setStrokeColor(colors.black)
        pdf.setLineWidth(1.25 if i % 3 == 0 else 0.35)
        pdf.line(x + i * cell, y, x + i * cell, y + size)
        pdf.line(x, y + i * cell, x + size, y + i * cell)

    for r in range(9):
        for c in range(9):
            number = grid[r][c]

            if number:
                pdf.setFont("Helvetica", max(5, min(12, cell * 0.48)))
                pdf.drawCentredString(
                    x + c * cell + cell / 2,
                    y + size - (r + 1) * cell + cell * 0.29,
                    str(number),
                )


def heading(pdf, page_size, subtitle=""):
    width, height = page_size

    draw_centered(
        pdf, width / 2, height - 32,
        "Sudoku Puzzle Book", size=15
    )

    if subtitle:
        draw_centered(
            pdf, width / 2, height - 51,
            subtitle, size=9
        )

    pdf.setStrokeColor(colors.HexColor("#777777"))
    pdf.setLineWidth(0.5)
    pdf.line(35, height - 62, width - 35, height - 62)


def draw_sudoku_batch(
    pdf, batch, start_number, difficulty, page_size, per_page
):
    width, height = page_size
    heading(pdf, page_size)

    margin, top, bottom, gap = 35, 76, 30, 16
    columns = 1 if per_page == 1 else 2
    rows = (per_page + columns - 1) // columns

    available_height = height - top - bottom

    slot_width = (
        width - 2 * margin - gap * (columns - 1)
    ) / columns

    slot_height = (
        available_height - gap * (rows - 1)
    ) / rows

    for index, (puzzle, _solution) in enumerate(batch):
        row, column = divmod(index, columns)

        slot_x = margin + column * (slot_width + gap)
        slot_top = height - top - row * (slot_height + gap)

        # Leave space for the title and text below the grid.
        grid_size = min(slot_width - 10, slot_height - 65)
        grid_x = slot_x + (slot_width - grid_size) / 2
        grid_y = slot_top - 26 - grid_size

        number = start_number + index

        # Mix provides a separate difficulty for each puzzle.
        if isinstance(difficulty, (list, tuple)):
            level = difficulty[number - 1]
        else:
            level = difficulty

        draw_centered(
            pdf,
            grid_x + grid_size / 2,
            slot_top - 15,
            f"Puzzle {number}",
            size=10,
        )

        draw_grid(pdf, puzzle, grid_x, grid_y, grid_size)

        draw_centered(
            pdf,
            grid_x + grid_size / 2,
            grid_y - 14,
            "1   2   3   4   5   6   7   8   9",
            size=9,
        )

        pdf.setFont("Helvetica", 8)
        pdf.drawRightString(
            grid_x + grid_size,
            grid_y - 28,
            f"Difficulty: {level}",
        )


def create_pdf(
    puzzles, difficulty="Easy", language="en", paper="A4", per_page=2
):
    if language != "en":
        raise ValueError("Only English is supported.")

    if per_page not in (1, 2, 4, 6):
        raise ValueError("Choose 1, 2, 4, or 6 puzzles per page.")

    page_size = A4 if paper == "A4" else letter
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=page_size)
    pdf.setTitle("Sudoku Puzzle Book")

    # Print puzzles only.
    for start in range(0, len(puzzles), per_page):
        batch = puzzles[start:start + per_page]

        draw_sudoku_batch(
            pdf,
            batch,
            start + 1,
            difficulty,
            page_size,
            per_page,
        )

        pdf.showPage()

    pdf.save()
    buffer.seek(0)
    return buffer