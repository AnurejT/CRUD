from flask import Flask, request, render_template, redirect, flash, session, url_for
from models import db, StudentModel
from functools import wraps

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y_change_in_prod"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ── Auth decorator ────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Please log in to continue.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ── Home / list with search & pagination ─────────────────────────────────────
@app.route('/', methods=['GET'])
@login_required
def home():
    search = request.args.get('search', '').strip()
    page   = request.args.get('page', 1, type=int)
    per_page = 8

    query = StudentModel.query
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                StudentModel.first_name.ilike(like),
                StudentModel.last_name.ilike(like),
                StudentModel.email.ilike(like),
                StudentModel.country.ilike(like),
            )
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    students   = pagination.items
    total      = query.count()

    return render_template('home.html',
                           students=students,
                           pagination=pagination,
                           search=search,
                           total=total)

# ── Create ────────────────────────────────────────────────────────────────────
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        hobby   = request.form.getlist('hobbies')
        hobbies = ", ".join(hobby)

        first_name  = request.form.get('first_name', '').strip()
        second_name = request.form.get('second_name', '').strip()
        email       = request.form.get('email', '').strip()
        password    = request.form.get('password', '').strip()
        gender      = request.form.get('gender', '')
        country     = request.form.get('country', '')

        if not all([first_name, second_name, email, password, gender, country]):
            flash("All fields are required.", "danger")
            return render_template('create.html')

        if StudentModel.query.filter_by(email=email).first():
            flash("A student with that email already exists.", "danger")
            return render_template('create.html')

        student = StudentModel(
            first_name=first_name,
            second_name=second_name,
            email=email,
            password=password,
            gender=gender,
            hobbies=hobbies,
            country=country
        )
        db.session.add(student)
        db.session.commit()
        flash(f"Student '{first_name} {second_name}' added successfully!", "success")
        return redirect(url_for('home'))

    return render_template('create.html')

# ── Edit ──────────────────────────────────────────────────────────────────────
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    student = StudentModel.query.get_or_404(id)

    if request.method == 'POST':
        hobby   = request.form.getlist('hobbies')
        hobbies = ", ".join(hobby)

        first_name  = request.form.get('first_name', '').strip()
        second_name = request.form.get('second_name', '').strip()
        email       = request.form.get('email', '').strip()
        password    = request.form.get('password', '').strip()
        gender      = request.form.get('gender', '')
        country     = request.form.get('country', '')

        if not all([first_name, second_name, email, password, gender, country]):
            flash("All fields are required.", "danger")
            return render_template('edit.html', student=student)

        # Check duplicate email (excluding current student)
        existing = StudentModel.query.filter(
            StudentModel.email == email,
            StudentModel.id != id
        ).first()
        if existing:
            flash("Another student with that email already exists.", "danger")
            return render_template('edit.html', student=student)

        student.first_name = first_name
        student.last_name  = second_name
        student.email      = email
        student.password   = password
        student.gender     = gender
        student.hobbies    = hobbies
        student.country    = country

        db.session.commit()
        flash(f"Student '{first_name} {second_name}' updated successfully!", "success")
        return redirect(url_for('home'))

    return render_template('edit.html', student=student)

# ── Delete ────────────────────────────────────────────────────────────────────
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    student = StudentModel.query.get_or_404(id)
    if request.method == 'POST':
        name = f"{student.first_name} {student.last_name}"
        db.session.delete(student)
        db.session.commit()
        flash(f"Student '{name}' deleted.", "info")
        return redirect(url_for('home'))
    return render_template('delete.html', student=student)

# ── Login / Logout ────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('studentid', '').strip()
        password = request.form.get('password', '').strip()

        if username == 'anurej' and password == '123':
            session['logged_in'] = True
            session['username']  = username
            flash("Welcome back, anurej!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
