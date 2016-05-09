from Bots.EmoBayesActorToo import EmoBayesActorToo
from Bots.EmoBayesActorTooB import EmoBayesActorTooB
import random
import math
import time
import sys
import os
import numpy
import scipy.stats as stats

def main(eName, N, p, runExperimentTwo, idIn, timeout):
    print "Starting Wubben2011"
    
    #N=1
    #eName = "Experiment-2-test"
    #p=0.4
    if(not runExperimentTwo):
        path="D:\Research Data\CS886\Wubben2011a"
        print " Specifically, experiment 1, named",eName," with N=",N,"and p=",p,"; path is:",path
        experimentOne(eName, N, p, path, idIn, timeout)
    else:
        path="D:\Research Data\CS886\Wubben2011b"
        print " Specifically, experiment 2, named",eName," with N=",N,"and p=",p,"; path is:",path                
        experimentTwo(eName, N, p, path, idIn, timeout)

    
    
def chooseIdentities(N, idFile, idIn):
    with open(idFile) as f:
        content = f.readlines()
        
    result = []
    if(idIn == "NA"):
        for i in range(0, N):
            newID = random.randint(0,len(content)-1)
            #print "id selected",content[newID].split(',', 1)[0]
            result.append(content[newID].split(',', 1)[0])
    else:
        for i in range(0, N):
            result.append(idIn)
            
    return result

def chooseGenders(N, p):
    result = []
    numFemale = 0
    for i in range(0, N):
        rVal = random.random()
        
        if(rVal >= p):
            gender = "male"
        else:
            gender = "female"
            numFemale = numFemale + 1
        result.append(gender)
        
    return (result,numFemale)

def chooseEmotions(N):
    result = []
    numAnger = 0
    numDisappointment = 0
    for i in range(0, N):
        rVal = random.choice(["anger","disappointment","no emotion"])
        
        if(rVal == "anger"):
            numAnger = numAnger +1
        elif(rVal == "disappointment"):
            numDisappointment = numDisappointment + 1
        
        result.append(rVal)
        
    return (result,numAnger,numDisappointment)
    
    
def experimentTwo(eName, N, p,path, idIn, timeout):
    print "Starting Experiment 2"
    
    #assert N > 2
    name = "Experiment " + eName + " " +time.strftime("%d-%m-%Y") + "-" + time.strftime("%H-%M")
    directory = path + "\\" + name    
    
    logFileName = directory + "\\" + name + " log.txt"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    
    logFile = open(logFileName, 'w')
    
    idFile = "D:\\Libraries\\Python\\bayesact-emot-supplemental\\bactfiles\\fidentities.dat"
    
    #N > 2 students involved in a chain/cycle
    
    
    
    #Choose N random IDs
    ids = chooseIdentities(N, idFile, idIn)
    
    #choose emotion groups
    (emoGroup, numAnger, numDisappointment) = chooseEmotions(N)
    numNoEmo = N - (numAnger + numDisappointment)
    
    #Choose N random genders
    (genders,numFemale) = chooseGenders(N, p)
    
    numMale = N-numFemale
    logFile.write(eName + "\n")
    logFile.write("Number of participants: " + str(N) + "\n")
    logFile.write("Probability of a participant being female: " + str(p) + "\n")
    logFile.write("Number of male (female) participants: " + str(numMale) +" ("+str(numFemale)+")" + "\n")
    logFile.write("Number of anger participants: " + str(numAnger) + "\n")
    logFile.write("Number of disappointment participants: " + str(numDisappointment) + "\n")
    logFile.write("Number of no emotion participants: " + str(numNoEmo) + "\n")
    logFile.write("Timeout:" +str(timeout) + "\n")
    logFile.write("Fixed ID:" + idIn + "\n")
    
    #make names
    names = []
    for i in range(0, N):
        names.append("BayesActorEmo" + str(i))
    
    #First, make the N BayesActors and set them up.
    #There will need to be a way to set them up so they can observe two other actors
    
    oldstdout = sys.stdout

    specificLogFiles = []

    for i in range(0, N):
        sys.stdout = oldstdout
        print "Main loop iteration: ",i   
        
        specificLogFile = directory + "\\" + names[i] + "--"+str(i)+"-("+genders[i] + "," + ids[i]+","+emoGroup[i]+")log.txt"
        specificLogFiles.append(specificLogFile)
        logFile.write(names[i] + " is a " + genders[i] +" "+ ids[i] + " in group " + emoGroup[i] + " whose data is in " + specificLogFile + "\n")
        
        sys.stdout = open(specificLogFile, 'w')
        
        #let N, O play their game, from the perspective of P
        observeGame(names[i], genders[i], ids[i], emoGroup[i], timeout) #
        
    sys.stdout = oldstdout
    statFile =  directory + "\\" + name + " stats.txt"
    collectStats(specificLogFiles, statFile)
    
    print "Experiment 2 has terminated."
        
def collectStats(logs, pFile):

    pFile = open(pFile, 'w')
    results =[[[] for j in range(6)] for i in range(3)]    
    
    
    for i in range(0, len(logs)):
        lFile= open(logs[i])
        lines = lFile.readlines()
        
        if(logs[i].count("anger") > 0):
            c = 1
        elif(logs[i].count("disappointment") > 0):
            c = 2
        else:
            c = 0
        
        #print "c:",c
                
        for j in range(0, len(lines)):
            #print "line is: ",lines[j]
            if(lines[j].startswith("StatA")):
                value = (lines[j])[7:]
                results[c][0].append(float(value))
            elif(lines[j].startswith("StatB")):
                value = (lines[j])[7:]
                results[c][1].append(float(value))
            elif(lines[j].startswith("StatC")):
                value = (lines[j])[7:]
                results[c][2].append(float(value))
            elif(lines[j].startswith("StatD")):
                value = (lines[j])[7:]
                results[c][3].append(float(value))
            elif(lines[j].startswith("StatE")):
                value = (lines[j])[7:]
                results[c][4].append(float(value))                
            elif(lines[j].startswith("StatF")):
                value = (lines[j])[7:]
                results[c][5].append(float(value))
    #for i in range(6):
    #    print results[0][i]
    
    pFile.write("no emotion\n")
    for k in range(6):
        pFile.write(str(numpy.mean(results[0][k])) + "," + str(numpy.std(results[0][k])) + "\n")
        pFile.flush()
    pFile.write("anger\n")
    for k in range(6):
        pFile.write(str(numpy.mean(results[1][k])) + "," + str(numpy.std(results[1][k])) + "\n")
        pFile.flush()
    pFile.write("disappointment\n")
    for k in range(6):
        pFile.write(str(numpy.mean(results[2][k])) + "," + str(numpy.std(results[2][k])) + "\n")
        pFile.flush()
        
        
def observeGame(pName, pGender, pId, pEmoGroup, timeout):
    #randomly pick genders for each of N and O - p doesn't know these anyways.
    nGender = random.choice(["male","female"])
    oGender = random.choice(["male","female"])
    
    nBayes = EmoBayesActorTooB([pName+"-P-N", pGender, pId, pName+"-L-c",[],nGender, True, timeout])
    
    #get what P thinks N is
    n_pre_agent_avgs = nBayes.agent.getAverageState()    
    (nAid,nCid)=nBayes.agent.get_avg_ids(n_pre_agent_avgs.f)
    print "Wubben2011b:  Agent ",pName,"thinks it was most likely a: ",nAid
    print "Wubben2011b:  Agent ",pName,"thought you (N) were most likely a: ",nCid     
    nId = nCid     
    
    oBayes = EmoBayesActorTooB([pName+"-P-O", pGender, pId, pName+"-K-c",[],oGender, False, timeout])
    #get what P thinks o is
    o_pre_agent_avgs = oBayes.agent.getAverageState()    
    (oAid,oCid)=oBayes.agent.get_avg_ids(o_pre_agent_avgs.f)
    print "Wubben2011b:  Agent ",pName,"thinks it was most likely a: ",oAid
    print "Wubben2011b:  Agent ",pName,"thought you (O) were most likely a: ",oCid     
    oId = oCid         
    
    print 70*"$"
    print "Wubben2011b: starting to play the first indirect game."
    
    #observe the game (ignores actions from O to N, as we don't know what they are anyways
    noBayes = EmoBayesActorTooB([pName+"-NO-a", oGender, oId, pName+"-NO-b",nId,nGender, True, timeout])   
    noBayes = doThreeTurns(noBayes, oId,oGender, nId,nGender,pName, pEmoGroup, timeout)    



    #get what P thinks O thinks of N, since N provided some emotion to O
    no_pre_agent_avgs = noBayes.agent.getAverageState()    
    (noAid,noCid)=noBayes.agent.get_avg_ids(no_pre_agent_avgs.f)
    print "Wubben2011b:  Agent ",pName,"thinks it (O) was most likely a: ",noAid
    print "Wubben2011b:  Agent ",pName,"thought you (N) were most likely a: ",noCid     
    newNid = noCid
    
        
    print 70*"$"
    print "Wubben2011b: starting to consider player X."
    
    #pick a new id (for X), but first see if O's id has changed; use that instead
    newOid = noAid
    xId=[]
    xGender = random.choice(["male","female"])
    oBayesNew = EmoBayesActorTooB([pName+"-O-X", oGender, newOid, pName+"-O-X-b",xId,xGender, False, timeout])
    #oBayesNew decides if it wants to give to X or not
    oBayesNew.takeTurn(0)
    #get new O id after the action
    ox_pre_agent_avgs = oBayesNew.agent.getAverageState()    
    (oxAid,oxCid)=oBayesNew.agent.get_avg_ids(ox_pre_agent_avgs.f)
    print "Wubben2011b:  Agent ",pName,"thinks it (O) was most likely a: ",oxAid
    print "Wubben2011b:  Agent ",pName,"thought you (X) were most likely a: ",oxCid       
    newOid = oxAid
    finalXid = oxCid
    
    #make a new N bot - with the new idea of O - this represents N changing what it (or P's perception of N) thinks of O
    #...since newNObot never has things called on it, it probably is necessary to do this.
    #newNObot = EmoBayesActorTooB([pName+"-NO-2", nGender, newNid, pName+"-NO-2",newOid,oGender, False])
    #nno_pre_agent_avgs = newNObot.agent.getAverageState()    
    #(nnoAid,nnoCid)=newNObot.agent.get_avg_ids(nno_pre_agent_avgs.f)
    #print "Wubben2011b:  Agent ",pName,"thinks it (N) was most likely a: ",nnoAid
    #print "Wubben2011b:  Agent ",pName,"thought you (O) were most likely a: ",nnoCid       
    #newOid = nnoCid
    
    
    print 70*"$"
    print "Wubben2011b: determining if P wants to help O."
    #use latest id of O to make a P bot, determine if P wants to help O
    finalPObot = EmoBayesActorTooB([pName+"-O-2", pGender, pId, pName+"-O-2-b",newOid,oGender, False, timeout])
    finalPObot.takeTurn(0)
    
    #update id of P
    fpo_pre_agent_avgs = finalPObot.agent.getAverageState()    
    (fpoAid,fpoCid)=finalPObot.agent.get_avg_ids(fpo_pre_agent_avgs.f)
    print "Wubben2011b:  Agent ",pName,"thinks it (P) was most likely a: ",fpoAid
    print "Wubben2011b:  Agent ",pName,"thought you (O) were most likely a: ",fpoCid       
    newPid = fpoAid
    finalOid = fpoCid
    
    
    print 70*"$"
    print "Wubben2011b: sending an emotional message from N to P"    
    #use latest id of N to make a P bot, and have N communicate an emotion to P, if appropriate
    finalPNbot = EmoBayesActorTooB([pName+"-N-2", pGender, newPid, pName+"-N-2-b",newNid,nGender, True, timeout])
    finalPNbot.receiveEmotMessageBasicWrapper(pEmoGroup) #finalPNbot.receiveEmotMessageBasic(pEmoGroup) #april 1 change

    #update id of P for the last time
    fpn_pre_agent_avgs = finalPNbot.agent.getAverageState()    
    (fpnAid,fpnCid)=finalPNbot.agent.get_avg_ids(fpn_pre_agent_avgs.f)
    print "Wubben2011b:  Agent ",pName,"thinks it (P) was most likely a: ",fpnAid
    print "Wubben2011b:  Agent ",pName,"thought you (N) were most likely a: ",fpnCid       
    newPid = fpnAid
    finalNid = fpnCid
    finalPid = newPid
    print 70*"$"
    print "Wubben2011b: final P id established; this participant's simulation is complete."
    
    
    statA = computeA(finalOid,oGender,nGender,finalNid, pName, timeout)
    statC = computeC(finalOid,oGender,pGender,finalPid,pName, timeout)
    statD = computeD(finalPid,pGender,finalXid,xGender,pName,0,finalOid, oGender, timeout)
    statE = computeD(finalPid,pGender,finalXid,xGender,pName,10,finalOid, oGender, timeout)
    statF = computeF(finalOid,oGender,finalNid,nGender,pName, timeout)
    
    print "StatA:",statA
    print "StatB:",0
    print "StatC:",statC
    print "StatD:",statD
    print "StatE:",statE
    print "StatF:",statF
    
def computeA(oId,oGender,nGender,nId,pName, timeout):
    actor = EmoBayesActorTooB([pName+"-N-2", oGender, oId, pName+"-N-2-b",nId,nGender, False, timeout])
    (action, percent) = actor.getNextAction()
    if (action == "collab"):
        return convertToScale(percent)
    elif (action == "defect"):
        return (-1.0)*convertToScale(percent)
    else:
        return 0.0
    
def computeC(oId,oGender,pGender,pId,pName, timeout):
    actor = EmoBayesActorTooB([pName+"-N-2", pGender, pId, pName+"-N-2-b",oId,oGender, False, timeout])
    (action, percent) = actor.getNextActionBiasedCoop()
    return convertToScale(percent)

def computeD(pId,pGender,qId,qGender,pName, num, oId, oGender, timeout):
    #basically, P assumes that Q knows the identity of P after P donates num coins. Then Q decides (or at least P simulates this decision)
    
    #NOTE: roles are reversed for simplicity
    
    actor = EmoBayesActorTooB([pName+"-N-2", oGender, oId, pName+"-N-2-b",pId,pGender, True, timeout])
    actor.updateLastAction(num)

    pre_agent_avgs = actor.agent.getAverageState()    
    (Aid,Cid)=actor.agent.get_avg_ids(pre_agent_avgs.f)
    print "Wubben2011b:  Agent thinks it (O) was most likely a: ",Aid
    print "Wubben2011b:  Agent thought you (N) were most likely a: ",Cid  #this is what P thinks of itself *IN THIS CASE ONLY*  
    
    Qactor = EmoBayesActorTooB([pName+"-N-2", qGender, qId, pName+"-N-2-b",Cid,pGender, False, timeout])
    (collab, percent) = Qactor.getNextActionBiasedCoop()
    return convertToScale(percent)
    
def computeF(oId,oGender,nId,nGender,pName, timeout):
    actor = EmoBayesActorTooB([pName+"-N-2", oGender, oId, pName+"-N-2-b",nId,nGender, False, timeout])
    (collab, percent) = actor.getNextActionBiasedCoop()
    
    numDonated = int(percent*10)
    
    pre_agent_avgs = actor.agent.getAverageState()    
    (Aid,Cid)=actor.agent.get_avg_ids(pre_agent_avgs.f)
    print "Wubben2011b:  Agent thinks it (O) was most likely a: ",Aid
    print "Wubben2011b:  Agent thought you (N) were most likely a: ",Cid  
    
    actor = EmoBayesActorTooB([pName+"-N-2", oGender, Aid, pName+"-N-2-b",Cid,nGender, False, timeout])
    (collab, percent) = actor.getNextActionBiasedCoop()
    
    numDonated = numDonated + int(percent*10)    
    
    pre_agent_avgs = actor.agent.getAverageState()    
    (Aid,Cid)=actor.agent.get_avg_ids(pre_agent_avgs.f)
    print "Wubben2011b:  Agent thinks it (O) was most likely a: ",Aid
    print "Wubben2011b:  Agent thought you (N) were most likely a: ",Cid  
    
    actor = EmoBayesActorTooB([pName+"-N-2", oGender, Aid, pName+"-N-2-b",Cid,nGender, False, timeout])
    (collab, percent) = actor.getNextActionBiasedCoop()
    
    numDonated = numDonated + int(percent*10) 

    return numDonated
    
def doThreeTurns(bayes,oId,oGender,nId,nGender,pName,pEmoGroup, timeout):
    bayes.updateLastAction(8)
    print "Wubben2011b: first indirect game - turn 1 done"
    print "Wubben2011b: resetting - simulates a fair 'wait' "
    
    pre_agent_avgs = bayes.agent.getAverageState()    
    (Aid,Cid)=bayes.agent.get_avg_ids(pre_agent_avgs.f)
    print "Wubben2011b:  Agent thinks it (O) was most likely a: ",Aid
    print "Wubben2011b:  Agent thought you (N) were most likely a: ",Cid   
    
    bayes = EmoBayesActorTooB([pName+"-NO-a-2", oGender, Aid, pName+"-NO-b-2",Cid,nGender, True, timeout])   
    
    bayes.updateLastAction(8)
    print "Wubben2011b: first indirect game - turn 2 done"
    print "Wubben2011b: resetting - simulates a fair 'wait' "
    
    pre_agent_avgs = bayes.agent.getAverageState()    
    (Aid,Cid)=bayes.agent.get_avg_ids(pre_agent_avgs.f)
    print "Wubben2011b:  Agent thinks it (O-2) was most likely a: ",Aid
    print "Wubben2011b:  Agent thought you (N-2) were most likely a: ",Cid   
    
    bayesFinal = EmoBayesActorTooB([pName+"-NO-a-3", oGender, Aid, pName+"-NO-b-3",Cid,nGender, True, timeout]) 
    bayesFinal.updateLastActionWithEmotionBasic(8, pEmoGroup)
    print "Wubben2011b: first indirect game - turn 3 done"
    print "Wubben2011b: Note - agent is not reset"
    
    return bayesFinal

def experimentOne(eName, N, p,path, idIn, timeout):
    print "Starting Experiment 1"
    
    assert N > 2
    name = "Experiment " + eName + " " +time.strftime("%d-%m-%Y") + "-" + time.strftime("%H-%M")
    directory = path + "\\" + name    
    
    logFileName = directory + "\\" + name + " log.txt"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    
    logFile = open(logFileName, 'w')
    
    idFile = "D:\\Libraries\\Python\\bayesact-emot-supplemental\\bactfiles\\fidentities.dat"
    
    #N > 2 students involved in a chain/cycle
    
    
    
    #Choose N random IDs
    ids = chooseIdentities(N, idFile, idIn)
    
    #Choose N random genders
    (genders,numFemale) = chooseGenders(N, p)
    
    numMale = N-numFemale
    logFile.write(eName + "\n")
    logFile.write("Number of participants: " + str(N) + "\n")
    logFile.write("Probability of a participant being female: " + str(p) + "\n")
    logFile.write("Number of male (female) participants: " + str(numMale) +" ("+str(numFemale)+")" + "\n")
    logFile.write("Timeout:" +str(timeout) + "\n")
    logFile.write("Fixed ID:" + idIn + "\n")
    
    #make names
    names = []
    for i in range(0, N):
        names.append("BayesActorEmo" + str(i))
    
    #First, make the N BayesActors and set them up.
    #There will need to be a way to set them up so they can observe two other actors
    
    oldstdout = sys.stdout

    for i in range(0, N):
        sys.stdout = oldstdout
        print "Main loop iteration: ",i
        
        specificLogFile = directory + "\\" + names[i] + "--"+str(i)+"-("+genders[i] + "," + ids[i]+")log.txt"
        logFile.write(names[i] + " is a " + genders[i] +" "+ ids[i] + " whose data is in " + specificLogFile + "\n")
        
        sys.stdout = open(specificLogFile, 'w')
        
        print names[i],genders[i],ids[i]
        
        #perform first questionnaire
        (perceptionOfL, perceptionOfK, lGender, kGender) = firstQuestionnaire(names[i], ids[i], genders[i], timeout)
        print names[i],"for the first questionnaire, thought that L was a",perceptionOfL,"and K was a", perceptionOfK
        
        #now we must make agent i actually choose to donate to L
        bayesAgent = EmoBayesActorToo([names[i]+"-Choice", genders[i], ids[i], names[i]+"-L", perceptionOfL,lGender,False, timeout])
        (action, percent) = bayesAgent.getNextAction()
        
        pre_agent_avgs = bayesAgent.agent.getAverageState()
        (aid,cid)=bayesAgent.agent.get_avg_ids(pre_agent_avgs.f)
        #print "Agent thinks it was most likely a: ",aid
        #print "Agent thought you were most likely a: ",cid    
        
        print names[i],"actually decided to",action,"and now feels like a",aid
        print names[i],"now thinks L is a ",cid
        
        print 20*"#","Starting second questionnaire"
        #and now perform the second questionnaire
        secondQuestionnaire(names[i],aid,genders[i],cid,perceptionOfK, lGender, kGender, timeout)
        
        print 60*">>","Done with player",i
    
    sys.stdout = oldstdout
    print "Experiment finished."
        
     
def secondQuestionnaire(name, mId, mGender, perceptionOfL, perceptionOfK, lGender, kGender, timeout):
    
    lkBayesA = EmoBayesActorToo([name+"-M-L-Q2", lGender, perceptionOfL, name+"-M-K", perceptionOfK, kGender, True, timeout])
    lkBayesB = EmoBayesActorToo([name+"-M-L-Q2", lGender, perceptionOfL, name+"-M-K", perceptionOfK, kGender, True, timeout])
    lkBayesC = EmoBayesActorToo([name+"-M-L-Q2", lGender, perceptionOfL, name+"-M-K", perceptionOfK, kGender, True, timeout])
    
    
    scenarios = ["anger","disappointment","no emotion"]
    random.shuffle([scenarios])
    
    print "Wubben2011: 2ndQ: first scenario:", scenarios[0]
    
    #first scenario (whatever that is)
    lkBayesA.updateLastActionWithEmotionBasic(0, scenarios[0])
    lkA_pre_agent_avgs = lkBayesA.agent.getAverageState()
    (lkAaid,lkAcid)=lkBayesA.agent.get_avg_ids(lkA_pre_agent_avgs.f)
    print "Wubben2011: 2ndQ: first scenario: Agent thinks it was most likely a: ",lkAaid
    print "Wubben2011: 2ndQ: first scenario: Agent thought you were most likely a: ",lkAcid    
    newFeelingOfLA = lkAaid 
    
    newFeelingOfKA = lkAcid
    inferredCoopA = computeA(newFeelingOfKA, kGender, lGender, newFeelingOfLA, name, timeout)
    
    bayesA = EmoBayesActorToo([name+"-M-L-Q2-b-A", mGender, mId, name+"-Q2-L-A", newFeelingOfLA, lGender, False, timeout])
    (actionA, percentDonatedA) = bayesA.getNextAction()
    numCentsDonatedA = 200*percentDonatedA
    
    #second scenario
    print "Wubben2011: 2ndQ: second scenario:", scenarios[1]
    lkBayesB.updateLastActionWithEmotionBasic(0, scenarios[1])
    lkB_pre_agent_avgs = lkBayesB.agent.getAverageState()
    (lkBaid,lkBcid)=lkBayesB.agent.get_avg_ids(lkB_pre_agent_avgs.f)
    print "Wubben2011: 2ndQ: first scenario: Agent thinks it was most likely a: ",lkBaid
    print "Wubben2011: 2ndQ: first scenario: Agent thought you were most likely a: ",lkBcid    
    newFeelingOfLB = lkBaid
    
    newFeelingOfKB = lkBcid
    inferredCoopB = computeA(newFeelingOfKB, kGender, lGender, newFeelingOfLB, name, timeout)    
    
    bayesB = EmoBayesActorToo([name+"-M-L-Q2-b-B", mGender, mId, name+"-Q2-L-B", newFeelingOfLB, lGender, False, timeout])
    (actionB, percentDonatedB) = bayesB.getNextAction()
    numCentsDonatedB = 200*percentDonatedB   

    #third scenario 
    print "Wubben2011: 2ndQ: third scenario:", scenarios[2]
    lkBayesC.updateLastActionWithEmotionBasic(0, scenarios[2])
    lkC_pre_agent_avgs = lkBayesC.agent.getAverageState()
    (lkCaid,lkCcid)=lkBayesC.agent.get_avg_ids(lkC_pre_agent_avgs.f)
    print "Wubben2011: 2ndQ: first scenario: Agent thinks it was most likely a: ",lkCaid
    print "Wubben2011: 2ndQ: first scenario: Agent thought you were most likely a: ",lkCcid    
    newFeelingOfLC = lkCaid
    
    newFeelingOfKC = lkCcid
    inferredCoopC = computeA(newFeelingOfKC, kGender, lGender, newFeelingOfLC, name, timeout) 
        
    bayesC = EmoBayesActorToo([name+"-M-L-Q2-b-C", mGender, mId, name+"-Q2-L-C", newFeelingOfLC, lGender, False, timeout])
    (actionC, percentDonatedC) = bayesC.getNextAction()
    numCentsDonatedC = 200*percentDonatedC      
    
    print "Questionnaire 2 results for", name
    print "Situation A was", scenarios[0],"results:",actionA,numCentsDonatedA,newFeelingOfLA,inferredCoopA
    print "Situation B was", scenarios[1],"results:",actionB,numCentsDonatedB,newFeelingOfLB,inferredCoopB
    print "Situation C was", scenarios[2],"results:",actionC,numCentsDonatedC,newFeelingOfLC,inferredCoopC
            

def firstQuestionnaire(name, mId, mGender, timeout):
    
    #randomly pick genders for each of l and k - M doesn't know these anyways.
    lGender = random.choice(["male","female"])
    kGender = random.choice(["male","female"])

    
    lBayes = EmoBayesActorToo([name+"-M-L-c", mGender, mId, name+"-L-c",[],lGender, True, timeout])
    kBayes = EmoBayesActorToo([name+"-M-K-c", mGender, mId, name+"-K-c",[],kGender, True, timeout])
    
    print "Wubben2011: Actors set up for first questionnaire."
    
    l_pre_agent_avgs = lBayes.agent.getAverageState()
    (laid,lcid)=lBayes.agent.get_avg_ids(l_pre_agent_avgs.f)
    #print "Agent thinks it was most likely a: ",aid
    #print "Agent thought you were most likely a: ",cid    
    mPerceptionOfL = lcid
    
    k_pre_agent_avgs = kBayes.agent.getAverageState()
    (kaid,kcid)=kBayes.agent.get_avg_ids(k_pre_agent_avgs.f)
    #print "Agent thinks it was most likely a: ",aid
    #print "Agent thought you were most likely a: ",cid    
    mPerceptionOfK = kcid
    
    lBayesCopy = EmoBayesActorToo([name+"-M-L-d", mGender, mId, name+"-L-d",[],lGender, True, timeout])
    kBayesCopy = EmoBayesActorToo([name+"-M-K-d", mGender, mId, name+"-K-d",[],kGender, True, timeout])
    
    lc_pre_agent_avgs = lBayesCopy.agent.getAverageState()
    (lcaid,lccid)=lBayesCopy.agent.get_avg_ids(lc_pre_agent_avgs.f)
    #print "Agent thinks it was most likely a: ",aid
    #print "Agent thought you were most likely a: ",cid    
    mPerceptionOfLcopy = lccid
    
    kc_pre_agent_avgs = kBayesCopy.agent.getAverageState()
    (kcaid,kccid)=kBayesCopy.agent.get_avg_ids(kc_pre_agent_avgs.f)
    #print "Agent thinks it was most likely a: ",aid
    #print "Agent thought you were most likely a: ",cid    
    mPerceptionOfKcopy = kccid    


    print "Wubben2011: first questionnaire: perceptions acquired."
    
    #get anger of M if L defects
    #get disappointment of M if L defects
    #get anger of M if L collaborates    
    #get disappointment of M if L collaborates
    #also get distance to collaborate or abandon L 
    (lDefectAnger, lDefectDis, lCollabAnger, lCollabDis, lDistToDefectIfDefected, lDistToCollabIfDefected,lDistToDefectIfCollab, lDistToCollabIfCollab) = getResults(lBayes, lBayesCopy, True)

    #get anger of M if K defects
    #get disappointment of M if K defects
    #get anger of M if K collaborates    
    #get disappointment of M if K collaborates    
    (kDefectAnger, kDefectDis, kCollabAnger, kCollabDis, kDistToDefectIfDefected, kDistToCollabIfDefected,kDistToDefectIfCollab, kDistToCollabIfCollab) = getResults(kBayes, kBayesCopy, False)
    
    #L defects; K defects
    situationAanger = (lDefectAnger + kDefectAnger)/2
    situationAdis = (lDefectDis + kDefectDis)/2
    if(lDistToDefectIfDefected > lDistToCollabIfDefected):
        sitAwouldDonate = False
    else:
        sitAwouldDonate = True
    
    #L defects; K collabs
    situationBanger = (lDefectAnger + kCollabAnger)/2
    situationBdis = (lDefectDis + kCollabDis)/2
    if(lDistToDefectIfDefected > lDistToCollabIfDefected):
        sitBwouldDonate = False
    else:
        sitBwouldDonate = True    
    
    #L collabs, K defects
    situationCanger = (lCollabAnger + kDefectAnger)/2
    situationCdis = (lCollabDis + kDefectDis)/2    
    if(lDistToDefectIfCollab > lDistToCollabIfCollab):
        sitCwouldDonate = False
    else:
        sitCwouldDonate = True     
    
    #L collabs, K collabs
    situationDanger = (lCollabAnger + kCollabAnger)/2
    situationDdis = (lCollabDis + kCollabDis)/2
    if(lDistToDefectIfCollab > lDistToCollabIfCollab):
        sitDwouldDonate = False
    else:
        sitDwouldDonate = True 
    
    print "Printing scale results for",name
    print "Situation A:",convertToScale(situationAanger),",",convertToScale(situationAdis),",",getEmotionSummary(situationAanger, situationAdis),",",sitAwouldDonate
    print "Situation B:",convertToScale(situationBanger),",",convertToScale(situationBdis),",",getEmotionSummary(situationBanger, situationBdis),",",sitBwouldDonate
    print "Situation C:",convertToScale(situationCanger),",",convertToScale(situationCdis),",",getEmotionSummary(situationCanger, situationCdis),",",sitCwouldDonate
    print "Situation D:",convertToScale(situationDanger),",",convertToScale(situationDdis),",",getEmotionSummary(situationDanger, situationDdis),",",sitDwouldDonate
    
    
    mPerceptionOfKFinal = random.choice([mPerceptionOfK, mPerceptionOfKcopy])
    mPerceptionOfLFinal = random.choice([mPerceptionOfL, mPerceptionOfLcopy])
    
    
    return (mPerceptionOfLFinal, mPerceptionOfKFinal, lGender, kGender)
     
def getEmotionSummary(anger, disappointment):
    if(anger > disappointment):
        if (anger > 0.1):
            return "anger"
        else:
            return "no emotion"
    else:
        if(disappointment > 0.1):
            return "disappointment"
        else:
            return "no emotion"
    
def convertToScale(value):
    #print "Wubben2011: 1stQ: value:",value,float(1.0/7.0),1.0/7.0
    if (value >= 0.0 and value < (1.0/7.0)):
        return 1
    elif (value >= (1.0/7.0) and value < (2.0/7.0)):
        return 2
    elif (value >= (2.0/7.0) and value < (3.0/7.0)):
        return 3
    elif (value >= (3.0/7.0) and value < (4.0/7.0)):
        return 4
    elif (value >= (4.0/7.0) and value < (5.0/7.0)):
        return 5    
    elif (value >= (5.0/7.0) and value < (6.0/7.0)):
        return 6
    elif (value >= (6.0/7.0)):
        return 7        
    else:
        print "Wubben2011 - warning: scale conversion failed"
        return 1
    
def getResults(bayes, copy, shouldDecide):
    #EPA for anger
    AngerEPA = [-1.45, -0.30, 1.13]
    
    #EPA for disappointment
    DisappointmentEPA = [-1.71, -1.20, -1.34]
    
    #first, compute if defected
    bayes.updateLastAction(0);
    (defectEmoEPA, defectEmo) = bayes.getAgentEmotion()
    defectA = cosine_similarity(defectEmoEPA, AngerEPA)
    defectD = cosine_similarity(defectEmoEPA, DisappointmentEPA)
    

    
    #now, compute if donated
    copy.updateLastAction(10);
    (collabEmoEPA, collabEmo) = copy.getAgentEmotion()
    collabA = cosine_similarity(collabEmoEPA, AngerEPA)
    collabD = cosine_similarity(collabEmoEPA, DisappointmentEPA)
    
    print "Wubben2011: 1stQ: getting similarities, if necessary."
    
    if(shouldDecide):
        #currently not using percents
        (DdefectDistance, DdefectPercent, DcollabDistance, DcollabPercent) = bayes.getSimilarities()
        print "Wubben2011: 1stQ: similarities for bayes acquired."
        (CdefectDistance, CdefectPercent, CcollabDistance, CcollabPercent) = copy.getSimilarities()
        print "Wubben2011: 1stQ: similarities for bayes-copy acquired."
    else:
        (DdefectDistance, DdefectPercent, DcollabDistance, DcollabPercent) = (0,0,0,0)
        (CdefectDistance, CdefectPercent, CcollabDistance, CcollabPercent) = (0,0,0,0)
    
    return (defectA, defectD, collabA, collabD, DdefectDistance, DcollabDistance, CdefectDistance, CcollabDistance,)    

    
def cosine_similarity(v1,v2):
    #"compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    result = sumxy/math.sqrt(sumxx*sumyy)      
    return abs(result)

def collectEOneDataA():
    print "Collecting stats..."      
    
    #when done again, change just these directories. Should work fine, although some parts are untested (marked)
    
    outputFile = "D:\\Research Data\\CS886\\Wubben2011a\\Experiment E1-undergrad-full-long 08-04-2016-05-51\\undergrad-full-long-stats.txt"
    logs = [] 
    
    allfiles = os.listdir("D:\\Research Data\\CS886\\Wubben2011a\\Experiment E1-undergrad-full-long 08-04-2016-05-51")
    for i in range(0, len(allfiles)):
        print allfiles[i]
        if(allfiles[i].count("--") > 0):
            logs.append("D:\\Research Data\\CS886\\Wubben2011a\\Experiment E1-undergrad-full-long 08-04-2016-05-51\\" + allfiles[i])
            print "...appended"
    
    pFile = open(outputFile, 'w')
    
    #logs is the list of individual logs
    
    #first questionnaire data
    FQsituationA = [[],[]]
    FQsituationB = [[],[]]
    FQsituationC = [[],[]]
    FQsituationD = [[],[]]
    FQsitAdonate = 0
    FQsitBdonate = 0
    FQsitCdonate = 0
    FQsitDdonate = 0
    FQsitAdonateNot = 0
    FQsitBdonateNot = 0
    FQsitCdonateNot = 0
    FQsitDdonateNot = 0
    FQmoreAngryA = 0
    FQmoreDisappointedA = 0
    FQmoreAngryB = 0
    FQmoreDisappointedB = 0
    FQmoreAngryC = 0
    FQmoreDisappointedC = 0
    FQmoreAngryD = 0
    FQmoreDisappointedD = 0
    
    #disappointment, anger, none
    SQinferred = [ [], [], []]
    SQBooleanDonated = [ [], [], []]
    SQDonatedDisNot = 0
    SQDonatedAngNot = 0
    SQDonatedNoNot = 0  
    SQDonated = [ [], [], []] 
    
     
    
    #first, want to collect data to populate table 2 (1 in original)
    for i in range(0, len(logs)):
        lFile= open(logs[i])
        
        print "parsing file",logs[i]
        
        lines = lFile.readlines()
        
        for j in range(0, len(lines)):
            #print "line is: ",lines[j]
            if(lines[j].startswith("Situation A:")):
                afterSit = (lines[j])[12:]
                values = [x.strip() for x in afterSit.split(',')]
                feelingOfAnger = values[0]
                feelingOfDisappointment = values[1]
                emotionFelt = values[2]
                wouldDonate = values[3]
                #print feelingOfAnger
                FQsituationA[0].append(feelingOfAnger)
                FQsituationA[1].append(feelingOfDisappointment)
                
                if(emotionFelt=="anger"):
                    FQmoreAngryA = FQmoreAngryA + 1
                else:
                    FQmoreDisappointedA = FQmoreDisappointedA + 1
                    
                if(wouldDonate=="True"):
                    FQsitAdonate = FQsitAdonate + 1
                else:
                    FQsitAdonateNot = FQsitAdonateNot + 1
            elif(lines[j].startswith("Situation B:")):
                afterSit = (lines[j])[12:]
                values = [x.strip() for x in afterSit.split(',')]
                feelingOfAnger = values[0]
                feelingOfDisappointment = values[1]
                emotionFelt = values[2]
                wouldDonate = values[3]
                #print feelingOfAnger
                FQsituationB[0].append(feelingOfAnger)
                FQsituationB[1].append(feelingOfDisappointment)
                
                if(emotionFelt=="anger"):
                    FQmoreAngryB = FQmoreAngryB + 1
                else:
                    FQmoreDisappointedB = FQmoreDisappointedB + 1
                    
                if(wouldDonate=="True"):
                    FQsitBdonate = FQsitBdonate + 1
                else:
                    FQsitBdonateNot = FQsitBdonateNot + 1                
            elif(lines[j].startswith("Situation C:")):
                afterSit = (lines[j])[12:]
                values = [x.strip() for x in afterSit.split(',')]
                feelingOfAnger = values[0]
                feelingOfDisappointment = values[1]
                emotionFelt = values[2]
                wouldDonate = values[3]
                #print feelingOfAnger
                FQsituationC[0].append(feelingOfAnger)
                FQsituationC[1].append(feelingOfDisappointment)
                
                if(emotionFelt=="anger"):
                    FQmoreAngryC = FQmoreAngryC + 1
                else:
                    FQmoreDisappointedC = FQmoreDisappointedC + 1
                    
                if(wouldDonate=="True"):
                    FQsitCdonate = FQsitCdonate + 1
                else:
                    FQsitCdonateNot = FQsitCdonateNot + 1                
            elif(lines[j].startswith("Situation D:")):
                afterSit = (lines[j])[12:]
                values = [x.strip() for x in afterSit.split(',')]
                feelingOfAnger = values[0]
                feelingOfDisappointment = values[1]
                emotionFelt = values[2]
                wouldDonate = values[3]
                #print feelingOfAnger
                FQsituationD[0].append(float(feelingOfAnger))
                FQsituationD[1].append(float(feelingOfDisappointment))
                
                if(emotionFelt=="anger"):
                    FQmoreAngryD = FQmoreAngryD + 1
                else:
                    FQmoreDisappointedD = FQmoreDisappointedD + 1
                    
                if(wouldDonate=="True"):
                    FQsitDdonate = FQsitDdonate + 1
                else:
                    FQsitDdonateNot = FQsitDdonateNot + 1
                    
            #untested for rest of loop
            if(lines[j].startswith("Situation A was")):
                afterSit = (lines[j])[12:]
                values = [x.strip() for x in afterSit.split(' ')]
                emoWas = values[1] #[0] is 'was'
                action = values[3]
                numCents = values[4]
                label = values[5] #never used
                inferredCoop = values[6]
                
                if(emoWas=="disappointment"):
                    SQinferred[0].append(float(inferredCoop))
                    SQDonated[0].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedDisNot = SQDonatedDisNot + 1
                    else:
                        SQBooleanDonated[0].append(float(1))
                elif(emoWas=="anger"):
                    SQinferred[1].append(float(inferredCoop))
                    SQDonated[1].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedAngNot = SQDonatedAngNot + 1
                    else:
                        SQBooleanDonated[1].append(float(1))
                else:
                    #'no emotion is two tokens, so we need to change things
                    emoWasNo = values[1]
                    emoWasEmo = values[2]
                    results = values[3]
                    
                    action = values[4]
                    numCents = values[5]
                    label=values[6]
                    inferredCoop  = values[7]
                    
                    SQinferred[2].append(float(inferredCoop))
                    SQDonated[2].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedNoNot = SQDonatedNoNot + 1
                    else:
                        SQBooleanDonated[2].append(float(1))
                        
            if(lines[j].startswith("Situation B was")):
                afterSit = (lines[j])[12:]
                values = [x.strip() for x in afterSit.split(' ')]
                emoWas = values[1] #[0] is 'was'
                action = values[3]
                numCents = values[4]
                label = values[5] #never used
                inferredCoop = values[6]
                
                if(emoWas=="disappointment"):
                    SQinferred[0].append(float(inferredCoop))
                    SQDonated[0].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedDisNot = SQDonatedDisNot + 1
                    else:
                        SQBooleanDonated[0].append(float(1))
                elif(emoWas=="anger"):
                    SQinferred[1].append(float(inferredCoop))
                    SQDonated[1].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedAngNot = SQDonatedAngNot + 1
                    else:
                        SQBooleanDonated[1].append(float(1))
                else:
                    #'no emotion is two tokens, so we need to change things
                    emoWasNo = values[1]
                    emoWasEmo = values[2]
                    results = values[3]
                    
                    action = values[4]
                    numCents = values[5]
                    label=values[6]
                    inferredCoop  = values[7]
                                        
                    SQinferred[2].append(float(inferredCoop))
                    SQDonated[2].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedNoNot = SQDonatedNoNot + 1
                    else:
                        SQBooleanDonated[2].append(float(1))
                        
            if(lines[j].startswith("Situation C was")):
                afterSit = (lines[j])[12:]
                values = [x.strip() for x in afterSit.split(' ')]
                emoWas = values[1] #[0] is 'was'
                action = values[3]
                numCents = values[4]
                label = values[5] #never used
                inferredCoop = values[6]
                
                if(emoWas=="disappointment"):
                    SQinferred[0].append(float(inferredCoop))
                    SQDonated[0].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedDisNot = SQDonatedDisNot + 1
                    else:
                        SQBooleanDonated[0].append(float(1))
                elif(emoWas=="anger"):
                    SQinferred[1].append(float(inferredCoop))
                    SQDonated[1].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedAngNot = SQDonatedAngNot + 1
                    else:
                        SQBooleanDonated[1].append(float(1))
                else:
                    #'no emotion is two tokens, so we need to change things
                    emoWasNo = values[1]
                    emoWasEmo = values[2]
                    results = values[3]
                    
                    action = values[4]
                    numCents = values[5]
                    label=values[6]
                    inferredCoop  = values[7]
                    
                    SQinferred[2].append(float(inferredCoop))
                    SQDonated[2].append(float(numCents))
                    if(action=="defect"):
                        SQDonatedNoNot = SQDonatedNoNot + 1
                    else:
                        SQBooleanDonated[2].append(float(1))
                
    
    pFile.write("First Questionnaire Results\n")                
    ###A
    pFile.write("Situation A\n")
    pFile.write(str(FQmoreAngryA) + " of participants were more angry, " + str(FQmoreDisappointedA) + " were more disappointed\n")
    pFile.write(str(FQsitAdonate) + " of participants would donate, " + str(FQsitAdonateNot) + " would not\n")
    
    #print "what?"
    #print numpy.array(FQsituationA[0]).astype(numpy.float)
    #print "..."
    sitAangerMean = numpy.mean(numpy.array(FQsituationA[0]).astype(numpy.float))
    sitADisappointmentMean = numpy.mean(numpy.array(FQsituationA[1]).astype(numpy.float))
                                        
    #print "ok...", sitAangerMean
    
    sitAangerStd = numpy.std(numpy.array(FQsituationA[0]).astype(numpy.float))
    sitADisappointmentStd = numpy.std(numpy.array(FQsituationA[1]).astype(numpy.float))
    pFile.write("sitAangerMean,std ; sitAdisappointmentMean, std\n")
    pFile.write(str(sitAangerMean)+","+str(sitAangerStd)+"\n")
    pFile.write(str(sitADisappointmentMean)+","+str(sitADisappointmentStd)+"\n")
    
    sitAt, sitAp = stats.ttest_ind(numpy.array(FQsituationA[0]).astype(numpy.float), numpy.array(FQsituationA[1]).astype(numpy.float), equal_var=False)
    pFile.write("sitA t, p\n")
    pFile.write(str(sitAt) + "," + str(sitAp) + "\n")
    
    ###B
    pFile.write("\nSituation B\n")
    pFile.write(str(FQmoreAngryB) + " of participants were more angry, " + str(FQmoreDisappointedB) + " were more disappointed\n")
    pFile.write(str(FQsitBdonate) + " of participants would donate, " + str(FQsitBdonateNot) + " would not\n")

    sitBangerMean = numpy.mean(numpy.array(FQsituationB[0]).astype(numpy.float))
    sitBDisappointmentMean = numpy.mean(numpy.array(FQsituationB[1]).astype(numpy.float))
    
    sitBangerStd = numpy.std(numpy.array(FQsituationB[0]).astype(numpy.float))
    sitBDisappointmentStd = numpy.std(numpy.array(FQsituationB[1]).astype(numpy.float))
    pFile.write("sitBangerMean,std ; sitBdisappointmentMean, std\n")
    pFile.write(str(sitBangerMean)+","+str(sitBangerStd)+"\n")
    pFile.write(str(sitBDisappointmentMean)+","+str(sitBDisappointmentStd)+"\n")
    
    sitBt, sitBp = stats.ttest_ind(numpy.array(FQsituationB[0]).astype(numpy.float), numpy.array(FQsituationB[1]).astype(numpy.float), equal_var=False)
    pFile.write("sitB t, p\n")
    pFile.write(str(sitBt) + "," + str(sitBp) + "\n")    
    
    ###C
    pFile.write("\nSituation C\n")
    pFile.write(str(FQmoreAngryC) + " of participants were more angry, " + str(FQmoreDisappointedC) + " were more disappointed\n")
    pFile.write(str(FQsitCdonate) + " of participants would donate, " + str(FQsitCdonateNot) + " would not\n")
    
    sitCangerMean = numpy.mean(numpy.array(FQsituationC[0]).astype(numpy.float))
    sitCDisappointmentMean = numpy.mean(numpy.array(FQsituationC[1]).astype(numpy.float))
    
    sitCangerStd = numpy.std(numpy.array(FQsituationC[0]).astype(numpy.float))
    sitCDisappointmentStd = numpy.std(numpy.array(FQsituationC[1]).astype(numpy.float))
    pFile.write("sitCangerMean,std ; sitCdisappointmentMean, std\n")
    pFile.write(str(sitCangerMean)+","+str(sitCangerStd)+"\n")
    pFile.write(str(sitCDisappointmentMean)+","+str(sitCDisappointmentStd)+"\n")
    
    sitCt, sitCp = stats.ttest_ind(numpy.array(FQsituationC[0]).astype(numpy.float), numpy.array(FQsituationC[1]).astype(numpy.float), equal_var=False)
    pFile.write("sitC t, p\n")
    pFile.write(str(sitCt) + "," + str(sitCp) + "\n")
    
    
    ###D
    pFile.write("\nSituation D\n")
    pFile.write(str(FQmoreAngryD) + " of participants were more angry, " + str(FQmoreDisappointedD) + " were more disappointed\n")
    pFile.write(str(FQsitDdonate) + " of participants would donate, " + str(FQsitDdonateNot) + " would not\n")
    
    sitDangerMean = numpy.mean(numpy.array(FQsituationD[0]).astype(numpy.float))
    sitDDisappointmentMean = numpy.mean(numpy.array(FQsituationD[1]).astype(numpy.float))
    
    sitDangerStd = numpy.std(numpy.array(FQsituationD[0]).astype(numpy.float))
    sitDDisappointmentStd = numpy.std(numpy.array(FQsituationD[1]).astype(numpy.float))
    pFile.write("sitDangerMean,std ; sitDdisappointmentMean, std\n")
    pFile.write(str(sitDangerMean)+","+str(sitDangerStd)+"\n")
    pFile.write(str(sitDDisappointmentMean)+","+str(sitDDisappointmentStd)+"\n")
    
    sitDt, sitDp = stats.ttest_ind(numpy.array(FQsituationD[0]).astype(numpy.float), numpy.array(FQsituationD[1]).astype(numpy.float), equal_var=False)
    pFile.write("sitD t, p\n")
    pFile.write(str(sitDt) + "," + str(sitDp) + "\n")

    pFile.flush()
    
    #untested
    N = len(logs)
    
    pFile.write("\n\nSecond Questionnaire\n")
    pFile.write("\nDisappointment\n")
    pFile.write("inferred mean, std\n")
    disStd = numpy.std(numpy.array(SQinferred[0]).astype(numpy.float))
    disMean = numpy.mean(numpy.array(SQinferred[0]).astype(numpy.float))
    pFile.write(str(disMean)+","+str(disStd)+"\n")    
    SQDonatedDis = N - SQDonatedDisNot
    pFile.write(str(SQDonatedDis) + " donated, " + str(SQDonatedDisNot) + " did not\n")
    pFile.write("donatedcents mean, std\n")
    disStd = numpy.std(numpy.array(SQDonated[0]).astype(numpy.float))
    disMean = numpy.mean(numpy.array(SQDonated[0]).astype(numpy.float))  
    pFile.write(str(disMean) + "," + str(disStd)+"\n")
    infDt, infDp = stats.ttest_ind(numpy.array(SQinferred[0]).astype(numpy.float), numpy.array(SQinferred[2]).astype(numpy.float), equal_var=False)
    pFile.write("inferred t, p\n")
    pFile.write(str(infDt) + "," + str(infDp) + "\n")  
    boolDt, boolDp = stats.ttest_ind(numpy.array(SQBooleanDonated[0]).astype(numpy.float), numpy.array(SQBooleanDonated[2]).astype(numpy.float), equal_var=False)
    pFile.write("boolean donated t, p\n")
    pFile.write(str(boolDt) + "," + str(boolDp) + "\n")  
    donatedDt, donatedDP = stats.ttest_ind(numpy.array(SQDonated[0]).astype(numpy.float), numpy.array(SQDonated[2]).astype(numpy.float), equal_var=False)
    pFile.write("donatedcents t, p\n")
    pFile.write(str(donatedDt) + "," + str(donatedDP) + "\n")

    pFile.write("\nAnger\n")
    pFile.write("inferred mean, std\n")
    angStd = numpy.std(numpy.array(SQinferred[1]).astype(numpy.float))
    angMean = numpy.mean(numpy.array(SQinferred[1]).astype(numpy.float))
    pFile.write(str(angMean)+","+str(angStd)+"\n")    
    SQDonatedAng = N - SQDonatedAngNot
    pFile.write(str(SQDonatedAng) + " donated, " + str(SQDonatedAngNot) + " did not\n")
    pFile.write("donatedcents mean, std\n")
    angStd = numpy.std(numpy.array(SQDonated[1]).astype(numpy.float))
    angMean = numpy.mean(numpy.array(SQDonated[1]).astype(numpy.float))  
    pFile.write(str(angMean) + "," + str(angStd)+"\n")
    infAt, infAp = stats.ttest_ind(numpy.array(SQinferred[1]).astype(numpy.float), numpy.array(SQinferred[2]).astype(numpy.float), equal_var=False)
    pFile.write("inferred t, p\n")
    pFile.write(str(infAt) + "," + str(infAp) + "\n")  
    boolAt, boolAp = stats.ttest_ind(numpy.array(SQBooleanDonated[1]).astype(numpy.float), numpy.array(SQBooleanDonated[2]).astype(numpy.float), equal_var=False)
    pFile.write("boolean donated t, p\n")
    pFile.write(str(boolAt) + "," + str(boolAp) + "\n")  
    donatedAt, donatedAP = stats.ttest_ind(numpy.array(SQDonated[1]).astype(numpy.float), numpy.array(SQDonated[2]).astype(numpy.float), equal_var=False)
    pFile.write("donatedcents t, p\n")
    pFile.write(str(donatedAt) + "," + str(donatedAP) + "\n")

    pFile.write("\nNo emotion\n")
    pFile.write("inferred mean, std\n")
    noStd = numpy.std(numpy.array(SQinferred[2]).astype(numpy.float))
    noMean = numpy.mean(numpy.array(SQinferred[2]).astype(numpy.float))
    pFile.write(str(noMean)+","+str(noStd)+"\n")    
    SQDonatedNo = N - SQDonatedNoNot
    pFile.write(str(SQDonatedNo) + " donated, " + str(SQDonatedNoNot) + " did not\n")
    pFile.write("donatedcents mean, std\n")
    noStd = numpy.std(numpy.array(SQDonated[2]).astype(numpy.float))
    noMean = numpy.mean(numpy.array(SQDonated[2]).astype(numpy.float))  
    pFile.write(str(noMean) + "," + str(noStd)+"\n")
    
    pFile.flush()

def computeTtestsETwo():
    print "Computing t-tests..."      
    
    #outputFile = "D:\\Research Data\\CS886\\Wubben2011b\\Experiment E2-undergrad-long 07-04-2016-08-26\\undergrad-long-t-tests.txt"
    outputFile = "D:\\Research Data\\CS886\\Wubben2011b\\Experiment E2-similar-long 06-04-2016-21-58\\similar-long-t-tests.txt"
    logs = [] 
    
    #allfiles = os.listdir("D:\\Research Data\\CS886\\Wubben2011b\\Experiment E2-undergrad-long 07-04-2016-08-26")
    allfiles = os.listdir("D:\\Research Data\\CS886\\Wubben2011b\\Experiment E2-similar-long 06-04-2016-21-58")
    for i in range(0, len(allfiles)):
        print allfiles[i]
        if(allfiles[i].count("--") > 0):
            #logs.append("D:\\Research Data\\CS886\\Wubben2011b\\Experiment E2-undergrad-long 07-04-2016-08-26\\" + allfiles[i])
            logs.append("D:\\Research Data\\CS886\\Wubben2011b\\Experiment E2-similar-long 06-04-2016-21-58\\" + allfiles[i])
            print "...appended"
    
    pFile = open(outputFile, 'w')
    
        
    results =[[[] for j in range(6)] for i in range(3)]    
    
    
    for i in range(0, len(logs)):
        lFile= open(logs[i])
        lines = lFile.readlines()
        
        if(logs[i].count("anger") > 0):
            c = 1
        elif(logs[i].count("disappointment") > 0):
            c = 2
        else:
            c = 0
        
        #print "c:",c
                
        for j in range(0, len(lines)):
            #print "line is: ",lines[j]
            if(lines[j].startswith("StatA")):
                value = (lines[j])[7:]
                results[c][0].append(float(value))
            elif(lines[j].startswith("StatB")):
                value = (lines[j])[7:]
                results[c][1].append(float(value))
            elif(lines[j].startswith("StatC")):
                value = (lines[j])[7:]
                results[c][2].append(float(value))
            elif(lines[j].startswith("StatD")):
                value = (lines[j])[7:]
                results[c][3].append(float(value))
            elif(lines[j].startswith("StatE")):
                value = (lines[j])[7:]
                results[c][4].append(float(value))                
            elif(lines[j].startswith("StatF")):
                value = (lines[j])[7:]
                results[c][5].append(float(value))
    #for i in range(6):
    #    print results[0][i]
    
    pFile.write("anger-stat,t,p\n")
    for k in range(6):
        t_stat, p_value = stats.ttest_ind(results[1][k], results[0][k], equal_var=False)
        pFile.write(str(k) + "," + str(t_stat) + "," + str(p_value) + "\n")
        pFile.flush()
    pFile.write("disappointment-stat,t,p\n")
    for k in range(6):
        t_stat, p_value = stats.ttest_ind(results[2][k], results[0][k], equal_var=False)
        pFile.write(str(k) + "," + str(t_stat) + "," + str(p_value) + "\n")
        pFile.flush()        

if __name__ == "__main__":
    oldstdout = sys.stdout
    
    
    #main("E2-test", 100, 0.5, True, "NA", 5.0)
    #sys.stdout = oldstdout
    
    '''
    #experiment 1
    main("E1-similar", 30, 0.5, False, "NA", 5.0)
    sys.stdout = oldstdout
    
    main("E1-undergrad", 30, 0.5, False, "undergraduate", 5.0)
    sys.stdout = oldstdout    
    
    main("E1-similar-long", 30, 0.5, False, "NA", 30.0)
    sys.stdout = oldstdout
    
    main("E1-undergrad-long", 30, 0.5, False, "undergraduate", 30.0)
    sys.stdout = oldstdout
    
    #experiment 2
    main("E2-similar", 80, 0.67, True, "NA", 5.0)
    sys.stdout = oldstdout
    
    main("E2-undergrad", 80, 0.67, True, "undergraduate", 5.0)
    sys.stdout = oldstdout    
    
    main("E2-similar-long", 80, 0.67, True, "NA", 30.0)
    sys.stdout = oldstdout
    
    main("E2-undergrad-long", 80, 0.67, True, "undergraduate", 30.0)
    sys.stdout = oldstdout 
    '''   
    '''
    #experiment 1 (fixed to report that one statistic..)
    main("E1-similar-full", 30, 0.5, False, "NA", 5.0)
    sys.stdout = oldstdout
    
    main("E1-undergrad-full", 30, 0.5, False, "undergraduate", 5.0)
    sys.stdout = oldstdout    
    
    main("E1-similar-full-long", 30, 0.5, False, "NA", 30.0)
    sys.stdout = oldstdout
    
    main("E1-undergrad-full-long", 30, 0.5, False, "undergraduate", 30.0)
    sys.stdout = oldstdout
    '''
    
    #computeTtestsETwo()
    
    
    collectEOneDataA()
    print "Done running experiments for Wubben2011"