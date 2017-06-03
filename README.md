# ETL_Electricidad
Proyecto destinado a la asignatura de TIN usando software de ETL Pentaho, el cual extraerá datos de distintas webs sobre consumo y precios de la electricidad y crearemos análisis de diversas formas sobre dichos datos.

## Bots (python)
### Configuración Previa
Para la generación de ficheros json de consumo y precios de la electricidad en España ejecutaremos el fichero _./src/main.py_. Previamente a la ejecución estableceremos los parámetros necesarios para la misma, creando una copia del fichero _./config/Params-default.py_ en el siguiente path _./config/Params.py_.

**Comando de ayuda:**

`cp ./config/Params-default.py ./config/Params.py`

A continuación estableceremos los parámetros del fichero _./config/Params.py_ como se indican en los comentarios. Para establecer las variables:
-  auth_key
-  rand_1
-  rand_2
-  cookie

**Realizado en Firefox**

Seguiremos los siguientes pasos:
  1.  Accedemos a la siguiente URL: [Precios Endesa](https://www.endesaclientes.com/precio-luz-pvpc.html)
  2.  Click derecho e _Inspeccionar Elemento_
  3.  Accederemos a la pestaña de **_red_**
     [Imagen Inspector](https://www.dropbox.com/s/k00hc41eixza2fj/Petici%C3%B3n%20Web%201.png?dl=0)
  4.  Hacemos click en un día previo al de hoy esperando recibir la respuesta marcada
     [Imagen Petición Red](https://www.dropbox.com/s/3mm6axfnqpnij9s/Petici%C3%B3n%20Web%202.png?dl=0)
  5.  Hacemos click en _Editar y volver a enviar_
  6.  Extraemos de aquí las variables necesarias (previamente nombradas)
     [Imagen Variables](https://www.dropbox.com/s/qz81fky8w29hys9/Petici%C3%B3n%20Web%203.png?dl=0)
     Puede usar el comando: `nano ./config/Params.py`

En caso de que el fichero de de algún tipo de error la generacion del fichero _*.precio.json_, repetir estos pasos limpiando la caché del navegador.

### Instalación Dependencias
Para instalar las dependencias necesarias para la ejecución de los bots habrá que ejecutar previamente el siguiente comando en el directorio raiz del repositorio

`./config/Install-dependencies.sh`

### Ejecución de los BOTS
Para ejecutar los bots en el directirio raiz del repositorio usar el siguiente comando:

`python ./src/main.py`

La terminal solicitará una fecha de inicio y fin las cuales deberá ser ingresada con el formato de _d/m/YYYY_. Y posterior mente el nombre del fichero, el cual será creado en la ruta establecida en el fichero de configuración previamente editado ( variable **tmp_directory** ) y el nombre de los ficheros será: **<NombreIntroducido>.consumo.json** y **<NombreIntroducido>.precio.json**.