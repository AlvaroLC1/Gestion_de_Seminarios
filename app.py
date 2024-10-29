from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key= 'unaclavesecreta'

def generar_id():
    if 'seminarios' in session and len(session['seminarios']) > 0:
        return max(item['id'] for item in session['seminarios'])+1   
    else:
        return 1

@app.route("/")
def index():
    if 'seminarios' not in session:
        session['seminarios'] = []

    seminarios = session.get('seminarios',[])
    return render_template('index.html',seminarios=seminarios)

@app.route("/nuevo",methods=['GET','POST'])
def nuevo():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        cursos= request.form.getlist('curso')

        nuevo_seminario = {
            'id':generar_id(),
            'fecha':fecha,
            'nombre':nombre,
            'apellidos':apellidos,
            'turno':turno,
            'curso':cursos
        }

        if 'seminarios' not in session:
            session['seminarios'] = []

        session['seminarios'].append(nuevo_seminario)
        session.modified=True
        return redirect(url_for('index'))

    return render_template('nuevo.html')

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    lista_seminarios = session.get('seminarios',[])
    seminario= next( (s for s in lista_seminarios if s['id'] == id), None)
    if not seminario:
        return redirect(url_for('index'))
    
    if request.method=='POST':
        seminario['fecha'] = request.form['fecha']
        seminario['nombre'] = request.form['nombre']
        seminario['apellidos'] = request.form['apellidos']
        seminario['turno'] = request.form['turno']
        seminario['curso'] = request.form.getlist('curso')
        session.modified=True
        return redirect(url_for('index'))
    return render_template('editar.html',seminario=seminario)
    
@app.route("/elminar/<int:id>",methods=["GET"])
def eliminar(id):
    lista_seminarios = session.get('seminarios',[])
    seminario = next((s for s in lista_seminarios if s['id'] == id) ,None)
    if seminario:
        session['seminarios'].remove(seminario)
        session.modified = True
    return redirect(url_for('index'))

if __name__ ==  "__main__":
    app.run(debug=True)