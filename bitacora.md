

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