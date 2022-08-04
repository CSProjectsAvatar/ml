# ml

En este repositorio se encuentra todo lo relacionado con la asignatura *Aprendizaje de Máquina* de la carrera Ciencias de la Computación.

## 1er Proyecto

### Datos del proyecto

**Nombre**: Reforzando el Lenguaje
**Repositorio**: [https://github.com/CSProjectsAvatar/ml](https://github.com/CSProjectsAvatar/ml)
**Reporte**: [https://github.com/CSProjectsAvatar/ml/blob/main/README.md](https://github.com/CSProjectsAvatar/ml/blob/main/README.md)

### Breve resumen

Existe un lenguaje de consultas bien definido en grafos de conocimiento. El objetivo es traducir una consulta elaborada en lenguaje natural a una en el lenguaje formal de búsqueda en grafos. Para esto se quiere emplear un parser como parte de la solución.
Como sabemos, en el lenguaje natural existen ambigüedades, lo cual provoca conflictos en el parseo(conflictos Shift-Reduce x ej).
El problema a resolver es entrenar un modelo que indique al parser que producción aplicar en un caso de ambigüedad(Problema de Clasificación)

Hasta ahora se ha pensado en 2 enfoques de atacar el problema, el primero, como problema de clasificación supervisado, donde se usaría alguno de los clasificadores vistos en clase; el segundo, atacarlo con reforzamiento.

### Miembros del equipo

- Omar Alejandro Hernandez Ramirez (@OmarHernandez99)(@omaro43)
- Andy Ledesma Garcia (@MakeMake23)(@@andyRsdEla)
- Aylín Alvarez Santos (@Chains99)(@Chains99)

### Otras asignaturas o investigación en los que impacte el proyecto
Este proyecto formará parte de la investigación para la tesis de @OmarHernandez99, tutoreado por @apiad y el profe Sadan.

### Para Desarrolladores
En `1st-project/domain/` están los nodos del AST  y el enum del posible rol que puede tener una palabra en una BD de grafo.

En `1st-project/grammars/` se encuentra definida la gramática y se ilustra su AST en `ast-query-cypher.pdf`

En `1st-project/interfaces/` está la clase abstracta `GraphInteract` que es una API para obtener información de la BD de grafo. Se debe refactorizar ese archivo porque no debe ir en esa carpeta. Hay también una implementación de prueba en el archivo `graph.py`. Se requiere que exista una implementación verdadera en `1st-project/interfaces/` o en `1st-project/infrastruct/`.

En `1st-project/usecases/cypher_visitors.py` se encuentran los visitantes del AST: uno para generar una consulta en inglés y otro para generar ASTs. El primero corre bien pero no ha sido probado lo suficiente; mientras que el segundo todavía no corre pero la idea está implementada. En ambos se puede apreciar cómo implementar un visitante mediante el empleo del decorador `visitor` definido en `1st-project/usecases/visitor.py`.

`WordGraphClassf` (archivo `1st-project/usecases/graphrole_interact.py`) es una clase que determina el rol de una palabra en al grafo.