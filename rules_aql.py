#text="code to search" AND filename="File name" AND dirname="directory name" OR age="date" AND source="google drive" OR author="Jason" AND size="<10M and >10G"
import parsley
followed_by = []
request_dictionary = []
def add(oper):
    global followed_by
    followed_by.append(oper)
def add_2(column,value):
    global request_dictionary
    dict1 = {'column':column,'value':value}
    request_dictionary.append(dict1)
def aql_parser(decoded_aql):
    global followed_by,request_dictionary
    followed_by = []
    request_dictionary = []
    rules = '''
    space = ' '+
    q = '"'
    words = words_1 space words
    words = words_1
    words_1 = words_2 "_" words_1
    words_1 = words_2
    words_2 = "_"* letterOrDigit+ mistake{0,1}
    words_2 = operator letterOrDigit+
    mistake = '~' digit+
    value = value_1 followed_by value
    value = value_1
    value_1 = operator*  letterOrDigit+
    filename = filename_1 space followed_by space filename
    filename = filename_1
    filename_1 = letterOrDigit+ "." letterOrDigit+
    filename_1 = "*"{0,1} "." letterOrDigit+
    operator = '>' | '<' | '<=' | '>='
    followed_by = 'AND' | 'OR'
    file_path = "*"{0,1} '/' file_path_names '/' "*"{0,1} filename_1*
    file_path_names = path '/' path
    file_path_names = path
    path = path_1 "-" path
    path = path_1
    path_1 = words_1
    start = query
    query = query_1 space <followed_by>:a space query->adder(a)
    query = query_1 space <followed_by>:a space query_1->adder(None),adder(a)
    query = query_1->adder(None)
    query_1 = q{0,1} <words>:a q{0,1}  '=' q{0,1} <words>:b q{0,1}->adder_2(a,b)
    query_1 = q{0,1} <words>:a q{0,1} '=' q <value>:b q->adder_2(a,b)
    query_1 = q{0,1} <words>:a q{0,1} '=' q{0,1} <filename>:b q{0,1}->adder_2(a,b)
    query_1 = q{0,1} <words>:a q{0,1} '=' q{0,1} <file_path>:b q{0,1}->adder_2(a,b)
    '''
    x = parsley.makeGrammar(rules,{'adder':add,'adder_2':add_2})
    string = x(decoded_aql).start()
    followed_by = followed_by[::-1]
    return followed_by,request_dictionary
decoded_aql ='text="code to search~81" AND filename="*/John-Recipe/goobe/*.jpg" AND dirname="directory name" OR age="date" AND source="google drive" OR author="Jason" AND size="<10M AND >10G"'
a,b = aql_parser(decoded_aql)
print(a)
print(b)
