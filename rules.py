import parsley
requests = []
requests_dictionary = []
def add_2(column, operator, value):
    global requests_dictionary
    list1 = [{'column': column, 'operator': operator, 'value': value}]
    requests_dictionary.append(list1)


def add(request, oper):
    global requests
    requests.append([request, oper])
def parser(decoded_mql):
    global requests,requests_dictionary
    operators = ['in', '<', '<=', '>', '>=', 'DESC', '==']
    '''
    The rules string is the context-free grammar used for lexically
    analysing and parsing the request by the end user.
    In the productions/rules S corresponds to the start state.
    S is used to produce the non-terminal state T which is in-turn
    used to expand to as many request as the user gives.
    After T is expanded ,productions are used to expand to individual 
    requests such as ,U,V,W and so on.
    '''
    rules = """
    q = '"'
    c = ','
    op = '('
    cp = ')'
    operator = 'in' | '<' | '>' | 'DESC' | '=='
    p='publisher'
    space = ' '
    words = words_1 space* words | words_1
    words_1 = letterOrDigit+
    S = T
    T = <T1>:a ws 'AND' ws T->adder(a,"AND")
    T = <T1>:b ws 'OR' ws T->adder(b,"OR")
    T = <T1>:c ws 'order by' ws <X>:d->adder(d,None),adder(c,"ORDER BY")
    T = T1
    T1 = q <words>:aa q  ws operator:oo ws op <U>:bb cp ->adder_2(aa,oo,bb) 
    T1 = V 
    T1 = W 
    T1 = X
    U = U c ws U1 | U1
    U1 = q words q
    V = q <words>:aa q ws <operator>:oo ws < q{0,1} letterOrDigit+ q{0,1}>:bb ->adder_2(aa,oo,bb) 
    W = <words>:aa   ws <operator>:oo  ws <q{0,1} letterOrDigit+ q{0,1}>:bb ->adder_2(aa,oo,bb) 
    X = q <words>:aa q ws <operator>:oo ->adder_2(aa,oo,None)
    """
    x = parsley.makeGrammar(rules, {'adder': add,'adder_2': add_2})
    string = x(decoded_mql).S()
    requests = requests[::-1]
    return requests, requests_dictionary
