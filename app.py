# from flask import Flask, request, render_template, jsonify
# import os
# from pdf_utils import extract_text_from_pdf
# from vector_store import create_faiss_index, load_index, get_top_chunks

# UPLOAD_FOLDER = 'uploaded_pdfs'
# SYLLABUS_FOLDER = 'syllabus_pdfs'

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Load syllabus index on startup
# index, chunks = None, []

# def preload_syllabus():
#     texts = []
#     for filename in os.listdir(SYLLABUS_FOLDER):
#         if filename.endswith(".pdf"):
#             filepath = os.path.join(SYLLABUS_FOLDER, filename)
#             text = extract_text_from_pdf(filepath)
#             chunked = [text[i:i+500] for i in range(0, len(text), 500)]
#             texts.extend(chunked)
#     create_faiss_index(texts)
#     return load_index()

# @app.route('/')
# def index_page():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_pdf():
#     global index, chunks
#     file = request.files['pdf']
#     if file:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)
#         text = extract_text_from_pdf(filepath)
#         chunked = [text[i:i+500] for i in range(0, len(text), 500)]
#         create_faiss_index(chunked)
#         index, chunks = load_index("syllabus_index")  # reload from uploaded file
#         return "PDF uploaded and processed!"
#     return "No file received."



# @app.route('/ask', methods=['POST'])
# def ask_question():
#     global index, chunks
#     if index is None:
#         return jsonify(["❌ No syllabus or file loaded."])

#     query = request.form['question']
#     top_chunks = get_top_chunks(query, index, chunks)

#     if not top_chunks:
#         return jsonify(["❌ Sorry, I couldn't find an answer."])

#     # Combine top chunks and format into point-wise detailed answer
#     detailed_answer = generate_detailed_answer(query, top_chunks)
#     return jsonify([detailed_answer])


# def generate_detailed_answer(question, chunks):
#     answer = f"🔹 **Detailed Answer for:** _{question}_\n\n"
#     for idx, chunk in enumerate(chunks, 1):
#         answer += f"**{idx}.** {chunk.strip()}\n\n"
#     answer += "\n✅ _Hope this explanation helped you!_"
#     return answer


# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     if not os.path.exists(SYLLABUS_FOLDER):
#         os.makedirs(SYLLABUS_FOLDER)
#     index, chunks = preload_syllabus()
#     app.run(debug=True)
# -------------------------------------------------



# from flask import Flask, request, render_template, jsonify
# import os
# from pdf_utils import extract_text_from_pdf
# from vector_store import create_faiss_index, load_index, get_top_chunks

# UPLOAD_FOLDER = 'uploaded_pdfs'
# SYLLABUS_FOLDER = 'syllabus_pdfs'

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Load syllabus index on startup
# index, chunks = None, []

# def preload_syllabus():
#     texts = []
#     for filename in os.listdir(SYLLABUS_FOLDER):
#         if filename.endswith(".pdf"):
#             filepath = os.path.join(SYLLABUS_FOLDER, filename)
#             text = extract_text_from_pdf(filepath)
#             chunked = [text[i:i+500] for i in range(0, len(text), 500)]
#             texts.extend(chunked)
#     if texts:
#         create_faiss_index(texts)
#         return load_index()
#     else:
#         return None, []

# @app.route('/')
# def index_page():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_pdf():
#     global index, chunks
#     file = request.files['pdf']
#     if file:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)
#         text = extract_text_from_pdf(filepath)
#         chunked = [text[i:i+500] for i in range(0, len(text), 500)]
#         create_faiss_index(chunked)
#         index, chunks = load_index()
#         return "✅ PDF uploaded and processed!"
#     return "❌ No file received."

# @app.route('/ask', methods=['POST'])
# def ask_question():
#     global index, chunks
#     if index is None:
#         return jsonify(["❌ No syllabus or file loaded."])

#     query = request.form['question']
#     top_chunks = get_top_chunks(query, index, chunks, k=5)

#     if not top_chunks:
#         return jsonify(["❌ Sorry, I couldn't find an answer."])

#     # Generate detailed answer
#     detailed_answer = generate_detailed_answer(query, top_chunks)
#     return jsonify([detailed_answer])

# def generate_detailed_answer(question, chunks):
#     answer = f"<h3>📚 Detailed Explanation for: <i>{question}</i></h3><br>"

#     combined_text = " ".join(chunks)
#     sentences = combined_text.replace('\n', ' ').split(". ")

#     points = []
#     current_point = ""

#     for sentence in sentences:
#         if len(current_point) + len(sentence) < 200:
#             current_point += sentence + ". "
#         else:
#             points.append(current_point.strip())
#             current_point = sentence + ". "

#     if current_point:
#         points.append(current_point.strip())

#     # Limit 5 to 8 points for neatness
#     final_points = points[:8]

#     for idx, point in enumerate(final_points, 1):
#         answer += f"<b>{idx}.</b> {point}<br><br>"

#     answer += "✅ <i>Hope this detailed explanation helped you understand better!</i>"
#     return answer


# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     if not os.path.exists(SYLLABUS_FOLDER):
#         os.makedirs(SYLLABUS_FOLDER)
#     index, chunks = preload_syllabus()
#     app.run(debug=True)

from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import os
from pdf_utils import extract_text_from_pdf
from vector_store import create_faiss_index, load_index, get_top_chunks

UPLOAD_FOLDER = 'uploaded_pdfs'
SYLLABUS_FOLDER = 'syllabus_pdfs'

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

index, chunks = None, []

users = {}  # Simple dictionary for login/signup

def preload_syllabus():
    texts = []
    for filename in os.listdir(SYLLABUS_FOLDER):
        if filename.endswith(".pdf"):
            filepath = os.path.join(SYLLABUS_FOLDER, filename)
            text = extract_text_from_pdf(filepath)
            chunked = [text[i:i+500] for i in range(0, len(text), 500)]
            texts.extend(chunked)
    if texts:
        create_faiss_index(texts)
        return load_index()
    else:
        return None, []

@app.route('/')
def index_page():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index_page'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error="Username already exists")
        else:
            users[username] = password
            session['username'] = username
            return redirect(url_for('index_page'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global index, chunks
    file = request.files['pdf']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        text = extract_text_from_pdf(filepath)
        chunked = [text[i:i+500] for i in range(0, len(text), 500)]
        create_faiss_index(chunked)
        index, chunks = load_index()
        return "✅ PDF uploaded and processed!"
    return "❌ No file received."

@app.route('/ask', methods=['POST'])
def ask_question():
    global index, chunks
    if index is None:
        return jsonify(["❌ No syllabus or file loaded."])

    query = request.form['question']
    top_chunks = get_top_chunks(query, index, chunks, k=5)

    if not top_chunks:
        return jsonify(["❌ Sorry, I couldn't find an answer."])

    detailed_answer = generate_detailed_answer(query, top_chunks)
    return jsonify([detailed_answer])

def generate_detailed_answer(question, chunks):
    answer = f"<h3>📚 Detailed Explanation for: <i>{question}</i></h3><br>"

    combined_text = " ".join(chunks)
    sentences = combined_text.replace('\n', ' ').split(". ")

    points = []
    current_point = ""

    for sentence in sentences:
        if len(current_point) + len(sentence) < 200:
            current_point += sentence + ". "
        else:
            points.append(current_point.strip())
            current_point = sentence + ". "

    if current_point:
        points.append(current_point.strip())

    final_points = points[:8]

    for idx, point in enumerate(final_points, 1):
        answer += f"<b>{idx}.</b> {point}<br><br>"

    answer += "✅ <i>Hope this detailed explanation helped you understand better!</i>"
    return answer

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(SYLLABUS_FOLDER):
        os.makedirs(SYLLABUS_FOLDER)
    index, chunks = preload_syllabus()
    app.run(debug=True)
