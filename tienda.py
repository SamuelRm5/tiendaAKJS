from flask import Flask,request,render_template,url_for,redirect

app=Flask(__name__)

listaCliente = []

@app.route ('/')
def inicio():
    return render_template('index.html')

# SECCIÓN PARA AGREGAR CLIENTES

@app.route ('/agregarClientes')
def agregarClientes():
    return render_template('agregarClientes.html')

@app.route ('/mensajeAgregacion')
def mensajeAgregacion():
    veri=True
    return render_template('agregarClientes.html',veri=veri)

@app.route ('/agregacion',methods=['POST'])
def agregacion():
    if request.method=='POST':
        lista=[]
        # Validaciones
        vacio=True
        existente=True
        documento = request.form['documento']
        for dato in listaCliente:
            if dato[0]==documento:
                return render_template('agregarClientes.html',existente=existente)
        if len(documento)==0:
            return render_template('agregarClientes.html',vacio=vacio)
        else:
            nombre = request.form['nombre']
            nombre=nombre.upper()
            if len(nombre)==0:
                return render_template('agregarClientes.html',vacio1=vacio)

            telefono = request.form['telefono']
            if len(telefono)==0:
                return render_template('agregarClientes.html',vacio2=vacio)

            direccion = request.form['direccion']
            if len(direccion)==0:
                return render_template('agregarClientes.html',vacio3=vacio)

            saldoPe = request.form['saldoPe']
            if len(saldoPe)==0:
                return render_template('agregarClientes.html',vacio4=vacio)
            saldoPe=int(saldoPe)

            lista.append(documento)
            lista.append(nombre)
            lista.append(telefono)
            lista.append(direccion)
            lista.append(saldoPe)

            listaCliente.append(lista)

            print(f"//////////////// \n{listaCliente} \n/////////////////")

            return redirect(url_for('mensajeAgregacion'))
    else:
        return "No es posible la acción"

# SECCIÓN PARA MOSTRAR LOS CLIENTES

@app.route ('/presentacion')
def presentacion():
    return render_template('eleMostrar.html')

@app.route ('/mostrarCliente')
def mostrarCliente():
    return render_template('consultarCliente.html')

@app.route ('/mostrarUno',methods=['POST'])
def mostrarUno():
    if request.method=='POST':
        documento=request.form['documento']
        validacion=True
        for dato in listaCliente:
            if dato[0]==documento:
                return render_template('consultarCliente.html',validacion=validacion,dato=dato)
                
        return render_template('consultarCliente.html',inexistencia=validacion)

@app.route ('/mostrarClientes')
def mostrarClientes():
    if len(listaCliente)==0:
        vacio=True
        return render_template('consultarClientes.html',vacio=vacio)
    return render_template('consultarClientes.html',lista=listaCliente)

# SECCIÓN PARA MODIFICAR LOS CLIENTES

@app.route ('/modificarClientes')
def modificarClientes():
    return render_template('modificarClientes.html')

@app.route ('/modificadorClientes')
def modificadorClientes():
    return render_template ('modificadorCl.html')

@app.route ('/mensajeActualizacion')
def mensajeActualizacion():
    validacion=True
    return render_template('modificarClientes.html',validacion=validacion)

@app.route ('/validacioDocumento',methods=['POST'])
def validacioDocumento():
    if request.method=='POST':
        documento = request.form['documento']
        validacion=True
        for dato in listaCliente:
            if dato[0]==documento:
                return render_template('modificadorCl.html',validacion=validacion,dato=dato)
        return render_template ('/modificarClientes.html',inexistencia=validacion)
    else:
        return "No es posible la acción"

@app.route ('/actualizacion',methods=['POST'])
def actualizacion():
    if request.method=='POST':
        documento=request.form['documento']
        nombre=request.form['nombre']
        telefono=request.form['telefono']
        direccion=request.form['direccion']
        abono=request.form['abono']
        abono=int(abono)
        nombre=nombre.upper()
        for x in listaCliente:
            if x[0]==documento:
                x[0]=documento
                x[1]=nombre
                x[2]=telefono
                x[3]=direccion
                pago=x[4]-abono
                x[4]=pago
        return redirect(url_for('mensajeActualizacion'))

    else:
        return "La acción no es permitida"

# SECCIÓN PARA ELIMINAR CLIENTES CON SALDO EN 0

@app.route ('/eliminarClientes')
def eliminarClientes():
    lista=[]
    inexistencia=True
    for persona in listaCliente:
        if persona[4]==0:
            lista.append(persona)
    print(lista)
    if len(lista)==0:
        inexistencia=True
        return render_template('eliminarCliente.html',inexistencia=inexistencia)
    inexistencia=False
    return render_template('eliminarCliente.html',lista=lista,inexistencia=inexistencia)

@app.route ('/eliminacion',methods=['POST'])
def eliminacion():
    if request.method=='POST':
        lista=[]
        for x in listaCliente:
            if x[4]==0:
                lista.append(x[0])
        print(lista)
        documento=request.form['documento']
        if documento in lista:
            for x in listaCliente:
                if x[0]==documento:
                    listaCliente.remove(x)
            return redirect(url_for('eliminarClientes'))
        else:
            error=True
            return redirect(url_for('docIncorrecto'))
    else:
        return "Acción no permitida"

@app.route ('/eliminado')
def eliminado():
    eliminado=True
    return render_template('index.html',eliminado=eliminado)

@app.route ('/docIncorrecto')
def docIncorrecto():
    error=True
    inexistencia=False
    return render_template('eliminarCliente.html',error=error,inexistencia=inexistencia)


if __name__ == '__main__':
    app.run(debug=True)