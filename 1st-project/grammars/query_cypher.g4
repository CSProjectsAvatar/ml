
grammar query_cypher;

oC_Cypher : oC_SingleQuery;

oC_SingleQuery : oC_ReadingClause oC_Return;

oC_ReadingClause : oC_Match
                // | oC_Unwind
                ;

oC_Match :  (OPTIONAL)? MATCH oC_Pattern ( oC_Where )? ;

oC_Pattern :  oC_NodePattern (oC_RelationshipPattern  oC_NodePattern)*;

oC_NodePattern
           : '(' ( oC_Variable  )? ( oC_NodeLabels  )? ( oC_Properties  )? ')';

oC_RelationshipPattern
                   :  ( oC_LeftArrowHead  oC_Dash  oC_RelationshipDetail?  oC_Dash  oC_RightArrowHead ) // <-[]->
                       | ( oC_LeftArrowHead  oC_Dash  oC_RelationshipDetail?  oC_Dash ) // <-[]-
                       | ( oC_Dash  oC_RelationshipDetail?  oC_Dash  oC_RightArrowHead ) // -[]->
                       | ( oC_Dash  oC_RelationshipDetail?  oC_Dash ) // -[]-
                       ;

oC_RelationshipDetail
                  :  '['  ( oC_Variable  )? ( oC_RelationshipTypes  )? ( oC_Properties  )? ']' ;


oC_Return :  RETURN oC_ProjectionBody ;

oC_ProjectionBody
              :  (  DISTINCT )?  oC_ProjectionItems (  oC_Order )? ( oC_Skip )? (  oC_Limit )? ;

oC_Order :  ORDER  BY ORDER;

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

atom:
    NUMBER |
    STRING |
    ID '.' ID // attribute accessor
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