from flask import Flask, request, render_template, redirect
from models import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/create', methods=['GET', 'POST'])    
def create():
    if request.method == 'GET':
        return render_template('create.html', request=request)
    
    if request.method == 'POST':
        hobby = request.form.getlist('hobbies')
        hobbies = ",".join(map(str, hobby))
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        country = request.form['counry']

        student = StudentModel(
            first_name=first_name,
            second_name=second_name,
            email=email,
            password=password,
            gender=gender, 
            hobbies=hobbies,
            counry=country
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/')
    
@app.route('/', methods=['GET'])    
def Home():
    students = StudentModel.query.all()
    return render_template('home.html', students=students, request=request)

@app.route('/view', methods=['GET'])    
def ViewList():
    students = StudentModel.query.all()
    return render_template('home.html', students=students, request=request)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    student = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect('/')
    return render_template('delete.html', request=request)       

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    student = StudentModel.query.filter_by(id=id).first()

    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        if student:
            hobby = request.form.getlist('hobbies')
            hobbies = ",".join(map(str, hobby))
            first_name = request.form['first_name']
            second_name = request.form['second_name']
            email = request.form['email']
            password = request.form['password']
            gender = request.form['gender']
            country = request.form['counry']

            student = StudentModel(
                first_name=first_name,
                second_name=second_name,
                email=email,
                password=password,
                gender=gender, 
                hobbies=hobbies,
                counry=country
            )
            db.session.add(student)
            db.session.commit()
            return redirect('/')

    return render_template('edit.html', student=student, request=request) 
    
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
