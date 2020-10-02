# 
import traceback 
span = 4

# json转换为str
def json_to_str(jo):
    try:
        if isinstance(jo,list):
            return list_to_s(jo,0,hasPre=False)
        elif isinstance(jo,dict):
            return obj_to_s(jo,0,hasPre=False)
    except Exception as e:
        traceback.print_exc()
        return ""

# 将str解析为json
def str_to_json(s):
    if s == None or not isinstance(s,str) or len(s) == 0:
        return None 
    i = 0

    while i< len(s) and s[i] == ' ':
        i+=1
    if i == len(s):
        return None 
    try:
        if s[i] == '[':
            v,i= parseList(s,0)
            i = passSpace(s,i)
            if i == len(s):
                return v 
            else:
                return None 
        elif s[i] == '{':
            v,i = parseDict(s,0)
            i = passSpace(s,i)
            if i == len(s):
                return v 
            else:
                return None 
        else:
            raise Exception
    except Exception as e:
        traceback.print_exc()
        return None 
class ParseErr(Exception):
    pass
def parseList(s,i):
    r = []
    i = passSpace(s,i)
    
    if i < len(s) and  s[i] == '[':
        i+=1
        while i < len(s):
            i = passSpace(s,i)
            if i>= len(s):
                raise ParseErr() 
            if s[i] == ']':
                return r,i+1
            v,i = parseVal(s,i)
            r.append(v)
            i = passSpace(s,i)
            if i<len(s) and s[i] == ']':
                return r,i+1
            if i < len(s) and s[i] == ',':
                i+=1
            else:
                raise ParseErr()
    raise ParseErr()
def parseDict(s,i):
    r = {}
    i = passSpace(s,i)
    if i < len(s) and s[i] == '{':
        i+=1
        while i < len(s):
            i = passSpace(s,i)
            if i >= len(s):
                raise ParseErr()
            if s[i] == '}':
                return r,i+1
            k,i = parseStr(s,i)
            i = passSpace(s,i)
            if s[i] != ':':
                raise ParseErr()
            i+=1
            i = passSpace(s,i)
            v,i = parseVal(s,i)
            r[k] = v 
            i = passSpace(s,i)
            if i < len(s) and s[i] == '}':
                return r,i+1
            if i < len(s) and s[i] == ',':
                i+=1
            else:
                raise ParseErr()
    raise ParseErr()

def isSpace(s,i):
    if i < len(s):
        if s[i] == ' ' or s[i] == '\t' or s[i] == '\n':
            return True 
        return False 
    raise ParseErr()
def passSpace(s,i):
    while i<len(s) and isSpace(s,i):
        i+=1
    return i
def parseStr(s,i):
    if i >= len(s):
        raise ParseErr()
    if s[i] == '"':
        j = i+1
        while j < len(s) and s[j] != '"':
            j+=1 
        if j == len(s):
            raise ParseErr()
        if s[j] == '"':
            return s[i+1:j],j+1
    else:
        raise ParseErr()

def parseVal(s,i):
    if i >= len(s):
        raise ParseErr()
    method = {
        "n":parseNull,
        "t":parseTrue,
        "f":parseFalse,
        '"':parseStr,
        '{':parseDict,
        '[':parseList,
    }
    m = method.get(s[i])
    if m:
        return m(s,i)
    else:
        return parseNumber(s,i)

def parseNumber(s,i):
    fu = False 
    if s[i] == '-':
        fu = True 
        i+=1
    if i == len(s):
        raise ParseErr()
    number = 0
    t = 0
    if  s[i] == '0':
        i+=1
        if i == len(s) or s[i] != '.':
            raise ParseErr()
        i+=1
        p = 0.1

        while i<len(s) and ord('0') <= ord(s[i]) <= ord('9'):
            t +=(ord(s[i]) - ord('0'))*p
            p = p*0.1
            i+=1
        if i == len(s):
            raise ParseErr()
    elif ord('0') <= ord(s[i]) <= ord('9'):
        while i<len(s) and ord('0') <= ord(s[i]) <= ord('9'):
            t = t*10+ord(s[i]) - ord('0')
            i+=1
        if i<len(s) and  s[i] == '.':
            p = 0.1
            i+=1
            while i<len(s) and ord('0') <= ord(s[i]) <= ord('9'):
                t +=(ord(s[i]) - ord('0'))*p
                p = p*0.1
                i+=1
            if i == len(s):
                raise ParseErr()
    if fu:
        return -t,i
    else:
        return t, i

def parseNull(s,i):
    if i+4  >= len(s):
        raise ParseErr()
    if s[i:i+4] == 'null':
        return None,i+4
    raise ParseErr()

def parseTrue(s,i):
    if i+4 >= len(s):
        raise ParseErr()
    if s[i:i+4] == 'true':
        return True,i+4
    raise ParseErr()
def parseFalse(s,i):
    if i+5 >= len(s):
        raise ParseErr()
    if s[i:i+5] == 'false':
        return False,i+5
    raise ParseErr() 

def val_to_s(obj,n,hasPre):
    if obj == None:
        return 'null'
    
    to_str = {
        None:none_to_s,
        bool:bool_to_s,
        int:number_to_s,
        float:number_to_s,
        str:str_to_s,
        dict:obj_to_s,
        list:list_to_s,
    }
    method = to_str.get(type(obj))
    if method == None:
        raise ParseErr()
    return method(obj,n,hasPre)
   

def obj_to_s(l,n,hasPre):
    s = ''
    if hasPre:
        s ='{'+'\n'
    else:
        s += ' '*n+'{'+'\n'
    ss = []
    for k in l:
        ss.append(' '*(n+span)+ '"'+k+'"'+':'+val_to_s(l[k],n+span,True))
    s+=',\n'.join(ss)+'\n'+' '*n + '}'
    return s 

def list_to_s(v,n,hasPre):
    if not isinstance(v,list):
        raise ParseErr()
    s = ''
    if hasPre:
        s = '['+'\n'
    else:
        s =  ' '*n + '['+'\n'
    ss = []
    for e in v:
        ss.append(val_to_s(e,n+span,False))
    
    s+=',\n'.join(ss)+'\n'+' '*n +']'
    return s 

def none_to_s(v,n,hasPre):
    if hasPre:
        return 'null'
    else:
        return ' '*n+'null'

def bool_to_s(v,n,hasPre):
    if hasPre:
        if v == True:
            return  'true'
        else:
            return  'false'
    else:
        if v == True:
            return  ' '*n + 'true'
        else:
            return  ' '*n + 'false'
def number_to_s(v,n,hasPre):
    if hasPre:
        return str(v)
    else:
        return ' '*n + str(v)
def str_to_s(v,n,hasPre):
    if hasPre:
        return '"'+v+'"'
    else:
        return ' '*n+'"'+v+'"' 





