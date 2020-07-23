import parsley
followed_by = []
requests_dictionary = []
def add_2(column, operator, value):
    global requests_dictionary
    list1 = {'column': column, 'operator': operator, 'value': value}
    requests_dictionary.append(list1)

def add(oper):

    global requests
    followed_by.append(oper)

def parser(decoded_mql):
    global followed_by,requests_dictionary
    followed_by=[]
    requests_dictionary=[]
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
    operator = 'in' | '<' | '>' | 'DESC' | '=' | 'ASC'
    space = ' '
    words = words_1 space* words* | words_1
    words_1 = "_"* letterOrDigit+ "_"* letterOrDigit*
    S = T
    T = T1 ws 'AND' ws T->adder("AND")
    T = T1 ws 'OR' ws T->adder("OR")
    T = T1 ws 'order by' ws X->adder(None),adder("ORDER BY")
   
    T = T1 ws 'AND' ws T1->adder(None),adder("AND")
    T = T1 ws 'OR' ws T1->adder(None),adder("OR")
    T = T1->adder(None)
    T1 = <words_1>:aa  ws operator:oo ws op <U>:bb cp ->adder_2(aa,oo,bb)
    T1 = q <words>:aa q ws operator:oo ws op <U>:bb cp -> adder_2(aa,oo,bb)
    T1 = V
    T1 = W
    U = U c ws U1 | U1
    U1 = q words q
    U1 = words_1
    V = q <words>:aa q ws <operator>:oo ws < q{0,1} letterOrDigit+ q{0,1}>:bb ->adder_2(aa,oo,bb)
    W = <words_1>:aa   ws <operator>:oo  ws <q{0,1} letterOrDigit+ q{0,1}>:bb ->adder_2(aa,oo,bb)
    X = q <words>:aa q ws <operator>:oo ->adder_2(aa,oo,None)
    X = <words_1>:aa ws <operator>:oo->adder_2(aa,oo,None)
    """
    x = parsley.makeGrammar(rules, {'adder': add,'adder_2': add_2})
    try:
        string = x(decoded_mql).S()
    except:
        return None

    followed_by = followed_by[::-1]
    return followed_by, requests_dictionary
