# 想要更加通用的处理 jsfuck 的解密
# 暂时并没有解决该密码的解密处理。


# 为了更加贴近语法逻辑就有了下面的函数
# 可以从 [+!+[]+[]] 中找到最大的中括号并且收集匹配到的内容
def findall_middle_brackets(string, leftright='[]', force=True):
    left, right = leftright
    s = string
    p = {}
    l, r = 0, 0
    q = s.find(left)
    while True:
        c = []
        if q == -1: break
        for idx,i in enumerate(s[q:]):
            if i == left:  c.append(left)
            if i == right: c.pop()
            if len(c) == 0:
                l, r = q, q + idx + 1
                p[(l, r)] = s[l:r]
                q = s.find(left, r)
                break
        if len(c) > 0:
            if force: return p
            raise KeyError('unparse in index:{}'.format(l))
    return p

def parse(string):
    q = [
        ["+!+[]", "+1"],
        ["+!![]", "+1"],
        ["+![]",  "+0"],
        ["+[]", "+0"],
        ["!+[]", "1"],
        ["!![]", "true"],
        ["![]", "false"],
        ["[][[]]", "undefined"],
        ["[]+[]", "''"],
        ["[+!+[]]+[+[]]", "10"] # 这里并不通用
    ]
    p = []
    f = lambda i: ''.join(['\\'+j if j in r'*.?+$^[](){}|\/' else j for j in i])
    def _parse(string, ls):
        s = string
        p = []
        t = True
        while t:
            for a, b in q:
                if s and s[0] not in '+![]()':
                    p.append(s[0])
                    s = s[1:]
                    break
                v = re.findall(r'^\+?'+f(a), s)
                if v:
                    s = re.sub(r'^\+?'+f(a), '', s)
                    t = True
                    p.append(v[0])
                    break
                t = False
        k = dict(ls)
        for i in range(len(p)):
            if p[i] in k:
                p[i] = k[p[i]]
        return ''.join(p)

    s = string[1:-1]
    s = _parse(s, q)
    try:
        s = str(eval(s))
        if string[0] == '(' and string[-1] == ')':
            return s
    except:
        pass
    return string[0] + s + string[-1] # 括号或中括号

def replace_func_brackets(string):
    s = string
    if s == '[]': return s
    return parse(s)







# 针对上面的函数的增强，可以对获取到的数据进行函数替换处理
# 后续需要考虑改成深度迭代，目前这种暂时还不能解决各种问题
def sub_middle_brackets(string, func, leftright='[]',force=True):
    s = string
    d = findall_middle_brackets(string, leftright)
    k = sorted(d)
    ll, rr = 0, len(s) + 1
    if k and func:
        q = [ll]
        for l,r in k:
            q.append(l); q.append(r)
        q.append(rr)
        e = {}
        w = {}
        for i in range(len(q) - 1):
            k, v = (q[i], q[i+1]), s[q[i]:q[i+1]]
            if i%2 == 0: e[k] = v
            if i%2 == 1: w[k] = v
        for i in w: w[i] = func(w[i])
        e.update(w)
        k = sorted(e)
        r = ''.join([e[i] for i in k])
        return r

import re
# 小括号的处理可以直接用正则处理
def sub_parentheses(string, replace_func_brackets):
    s = string
    s = re.sub(r'\([^\(\)]+\)', lambda i:replace_func_brackets(i.group(0)), s)
    return s

s = '''$hidescript=String.fromCharCode(+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[],+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]);;_="constructor";_[_][_]((+{}+[]+[]+[]+[]+{})[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+$hidescript[(+[])]+([![]]+[][[]])[+!+[]+[+[]]]+$hidescript[(+!+[])]+(!![]+[])[!+[]+!+[]+!+[]]+([]+[]+{})[+!+[]]+(!![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+$hidescript[+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]]+([![]]+{})[+!+[]+[+[]]]+([]+[]+{})[+!+[]]+$hidescript[(+!+[])]+$hidescript[+!+[]+!+[]+!+[]+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+(![]+[])[+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+([![]]+{})[+!+[]+[+[]]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+([]+[]+{})[!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+(![]+[])[+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+([]+[]+[][[]])[!+[]+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+([]+[]+{})[!+[]+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+([![]]+{})[+!+[]+[+[]]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+([]+[]+{})[!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+([![]]+{})[+!+[]+[+[]]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+(![]+[])[+!+[]]+(!![]+[])[+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]+(![]+[])[+!+[]]+([]+[]+[][[]])[+!+[]]+([]+[]+[][[]])[!+[]+!+[]]+([]+[]+{})[+!+[]]+$hidescript[(+!+[])]+$hidescript[+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+$hidescript[+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]])();'''
# s = '+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]));jCAUZzW.O+=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![])+(+!![])+(+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+!![]))/+((!+[]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]));jCAUZzW.O+=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]));jCAUZzW.O+=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]));jCAUZzW.O-=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![])+(+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]));jCAUZzW.O-=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+!![]+[])+(!+[]+!![])+(+[])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]));jCAUZzW.O+=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(!+[]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]))/+((!+[]+!![]+[])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+!![])+(+[]));jCAUZzW.O*=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]))/+((!+[]+!![]+[])+(!+[]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]))'
# s = '[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]](([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(+(+!+[]+[+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+[!+[]+!+[]]+[+[]])+[])[+!+[]]+(![]+[])[!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(+![]+[![]]+([]+[])[([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]]+(![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]]+[+!+[]]+[!+[]+!+[]]+[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]])()'

# v = sub_parentheses(s, replace_func_brackets)
# v = sub_middle_brackets(v, replace_func_brackets)
# print(v)


# 上面的部分是通过某个表进行映射处理的，感觉很不通用。
# 下面我还是考虑其他方法。通过自行实现js + 计算部分？
##########################################################












def some2(string, force=True):
    # 切分算式，这里抛弃对 () 的考虑，小括号的处理专门使用正则迭代着取出内容进行运算
    # 运算之后将计算结果替换到原始内容当中。所以这里会专门针对 +![] 的计算进行处理
    def combine(p):
        # 合并相连的中括号，让功能能够更方便的处理
        pr = None
        ci = 0
        cb = {}
        for cr in sorted(p):
            if pr:
                if pr[1] == cr[0]:
                    if ci not in cb: cb[ci] = []
                    if pr not in cb[ci]: cb[ci].append(pr)
                    if cr not in cb[ci]: cb[ci].append(cr)
                else:
                    ci += 1
                    if ci not in cb: cb[ci] = []
                    if cr not in cb[ci]: cb[ci].append(cr)
            else:
                if ci not in cb: cb[ci] = []
                if cr not in cb[ci]: cb[ci].append(cr)
            pr = cr
        d = {}
        for pi in sorted(cb):
            v = cb[pi]
            l, r = v[0][0], v[-1][1]
            d[(l, r)] = ''.join([p[i] for i in v])
        return d
    left, right = '[]'
    s = string
    p = {}
    l, r = 0, 0
    q = s.find(left)
    t = True
    while t:
        c = []
        if q == -1: break
        for idx,i in enumerate(s[q:]):
            if i == left:  c.append(left)
            if i == right: c.pop()
            if len(c) == 0:
                l, r = q, q + idx + 1
                p[(l, r)] = s[l:r]
                q = s.find(left, r)
                break
        if len(c) > 0:
            t = False
    s = string
    d = combine(p)
    k = sorted(d)
    ll, rr = 0, len(s) + 1
    if k:
        q = [ll]
        for l,r in k:
            q.append(l); q.append(r)
        q.append(rr)
        e = {}
        w = {}
        pr = ''
        for i in range(len(q) - 1):
            k, v = (q[i], q[i+1]), s[q[i]:q[i+1]]
            if i%2 == 0: 
                # c = re.findall(r'\+!+\+$|\+$', v)
                c = re.findall(r'\+((?:!*\+)?)$', v)
                pr = c[0] if c else ''
                e[k] = v[:len(v) - len(pr)]
            if i%2 == 1: 
                w[k] = pr + v
        e.update(w)
        k = sorted(e)
        r = [e[i] for i in k if e[i]]
        if len(r) >= 2 and not r[0].endswith(']'):
            r = [r[0] + r[1]] + r[2:]
        return r


# print(some(s))
s = '+!+$+!+$+!+$+[true]+[][asdf[+dasdf]]+[][][]'
s = '[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]](([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(+(+!+[]+[+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+[!+[]+!+[]]+[+[]])+[])[+!+[]]+(![]+[])[!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(+![]+[![]]+([]+[])[([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]]+(![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]]+[+!+[]]+[!+[]+!+[]]+[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]])()'
# s = '+!+[]+!+[]+!+[]+[]+[][[]]+[[[]]]'
# for i in re.findall(r'\(([^\(\)]+)\)', s):
#     print(i)
#     print(some2(i))
#     print()

# s = '[![]]+[][[]]'
# s = '+!+[]+!+[]+!+[]+[]+[][[]]+[[[]]]'
# s = '+[![]]+[][[]]'
# print(some2(s))


'''
用映射的方式简直太丑陋，所以想要自己实现各种计算解构
考虑到 jsfuck 的局限性，很可能这里的 jsfuck 里面只需要 [] 作为最最基本的单原件
    或许在一定程度上还是需要一些基映射处理比较简单的部分？

# +
+true       1
+false      0
+[]         0
+''         0
+'asdf'     NaN
+'123123'   123123
+123        123
+undefined  NaN

# !
![]         false
!''         true
!'asdf'     false
!true       false
!false      true
!undefined  true

# [?] 
[][[]]      undefined
[][true]    undefined
[?][?]      undefined # 通常 [][?] 这种类型就是通过找列表对象找不到则返回一个undefined

# ''
'' + 'asdf'     # 'asdf'        字符串
'' + 123        # '123'         字符串
'' + undefined  # 'undefined'   字符串
'' + true       # 'true'        字符串
'' + false      # 'false'       字符串
'' + [true]     # 'true'        字符串
'' + [false]    # 'false'       字符串
'' + [123,123]  # '123,123'     字符串
'' + NaN        # 'NaN'         字符串

# []
同上，都会生成字符串

# 123
123 + 'asdf'    # 字符串
123 + 123       # 数字
123 + undefined # NaN
123 + true      # 124
123 + false     # 123
123 + [true]    # 字符串
123 + [false]   # 字符串
123 + [123,123] # '123123,123'
123 + NaN       # NaN



自行实现js的计算，统计一下所有的类型：
数字
字符串
undefined
true,false 
null
NaN

'''
# 考虑先抽取 ! 部分的处理
# 先用 !+ 的前缀方式切割一个纯计算模块（纯计算模块即为没有嵌套部分的计算模块）
# ! 在js里面可以多重并接，而 + 不可以多个并在一起，以此为正则开始处理
s = '+!+[]+!+[]+!+[]+[]+[][[]]'

def some(ls):
    _unfind     = -1
    _int        = 0
    _str        = 1
    _undefined  = 2
    _boolen     = 3
    _null       = 4
    _NaN        = 5
    _list       = 6
    q = [
        ["+!+[]",   "1",        _int],
        ["+!!+[]",  "0",        _int],
        ["+![]",    "0",        _int],
        ["+!![]",   "1",        _int],
        ["+[]",     "0",        _int],
        ["!+[]",    "true",     _boolen],
        ["!!+[]",   "false",    _boolen],
        ["![]",     "false",    _boolen],
        ["!![]",    "true",     _boolen],
        ["[]",      "[]",       _list],
        ["[][[]]",  "undefined",_undefined],
    ]
    def get_fit(s):
        if isinstance(s, (list,tuple)):
            return s
        for i in q:
            if s == i[0]:
                return i
        return ['', '', _unfind]
    def plus(a, b):
        ak, av, at = a
        bk, bv, bt = b
        types = [at, bt]
        if _list in types or _str in types:
            rt = _str
        elif _NaN in types or _undefined in types:
            rt = _NaN
        elif _int in types:
            if types.count(_int) == 2:
                rt = _int
            elif _boolen in types or _null in types:
                rt = _int
        elif _boolen in types:
            if types.count(_boolen) == 2:
                rt = _int
            elif _null in types:
                rt = _int
        elif _null in types:
            if types.count(_boolen) == 2:
                rt = _int

        def parse_type(xv, xt, tp):

            if tp == _NaN:
                return 'NaN'
            if tp == _int:
                if xt != _int:
                    if xv == 'true':    return '1'
                    if xv == 'false':   return '0'
                    if xv == 'null':    return '0'
                else:
                    return xv
            if tp == _str:
                print(xt,xv,tp)
                if xt != _str:
                    if   xv == '[]':          return repr('')
                    elif xv == 'NaN':         return repr('NaN')
                    elif xv == 'null':        return repr('null')
                    elif xv == 'true':        return repr('true')
                    elif xv == 'false':       return repr('false')
                    elif xv == 'undefined':   return repr('undefined')
                    else: return repr(xv)
                else:
                    return repr(xv)

        # 将a,b的数据类型统一后进行计算
        _a = parse_type(av, at, rt)
        _b = parse_type(bv, bt, rt)
        # print(_a, av, at, rt)
        # print(_b, bv, bt, rt)
        # print('{}+{}'.format(_a,_b))
        if rt == _NaN: val = 'NaN'
        if rt == _str: val = repr(eval(_a)+eval(_b))
        if rt == _int: val = int(_a) + int(_b)
        return None,str(val),rt
    
    l = ls[::-1]
    t = True
    p = []
    while t and len(l):
        p.append(l.pop())
        if len(p) == 3 and p[1] == '+':
            left  = get_fit(p[0])
            right = get_fit(p[2])
            # print(left, right)
            p = [plus(left, right)]
            # print(p)


        

s = '[![]]+[][[]]'
s = '+!+[]+!+[]+!+[]+[]+[][[]]+[[[]]]'
# s = '[![]]+[][[]]+"asdf"+12312'
v = some2(s)
print(v)
some(v)