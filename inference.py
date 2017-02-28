'''
Created on Nov 30, 2015

@author: akhila
'''
import sys
fp = open(sys.argv[2])
nqueries=int(fp.readline().rstrip())
#print "n queries is",nqueries
allqueries=[]
i=0
while i <nqueries:
    allqueries.append(fp.readline().rstrip())
    i=i+1
#print "all queries are", allqueries

nclauses=int(fp.readline().rstrip())
#print "no of  clauses in kb",nclauses

j=0
allclauses=[]
while j<nclauses:
    allclauses.append(fp.readline().rstrip())
    j=j+1
    
#print "all given clauses are",allclauses

#make a list of facts and clauses
given_facts = []
given_implications = []
mainpart=dict()
sub=dict()
kbase=[]
kk=0
i = 0
while i < nclauses:
    if "=>" in allclauses[i]:
        allclauses[i]=allclauses[i]+";"
        kk=allclauses[i].index('=')
        sub["lhs"]=allclauses[i][0:kk]
        #print "before ^",sub['lhs']     
        sub['lhs']=map(lambda x: x.strip(), sub['lhs'].split("^"))
        #print "after ^",sub['lhs']
        #print "final lhs is",sub['lhs'
            #print "after stripping",akhi
        kk=kk+2
        ll=allclauses[i].index(';')
        sub['rhs']=allclauses[i][kk:ll]
        sub['rhs']=sub['rhs'].strip()
        kbase.append(sub)
        sub=dict()
        #given_implications=[]
        
    else:
        sub["lhs"]=''
        sub['rhs']=allclauses[i]
        sub['rhs']=sub['rhs'].strip()
        kbase.append(sub)
        sub=dict()
    i=i+ 1
    
#print "kbase is",kbase
#print kbase[0]
"""for aa in kbase:
    print aa"""
#print kbase[0]['lhs'][0]
#print kbase[0]['rhs'][1]
    

visited_rules=[]

#to find all the arguments given inside paranthesis
def findargs(cl):
    length=len(cl)
    templist=[]
    ii=0
    jj=0
    #print "in findargs"
    while ii<length:
        #print "inside while"
        #print "ii is",ii
        #print "in cl that letter is",cl[ii]
        if ',' in cl[ii] or ii==length-1:
            #print "comma found"
            if ii==length-1:
                ii=ii+1
                #print "im printing",cl[ii]
            #print 'adding'
            #print cl[jj:ii]
            templist.append(cl[jj:ii])
            #print "list is",templist
            
            jj=ii+1
            #print "jj is",jj
            ii=ii+1
        else:
            ii=ii+1
    #print templist
    return templist

#to find if var is a variable or not            
def isvariable(var):
    if len(var)==1:
        if var.isupper()==True:
            return False
        else:
            return True
    else:
        return False
 
    
#to trim off braces and whatever is inside and give predicate symmbol   
def getpredicate_symbol(some):
    ww=some.index('(')
    return some[0:ww]    
#to give me what ever is inside the paranthesis
def removeparan(cc):
    ia=cc.index('(')+1
    ja=cc.index(')')
    return cc[ia:ja]
    

def find_match(goalgoal):
    #print "received goal in find_match",goalgoal
    matching_sentences=[]
    list1=[]
    list2=[]
    list11=[]
    list22=[]
    modgoal1=[]
    if goalgoal in visited_rules:
        return []
    else:
        # add if condition where all args in goal are constant
        #print "in else"
        myflag=True
        modgoal=removeparan(goalgoal)
        #print modgoal
        modgoal1=findargs(modgoal)
        #print modgoal1
        modsize=len(modgoal1)
        #print modsize
        for ll in range(0,modsize):
            #print modgoal1[ll]
            if (isvariable(modgoal1[ll])==True):
                #print "inside if"
                myflag=False
        if myflag==True:   
            #print "in if of find_match===>adding goal to visited"    
            visited_rules.append(goalgoal)
    for sentence in kbase:
        #print sentence,sentence['lhs']
        if sentence['lhs']=='':#if it is a fact
            #print "hi"
            #print sentence,getpredicate_symbol(sentence['rhs'])
            #print "this",getpredicate_symbol(sentence['rhs'])
            #print "that",getpredicate_symbol(goalgoal)
            if getpredicate_symbol(sentence['rhs'])==getpredicate_symbol(goalgoal):
                #print "yes matched!!!!!!!!!!!!!"
                #flag=True
                
                goalgoal1=removeparan(goalgoal)
                list1=findargs(goalgoal1)
                #print "list1 is",list1
                goalgoal2=removeparan(sentence['rhs'])
                list2=findargs(goalgoal2)
                #print "list2 is",list2
                noofargs=len(list2)
                #print "len is",noofargs
                nflag = True
                #to know if arguments of both lists are constants or not 
                for qq in range(0,noofargs):
                    #print "inside for loop"
                    #print "qq is",qq
                    #print isvariable(list1[qq])
                    innerflag2=True
                    innerflag1=True
                    if (isvariable(list1[qq])==True):
                        innerflag1=False
                    if(isvariable(list2[qq])==True):
                        innerflag2=False
                    
                    #print cons
                    #print "innerflag1 is",innerflag1
                    if innerflag1==True and innerflag2==True:#means both are constants
                        #print 'both constant'
                        if(list1[qq]!=list2[qq]):
                            nflag = False
                            break
                        #print "inside last if"
                if nflag:
                        matching_sentences.append(sentence)
                        #print "going to break"
                        #break            
        else:
            #print "here",sentence
            #print "in rhs",getpredicate_symbol(sentence['rhs'][0:])
            #print "in given goal",getpredicate_symbol(goalgoal)
            if getpredicate_symbol(sentence['rhs'][0:])==getpredicate_symbol(goalgoal):
                #print "yes matched!!!!!!!!!!!!!"
                #flag=True
                goalgoal11=removeparan(goalgoal)
                list11=findargs(goalgoal11)
                #print "list1 is",list11
                goalgoal22=removeparan(sentence['rhs'])
                list22=findargs(goalgoal22)
                #print "list2 is",list22
                noofargs=len(list22)
                #print "len is",noofargs
                nflag = True
                #to know if arguments of both lists are constants or not 
                for qqq in range(0,noofargs):
                    #print "inside for loop"
                    #print "qq is",qq
                    innerflag22=True
                    innerflag11=True
                    #print isvariable(list1[qq])
                    if (isvariable(list11[qqq])==True):
                        innerflag11=False
                    if(isvariable(list22[qqq])==True):
                        innerflag22=False
                    
                    #print cons
                    #print "innerflag1 is",innerflag1
                    if innerflag11==True and innerflag22==True:#means both are constants
                        #print("here")
                        if(list11[qqq]!=list22[qqq]):
                            nflag = False
                            break
                        #print "inside last if"
                if nflag:
                        matching_sentences.append(sentence)
                        #print "going to break"
                        #break
                        
    #print "before returning",matching_sentences           
    return matching_sentences   
                    
           
        
      
#to substitute and give me clause by substituting the value
def functionsubs(clause,substitutions):
    #print "clause isssss",clause
    i=clause.index('(')+1
    j=clause.index(')')
    temp = clause
    if clause.find(',')==-1:
        lol=removeparan(clause)
        i=clause.index('(')
        tt = clause[:i+1]
        j=clause.index(')')+1
        if isvariable(lol)==False:
            #print clause[i:j]
            return clause[0:j]
        else:
            if substitutions!={}:
                temp=clause
                if lol in substitutions.keys():
                    temp = tt + substitutions[lol] + ')'
                
    else:
        #print "in else"
        listofargs=[]
        listofargs=findargs(clause[i:j])
        #print "list of args reurned",listofargs
        temp=clause
        tt = clause[:i]
        nargs = list(listofargs)
        #print "temp before changing",temp
        ti = 0
        for arg in listofargs:
            if(isvariable(arg)):
                #print "yes",arg
                if arg in substitutions.keys():
                    #print "inside if"
                    #print "arg is",arg
                    #print "its substituion is",substitutions[arg]
                    nargs[ti] = substitutions[arg]
                    #print temp
                    
            ti += 1
        temp = tt + ','.join(nargs) + ')'
    #print 'subsition',clause,temp
    return temp


def unification(p,pq):
    #print "in unification"
    #print p
    #print pq
    uu=[]
    vv=[]
    temporary={}
    t = {}
    #print "is",temporary
    uu=findargs(removeparan(p))
    vv=findargs(removeparan(pq))
    #print uu
    #print vv
    for l in range(len(vv)):
        if isvariable(uu[l])==True and isvariable(vv[l])==False:
            if uu[l] in temporary.keys():
                if vv[l]!=temporary[uu[l]]:
                    return None
            else:
                temporary[uu[l]]=vv[l]
    subs={}
    for m in range(len(vv)):
        if isvariable(uu[m])==False and isvariable(vv[m])==True:
            if vv[m] in subs.keys():
                if uu[m]!= subs(vv[m]):
                    return None
            else:
                subs[vv[m]]=uu[m]
    for n in range(len(vv)):
        if isvariable(uu[n])==True and isvariable(vv[n])==True :
            if uu[n] in temporary.keys():
                if vv[n] in subs.keys():
                    if temporary[uu[n]]!=subs[vv[n]]:
                        return None
                else:
                    subs[vv[n]]=temporary[uu[n]]
            elif uu[n] in t.keys():
                subs[vv[n]] = t[uu[n]]
            else:
                t[uu[n]] = vv[n] 
    return subs

def and_algo(g,s):
    
    #print "in and_algo"
    #print "received goal in and_algo",g
    #print "received substituiton in and_algo",s
    rosult_subs=[]
    if g==[]:
        #print "inside if of and_algo"
        rosult_subs.append(s)
    else:
        #print "inside else of and_algo"
        #print "$$$$$$$",g
        #print "first is",g[0]
        first=g[0]
        rest=g[1:]
        #print "first is",first
        #print "rest is",rest
        t_subs=or_algo(first, s)
        #print t_subs
        for sob in t_subs:
            n_subs=s.copy()
            n_subs.update(sob)
            r_subst=and_algo(rest,n_subs)
            for rsub in r_subst:
                n_subs.update(rsub)
                rosult_subs.append(n_subs)
    return rosult_subs
        

def or_algo(goal1,subs):
    #print "received goal in or_algo",goal1
    result_sub=[]
    nsubs={}
    modified_goal=functionsubs(goal1,subs)
    #print "modified_goal in or_algo is",modified_goal
    matching_rules=find_match(modified_goal)
    #print "rules matched in or_algo",matching_rules
    for s in matching_rules:
        nsubs=unification(modified_goal,s['rhs'])
        #print "result from unification in or_algo",nsubs
        if nsubs!=None:
            if s['lhs']=='':
                #print "inside if"
                result_sub.append(unification(s['rhs'],goal1))
            else:
                #print "inside else"
                r_subs=and_algo(s['lhs'],nsubs)
                for rsob in r_subs:
                    f_clause=functionsubs(s['rhs'],rsob)
                    result_sub.append(unification(f_clause,goal1))
    return result_sub
    
fp1 = open("output.txt", 'w')   
for bhavi in range(0,len(allqueries)):
    goal=allqueries[bhavi]
    #print "global goal is",goal 
    answer=[]
    answer= or_algo(goal,{})
    #print "Answer is",answer
    if answer!=[]:
        fp1.write("TRUE")
        fp1.write("\n")
    else:
        fp1.write("FALSE")
        fp1.write("\n")



