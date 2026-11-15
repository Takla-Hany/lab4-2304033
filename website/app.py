import os
from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import pymysql
from werkzeug.utils import secure_filename
from db import get_db_connection, get_library_connection

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_dev_key")

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # recive the register form information
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not name:
            return render_template('register.html', error="Name is required")
        if not email:
            return render_template('register.html', error="Email is required")
        if not password:
            return render_template('register.html', error="Password is required")
        if not confirm_password:
            return render_template('register.html', error="Confirm password is required")
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")

        # password Hashing
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        connection = get_db_connection()
        try:
            # add register info to database
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)"
                cursor.execute(sql, (email, name, hash.decode('utf-8')))
            connection.commit()

            # let user log-in
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM users WHERE email = %s", (email))
                user = cursor.fetchone()
                session['user_id'] = user['user_id']
                session['user_name'] = name
            
            return redirect(url_for('index'))

        except:
            return render_template('register.html', error="Email Already Exists")
        finally:
            connection.close()

    # Render register Page
    return render_template('register.html')

@app.route('/')
def index():
    # check the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    todos = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC", (session['user_id']))
            todos = cursor.fetchall()
    finally:
        connection.close()
        
    # BONUS
    open_count = sum(1 for todo in todos if todo['is_done'] == 0)
        
    return render_template('index.html', todos=todos, user_name=session.get('user_name', 'User'), open_count=open_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # recive log-in data
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')

        # Validation
        if not email:
            return render_template('login.html', error="Email is required")
        if not password:
            return render_template('login.html', error="Password is required")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # check for user data
                cursor.execute("SELECT user_id, name, password_hash FROM users WHERE email = %s", (email))
                user = cursor.fetchone()

                # if the user exists and the password matches:
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    session['user_id'] = user['user_id']
                    session['user_name'] = user['name']
                    return redirect(url_for('index'))
                else:
                    # wrong e-mail or wrong password
                    return render_template('login.html', error="Invalid email or password")
        finally:
            connection.close()

    # render login page
    return render_template('login.html')

@app.route('/logout')
def logout():
    # clear the session
    session.clear()
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
def add_todo():
    # chech the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form.get('title').strip()
    
    # Validation
    if not title or len(title) > 200:
        error = "Title is required" if not title else "Title is too long (200 characters at most)"
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC", (session['user_id']))
                todos = cursor.fetchall()
            return render_template('index.html', todos=todos, user_name=session.get('user_name'), error=error)
        finally:
            connection.close()

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # add to-do
            cursor.execute("INSERT INTO todos (user_id, title) VALUES (%s, %s)", (session['user_id'], title))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    # chech the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_title = request.form.get('title').strip()
    
    if not new_title or len(new_title) > 200:
        error = "Title is required" if not new_title else "Title is too long (200 characters at most)"
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC", (session['user_id']))
                todos = cursor.fetchall()
            return render_template('index.html', todos=todos, user_name=session.get('user_name', 'User'), error=error)
        finally:
            connection.close()

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # update to-do
            cursor.execute("UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s", (new_title, todo_id, session['user_id']))
        connection.commit()

    finally:
        connection.close()

    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    # chech the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    is_done = request.form.get('is_done')
    new_status = 1 if is_done == '1' else 0
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # update to-do
            cursor.execute("UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s", (new_status, todo_id, session['user_id']))
        connection.commit()

    finally:
        connection.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    # chech the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # update to-do
            cursor.execute("DELETE FROM todos WHERE todo_id = %s AND user_id = %s", (todo_id, session['user_id']))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('index'))




# LAB 3

# F2.1 Show a table of the books (with the author_id of each book) and a table of the authors.
@app.route('/library')
def library():
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM AUTHOR")
            authors = cursor.fetchall()
            cursor.execute("SELECT * FROM BOOK")
            books = cursor.fetchall()
    finally:
        connection.close()
    return render_template('library.html', authors=authors, books=books)

#F2.2 Add a book.
@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    price = request.form.get('price')
    author_id = request.form.get('author_id')
    
    # Handle image upload
    image = request.files.get('image')
    filename = None
    if image and image.filename and image.filename.split('.')[1].lower() in ['png', 'jpeg','jpg','webp']:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    connection = get_library_connection()
    try:
        if float(price) >= 0:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO BOOK (title, price, author_id, image_filename) VALUES (%s, %s, %s, %s)", (title, price, author_id, filename))
            connection.commit()
    finally:
        connection.close()
    return redirect(url_for('library'))

#F2.2 add an author.
@app.route('/add_author', methods=['POST'])
def add_author():
    name = request.form.get('name')
    country = request.form.get('country')
    
    # Handle image upload
    image = request.files.get('image')
    filename = None
    if image and image.filename and image.filename.split('.')[1].lower() in ['png', 'jpeg','jpg','webp']:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO AUTHOR (name, country, image_filename) VALUES (%s, %s, %s)", (name, country, filename))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('library'))

#F2.3 Edit a book.
@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    connection = get_library_connection()
    try:
        if request.method == 'POST':
            title = request.form.get('title')
            price = request.form.get('price')
            author_id = request.form.get('author_id')
            
            # Handle potential new image upload
            image = request.files.get('image')
            if image and image.filename and image.filename.split('.')[1].lower() in ['png', 'jpeg','jpg','webp']:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE BOOK SET title=%s, price=%s, author_id=%s, image_filename=%s WHERE book_id=%s", (title, price, author_id, filename, id))
            else:
                # Update without changing the image
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE BOOK SET title=%s, price=%s, author_id=%s WHERE book_id=%s", (title, price, author_id, id))
                    
            connection.commit()
            return redirect(url_for('library'))
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM BOOK WHERE book_id = %s", (id))
            book = cursor.fetchone()
            cursor.execute("SELECT * FROM AUTHOR")
            authors = cursor.fetchall()
    finally:
        connection.close()
    return render_template('edit_book.html', book=book, authors=authors)

# F2.3 edit an author.
@app.route('/edit_author/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    connection = get_library_connection()
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            country = request.form.get('country')
            
            # Handle potential new image upload
            image = request.files.get('image')
            if image and image.filename and image.filename.split('.')[1].lower() in ['png', 'jpeg','jpg','webp']:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE AUTHOR SET name=%s, country=%s, image_filename=%s WHERE author_id=%s", (name, country, filename, id))
            else:
                # Update without changing the image
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE AUTHOR SET name=%s, country=%s WHERE author_id=%s", (name, country, id))
                    
            connection.commit()
            return redirect(url_for('library'))
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM AUTHOR WHERE author_id = %s", (id))
            author = cursor.fetchone()
    finally:
        connection.close()
    return render_template('edit_author.html', author=author)


# F2.4 Remove a book.
@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM BOOK WHERE book_id = %s", (id))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('library'))

# F2.5 Remove an author.
@app.route('/delete_author/<int:id>', methods=['POST'])
def delete_author(id):
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s", (id))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('library'))



# LAB 4

# F2.1
@app.route('/search', methods=['GET'])
def search_books():
    keyword = request.args.get('keyword', '').strip()
    min_price = request.args.get('min_price', '').strip()
    max_price = request.args.get('max_price', '').strip()
    category_id = request.args.get('category_id', '').strip()

    min_val = float(min_price) if min_price != '' else 0.0
    max_val = float(max_price) if max_price != '' else 999999.99

    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM CATEGORY")
            categories = cursor.fetchall()

            sql = """
                SELECT b.book_id, b.title, b.price, b.publish_year, c.name AS category_name
                FROM BOOK b
                LEFT JOIN CATEGORY c ON b.category_id = c.category_id
                WHERE b.title LIKE %s
                AND b.price BETWEEN %s AND %s
            """
            params = [f"%{keyword}%", min_val, max_val]

            if category_id:
                sql += " AND b.category_id = %s"
                params.append(int(category_id))

            sql += " ORDER BY b.price ASC"
            cursor.execute(sql, tuple(params))
            books = cursor.fetchall()
    finally:
        connection.close()

    return render_template(
        'search_books.html',
        books=books,
        categories=categories,
        keyword=keyword,
        min_price=min_price,
        max_price=max_price,
        selected_category=category_id
    )

# F2.2
@app.route('/catalogue')
def catalogue():
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b.book_id, b.title, b.price, b.publish_year,
                a.name AS author_name,
                p.name AS publisher_name,
                c.name AS category_name
                FROM BOOK b
                JOIN AUTHOR a ON b.author_id = a.author_id
                JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
                JOIN CATEGORY c ON b.category_id = c.category_id
                ORDER BY b.book_id ASC
            """)
            books = cursor.fetchall()
    finally:
        connection.close()
    return render_template('catalogue.html', books=books)

# F2.3
@app.route('/reports')
def reports():
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            # (a)
            cursor.execute("""
                SELECT c.category_id, c.name AS category_name,
                COUNT(b.book_id) AS book_count,
                AVG(b.price) AS avg_price
                FROM CATEGORY c
                LEFT JOIN BOOK b ON c.category_id = b.category_id
                GROUP BY c.category_id, c.name
            """)
            category_stats = cursor.fetchall()

            # (b)
            cursor.execute("""
                SELECT a.author_id, a.name AS author_name, COUNT(b.book_id) AS book_count
                FROM AUTHOR a
                JOIN BOOK b ON a.author_id = b.author_id
                GROUP BY a.author_id, a.name
                HAVING COUNT(b.book_id) >= 2
            """)
            prolific_authors = cursor.fetchall()

            # (c)
            cursor.execute("""
                SELECT SUM(price) AS total_price,
                MIN(price) AS min_price,
                MAX(price) AS max_price
                FROM BOOK
            """)
            library_summary = cursor.fetchone()
    finally:
        connection.close()
    return render_template(
        'reports.html',
        category_stats=category_stats,
        prolific_authors=prolific_authors,
        library_summary=library_summary
    )

# F2.4
@app.route('/loans')
def loans():
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            # (a)
            cursor.execute("""
                SELECT l.loan_id, b.title AS book_title, m.name AS member_name, l.loan_date
                FROM LOAN l
                JOIN BOOK b ON l.book_id = b.book_id
                JOIN MEMBER m ON l.member_id = m.member_id
                WHERE l.return_date IS NULL
            """)
            active_loans = cursor.fetchall()

            # (b)
            cursor.execute("""
                SELECT m.member_id, m.name, m.email, m.join_date
                FROM MEMBER m
                LEFT JOIN LOAN l ON m.member_id = l.member_id
                WHERE l.loan_id IS NULL
            """)
            inactive_members = cursor.fetchall()

            # (c)
            cursor.execute("""
                SELECT b.book_id, b.title, b.price, b.publish_year
                FROM BOOK b
                LEFT JOIN LOAN l ON b.book_id = l.book_id
                WHERE l.loan_id IS NULL
            """)
            unborrowed_books = cursor.fetchall()
    finally:
        connection.close()
    return render_template(
        'loans.html',
        active_loans=active_loans,
        inactive_members=inactive_members,
        unborrowed_books=unborrowed_books
    )

# F2.5
@app.route('/most_borrowed')
def most_borrowed():
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            # (a)
            cursor.execute("""
                SELECT b.book_id, b.title, COUNT(l.loan_id) AS loan_count
                FROM BOOK b
                JOIN LOAN l ON b.book_id = l.book_id
                GROUP BY b.book_id, b.title
                ORDER BY loan_count DESC
                LIMIT 3
            """)
            top_books = cursor.fetchall()

            # (b)
            cursor.execute("""
                SELECT m.member_id, m.name, COUNT(l.loan_id) AS loan_count
                FROM MEMBER m
                JOIN LOAN l ON m.member_id = l.member_id
                GROUP BY m.member_id, m.name
                ORDER BY loan_count DESC
                LIMIT 1
            """)
            top_member = cursor.fetchone()
    finally:
        connection.close()
    return render_template('most_borrowed.html', top_books=top_books, top_member=top_member)

# F2.6
@app.route('/authors_books')
def authors_books():
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            # (a)
            cursor.execute("""
                SELECT a.author_id, a.name, a.country, COUNT(b.book_id) AS book_count
                FROM AUTHOR a
                LEFT JOIN BOOK b ON a.author_id = b.author_id
                GROUP BY a.author_id, a.name, a.country
            """)
            authors_count = cursor.fetchall()

            # (b)
            cursor.execute("""
                SELECT b.book_id, b.title, a.name AS author_name, p.name AS publisher_name, a.country
                FROM BOOK b
                JOIN AUTHOR a ON b.author_id = a.author_id
                JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
                WHERE a.country = p.country
            """)
            same_country_books = cursor.fetchall()
    finally:
        connection.close()
    return render_template(
        'authors_books.html',
        authors_count=authors_count,
        same_country_books=same_country_books
    )

if __name__ == '__main__':
    app.run(debug=True)