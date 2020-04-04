from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'l like you !'
app.config.from_object(config)
db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return 'Author: %s' % self.name


db.create_all()


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return 'Book: %s %s' % (self.book, self.author_id)


class viev(FlaskForm):
    book = StringField('书籍名称：', validators=[DataRequired()])
    author = StringField("书籍作者：", validators=[DataRequired()])
    submit = SubmitField("提交")


@app.route('/del_book/<book_id>')
def del_book(book_id):
    book = Book.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除失败！')
            db.session.rollback()
    else:
        flash('没有找到书籍！')
    return redirect(url_for('hello_world'))


@app.route("/del_author/<author_id>")
def del_author(author_id):
    author = Author.query.get(author_id)
    if author:
        try:
            Book.query.filter_by(author_id=author_id).delete()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("删除失败！")
            db.session.rollback()
    else:
        flash("没有找到作者！")
    return redirect(url_for("hello_world"))


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    vie = viev()
    if vie.validate_on_submit():
        author_name = vie.author.data
        book_name = vie.book.data
        author = Author.query.filter_by(name=author_name).first()
        if author:
            book = Author.query.filter_by(name=book_name).first()
            if book:
                flash("书籍已经存在")
            else:
                try:
                    new_book = Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash("添加书籍失败!")
                    db.session.rollback()
        else:
            try:
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()
                new_book = Book(name=book_name, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                flash("添加作者和书籍失败！")
                db.session.rollback()
    else:
        if request.method == "POST":
            flash("不能为空白")
    authors = Author.query.all()
    return render_template('index.html', form=vie, authors=authors)


if __name__ == '__main__':
    app.run(debug=True)
