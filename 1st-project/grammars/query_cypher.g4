
grammar query_cypher;

oC_Cypher : oC_SingleQuery;

oC_SingleQuery : oC_ReadingClause oC_Return;

oC_ReadingClause : oC_Match
                // | oC_Unwind
                ;

oC_Match :  (OPTIONAL)? MATCH oC_Pattern ( oC_Where )? ;

oC_Pattern :  oC_NodePattern (oC_RelationshipPattern  oC_NodePattern)*;

oC_NodePattern
           : '('  ID? ( oC_NodeLabels  )? ( oC_Properties  )? ')'; // (p:Person {name:'John', age:30})

oC_NodeLabels
    : (':' ID)+
    ;

oC_Properties
    : '{' key_value ( ',' key_value )* '}'
    ;

key_value
    : ID ':' literal
    ;

oC_RelationshipPattern
                   :  ( oC_LeftArrowHead  oC_Dash  oC_RelationshipDetail?  oC_Dash  oC_RightArrowHead ) // <-[]->
                       | ( oC_LeftArrowHead  oC_Dash  oC_RelationshipDetail?  oC_Dash ) // <-[]-
                       | ( oC_Dash  oC_RelationshipDetail?  oC_Dash  oC_RightArrowHead ) // -[]->
                       | ( oC_Dash  oC_RelationshipDetail?  oC_Dash ) // -[]-
                       ;

oC_RelationshipDetail
                  :  '['  ID? ( oC_RelationshipTypes  )? ( oC_Properties  )? ']' ; // [r:Eats|Plays|Enjoys {type: 'fun'}]

oC_RelationshipTypes
    : ':' ID ('|' ':'? ID)*
    ;

oC_Return :  RETURN oC_ProjectionBody ;

oC_ProjectionBody
              :  (  DISTINCT )?  oC_ProjectionItems (  oC_Order )? ( oC_Skip )? (  oC_Limit )? ;

oC_ProjectionItems
    : projection ( ',' projection )*
    ;

projection
    : ID
    | attr
    ;

oC_Order :  ORDER BY attr ( 'ASCENDING' | 'ASC' | 'DESCENDING' | 'DESC' )? ;

oC_Skip :  L_SKIP  oC_Expression ;
oC_Where :  WHERE  oC_Expression ;

oC_Limit :  LIMIT  NUMBER ;

oC_Expression: 
    condition
    ;

condition: 
    conj ('OR' conj)*
    ;

conj: 
    cmp ('AND' cmp)* |
    ;

cmp: 
    atom (('<'|'>')'='? | '=') atom | // <, >, <=, >= or =
    ;

atom
    : literal
    | attr
    ;

attr
    : ID '.' ID // attribute accessor
    ;

literal
    : NUMBER
    | STRING
    ;

// lexer rules

NUMBER: [0-9]+('.'[0-9]+)? ;
STRING: '\'' ~[']* '\'' ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
RETURN : 'RETURN'; 
DISTINCT : 'DISTINCT';
// oC_ProjectionItems :  'ITEMS';
AS : 'AS';
ORDER : 'ORDER';
BY : 'BY';
L_SKIP : 'SKIP';
OPTIONAL : 'OPTIONAL' ;
MATCH : 'MATCH' ;
LIMIT : 'LIMIT';
WHERE : 'WHERE';
// oC_NodeLabels : 'Node Labels'; 
// oC_Variable : 'Var';
// oC_RelationshipTypes : 'Rel Types'; 
// oC_Properties :  'Properties';
// oC_LeftArrowHead :  '<';
// oC_RightArrowHead :  '>';
// oC_Dash:  '-';
WHITESPACE: ' ' -> skip ; 