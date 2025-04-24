from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ejemplo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Articulo {self.id} - {self.title}"

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/Articulos")
def lista():
    articulos = Articulo.query.all()
    mostrar = """
    <h1>Lista de Artículos</h1>
    <ul>
    {% for articulo in articulos %}
        <li>{{ articulo.title }}</li>
    {% endfor %}
    </ul>
    """
    return render_template_string(mostrar, articulos=articulos)

@app.route("/crear-articulo", methods=["GET", "POST"])
def crear_articulo():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form.get("content")
        
        
        new_articulo = Articulo(title=title, content=content)
        db.session.add(new_articulo)
        db.session.commit()
        
        # Crear y guardar el artículo en la base de datos
        nuevo_articulo = Articulo(title=title, content=content)
        db.session.add(nuevo_articulo)
        db.session.commit()
        
        return f"Artículo creado: {title} - {content}"
    
    return '''
    <form method="POST">
        <input type="text" name="title" placeholder="Título">
        <input type="text" name="content" placeholder="Contenido">
        <button type="submit">Crear</button>
    </form>
    '''

@app.route("/crear-articulo/<int:id>")
def crear_articulo_id(id):
    return f"Artículo {id}"

if __name__ == "__main__":
    app.run(debug=True)
