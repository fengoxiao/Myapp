#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import random
import operator
import re
import argparse
from fractions import Fraction

def getSymbol():#获得符号列表
    symbol=[]
    syb=0
    i=random.randint(1, 3)
    for x in range(i):
        sy=random.choice(['+','-','×','÷'])
        if sy=='+'or sy=='-':
            syb +=10**(i-x-1)
        else :
            syb += 2 * (10 ** (i - x - 1))
        symbol.append(sy)
    return symbol,i,syb

def getNumerical(i,r):#获得数值列表
    numerical,n,m=[],1,0
    if r < 10:
        n = int(10 / r)
    if n==1:
        while m <= i:
            numerical.append(Fraction(random.randint(1, r), random.randint(1, r)))
            m+=1
    else:
        while m <= i:
            nu = Fraction(random.randint(1, r * n), random.randint(1, r * n))
            if nu<=r:
                numerical.append(nu)
                m += 1
    return numerical

def calculate(a,b,c):#计算
    answer=0
    if c=='+':
        answer=a+b
    elif c=='-':
        if a>=b:answer=a-b
        else:answer=-1
    elif c=='×':
        answer=a*b
    else:answer=a/b
    return answer

def cf(fraction):#真分数的表达
    if fraction.numerator%fraction.denominator==0:
        return '%d'%(fraction.numerator/fraction.denominator)
    elif fraction.numerator>fraction.denominator:
        a=int(fraction.numerator/fraction.denominator)
        b, c = fraction.numerator - a * fraction.denominator, fraction.denominator
        return '%d%s%d%s%d' % (a,'’',b,'/',c)
    else:
        b, c = fraction.numerator, fraction.denominator
        return '%d%s%d' % (b,'/',c)

def rcf(fra):#真分数转化为分数
    line = re.sub(r'[\’\/]', ' ', fra)
    wo = line.split(' ')  # 空格分割单词
    wo = [int(x) for x in wo]
    i=len(wo)
    if i==1:
        return wo[0]
    elif i==2:
        return Fraction(wo[0], wo[1])
    else:return Fraction(wo[0]*wo[2]+wo[1], wo[2])

def writeFormula(symbol,numerical,syb):#算术表达式
    s=''
    if syb>100:
        if syb == 112 or syb ==212:
            s = '(%s %s %s %s %s) %s %s = ' % (cf(numerical[0]), symbol[0],
            cf(numerical[1]),symbol[1], cf(numerical[2]), symbol[2], cf(numerical[3]))
        elif syb == 121 or syb ==122:
            s = '(%s %s %s) %s %s %s %s = ' % (cf(numerical[0]), symbol[0],
            cf(numerical[1]),symbol[1], cf(numerical[2]), symbol[2], cf(numerical[3]))
        else:
            s = '%s %s %s %s %s %s %s = ' % (cf(numerical[0]), symbol[0],
            cf(numerical[1]),symbol[1], cf(numerical[2]), symbol[2], cf(numerical[3]))
    elif syb>10:
        if syb == 12:
            s = '(%s %s %s)%s %s = ' % (cf(numerical[0]), symbol[0],
            cf(numerical[1]), symbol[1], cf(numerical[2]))
        else:
            s = '%s %s %s %s %s = ' % (cf(numerical[0]), symbol[0],
            cf(numerical[1]), symbol[1], cf(numerical[2]))
    else :
        s ='%s %s %s = ' % (cf(numerical[0]),symbol[0],cf(numerical[1]))
    return s

def getFormula(n,r):#生成题目和答案列表
    Exercises,Answers,Exercises1,Exercises2=[],[],[],[]
    x=1
    while x<n+1:
        symbol,i,syb=getSymbol()
        numerical=getNumerical(i,r)
        answer = numerical[0]
        legal = True
        for y in range(i):
            cal=calculate(answer,numerical[y+1],symbol[y])
            if cal>=0:#判断算式是否合法
                answer=cal
            else:
                legal=False
                break
        if legal:#判断是否重复题目
            try:
                num=Answers.index(answer)#第一个重复答案的索引
                if operator.eq(Exercises1[num],symbol) and operator.eq(Exercises2[num],numerical):
                    pass
            except ValueError as e:#可以写入
                Answers.append(answer)
                Exercises1.append(symbol)
                Exercises2.append(numerical)
                Exercises.append('%d. %s'%(x,writeFormula(symbol,numerical,syb)))
                x+=1
        else:pass
    return Exercises,Answers

def text_save(filename, data):#filename为写入文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    file.seek(0)
    file.truncate()  # 清空文件
    for x in data:
        x='%s\n'%(x)
        file.write(x)
    file.close()
    print('%s文件保存成功'%filename)

def answers_read(filename):
    file = open(filename)
    read = file.readlines()
    answers=[]
    for line in read:
        line = re.sub(r'\n', '', line)
        answers.append(line.split(' ')[1])#字符串
    return answers

def exercises_read(filename):
    file = open(filename)
    read = file.readlines()
    answers2= []
    for line in read:
        line = re.sub(r'[\.\(\)\=\s]+', ' ', line)
        line = line.strip()  # 除去左右的空格
        wo = line.split( )  # 空格分割单词
        del wo[0]
        sy,nu=[],[]
        for x in range(len(wo)):
            if x%2:
                sy.append(wo[x])
            else:nu.append(rcf(wo[x]))
        ans = nu[0]
        for y in range(len(sy)):
            ans = calculate(ans, nu[y + 1], sy[y])
        answers2.append(ans)
    return answers2

def checkAnswer(a,e,ra,re):
    correct,wrong=[],[]
    for x in range(len(ra)):
        if operator.eq(ra[x],cf(re[x])):
            correct.append(x+1)
        else:wrong.append(x+1)
    file = open('Grade.txt', 'a')
    file.seek(0)
    file.truncate()  # 清空文件
    x1='Correct:%d%s\n'%(len(correct),correct)
    x2='Wrong:%d%s'%(len(wrong),wrong)
    file.write(x1)
    file.write(x2)
    file.close()
    print('题目文件%s与答案文件%s比对成功，结果已存入Grade.txt'%(e,a))

def controlParameter():#命令行控制模块
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='题目数量',type=int)
    parser.add_argument('-r', help='题目中数值的范围',type=int)
    parser.add_argument('-e', help='题目文件',type=str)
    parser.add_argument('-a', help='答案文件',type=str)
    return parser.parse_args()

if __name__ == '__main__':#主函数
    n=10#设置默认值
    args=controlParameter()
    if args.n:
        n=args.n
    if args.r:
        r=args.r
        Exercises, Answers=getFormula(n,r)
        for x in range(n):
            Answers[x]='%d. %s'%(x+1,cf(Answers[x]))
        print('n,r两个参数的值为%d,%d:'%(n,r))
        text_save('Exercises.txt',Exercises)
        text_save('Answers.txt',Answers)
    if args.e and args.a:#'Answers.txt','Exercises.txt'
        Answers1=args.a
        Exercises1=args.e
        checkAnswer(Answers1,Exercises1,answers_read(Answers1), exercises_read(Exercises1))