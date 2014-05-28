#coding=utf-8
def lines(file):
    for line in file: yield line
    yield '\n'

def blocks(file):
    block=[]
    for line in lines(file):
        if line.strip(): #line 非空
            block.append(line)
        elif block: #line是空行
            yield ' '.join(block).strip()   #将block列表转换为字符串，并返回
            block=[]
