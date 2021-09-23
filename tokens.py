DIGITS = r"\.*\d+\.*"
CHARACTERS = r'[\u200d\u200b\u0D80-\u0DFFa-zA-Z0-9_]+'

Tokens = {
	
	"INT":'INT',
	"FLOAT": 'FLOAT',
	"PLUS": 'PLUS : "+"',
	"MINUS": 'MINUS : "-"',
	"MUL": 'MUL : "*"',
	"DIV": 'DIV : "/"',
	"LPAREN": 'LPAREN : "("',
	"RPAREN": 'RPAREN : ")"',
	"EOF": "EOF",
	"ID": "IDENTIFIER",
	"KEYWORD": "KEYWORD",
	"POWER": "POWER : '^'",
	"EQ": "EQ : '='",
	"COMMA": "COMMA : ','",
	"EQEQ": "EQEQ : '=='",
	"NOTEQ": "NOTEQ : '!='",
	"LESSTHAN": "LESSTHAN : '<'",
	"GREATERTHAN": "GREATERTHAN : '>'",
	"LTEQ": "LTEQ : '<='",
	"GTEQ": "GTEQ : '>='",
	"NEWLINE":"NEWLINE",
	"ARROW": "ARROW : ->",
	"STRING": "STRING",
	"LSQUARE": "LSQUARE : '['",
	"RSQUARE": "RSQUARE : ']'",
	"PLUSEQ": "PLUSEQ: '+='",
	"MINUSEQ": "MINUSEQ: '-='"

	}

KEYWORDS = [

#English
  'var',
  'and',
  'or',
  'not',
  'if',
  'elseif',
  'else',
  'for',
  'to',
  'step',
  'while',
  'function',
  'then',
  'end',
  'return',
  'continue',
  'break',
  'do',

#Sinhala
  'විචල්ය', # variable
  'විචල්‍ය​',
  'සහ', # and
  'හෝ', # or
  'නොමැත', # not
  'නොව', # not
  'නැත', # not
  'නොවේ', # not
  'නොවන​', # not
  'ශ්‍රීතය', #function
  'කාර්යය', # function
  'නම්', #like-if
  'නැත්නම්', #like-else
  'නැතිනම්',#like-else
  'මෙහි', # start of case
  "එසේ_නැත්නම්", #like-elseif
  "එසේ_නැතිනම්",#like-elseif
  "එසේත්_නැත්නම්",#like-elseif
  "එසේත්_නැතිනම්",#like-elseif
  "අවසන්", #end
  "දක්වා", # |
  "පියවර",# දක්වා පියවර for i=0 to 10 step -2 then (it's like the step)
  "තෙක්", # like-then but for (for-loop)
  "සිට​", #like to
  "අතර​",# while
  "අතරතුර​", # while
  "නවත්වන්න", # break
  "දෙන්න", #return
  "දිගටම",
  "කරන්න",
]

BuiltIns = {
	"null":['ශුන්‍යයි'],
	"false":['බොරු'],
	"true":['සැබෑ'],
	"math_pi":['ගණිතය_pi'],
	"write":['ලියන්න'],
	#"preturn": [''],
	"input":['ආදානය'],
	"int_input":['සංඛ්‍යා_ආදානය'],
	"clear":['පැහැදිලිව'],
	"is_num":['අංකයක්_ද'],
	"is_str":['අක්ෂර_ද'],
	"is_list":['ලැයිස්තුවක්_ද'], 
	"is_function":['ශ්‍රිතයක්_ද'],
	"append":['අගට​_එකතු_කරන්න'],
	"pop":['පොප්'], 
	"extend":['දිගු_කරන්න'],
	"len":['දිග'], 
	"run":['ක්‍රියාත්මක_කරන්න'],
  "select": ['ලැයිස්තුවෙන්_තෝරන්න']

}

#CHARACTERS = r'[\u0000-\uFFFFa-zA-Z0-9_]+'

#u200d & u200b are zero-width space