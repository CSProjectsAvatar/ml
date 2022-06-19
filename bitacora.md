

## La Data
Nos hacia falta generar data, y para eso en algun momento se nos ocurrio usar Esta cosa de Rivales, pero estaba muy turbia
Tonces nos quedamos con la idea de generar AST validos aleatorios, ayudandonos de un Oraculo que sabe cosas de la BD en cuestion

## El Modelo
El modelo lo pensamos hacer supervisado como primer acercamiento. La Idea es modelar la query con los features que nos de el Oraculo,
al estilo si la query es: "Peliculas en las que trabajo Tom Hanks' --> (Tipo_de_Entidad, stopWords..., Relacion, Valor_de_Atributo_Name).
Una idea que nos aconsejaron los profes fue ayudarse del DAG que provee spacy al analizar una oracion, y darle al modelo ese DAG tambien.
De forma que lo ayude a hacer el AST.

Recordemos que queremos que dado la query, el modelo nos de un AST. Una interrogante que estamos en proceso de resolver es como modelamos el AST que queremos como salida, como un problema supervisado, de clasificacion probablemente.

Lo primero que se nos ocurrio fue asignarle un numero a cada nodo, en la representacion arborea que tiene nuestra gramatica, ya definida, y que lo que devuelva el modelo sea un vector con los numeros que correspoden a cada palabra. Eso como primer aproach no esta mal pero presenta varios problemas.
Uno de ellos es que hay estructuras en el arbol que se pueden repetir, del tipo:
(nodo) -> [Relacion] -> (nodo) <- [Relacion] -> (nodo)

Otro problema es que no creemos que el modelo logre "entender" esa representacion bien, ya que no estan claros conceptos como el de profundidad.

Otra idea que nos surgio fue representar el arbol como algo relacionado con parentesis anidados, que representa mejor conceptos como la profundidad, y las relaciones padre-hijo en un arbol, esta idea esta en proceso todavia.

Ahora en proceso de hacer el modelo, buscamos como coger toda la informacion que provee spacy. Vamos a tener en cuenta primeramente el atributo `pos` de los tokens, que viene con clasificaciones como: 'ADJ', 'ADV', 'CONJ', etc.
Creemos que esa es informacion util, luego valoraremos la necesidad de agregar la informacion referente al grafo de dependencias.

Una idea para usar el arbol de dependencias que da spacy, es darle al modelo la lista de los ancestros de cada palabra en el arbol, asi se le da informacion de relacion directa, indirecta y profundidad a la vez.

Lo que hicimos ahora fue agregarle a cada palabra la lista de tags que me da spacy, lemma, posicion en la oracion, etc., e hicimos un analisis de entidades y sustituimos los grupos de palabras que representan entidades por un span con estas. 

A esto pensamos agregarle la informacion recibida por el Oraculo y darselo al modelo. Un ej del input hasta ahora:

Dado una query: 'Actors who have acted in the movies directed by Christopher Nolan'
La data que estariamos dandole al modelo seria:

Texto, Lexema, Parte Or., Depnd, Alpha?, StopW?
['Actors', 'actor', 'NOUN', 'NNS', 'ROOT', True, False]
['who', 'who', 'PRON', 'WP', 'nsubj', True, True]
['have', 'have', 'AUX', 'VBP', 'aux', True, True]
['acted', 'act', 'VERB', 'VBN', 'relcl', True, False]
['in', 'in', 'ADP', 'IN', 'prep', True, True]
['the', 'the', 'DET', 'DT', 'det', True, True]
['movies', 'movie', 'NOUN', 'NNS', 'pobj', True, False]
['directed', 'direct', 'VERB', 'VBN', 'acl', True, False]
['by', 'by', 'ADP', 'IN', 'agent', True, True]
['Christopher Nolan', 'ENTITY', 'PERSON']

Estamos pensando si removerle las ultimas 2 columnas, ya que que una palabra sea alphanumerica no parece ser de mucha informacion.