# -*- coding: utf-8 -*-
"""Machine learning coop PF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zPA4l5ZDEnZh0eD4815N_noAP2OPsIWS

##**Entendimiento del negocio**##

A continuación se describe de manera general el modelo de negocio de la entidad de la cual se obtuvieron los datos.

Se trata de una entidad cooperativa perteneciente al sector solidario, en este sector se agrupan organizaciones de carácter asociativo solidario sin ánimo de lucro. Para ser más especificos esta entidad se clasifica como "cooperativa especializada en ahorro y crédito" a la cual se asocian personas empleadas y pensionadas de una institución de educación superior colombiana. Como cooperativa espacializada en ahorro y crédito tiene permitido ejercer actividades financieras (captacion y colocación) exclusivamente para sus asociados.

La cooperativa posee un core o sistema de información en el cual se registra la información general de sus asociados, los movimientos en sus cuentas de aportes, de ahorros y la cartera (deudas) además de las transacciones de entrada o salida de dinero que realizan interna y externamente desde las cuentas anteriormente mencionadas. Desde este sistema de información se obtendrá la muestra de los datos a analizar sobre los cuales se aplicarán metodologías de machine learning en el presente proyecto.

##Definición del problema##

La entidad cooperativa posee una base de datos donde tiene registrada la información de sus asociados y desea mejorar su proceso de colocación de crédito automatizando la toma de decisión a la hora de asignar o no un crédito, teniendo en cuenta que requiere disminuir el riesgo de no pago por parte del asociado.

##Metas del proyecto##

Este proyecto de machine learning tiene por objetivo:

* Implementar un modelo  de machine learning que de acuerdo las características de los clientes le permita a la entidad predecir si un asociado que solicita un crédito puede llegar a incumplir los pagos.
* Determinar cuales de las caracteristicas de  un Asociado influye en las probabilidad de incumplir o cumplir con sus pagos.

##Planeación del proyecto##

El proyecto que se ejecutará seguirá el conjunto de pasos que se describe a continuación:

1. Integración de las bases de datos disponibles ajustando los posibles errores que se presenten producto de la descarga, eliminación valores faltantes y atípicos consolidando los datos en un solo dataframe.
2. Analizar la muestra obtenida luego de la integración caracterizando la muestra mediante estadistica descriptiva.
3. Realizar preprocesamiento de los datos.
4. realizar reducción de la dimensionalidad de los datos.
5. Entrena y testear distintos modelos de aprendizaje supervisado y no supervisados evaluando sus desempeños.
6. Declarar un pipeline, ponerlo a prueba y evaluar su desempeño.
"""

# Instalación de librerías para acceder y autenticarse a Google Drive
!pip install pydrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Autenticación y creación de usuario (cliente) de PyDrive
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

"""## **Preparación de los datos**

Los datos que se van a importar son 4 bases que contienen información general, información de las captaciones actuales (ahorros y certificados de ahorros) e información de la cartera de los Asociados de una cooperativa de ahorro y crédito.
"""

# Actualizamos scikit-learn a la última versión
!pip install -U scikit-learn

# Importamos scikit-learn
import sklearn

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# %matplotlib inline
# %config InlineBackend.figure_format = 'retina'
from scipy import stats
import scipy
import statsmodels.api as sm
import statsmodels.formula.api as smf
import seaborn as sns   # Librería de visualización de datos estadísticos.
import mlxtend          # Librería de utilidades de aprendizaje computacional.

# Ignoramos las advertencias o warnings.
import warnings
warnings.simplefilter(action='ignore')

#Cargue de bases
saldo_asoc = pd.read_excel('/content/drive/MyDrive/Documentos Útiles Ing. Industrial/COOPROFESORESUN/bases de datos/Base saldos asociados a la fecha.xlsx')
info_gen = pd.read_excel('/content/drive/MyDrive/Documentos Útiles Ing. Industrial/COOPROFESORESUN/bases de datos/Reporte 9003.xlsx')
captaciones = pd.read_excel('/content/drive/MyDrive/Documentos Útiles Ing. Industrial/COOPROFESORESUN/bases de datos/Captaciones202108.xlsx')
cartera = pd.read_excel('/content/drive/MyDrive/Documentos Útiles Ing. Industrial/COOPROFESORESUN/bases de datos/planocartera08.xlsx')

"""##Entendimiento de los datos/ Análisis exploratorio##
Se tienen dos bases con la información general de los Asociados que se importaron como los dataframe nombrados "saldo_asoc" e "info_gen".

La base con el registro de captaciones de la cooperativa se importó como el dataframe "captaciones".

La base con la información de la cartera de la cooperativa se importó como el dataframe "cartera".

A continuación se realizará, como parte del entendimiento de los datos, una validación de la calidad de cada base anteriormente mencionada.
"""

saldo_asoc.info();
saldo_asoc.head(40)

"""Es posible que debido a un error del sistema de información que genera las bases, el dataframe (en adelante DF) "saldo_asoc" presenta como nombre de las columnas un conjunto de caracteristicas de uno de los asociados. Al realizar una previsualización de los datos, se encuentra que lo que debería ser el nombre de las columnas esta dentro del DataFrame en la fila indexada con el número 36. A continuación se renombrarán las columnas del DF "saldo_asoc" y se eliminarán las posibles filas duplicadas con los nombres de las columnas."""

saldo_asoc.columns = saldo_asoc.iloc[36].values #renombro las columnas del DataFrame con el arreglo conformado por los valores de la fila 36 del DF "saldo_asoc"
saldo_asoc = saldo_asoc.drop_duplicates(keep = False)
saldo_asoc.info();
saldo_asoc.head()

"""A continuación se limpiará el DF "saldo_asoc" para dejar solo las variables del DF que se consideran útiles para el análisis. Estas variables nos dan un perfil de asociado."""

cols = ['Cédula','Nombre','Edad','Ciudad','Ahorros','Cdats','Aportes','Cartera','Tarjeta BBTA','Tarjeta Visionamos']
saldo_asoc = saldo_asoc[cols]
saldo_asoc

info_gen.info()

"""Del mismo modo, para el DF "info_gen" se filtrarán las variables que se consideran de utilidad para el análisis. En este caso la cédula del asociado nos servirá para unir las bases en pasos posteriores y el resto de información aporta al perfilamiento del asociado."""

cols = ['Cédula','Género','Estado_Civil','Tipo_contrato_laboral','Nivel_educativo','Tipo_vivienda','Ingresos_fijos']
info_gen = info_gen[cols]
info_gen.info()

captaciones.info();
captaciones.head()

"""Para el caso del DF "captaciones" tambien realizaremos una selección de las variables de utilidad, el nit (que cambiaremos de nombre a cédula para facilitar la unión de los DF).   """

cols = ['NIT','NombreDeposito','FechaApertura','Plazo','TasaInteresEfectiva','InteresesCausados','DepositoInicial']
captaciones = captaciones[cols]
captaciones.rename(columns={'NIT':'Cédula'}, inplace=True)
captaciones.info()

cartera.info()
cartera.head()

"""De igual manera hacemos un proceso de selección para el DF "cartera". Todas las columnas selccionadas dan un perfil de cartera del asociado.

En este caso tambien se edita la columna id. cliente por cédula para facilitar la unión de los DF
"""

cols = ['Id. Cliente','Medio de pago','Monto Solicitado','Saldo Capital','Dias Vencidos','Tasa Col.(NAMV)','Tasa Peridodo(NAMV)','Clasificacion',
        'Tipo Garantia','Vlr Garantia','Vlr Cuota','No.Cuotas','Periodicidad','Calif. Aplicada','Forma de Pago','Codeudores']
cartera = cartera[cols]
cartera.rename(columns={'Id. Cliente':'Cédula'}, inplace=True)
cartera.info()

"""A continuación se agruparán los 3 DataFrames tomando como referencia el número de cédula del asociado registrado en la muestra con el objetivo de consolidar en un solo DF utilizando el método merge()."""

consolidado1 = saldo_asoc.merge(info_gen, on ='Cédula', how='outer')
consolidado2 = consolidado1.merge(captaciones, on ='Cédula', how='outer')
con_final = consolidado2.merge(cartera, on ='Cédula', how='outer')
con_final.info()

"""En el siguiente paso se realizará una limpieza a fondo de la muestra de datos del DF "con_final". Se eliminarán los duplicados referenciando el número cédula, de manera que no quedé dentro de la muestra información del mismo asociado, solo se dejará uno de los datos duplicados. Se eliminarán las filas de la muestra que presenten datos faltantes en las columnas cédula, edad, ingresos fijos, tasa de interés de los ahorros y monto solicitado y se pasará a númerico las caracteristicas que se ven como object. Luego reiniciaremos los indices."""

con_final.drop_duplicates('Cédula', keep = 'first',inplace=True)
con_final = con_final.dropna(subset=['Cédula','Edad','Ingresos_fijos','TasaInteresEfectiva','Monto Solicitado'])

con_final[["Edad", "Ahorros","Cdats","Aportes","Cartera","TasaInteresEfectiva","DepositoInicial","Saldo Capital","Dias Vencidos",
             "Tasa Peridodo(NAMV)","Vlr Garantia","Vlr Cuota","No.Cuotas"]] = con_final[["Edad", "Ahorros","Cdats","Aportes",
                                                                                         "Cartera","TasaInteresEfectiva",
                                                                                         "DepositoInicial","Saldo Capital",
                                                                                         "Dias Vencidos","Tasa Peridodo(NAMV)",
                                                                                         "Vlr Garantia","Vlr Cuota","No.Cuotas"]].apply(pd.to_numeric)

con_final.reset_index(drop=True, inplace=True)
con_final.info();
con_final.head()

"""## Análisis descriptivo##
En las siguientes celdas se visualizarán las distribuciones de las principales caracteristicas de la base de datos.
"""

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(14,7), dpi=80)

axes[0,0].hist(con_final['Edad'], alpha=0.5, color='r')
axes[0,1].hist(con_final['Ahorros'], alpha=0.5, color='b')
axes[0,2].hist(con_final['Cdats'],alpha=0.5, color='g')
axes[1,0].hist(con_final['Aportes'],alpha=0.5, color='y')
axes[1,1].hist(con_final['Cartera'],alpha=0.5, color='m')
axes[1,2].hist(con_final['Ingresos_fijos'],alpha=0.5, color='c')

axes[0,0].set_title('Edad')
axes[0,1].set_title('Ahorros')
axes[0,2].set_title('Cdats')
axes[1,0].set_title('Aportes')
axes[1,1].set_title('Cartera')
axes[1,2].set_title('Ingresos Fijos')

axes[0,0].set_xlabel("Años")
axes[0,0].set_ylabel("Frecuencia")
axes[0,1].set_xlabel("Monto")
axes[0,1].set_ylabel("Frecuencia")
axes[0,2].set_xlabel("Monto")
axes[0,2].set_ylabel("Frecuencia")
axes[1,0].set_xlabel("Monto")
axes[1,0].set_ylabel("Frecuencia")
axes[1,1].set_xlabel("Monto")
axes[1,1].set_ylabel("Frecuencia")
axes[1,2].set_xlabel("Monto")
axes[1,2].set_ylabel("Frecuencia")
;

fig.tight_layout()

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(14,7), dpi=80)

axes[0,0].boxplot(con_final['Edad'])
axes[0,1].boxplot(con_final['Ahorros'])
axes[0,2].boxplot(con_final['Cdats'])
axes[1,0].boxplot(con_final['Aportes'])
axes[1,1].boxplot(con_final['Cartera'])
axes[1,2].boxplot(con_final['Ingresos_fijos'])

axes[0,0].set_title('Edad')
axes[0,1].set_title('Ahorros')
axes[0,2].set_title('Cdats')
axes[1,0].set_title('Aportes')
axes[1,1].set_title('Cartera')
axes[1,2].set_title('Ingresos Fijos')
;

fig.tight_layout()

np.round(con_final.describe(),2)#.astype(str)

"""Los histogramas y diagramas de caja visualizados nos permiten ver las distribuciones de la edad y características financieras de los asociados a nivel general. Los diagramas de caja nos muestran que las características financieras presentan outliers.

Al utilizar el método describe para observar la información estadistica principal de cada caracteristica númerica obtenemos datos razonables para los montos, saldos y valores, sin embargo las tasas de colocación y captación se ven afectadas por filas que tienen estas columnas en 0.

A continuación se crea un nuevo DF con_final1 filtrando los asociados que no tengan ahorros o certificados de ahorro, que no posean aportes y que no posean cartera (deudas) con la cooperativa. Esto con el fin de tener un consolidado que permita realizar análisis descriptivo sobre caracteristicas importantes como las tasas de interés de ahorro y de colocación.
"""

con_final1 = con_final[(con_final['Ahorros']>0) & (con_final['Cdats']>0) & (con_final['Aportes']>0) & (con_final['Cartera']>0)]
con_final1.reset_index(drop=True, inplace=True)
con_final1.info();
np.round(con_final1.describe(),2)#.astype(str)

"""## Preprocesamiento##
Como primer paso del preprocesamiento se pasarán los datos a formato X, y, luego se identificarán las variables númericas y categóricas pasandolas a arreglos numpy. Antes se eliminarán las características "Cédula", "Nombre" y "FechaApertura" pues son identificadores.
"""

confin_full = con_final.drop(['Cédula','Nombre','Plazo','FechaApertura'],  axis=1) #se eliminan identificadores

X = confin_full.drop(['Calif. Aplicada'], axis=1)#se separan los datos X de la variable objetivo "Calif. Aplicada"
y = confin_full['Calif. Aplicada']#colmna de la variable objetivo

print(X.shape)
print(y.shape)

"""La variable objetivo del conjunto de datos posee tres clases, estas son las calificaciones de riesgo que le fue asignado al asociado de acuerdo a los pagos que ha realizado, estas calificaciones son
* A: Riesgo bajo
* B: Riesgo medio
* C: Riesgo medio-alto
* D: Riesgo alto
* E: Riesgo muy alto

A continuación se convertiran estas variables a números de acuerdo a la siguiente calificación
* 0 = A
* 1 = B
* 2 = C
* 3 = D
* 4 = E
"""

y = y.replace(['A', 'B', 'C', 'D', 'E'],[0, 1, 2, 3, 4])#reemplazamos las clases del variable objetivo a númericos
# .values retorna un arreglo de NumPy.
y = y.values
y

"""De acuerdo a lo anterior se puede validar que en la variable objetivo realmente tenemos muy pocos ejemplos de todas las clases posibles, esto puede ser problematico a la hora de entrenar y testear los modelos por ello, a continuación, llamaremos una nueva base donde tenemos Asociados con otras calificaciones además de la A y filtraremos las calificaciones B,C,D,E y rellenaremos los valores nulos con fillna y su metodo "bfill". Por último, concatenaremos este nuevo DF con el DF "confin_full"."""

cartera2 = pd.read_excel('/content/drive/MyDrive/Documentos Útiles Ing. Industrial/COOPROFESORESUN/bases de datos/cartera2.xlsx')
carte = cartera2[cols]
carte.rename(columns={'Id. Cliente':'Cédula'}, inplace=True)

new_cart = consolidado2.merge(carte, on ='Cédula', how='outer')
new_cart.drop_duplicates('Cédula', keep = 'last',inplace=True)
new_cart = new_cart[(new_cart['Calif. Aplicada']== 'B') | (new_cart['Calif. Aplicada']== 'C') | (new_cart['Calif. Aplicada']== 'D') | (new_cart['Calif. Aplicada']== 'E')]
new_full = new_cart.drop(['Cédula','Nombre','Plazo','FechaApertura'],  axis=1)

new_full = new_full.fillna(method="bfill")# llena los valores nulos con el ultimo valor valido

new_full = pd.concat([confin_full,new_full])
new_full.reset_index(drop=True, inplace=True)#reinicia los index del DF
new_full.info()

"""Nuevamente se covierte el DF a formato "X,y" ajustando."""

X = new_full.drop(['Calif. Aplicada'], axis=1)#se separan los datos X de la variable objetivo "Calif. Aplicada"
y = new_full['Calif. Aplicada']#columna de la variable objetivo

"""De la variable objetivo "y" se generarán dos sets para realizar pruebas en dos tipos de modelos, uno para un modelo de regresión logistica (binario) que se nombrará "y_bin" y otro para un modelo de clasificación multiclase "y_multi"."""

y_multi = y.replace(['A', 'B', 'C', 'D', 'E'],[0, 1, 2, 3, 4])
y_multi = y_multi.values
y_multi

"""la variable objetivo binaria "y_bin" se construye bajo la suposición de que un Asociado que paga al día siempre tendra clasificación A, pero si incurre en mora cambiará su calificación a B,C,D,E. Es decir, ahora tenemos dos clases "cumplidos" y "no cumplidos"."""

y_bin = y.replace(['A', 'B', 'C', 'D', 'E'],[0, 1, 1, 1, 1])
y_bin = y_bin.values
y_bin

"""Se dividen los datos X en númericos y categoricos para alistar el preprocesamiento con la librería "preprocesing" de scikitlearn conviritiendolos en arreglos con .values para facilitar la lectura."""

num = ['Edad', 'Ahorros', 'Cdats', 'Aportes','Cartera','Ingresos_fijos','TasaInteresEfectiva','InteresesCausados',
       'DepositoInicial','Monto Solicitado','Saldo Capital','Dias Vencidos','Tasa Col.(NAMV)','Tasa Peridodo(NAMV)',
       'Vlr Garantia','Vlr Cuota','No.Cuotas']

X_num = X[num].values

print(X_num.shape)
print(type(X_num))

X_cat = X.drop(num, axis=1)
X_cat.nunique()

"""No se tendrán en cuenta las características "ciudad" y "codeudores" por tener gran cantidad de clases."""

X_cat = X_cat.drop(['Ciudad','Codeudores'], axis=1).values
print(X_cat.shape)
print(type(X_cat))

"""En la siguiente celda se aplicará la transformación para las caracteristicas númericas."""

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))  # Declaramos el Transformer "StandardScaler"
X_num_minmax = scaler.fit_transform(X_num) # Transformamos la matriz "X_numeric"

"""En la siguiente celda se aplicará la transformación a las características categoricas"""

from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder(sparse=False)     # Declaramos el Transformer "OneHotEncoder".
X_cat_onehot = enc.fit_transform(X_cat) # Usamos "fit_transform" para obtener la matriz transformada.
print(X_cat_onehot.shape)
print(type(X_cat_onehot))

"""Ahora se unen los datos numéricos y los categoricos en un solo set de datos."""

X_full = np.concatenate((X_num_minmax, X_cat_onehot), axis=1) # Concatenamos por el eje vertical (columnas)
print(X_full.shape)

"""##Partición de entrenamiento y prueba##"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train_bin, y_test_bin = train_test_split(X_full,
                                                                        y_bin,#
                                                                        test_size=0.3,
                                                                        random_state=42)

"""## Aprendizaje supervisado: Regresión logistica##
Se importan las librerias para entrenar y testear un **modelo de regresión logística** utilizando el set de datos preprocesado sin redimensionar, con el objetivo de evaluar el desempeño del modelo .
"""

from sklearn import linear_model

clf_full = linear_model.LogisticRegression()
clf_full.fit(X_train, y_train_bin)

y_pred = clf_full.predict(X_test)

from sklearn import metrics

print(f'Precisión: {metrics.precision_score(y_test_bin, y_pred, pos_label=0)}')
print(f'Recall:    {metrics.recall_score(y_test_bin, y_pred, pos_label=0)}')
print(f'F_1 score: {metrics.f1_score(y_test_bin, y_pred, pos_label=0)}')

"""En las celdas anteriores entrenamos y testeamos un modelo de regresión logística, este modelo de clasificación binaria se entrenó con la variable objetivo preprocesada pasando sus 4 (A,B, C, D, E) clases a **clase binaria** -cumplido (0) o no cumplido(1)-. Los resultados de las métricas de evaluación precisión 93,8%, recall 98,2% y f1 96% muestran un muy buen desempeño.

## Reducción de la dimensionalidad##

A continuación realizaremos reducción de la dimensionalidad en el set de datos para:
* Probar el desempeño del modelo regresión logística con sus dimensiones reducidas.
* Aplicar en los modelos supervisados y no supervisados.
"""

from sklearn.decomposition import PCA

def cumulative_explained_variance_plot(expl_variance):

  cum_var_exp = np.cumsum(expl_variance)

  plt.figure(dpi = 100, figsize = (8, 6))
  plt.title('Curva acumulativa de la varianza explicada VS n° de componentes principales',
            fontdict= dict(family ='serif', size = 16))
  plt.xlabel('Número de componentes principales',
             fontdict= dict(family ='serif', size = 14))
  plt.ylabel('Varianza explicada acumulativa',
             fontdict= dict(family ='serif', size = 14))

  nc = np.arange(1, expl_variance.shape[0] + 1)

  plt.plot(nc, cum_var_exp, '--r')
  plt.plot(nc, cum_var_exp, 'c*', ms = 5)
  plt.show()

#Aplicación de la reducción
pca = PCA(n_components=None)
pca.fit_transform(X_full)
varianza_expl = pca.explained_variance_ratio_

cum_var_exp = np.cumsum(varianza_expl)

cumulative_explained_variance_plot(varianza_expl)

print(f'Primeras 2 componentes: {cum_var_exp[2]}')
print(f'Primeras 5 componentes: {cum_var_exp[5]}')
print(f'Primeras 8 componentes: {cum_var_exp[8]}')

"""La varianza explicada para 2, 5 y 8 componentes presentan al menos el 30% de la variabilidad, se toma la desición de reducir a 2 componentes. haciendo partición de entrenamiento y prueba al set reducido "X_full_trans"."""

# Función para visualizar un conjunto de datos en 2D

def plot_data(X, y):
    y_unique = np.unique(y)
    colors = plt.cm.rainbow(np.linspace(0.0, 1.0, y_unique.size))
    for this_y, color in zip(y_unique, colors):
        this_X = X[y == this_y]
        plt.scatter(this_X[:, 0], this_X[:, 1],  color=color,
                    alpha=0.5, edgecolor='k',
                    label="Class %s" % this_y)
    plt.legend(loc="best")


pca = PCA(n_components=2)
X_full_trans = pca.fit_transform(X_full)#obtenemos el set reducido

plt.figure(figsize = (10, 8), dpi = 105)
plt.xlabel('Componente principal 1')
plt.ylabel('Componente principal 2')
plt.title('Vectores singulares más significativos después de la transformación lineal a través de PCA')

plot_data(X_full_trans, y_bin)

plt.figure(figsize = (10, 8), dpi = 105)
plt.xlabel('Componente principal 1')
plt.ylabel('Componente principal 2')
plt.title('Vectores singulares más significativos después de la transformación lineal a través de PCA')
plot_data(X_full_trans, y_multi)

"""## Partición de entrenamiento y prueba del set reducido##"""

X_train_t, X_test_t, y_train_bin, y_test_bin = train_test_split(X_full_trans, #Se aplica la partición sobre el set reducido
                                                                        y_bin,# y sobre la variable objetivo binaria para probar modelo regresión logística
                                                                        test_size=0.3,
                                                                        random_state=42)

clf_full = linear_model.LogisticRegression()
clf_full.fit(X_train_t, y_train_bin)

y_pred_t = clf_full.predict(X_test_t)

print(f'Precisión: {metrics.precision_score(y_test_bin, y_pred_t, pos_label=0)}')
print(f'Recall:    {metrics.recall_score(y_test_bin, y_pred_t, pos_label=0)}')
print(f'F_1 score: {metrics.f1_score(y_test_bin, y_pred_t, pos_label=0)}')

"""Vemos una mejora en el recall, sin embargo la precisión baja lo que afecta también a la baja el f1. Para los datos disponibles en este ejercicio vemos que el modelo de regresión logística se desempeña mejor con las caracteristicas sin reducir.

##Aprendizaje supervisado: arboles de decisión.##
A continuación se entrenará un modelo de clasificación no lineal, especificamente un árbol de desición. Para este modelo utilizaremos la variable objetivo multiclase preprocesada (A, B, C, D, E pasó a 0, 1, 2, 3, 4).
"""

X_train, X_test, y_train_mult, y_test_mult = train_test_split(X_full, #partición sobre los datos sin reducir
                                                                        y_multi,# partición sobre var objetivo multiclase
                                                                        test_size=0.3,
                                                                        random_state=42)

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

# Números enteros de 1 a 20 como posibles valores del hiperparámetro de profundidad.
max_depth_values = np.arange(1, 21, 1)

# Arreglos vacíos para almacenar el error de entrenamiento y el de generalización.
train_error = np.empty(len(max_depth_values))
generalization_error = np.empty(len(max_depth_values))


for depth in max_depth_values:
    # Entrenamos un árbol de decisión para cada valor de profundidad.
    decision_tree = DecisionTreeClassifier(max_depth=depth)
    decision_tree.fit(X_train, y_train_mult)

    # Almacenamos el error de entrenamiento y de generalización por cada árbol.
    train_error[depth - 1] = (1 - decision_tree.score(X_train, y_train_mult))
    generalization_error[depth - 1] = (1 - decision_tree.score(X_test, y_test_mult))

def plot_learning_curve(train_error, generalization_error):
  n = len(train_error)
  if len(train_error) != len(generalization_error):
    print("Las secuencias de error de entrenamiento y generalización deben tener el mismo tamaño.")
    return

  balance_point = np.array(generalization_error).argmin() + 1
  plt.figure(figsize = (8, 5), dpi = 105)

  plt.plot(range(1, n + 1), train_error, label="Entrenamiento")
  plt.plot(range(1, n + 1), generalization_error, label="Generalización")
  plt.xticks(range(0, n + 1, 2))
  plt.xlabel("Profundidad máxima")
  plt.ylabel("Error")
  y_min, y_max = plt.gca().get_ylim()
  plt.vlines(balance_point, y_min, y_max, colors = ['red'], linestyles = ['dashdot'])
  plt.ylim([y_min, y_max])
  plt.text(balance_point + 1, 0.01, 'Punto de balance')
  plt.legend();


plot_learning_curve(train_error, generalization_error)

param_grid = {
    "max_depth": range(2, 20, 2),     # Profundidad máxima del árbol de decisión.
    "criterion": ["gini", "entropy"], # Criterio de partición del árbol.
  }

arb_clf =  DecisionTreeClassifier()#declaro el modelo de árbol

#declaro y entreno el gridsearch
gsearch = GridSearchCV(arb_clf, param_grid=param_grid, cv=3, return_train_score=True)
gsearch = gsearch.fit(X_train, y_train_mult)

if gsearch is not None:
  print(f'Mejores hiperparámetros:\n {gsearch.best_params_}')
  print(f'Mejor exactitud (validación): {gsearch.best_score_:.6f}')
else: print('El valor retornado no es un clasificador GridSearchCV válido.')

arb_clf =  DecisionTreeClassifier(max_depth=4, criterion="gini")
arb_clf = arb_clf.fit(X_full, y_multi)

print(f'Error: {1 - arb_clf.score(X_train, y_train_mult)}')

"""Para el caso en estudio podemos validar que el modelo de arboles de decisión presenta un sobreajuste, efectivamente esta es una de las desventajas de aplicar este tipo de modelo de clasificación no lineal, la razón de este sobreajustes es una posible memorización del conjunto de datos, sin embargo aplicaremos una de sus funciones para encontrar las variables que son más importantes en el conjunto de datos. Acontinuación se presentan estas importancias."""

arb_clf.feature_importances_

"""La caracteristica o variable que tiene la mayor importancia es **"días vencidos"**, estos son los días que han transcurrido despues de la fecha máxima de pago de la cuota del crédito. seguido por la forma de pago **"ventanilla"** o **"nómina"**, es decir cuando los Asociados se acercan a las oficinas a pagar su cuota o se hace descuento de nómina.

## Aprendizaje no supervisado: Agrupamiento K-means##

Con el objetivo de cumplir con uno de los oibjetivos del proyecto que se propone encontrar un agrupamiento de los clientes, de acuerdo a sus características, que le permita a la entidad alcanzar un conocimiento del mercado para ofrecer de manera efectiva los productos y servicios. Se desarrollará el siguiente modelo.
"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

inertia = []
silhouette = []
K = range(2, 15)
for i in K:
  # Declaramos y ejecutamos el algoritmo K-means.
  model = KMeans(n_clusters=i)
  model.fit(X_full_trans)

  # Predecimos las etiquetas de X_preprocessed.
  y_predk = model.predict(X_full_trans)

  # Almacenamos la métrica de inercia y el coeficiente de silueta.
  inertia.append(model.inertia_)
  silhouette.append(silhouette_score(X_full_trans, y_predk))

"""##Evaluación interna##"""

def plot_metric(K, scores, metric_name):
  plt.figure(dpi=110, figsize=(9, 5))
  plt.plot(K, scores, 'bx-')
  plt.xticks(K); plt.xlabel('$k$', fontdict=dict(family = 'serif', size = 14));  plt.ylabel(metric_name, fontdict=dict(family = 'serif', size = 14));
  plt.title(f'K vs {metric_name}', fontdict=dict(family = 'serif', size = 18))
  plt.show()

plot_metric(K, inertia, 'Inercia')
plot_metric(K, silhouette, 'Coeficiente de silueta')

"""Los resultados obtenidos para la inercia y coeficiente de silueta son confusos, si bien la inercia nos indica que los clusters deben ser entre 4 y 5, el coeficiente de siluetanos indica un 14, . A continuación se presentan los resultados de la evaluación externa para dar mayor claridad.

##Evaluación externa##
"""

from sklearn.metrics import homogeneity_score

def plot_extern_metric(X, y, metric, metric_name):
  scores = []
  for i in range(2,20):
    model = KMeans(n_clusters=i, random_state=32)
    model.fit(X)
    y_pred = model.predict(X)
    scores.append(metric(y, y_pred))

  plot_metric(range(2, 20), scores, metric_name)

plot_extern_metric(X_full_trans, y_bin, homogeneity_score, 'Homogeneidad')

from sklearn.metrics import mutual_info_score

plot_extern_metric(X_full_trans, y_bin, mutual_info_score, 'Información mutua')

from sklearn.metrics import adjusted_rand_score

plot_extern_metric(X_full_trans, y_bin,
            adjusted_rand_score, 'Índice de Rand ajustado')

"""El resultado del índice de rand nos da que los clusters deben ser 5. Teniendo en cuenta que con el indice de rand comparamos frente a los niveles de riesgo "y_bin" esta es una buena evaluación por la cual guiarnos."""

from sklearn.metrics.cluster import contingency_matrix

def show_contigency_matrix(X, y, n_clusters, classes):
  # Fijamos la semilla aleatoria para obtener resultados reproducibles.
  model = KMeans(n_clusters, random_state=32)
  model.fit(X)
  y_pred = model.predict(X)
  mat = contingency_matrix(y, y_pred)
  columns = ['Cluster ' + str(i) for i in range(n_clusters)]

  # Se retorna cómo un DataFrame de Pandas para mejorar la visualización.
  return pd.DataFrame(mat, columns=columns, index=classes)

from sklearn.metrics import silhouette_score

def plot_cluster_predictions(clustering, X, n_clusters = None, cmap = 'tab10',
                             plot_data=True, plot_centers=True, show_metric=None,
                             title_str="", ax = None):

    assert not hasattr(clustering, "n_clusters") or \
           (hasattr(clustering, "n_clusters") and n_clusters is not None), "must specify `n_clusters` for "+str(clustering)

    if n_clusters is not None:
        clustering.n_clusters = n_clusters

    y = clustering.fit_predict(X)
    # remove elements tagged as noise (cluster nb<0)
    X = X[y>=0]
    y = y[y>=0]

    if n_clusters is None:
        n_clusters = len(np.unique(y))

    if ax is None:
        ax = plt.gca()

    if plot_data:
        sns.scatterplot(X[:,0], X[:,1], hue = y, palette=cmap,
                        legend = False, alpha=.5 ,ax = ax, s = 40)

    if plot_centers and hasattr(clustering, "cluster_centers_"):
        sns.scatterplot(clustering.cluster_centers_[:,0],
                    clustering.cluster_centers_[:,1], hue = np.unique(y), s=180,  lw=3,
                    palette=cmap,
                    edgecolor="black", legend = False, ax = ax)

    if show_metric is not None:
        if show_metric == 'inercia' and hasattr(clustering, 'inertia_'):
          inertia = clustering.inertia_
          ax.set_title("Inercia = {:.0f}".format(inertia)+ title_str, fontdict=dict(family = 'serif', size = 20))
        elif show_metric == 'silueta':
          sc = silhouette_score(X, y) if len(np.unique(y)) > 1 else 0
          ax.set_title("Coeficiente de silueta = {:.3f}".format(sc)+ title_str, fontdict=dict(family = 'serif', size = 20))
    else:
        ax.set_title("k={}".format(n_clusters) +title_str, fontdict=dict(family = 'serif', size = 20))

    plt.axis("off")

    return

plot_cluster_predictions(KMeans(), X_full_trans, n_clusters=5, cmap='plasma', show_metric='silueta')

show_contigency_matrix(X_full_trans, y_bin, 5,['Cumplido','No cumplido'])

"""##Declaración de pipelines##

A continuación se realizará declaración de un pipeline que realizará los procesos de reducción de la dimensionalidad y aplicación de un modelo modelo de maquinas de vectores de soporte. Este pipeline se entrenará con un gridsearch con el objetivo de que nos devuelva los mejores hiperparametros.
"""

from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

parameters = {
    'pca__n_components': [2, 3, 5, 10],
    'svc__kernel': ['rbf', 'sigmoid']
}

pipeline = Pipeline([
                       ('pca', PCA(random_state=43)),
                       ('svc', SVC(random_state=43)),
                       ])

gsearch1 = GridSearchCV(pipeline,
                         parameters,
                         cv=3)
gsearch = gsearch1.fit(X_train, y_train_bin)

if gsearch is not None:
  print(f'Mejores hiperparámetros:\n {gsearch.best_params_}')
  print(f'Mejor exactitud (validación): {gsearch.best_score_:.6f}')
else: print('El valor retornado no es un clasificador GridSearchCV válido.')

"""##Prueba del pipeline##
Se pondrá a prueba el pipeline construido con sus mejores hiperparametros hallados y se evaluarán sus métricas para determinar el error de entrenamiento y el error de prueba que poseee.
"""

parameters = {
    'pca__n_components': [2],
    'svc__kernel': ['rbf']
}

pipeline = Pipeline([
                       ('pca', PCA(random_state=43)),
                       ('svc', SVC(random_state=43)),
                       ])

pipeline.fit(X_train, y_train_bin)

ypipe = pipeline.predict(X_test)
ypipe

print(f"Error en entrenamiento:\t{1-pipeline.score(X_train, y_train_bin):.4f}")
print(f"Error en prueba:\t{1-pipeline.score(X_test, y_test_bin):.4f}")

from sklearn.metrics import classification_report

reporte = classification_report(y_test_bin, ypipe, digits=4)
print(reporte)

"""## Conclusiones##

1. En el presente ejercicio se buscó encontrar un modelo machine learning ya sea supervisado o no supervisado que predijera el cumplimiento o imcumplimiento de pago de crédito de un Asociado, se probaron los desempeños de los modelos.

* regresión logistica
* arbol de decisión
* K-means
* maquina de vectores de soporte

Dos modelos tuvieron muy buen desempeño a la hora de predecir la variable objetivo, estos fueron el modelo de regresión logistica y el modelo maquina de vectores de soporte que se declaró dentro de un pipeline. Al final por practicidad se elige el modelo de regresión logistica.

2. las caracteristicas del set de datos que más influyen en el resultado de la variable objetivo son.
* **"días vencidos"**, estos son los días que han transcurrido despues de la fecha máxima de pago de la cuota del crédito.
* la **"forma de pago"**  es decir si los Asociados se acercan a las oficinas a pagar su cuota o se hace descuento de nómina.

Lo anterior se concluye gracias a los resultados obtenidos en el modelo de arboles de decisión.
"""

