import re
import copy
import queue
variable=('x','y','z','w','u','v')
#转换函数
def opposite(str):
    if str[0]=='¬':
        return str[1:]
    else:
        return '¬'+str

#去重
def unique(in_list):
    re_list=set(map(tuple, in_list))
    re_list=list(map(list,re_list))
    return re_list

def judge(list1:list,list2:list):
    sub=[]
    for i in range(1,len(list1)):
        #非变量但相等，则继续
        if list1[i] not in variable and list2[i] not in variable and list1[i]==list2[i]:
            continue
        #如果list1中为变量且list2中的为常量，则记录
        elif list1[i] not in variable and list2[i] in variable: #第一个为被替换成的常量，第二个为要进行替换的变量
            sub.append((list1[i],list2[i]))
        else:
            return False
    return sub

def resolustion (s:list,assignment:list,parent:list):
    for i,si in enumerate(s):
        for j,sj in enumerate(s):
            if i==j:
                continue
            for ki,kii in enumerate(s[i]):
                for kj,kjj in enumerate(s[j]):
                    if s[i][ki][0]==opposite(s[j][kj][0]) and len(s[i][ki]) == len(s[j][kj]): #存在相反的谓词
                        #参数项是否完全相等
                        if s[i][ki][1:]==s[j][kj][1:]:
                            #深复制
                            temp1=copy.deepcopy(s[i])
                            temp2=copy.deepcopy(s[j])
                            #删去互补对
                            del temp1[ki]
                            del temp2[kj]
                            #记录去重后的新子式
                            newS=unique(temp1+temp2)
                            parent.append([i,ki,j,kj]) #记录父子句
                            assignment.append([])  #记录变量替换
                            s.append(newS)
                            #如果新子句为空则退出函数
                            if newS == []:  
                                return
                            
                        #是否可以通过变量替换进行合一
                        else:
                            sub=judge(s[i][ki],s[j][kj])
                            if sub == False:
                                continue
                            else:
                                #深复制
                                temp1=copy.deepcopy(s[i])
                                temp2=copy.deepcopy(s[j])
                                #消去互补对
                                del temp1[ki]
                                del temp2[kj]
                                #将temp1中的变量替换为常量
                                for k in range(len(sub)):   #所有变量都替换
                                    for l in range(len(temp2)): 
                                        while sub[k][1] in temp2[l]:
                                            index=temp2[l].index(sub[k][1]) #找到要替换的变量位置
                                            temp2[l][index]=sub[k][0] #替换成常量
                                newS=unique(temp1+temp2)
                                parent.append([i,ki,j,kj])
                                assignment.append(sub)
                                s.append(newS)
                                #如果新子句为空则退出函数
                                if newS == []:
                                    return

#转换为标准形式需要的函数
def intoStd(lst:list):
    s=lst[0]+'('+','.join(lst[1:])+')'
    return s
def is_var(lst:list):
    if lst==[]:
        return ''
    elif(len(lst)==1):
        return f"({lst[0][1]}={lst[0][0]})"
    else:
        s=list()
        for i,li in enumerate(lst):
            s.append(f"{li[1]}={li[0]}")
        s='('+','.join(s)+')'
        return s
def is_mulsub(parent:list,id:int):
    if len(parent)==1:
        return ''
    else:
        return chr(id+97)

n=int(input())
s=list()
for i in range(n):
    #匹配字符串并转换成易于处理的形式
    s.append(re.findall(r'¬?\w+\(\w+\,*\w*\)',input()))#利用正则表达式转换为所需形式
    #把左括号全部转换成逗号并去掉由括号，再以逗号作为分隔符分割生成字符串列表
    for j in range(len(s[i])):
        s[i][j]=s[i][j].replace('(',',')
        s[i][j]=s[i][j].replace(')','')
        s[i][j]=s[i][j].split(',')

parent=[]
assignment=[]
#给parent赋空值,保持下标与s一致
for i in range(n):
    parent.append([])
resolustion(s,assignment,parent)


#回溯阶段
usedList=list()
q = queue.Queue()
q.put(parent[-1])
#s代表归结结果，parent代表这个结果是由哪两个子式归结而来，assignment为用到的变量
usedList.append([s[-1],parent[-1],assignment[-1]])
#层序遍历二叉树，回溯有用子式
while not q.empty():
    pre=q.get()
    if pre[0]>=n:
        usedList.append([s[pre[0]],parent[pre[0]],assignment[pre[0]-n]])
        q.put(parent[pre[0]])
    if pre[2]>=n:
        usedList.append([s[pre[2]],parent[pre[2]],assignment[pre[2]-n]])
        q.put(parent[pre[2]])
#此时的标号为原始标号
usedList.reverse()

#重新标号
reindex=dict()
#记录初始子式
for i in range(n):
    reindex[i]=None
#记录要用到的生成子式
for i,ui in enumerate(usedList):
    #将所有要用到的子句编号记录
    if ui[1][0] not in reindex:
        reindex[ui[1][0]]=None
    if ui[1][2] not in reindex:
        reindex[ui[1][2]]=None
#重新排序    
reindex=sorted(reindex.keys())
#列表解析式重新编号
reindex={x:reindex.index(x)+1 for x in reindex}


#标准输出
#输出每一步的归结步骤
for i,ui in enumerate(usedList):
    #如果输出的是空子句
    if i==len(usedList)-1:
        print(f"R[{reindex[ui[1][0]]},{reindex[ui[1][2]]}] = []")
        break
    else:
        print(f"R[{reindex[ui[1][0]]}{is_mulsub(s[ui[1][0]],ui[1][1])},{reindex[ui[1][2]]}{is_mulsub(s[ui[1][2]],ui[1][3])}]{is_var(ui[2])} = ",end='')
    #输出等号后面的内容，即经过等号左边归结后产生的新子句
    for j in range(len(ui[0])):
        if j is not len(ui[0])-1:
            print(intoStd(ui[0][j]),end=',')
        else:
            print(intoStd(ui[0][j]))

m1='test'
