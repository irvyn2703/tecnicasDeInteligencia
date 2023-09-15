var numPatrones = document.getElementById('N') // obtenemos el input N = numero de patrones
var checkbox = document.getElementById("aleatorios"); // obtenemos el input aleatorios (checkbox que indica si quiere patrones aleatorios)

document.getElementById("aleatorios").addEventListener("change", toggleCoordinateFields); // agregamos un evento al checbox para revisar cambios en su valor y llamamos la funcion toggleCoordinateFields

// si esta activado el checkbox ocultamos los campos para llenar patrones en caso contrario los mostraremos
function toggleCoordinateFields() {
    var coordinateFields = document.getElementById("coordinateFields");
    if (checkbox.checked) {
        // Si el checkbox no está marcado, oculta el elemento
        coordinateFields.style.display = "none";
    } else {
        // Si el checkbox está marcado, muestra el elemento
        coordinateFields.style.display = "block";
    }
}

// agregamos a la pagina el numero de patrones por clase que el usuario debe mandar
function addCoordinateFields() {
    // Obtener el valor del campo "numero de patrones"
    var numPatrones = parseInt(document.getElementById("N").value) * 2; // se multiplica por 2 porque son patrones por clase

    // Obtener el contenedor de campos de coordenadas
    var coordinateFieldsContainer = document.getElementById("coordinateFields");

    // Limpiar el contenedor de campos de coordenadas
    coordinateFieldsContainer.innerHTML = "";

    // Agregar título "Clase A" antes del primer conjunto de campos
    var tituloClaseA = document.createElement("h5");
    tituloClaseA.textContent = "Clase A";
    coordinateFieldsContainer.appendChild(tituloClaseA);

    // Agregar campos de coordenadas para la primera mitad de patrones
    for (var i = 0; i < numPatrones / 2; i++) {
        // agregamos las clases coorespondientes para la estetica de los contenedoros
        var coordinateFieldSet = document.createElement("div");
        coordinateFieldSet.classList.add("col", "row");

        var coordinateXField = document.createElement("div");
        coordinateXField.classList.add("col");
        coordinateXField.innerHTML = '<label class="form-label">Coordenada x</label><input class="form-control puntosXUser" type="number" name="puntoXUser" min="-10" max="10" value="' + (puntosUserData[i] ? puntosUserData[i][0] : '0') + '" required>'; // aqui agregamos el input y encaso de tener el valor previamente guardado en el backend lo agregamos en el input

        var coordinateYField = document.createElement("div");
        coordinateYField.classList.add("col");
        coordinateYField.innerHTML = '<label class="form-label">Coordenada y</label><input class="form-control puntosYUser" type="number" name="puntoYUser" min="-10" max="10" value="' + (puntosUserData[i] ? puntosUserData[i][1] : '0') + '" required>';// repetimos solo que este sera para la coordenada Y

        // lo agregamos
        coordinateFieldSet.appendChild(coordinateXField);
        coordinateFieldSet.appendChild(coordinateYField);
        coordinateFieldsContainer.appendChild(coordinateFieldSet);
    }

    // Agregar título "Clase B" antes del segundo conjunto de campos
    var tituloClaseB = document.createElement("h5");
    tituloClaseB.textContent = "Clase B";
    coordinateFieldsContainer.appendChild(tituloClaseB);

    // Agregar campos de coordenadas para la segunda mitad de patrones
    for (var i = numPatrones / 2; i < numPatrones; i++) {
        var coordinateFieldSet = document.createElement("div");
        coordinateFieldSet.classList.add("col", "row");

        var coordinateXField = document.createElement("div");
        coordinateXField.classList.add("col");
        coordinateXField.innerHTML = '<label class="form-label">Coordenada x</label><input class="form-control puntosXUser" type="number" name="puntoXUser" min="-10" max="10" value="' + (puntosUserData[i] ? puntosUserData[i][0] : '0') + '" required>'; // aqui agregamos el input y encaso de tener el valor previamente guardado en el backend lo agregamos en el input

        var coordinateYField = document.createElement("div");
        coordinateYField.classList.add("col");
        coordinateYField.innerHTML = '<label class="form-label">Coordenada y</label><input class="form-control puntosYUser" type="number" name="puntoYUser" min="-10" max="10" value="' + (puntosUserData[i] ? puntosUserData[i][1] : '0') + '" required>';// repetimos solo que este sera para la coordenada Y

        // lo agregamos
        coordinateFieldSet.appendChild(coordinateXField);
        coordinateFieldSet.appendChild(coordinateYField);
        coordinateFieldsContainer.appendChild(coordinateFieldSet);
    }
}


numPatrones.addEventListener('change', function(){ // en caso de cambiar el numero de patrones cambia el numero de campos con nuestra funcion ddCoordinateFields()
    addCoordinateFields();
});

// Función para verificar las coordenadas y mostrar un alert si es necesario
function verificarCoordenadasEnAreas() {
    if (checkbox.checked) { // en caso de que nuestro checkbox este activo no necesita comprobar las coodenadas
        // envia el formulario sin comprobar nada
        document.getElementById("procesar").submit();
    } else {
            // Obtener las coordenadas ingresadas nuestra variable sera un arreglo de todos los patrones que el usuario ingreso
            var coordenadaXElements = document.getElementsByClassName("puntosXUser");
            var coordenadaYElements = document.getElementsByClassName("puntosYUser");
        
            // Obtener las coordenadas de las áreas
            var px1 = parseFloat(document.getElementById("p1x").value);
            var py1 = parseFloat(document.getElementById("p1y").value);
            var px2 = parseFloat(document.getElementById("p2x").value);
            var py2 = parseFloat(document.getElementById("p2y").value);
            var px3 = parseFloat(document.getElementById("p3x").value);
            var py3 = parseFloat(document.getElementById("p3y").value);
            var px4 = parseFloat(document.getElementById("p4x").value);
            var py4 = parseFloat(document.getElementById("p4y").value);
        
            // Inicializar una lista para rastrear las coordenadas inválidas
            var coordenadasInvalidas = [];
        
            // Verificar si las coordenadas están dentro de las áreas
            for (var i = 0; i < coordenadaXElements.length; i++) {
                // obtiene la coordenada x,y
                var coordenadaX = parseFloat(coordenadaXElements[i].value);
                var coordenadaY = parseFloat(coordenadaYElements[i].value);
        
                // revisa si esta en el area A
                var area1Valida = coordenadaX >= Math.min(px1, px2) && coordenadaX <= Math.max(px1, px2) &&
                    coordenadaY >= Math.min(py1, py2) && coordenadaY <= Math.max(py1, py2);
        
                // revisa si esta en el area B
                var area2Valida = coordenadaX >= Math.min(px3, px4) && coordenadaX <= Math.max(px3, px4) &&
                    coordenadaY >= Math.min(py3, py4) && coordenadaY <= Math.max(py3, py4);
        
                if (i < coordenadaXElements.length / 2) { // previamente decidimos que la primera mitad de patrones deben ser del area A
                    // Verificar si alguna coordenada no está en el area A
                    if (!area1Valida) {// en caso de no estar guardamos la coordenada
                        coordenadasInvalidas.push(`(${coordenadaX}, ${coordenadaY})`);
                    }
                }else{// la segunda mitad debe ser del area B
                    // Verificar si alguna coordenada no está en el area B
                    if (!area2Valida) {// en caso de no estar guardamos la coordenada
                        coordenadasInvalidas.push(`(${coordenadaX}, ${coordenadaY})`);
                    }
                }
            }
        
            if (coordenadasInvalidas.length > 0) { // verificamos que no exista ninguna coordenada incorrecta
                // imprimimos las coordenadas erroneas
                alert(`Las siguientes coordenadas no están en ninguna área: ${coordenadasInvalidas.join(", ")}`);
            } else {
                // Todas las coordenadas están en alguna área, enviar el formulario
                document.getElementById("procesar").submit();
            }
        }
    }



// Escuchar el evento de clic en el botón "enviar"
document.getElementById("enviarBoton").addEventListener("click", function (e) {
    e.preventDefault(); // Evitar el comportamiento predeterminado del botón
    verificarCoordenadasEnAreas(); // Realizar la verificación
});



// llamamos a las funciones para ejecutarlas al iniciar la pagina
addCoordinateFields();
toggleCoordinateFields();