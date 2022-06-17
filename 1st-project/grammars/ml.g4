grammar ml;

// parser rules

query: 
    'select' ATTR (',' ATTR)* 
    'from' RELATION (',' RELATION)*
    'where' condition
    ;

condition: 
    conj ('or' conj)*
    ;

conj: 
    conj 'and' conj
    | ATTR 'in' '(' query ')'  
    | ATTR '=' ATTR
    | ATTR 'like' PATTERN
    ;

// lexer rules

PATTERN: 'foo'; // @todo 

RELATION : 'foo'; // @todo 

ATTR : 'foo'; // @todo 
