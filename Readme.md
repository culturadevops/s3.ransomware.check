# Análisis del Script AWS S3 Bucket Ransomware Scan

Este documento proporciona una descripción y análisis del script de Python diseñado para escanear y evaluar la configuración de los buckets de Amazon S3 en busca de vulnerabilidades a ataques de ransomware.

## Estructura del Script

El script consta de varias secciones principales:

### Importaciones de Módulos

- `argparse`: Se utiliza para analizar los argumentos de la línea de comandos.
- `sys`: Se utiliza para manipular variables y funciones relacionadas con el sistema.
- `time`: Se utiliza para obtener la hora actual del sistema.
- `boto3`: Para conectarnos a AWS 

### Clase `csv_manager`

- Esta clase se utiliza para gestionar la creación y escritura de archivos CSV.
- Tiene métodos para agregar filas al archivo CSV y escribir el archivo en disco.

### Función `main(args)`

- Esta función es la función principal del script.
- Valida los argumentos de la línea de comandos, asegurándose de que se proporcionen los perfiles de AWS CLI principal y secundario, y de que no sean iguales.
- Crea instancias de objetos de sesión de AWS S3 para los perfiles principal y secundario.
- Obtiene los buckets de destino para escanear, ya sea a partir de los argumentos de línea de comandos o mediante la obtención de todos los buckets del perfil principal si no se proporcionan buckets específicos.
- Escanea cada bucket obtenido, evaluando varios aspectos de su configuración, como permisos, configuración de versionamiento y eliminación con MFA.
- Registra los resultados del escaneo en un archivo CSV.

### Función `quit(err_msg, err_code=1)`

- Esta función se utiliza para imprimir un mensaje de error y salir del script con un código de error específico.

## Uso del Script

El script puede ejecutarse desde la línea de comandos proporcionando los argumentos necesarios, como los perfiles de AWS CLI principal y secundario, y los buckets específicos a escanear. Después de ejecutarse, generará un informe en formato CSV con los resultados del análisis.

## Conclusiones

El script proporciona una forma automatizada de escanear y evaluar la configuración de los buckets de Amazon S3 en busca de posibles vulnerabilidades a ataques de ransomware. Es útil para administradores de sistemas y equipos de seguridad que deseen mejorar la seguridad de sus recursos en la nube.


## comandos 
python3 s3_ranzov2.py -p default -s otracuenta -o nombredelarchivo

### ejemplos  
python3 s3_ranzov2.py -p default -s tercero -o analisis


## recursos para continuar aprendiendo 


https://github.com/MayankPandey01/OwnBucket

el ownbucket tiene la propiedad interesante de buscar en otras nube pero es fuerza bruta tambien tiene un bonito readme la funcion de generado de aleatoriedad esta raro 

https://github.com/mexploit30/java2s3/blob/main/java2s3.py
el java2s3 es muy level bajo sin embargo hace fuerza bruta desde archivo a rutas de s3 esto se podria mejorar asi que se puede tomar como base

https://github.com/sa7mon/S3Scanner/blob/main/README.md


https://medium.com/@cloud_tips/open-s3-buckets-examples-scanner-and-how-to-respond-522074481dc

