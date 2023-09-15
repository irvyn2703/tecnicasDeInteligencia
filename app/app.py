
import random # nospermite crear numeros aleatorios
from flask import Flask, render_template, request, redirect, url_for # nos permite crear un servidor web y controlar el backend con python
import numpy as np # nos ayuda para manejar arreglos,matrices y operaciones entre estos
from lab4 import AlgoritmoPerceptron # nos permite tener acceso a nuestro objeto lab4 (perceptron)

# variables globales para la pagina web
per1 = AlgoritmoPerceptron() # constructor del perceptron
puntosUser = [] # aqui guardaremos los puntos del usuario
data = { # inicializamos los datos
    'px1': 0,
    'px2': 0,
    'px3': 0,
    'px4': 0,
    'py1': 0,
    'py2': 0,
    'py3': 0,
    'py4': 0,
    'numFronteras': 2,
    'numEpocas': 2,
    'puntosUser' : puntosUser,
    'aleatorios' : True,
    'interMin' : 0,
    'interMax' : 1,
    'learning' : 0.01,
    'N' : 2, # numero de patrones
    'reconocimiento' : 0,
    'generalizacion' : 0,
}


app = Flask(__name__)

app.static_folder = 'static'


@app.route('/') #ruta index
def index():
    random_number = random.randint(1, 10000)  # Genera un número aleatorio
    return render_template('index.html', data=data, random_number=random_number) # renderizamos el index y enviamos data


@app.route('/procesar', methods=['GET'])
def procesar():
    global data  # Accedemos a la variable global data

    # Obtener los valores de la URL
    data['px1'] = float(request.args.get('p1x', data['px1']))
    data['px2'] = float(request.args.get('p2x', data['px2']))
    data['px3'] = float(request.args.get('p3x', data['px3']))
    data['px4'] = float(request.args.get('p4x', data['px4']))
    data['py1'] = float(request.args.get('p1y', data['py1']))
    data['py2'] = float(request.args.get('p2y', data['py2']))
    data['py3'] = float(request.args.get('p3y', data['py3']))
    data['py4'] = float(request.args.get('p4y', data['py4']))
    data['numFronteras'] = int(request.args.get('numFronteras', data['numFronteras']))
    data['numEpocas'] = int(request.args.get('numEpocas', data['numEpocas']))
    data['interMin'] = float(request.args.get('interMin', data['interMin']))
    data['interMax'] = float(request.args.get('interMax', data['interMax']))
    data['learning'] = float(request.args.get('learning', data['learning']))
    data['N'] = int(request.args.get('N', data['N']))

    # Verificar el estado del checkbox 'patrones aleatorios'
    aleatorios = request.args.get('aleatorios')
    data['aleatorios'] = aleatorios == 'on'

    # Actualizar puntosUser (también puedes mantener el código anterior)
    global puntosUser
    puntosUser = []
    puntoXUser = request.args.getlist('puntoXUser')
    puntoYUser = request.args.getlist('puntoYUser')
    if len(puntoXUser) == len(puntoYUser):
        for i in range(len(puntoXUser)):
            x = float(puntoXUser[i])
            y = float(puntoYUser[i])
            puntosUser.append((x, y))
    data['puntosUser'] = puntosUser


    # Dividir los puntos en claseA y claseB (en nuestra pagina web ya restringimos que la primera mitad sean de la claseA y la segunda sean de clase B)
    mitad = len(puntosUser) // 2
    claseA = puntosUser[:mitad]
    claseB = puntosUser[mitad:]

    # nuestro programa necesita recibir los puntos como p1 = [px1, py1], p2 = [px2, py2], p3 = [px3, py3], p4 = [px4, py4]
    p1 = [] 
    p2 = []
    p3 = []
    p4 = []

    p1.append(float(request.args['p1x']))
    p1.append(float(request.args['p1y']))
    p2.append(float(request.args['p2x']))
    p2.append(float(request.args['p2y']))
    p3.append(float(request.args['p3x']))
    p3.append(float(request.args['p3y']))
    p4.append(float(request.args['p4x']))
    p4.append(float(request.args['p4y']))

    # mandamos los parametros como nos los solicita el objeto perceptron
    if (int(request.args['numFronteras']) == 2): # el perceptron identifica como false = 2 fronteras y true = 4 fronteras
        per1.set_parametros(float(request.args['interMin']), float(request.args['interMax']), False, int(request.args['numEpocas']), float(request.args['learning']), int(request.args['N']), p1, p2, p3, p4)
    else:
        per1.set_parametros(float(request.args['interMin']), float(request.args['interMax']), True, int(request.args['numEpocas']), float(request.args['learning']), int(request.args['N']), p1, p2, p3, p4)
    per1.set_w_b() # llamamos el metodo para obtener los pesos aleatorios
    r1, r2 = per1.generar_puntos_aleatorios_en_dos_regiones() # generamos patrones aleatorios en las areas
    per1.set_patrones_salidas(r1, r2) # clasificamos los patrones
    per1.entrenamiento_perceptron() # entrenamos el perceptron
    per1.graficacion() # generamos la grafica que se graficara en la pagina web
    if request.args.get('aleatorios') == "on": # obtenemos la generalizacion con patrones aleatorios o con patrones del usuario dependiendo de la obcion que el usuario seleccione
        per1.set_recon_us(False) # el programa genera patrones aleatorios
    else:
        per1.set_recon_us(True, claseA, claseB) # el programa envia los patrones del usuario
    recon, gen = per1.get_recon_gen() # obtenemos el reconocimiento y la generalizacion
    # enviamos estos valores por data
    data['reconocimiento'] = recon 
    data['generalizacion'] = gen
    print("Reconocimiento: \n", recon)
    print("Generalizacion: \n", gen)
    return redirect(url_for('index')) # regresamos al index


if __name__ == '__main__':
    app.run(debug=True)# nos permite actualizar el servidor sin detenerlo
