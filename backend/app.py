from flask import Flask, request, render_template, session
import sqlite3
import google.generativeai as genai

from config import GEMINI_API_KEY

app = Flask(__name__)
app.secret_key = "civicai_secret_key"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


@app.route("/")
def home():
    session.clear()
    return render_template("index.html")


@app.route("/chat")
def chat():

    message = request.args.get("message", "").strip()

    if "chat_history" not in session:
        session["chat_history"] = []

    history = session["chat_history"]

    history.append({
        "role": "user",
        "text": message
    })

    # -------------------------
    # GEMINI CATEGORY + COUNTRY
    # -------------------------

    prompt = f"""
    Analyze the user message.

    Categories:
    - Students
    - Farmers
    - Senior Citizens
    - Low Income Families
    - Girls

    Countries:
    - India
    - USA
    - Canada
    - UK

    Return ONLY this format:

    Category|Country

    Examples:
    Students|India
    Farmers|Canada
    Senior Citizens|USA

    User Message:
    {message}
    """

    try:

        response = model.generate_content(prompt)

        result = response.text.strip()

        print("Gemini Response:", result)

        parts = result.split("|")

        if len(parts) == 2:

            target_group = parts[0].strip()
            country = parts[1].strip()

        else:

            target_group = ""
            country = "India"

    except Exception as e:

        target_group = ""
        country = "India"

        print("Gemini Error:", e)

    # -------------------------
    # SQLITE SEARCH
    # -------------------------

    connection = sqlite3.connect("civicai.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            scheme_name,
            benefit,
            documents
        FROM schemes
        WHERE target_group = ?
        AND country = ?
        """,
        (
            target_group,
            country
        )
    )

    rows = cursor.fetchall()

    connection.close()

    # -------------------------
    # RESPONSE
    # -------------------------

    if rows:

        ai_response = ""

        for row in rows:

            documents = row[2].replace(";", "\n• ")

            ai_response += (
                f"🏆 {row[0]}\n\n"
                f"📌 Benefit\n"
                f"{row[1]}\n\n"
                f"📄 Documents Required\n"
                f"• {documents}\n\n"
                f"🌍 Country: {country}\n\n"
                f"━━━━━━━━━━━━━━\n\n"
            )

    else:

        ai_response = (
            f"Detected Category: {target_group}\n"
            f"Detected Country: {country}\n\n"
            f"No matching schemes found."
        )

    history.append({
        "role": "ai",
        "text": ai_response
    })

    session["chat_history"] = history

    return render_template(
        "results.html",
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)