import secrets

from random import choice
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    session,
    redirect,
    url_for,
)

from generator import generate_puzzle, EMPTY_CELLS
from pdf_generator import create_pdf


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

LANGUAGES = {"en": "English"}
PAPER_SIZES = {"A4": "A4", "Letter": "US Letter"}
PUZZLES_PER_PAGE = (1, 2, 4, 6)
DIFFICULTIES = ("Easy", "Medium", "Hard", "Expert", "Mix")

# Temporarily keep solutions on the server, outside the PDF.
solution_packs = {}


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        difficulty = request.form.get("difficulty", "Easy")
        language = request.form.get("language", "en")
        paper = request.form.get("paper", "A4")

        try:
            count = int(request.form.get("count", "4"))
            per_page = int(request.form.get("per_page", "2"))
        except ValueError:
            count, per_page = 0, 0

        if difficulty not in DIFFICULTIES:
            error = "Please choose a valid Sudoku difficulty."
        elif language not in LANGUAGES:
            error = "Please choose English."
        elif paper not in PAPER_SIZES:
            error = "Please choose A4 or US Letter."
        elif per_page not in PUZZLES_PER_PAGE:
            error = "Choose 1, 2, 4, or 6 puzzles per page."
        elif not 1 <= count <= 30:
            error = "Choose between 1 and 30 Sudoku puzzles."
        else:
            if difficulty == "Mix":
                levels = [
                    choice(DIFFICULTIES[:-1])
                    for _ in range(count)
                ]
            else:
                levels = [difficulty] * count

            if any(level not in EMPTY_CELLS for level in levels):
                error = (
                    "The generator needs updating to support "
                    "all selected difficulty levels."
                )
            else:
                puzzles = []

                for level in levels:
                    puzzle, solution = generate_puzzle(level)
                    puzzles.append((puzzle, solution))

                pdf_file = create_pdf(
                    puzzles=puzzles,
                    difficulty=levels if difficulty == "Mix" else difficulty,
                    language=language,
                    paper=paper,
                    per_page=per_page,
                )

                # Replace this browser's previous solution pack.
                previous_pack = session.get("solution_pack")
                solution_packs.pop(previous_pack, None)

                # Limit how many packs are kept in memory.
                if len(solution_packs) >= 50:
                    oldest_pack = next(iter(solution_packs))
                    solution_packs.pop(oldest_pack)

                pack_id = secrets.token_urlsafe(24)
                solution_packs[pack_id] = [
                    {
                        "number": number,
                        "difficulty": level,
                        "solution": solution,
                    }
                    for number, ((_puzzle, solution), level)
                    in enumerate(zip(puzzles, levels), start=1)
                ]
                session["solution_pack"] = pack_id

                return send_file(
                    pdf_file,
                    mimetype="application/pdf",
                    as_attachment=True,
                    download_name="sudoku-puzzles.pdf",
                )

    return render_template(
        "index.html",
        error=error,
        difficulties=DIFFICULTIES,
        languages=LANGUAGES,
        papers=PAPER_SIZES,
        per_page_options=PUZZLES_PER_PAGE,
    )

@app.route("/solutions")
def solutions():
    pack_id = session.get("solution_pack")
    answers = solution_packs.get(pack_id)

    if not answers:
        return """
            <h2>No saved solutions found</h2>
            <p>Download a new puzzle PDF first.
            Then click View solutions.</p>
            <a href="/">Back to generator</a>
        """

    return render_template("solutions.html", answers=answers)


if __name__ == "__main__":
    app.run(debug=True)