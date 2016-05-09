'''
Created on Mar 2, 2016

@author: jgorzny, Jesse Hoey
'''


from bayesactemot import *


class EmoBayesActorToo(object):
    
    def __init__(self, params):
        print("New BayesAct player created for a new game.")
        self.name = params[0]
        self.longName = "EmoBayesActorToo[" + self.name + "]"
        #value of coins
        self.score = 0.0
        
        #lastAction will be an integer saying how many coins the opponent gave
        #on the last round
        self.lastAction = -1
        
        self.turnNumber = 0
        
        #will be used to calculate emotion intensity
        self.shortScore = 0
        self.shortMax = 0
        
        #BayesAct initialization follows        
                
        #num_games = 10
        self.num_samples = 1000
        initial_px = [1.0,0.0,0.0]

        self.client_goes_first = params[6]
        print self.longName, "will the client go first?", self.client_goes_first
        if(self.client_goes_first):
            initial_learn_turn = "client"
        else:
            initial_learn_turn = "agent"

        #action_names = ["wait","cooperate","defect"]

        agent_gender=params[1]
        print self.longName, "gender is:", agent_gender
        #client_gender="male"

        fbfname = "D:\\Libraries\\Python\\bayesact-0.5.1\\fbehaviours.dat"
        fifname = "D:\\Libraries\\Python\\bayesact-0.5.1\\fidentities.dat"
    
        self.fbehaviours_agent=readSentiments(fbfname,agent_gender)
        #fbehaviours_client=readSentiments(fbfname,client_gender)
    
    #(agent_mean_ids,agent_cov_ids)=getIdentityStats(fifname,agent_gender)
    #(client_mean_ids,client_cov_ids)=getIdentityStats(fifname,client_gender)

        '''
        agent_id = params[2] #"friend"
    #agent_id=getIdentity(fifname,agent_id,agent_gender)
    #if agent_id==[]:
    #    agent_id=NP.random.multivariate_normal(agent_mean_ids,agent_cov_ids)
        print self.longName,"agent id is: ",agent_id

        agent_id=NP.asarray([agent_id]).transpose()
    '''
        agent_id = params[2]
        agent_id=getIdentity(fifname,agent_id,agent_gender)
        agent_id_epa = agent_id
        (agent_mean_ids,agent_cov_ids)=getIdentityStats(fifname,agent_gender)
        
        if agent_id==[]:
            agent_id=NP.random.multivariate_normal(agent_mean_ids,agent_cov_ids)
        print self.longName,"agent id is: ",agent_id,"(",params[2],")"

        agent_id=NP.asarray([agent_id]).transpose()        
        client_id = []  #unknown if agent_knowledge = 0
    

    #agent_knowledge = 0
        agent_knowledge = 5


        true_client_id = [2.75, 1.88, 1.38] #friend  
    #true_client_id = [-1.95,-0.92,-1.34]  #loser
    #true_client_id = [-2.15, -0.21, -0.54] #scrooge
    
        default_friend_id = [2.75, 1.88, 1.38]
    
        client_id_in = params[4]
        client_gender_in = params[5]
        print self.longName,"is a",client_gender_in, client_id_in,"(default, if [] is displayed, is",default_friend_id,")"
        if (isinstance(client_id_in, basestring)):
            print self.longName,"detected that the client id was passed in as a string. Performing EPA lookup."
            client_id_in=getIdentity(fifname,client_id_in,client_gender_in)
            print self.longName,"client is now considered as", client_id_in#,len(client_id_in)


        
        if(client_id_in == []):
            client_id_in = [2.75, 1.88, 1.38]

    #one of two possible identities for both
        if agent_knowledge == 5:
            client_id.append(NP.asarray([client_id_in]).transpose())
            client_id.append(NP.asarray([[-2.15, -0.21, -0.54]]).transpose())
    
            agent_id = []
            agent_id.append(NP.asarray([agent_id_epa]).transpose())
        #comment the next line out if we know the agent is a friend only
            agent_id.append(NP.asarray([[-2.15, -0.21, -0.54]]).transpose())


        learn_initx=[initial_learn_turn,initial_px]

        use_pomcp = True
        pomcp_timeout = params[7]

        (learn_tau_init,learn_prop_init,learn_beta_client_init,learn_beta_agent_init)=init_id(agent_knowledge,agent_id,client_id,true_client_id)
    #make this a bit smaller - so the agent is pretty sure that this guy is a friend
    #learn_beta_client_init=1.0
    #learn_beta_agent_init=0.5
    #learn_beta_client_init=0.5
        learn_beta_agent_init=1.5
        learn_beta_client_init=1.5

    #learn_prop_init = [0.25, 0.25, 0.25, 0.25]  #the default
    #learn_prop_init = [0.05, 0.15, 0.2, 0.6]  #the self is bit more scroogy, but don't know the other at all

        wait_fb = [0,0,0]  #not relevant since only happens on client turn
        cooperate_fb = [1.44,1.11,0.61]  #collaborate with
        defect_fb = [-2.28,-0.48,-0.84]  #abandon 
        
        self.coopVect = cooperate_fb
        self.defectVect = defect_fb

        fixed_policy = {}
        fixed_policy[0] = wait_fb
        fixed_policy[1] = cooperate_fb
        fixed_policy[2] = defect_fb

        observation_resolution = 2.5
        action_resolution = 1.5
        numcact = 5

        learn_agent = PDEmotAgentB(N=self.num_samples,alpha_value=1.0,
                          beta_value_client_init=learn_beta_client_init,
                          beta_value_agent_init=learn_beta_agent_init,
                          use_pomcp=use_pomcp, fixed_policy = fixed_policy,
                          numcact = numcact,
                          identities_file="D:\\Libraries\\Python\\bayesact-0.5.1\\fidentities.dat",
                          behaviours_file="D:\\Libraries\\Python\\bayesact-0.5.1\\fbehaviours.dat",
                          obsres = observation_resolution,actres = action_resolution, pomcp_timeout=pomcp_timeout)
        self.agent = learn_agent
        
        self.learn_avgs=learn_agent.initialise_array(learn_tau_init,learn_prop_init,learn_initx)
        
        self.last_aab = [0,0,0] #temp; never used like this
        self.last_paab = 0 #temp; never used like this
        self.opponentsName = params[3]
        

    def cosine_similarity(self,v1,v2):
    #"compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(v1)):
            x = v1[i]; y = v2[i]
            sumxx += x*x
            sumyy += y*y
            sumxy += x*y
        return sumxy/math.sqrt(sumxx*sumyy)

#Game methods
    def getAgentEmotion(self):
        emoEPA = self.agent.expectedEmotion("agent")
        emotion = self.agent.findNearestEmotion(emoEPA)
        print self.longName," is reporting that it feels: ", emotion," with EPA: ", emoEPA
        
        return (emoEPA, emotion)
        
      
    def getSimilarities(self):

        #Interface with BayesAct here
        #Should always be 'agent' interactions
        (learn_aab,learn_paab)=self.agent.get_next_action(self.learn_avgs,exploreTree=False)
        
        #print "action set:"
        #self.agent.pomcp_agent.ucTree.root.print_aset(1, sys.stdout)
        
        #print "fb " + str(self.fbehaviours_agent)
        print self.longName," aab: " + str(learn_aab)
        aact=findNearestBehaviour(learn_aab,self.fbehaviours_agent)
        
        
               
        print self.longName," suggested action for the agent is :",learn_aab,"\n  closest label is: ",aact
        #print "agent propositional action : ",learn_paab #not needed?
        
        #get the action, find which it is closest to: co-operate, or defect
        #if, e.g. cooperate is closest, give a percentage of coins based on distance to cooperate
        #e.g., if cooperate is suggested explicitly, give 10
        #if defect is suggested, give 0        
        coopDist = math.sqrt(raw_dist(self.coopVect,learn_aab))
        defectDist = math.sqrt(raw_dist(self.defectVect,learn_aab))
        #cooperate
        percentCoop = abs(self.cosine_similarity(self.coopVect, learn_aab))
        percentDefect = abs(self.cosine_similarity(self.defectVect, learn_aab))
            
        return (defectDist,percentDefect,coopDist,percentCoop)
            
    
        
             
    def getNextAction(self):
        #Interface with BayesAct here
        #Should always be 'agent' interactions
        #print self.longName,"learn_avgs -->",str(self.learn_avgs)
        
        (learn_aab,learn_paab)=self.agent.get_next_action(self.learn_avgs,exploreTree=False)
                
        #print "fb " + str(self.fbehaviours_agent)
        print self.longName," aab: " + str(learn_aab)
        aact=findNearestBehaviour(learn_aab,self.fbehaviours_agent)
        
        
               
        print self.longName," suggested action for the agent is :",learn_aab,"\n  closest label is: ",aact
        #print "agent propositional action : ",learn_paab #not needed?
        
        #get the action, find which it is closest to: co-operate, or defect
        coopDist = math.sqrt(raw_dist(self.coopVect,learn_aab))
        defectDist = math.sqrt(raw_dist(self.defectVect,learn_aab))
        if(coopDist < defectDist):
            #cooperate
            percent = abs(self.cosine_similarity(self.coopVect, learn_aab))
            print self.longName,"wants to cooperate."
            result = "collab"
        else:
            #defect
            percent = abs(self.cosine_similarity(self.defectVect, learn_aab))
            print self.longName,"wants to defect."
            result = "defect"
            
        return (result, percent)
            
    def takeTurn(self, turnNumber):
        print(self.longName + " is taking turn " + str(self.turnNumber))
        toGive = 0

        #Interface with BayesAct here
        #Should always be 'agent' interactions
        (learn_aab,learn_paab)=self.agent.get_next_action(self.learn_avgs,exploreTree=False)
        
        #print "action set:"
        #self.agent.pomcp_agent.ucTree.root.print_aset(1, sys.stdout)
        
        #print "fb " + str(self.fbehaviours_agent)
        print self.longName," aab: " + str(learn_aab)
        aact=findNearestBehaviour(learn_aab,self.fbehaviours_agent)
        
        
               
        print self.longName," suggested action for the agent is :",learn_aab,"\n  closest label is: ",aact
        #print "agent propositional action : ",learn_paab #not needed?
        
        #get the action, find which it is closest to: co-operate, or defect
        #if, e.g. cooperate is closest, give a percentage of coins based on distance to cooperate
        #e.g., if cooperate is suggested explicitly, give 10
        #if defect is suggested, give 0        
        coopDist = math.sqrt(raw_dist(self.coopVect,learn_aab))
        defectDist = math.sqrt(raw_dist(self.defectVect,learn_aab))
        percent = 0
        if(coopDist < defectDist):
            #cooperate
            percent = abs(self.cosine_similarity(self.coopVect, learn_aab))
            print self.longName,"wants to cooperate with similarity",percent             
            toGive = abs(round(percent * 10))
        else:
            #defect
            percent = abs(self.cosine_similarity(self.defectVect, learn_aab))
            print self.longName,"wants to defect with similarity",percent 
            
            toGive = abs(round((1-percent) * 10))
        
        self.last_aab = learn_aab
        self.last_paab = learn_paab
        print(self.longName + " is giving " + str(toGive) + " coins. (Keeping " + str((10-toGive)) + " coins.)")
        
        learn_xobserv = [State.turnnames.index("client"),0]#[1]#[State.turnnames.index("agent"),1] #[1]
        learn_observ = []
        self.learn_avgs=self.agent.propagate_forward(self.last_aab,learn_observ,learn_xobserv,self.last_paab)        
        
        return toGive
        
    def updateScore(self, numReceived, numKept):
        self.score = self.score + numReceived + (0.5 * numKept)
        
    def updateLastAction(self, numReceived):
        self.lastAction = numReceived

        '''
        Following in the line of Asghar and Hoey, we convey only 'abandon' or 
        'collaborate with' for non-message updates to our agent. We round up, so
        that 5 or more coins is 'collaborate with'.
        '''
        
        
        #if(self.turnNumber == 1):
        #    learn_xobserv = [State.turnnames.index("client"),0]
        #else:
        #    learn_xobserv = [State.turnnames.index("agent"),2]#[1]#[State.turnnames.index("agent"),1] #[1]
        learn_xobserv = [State.turnnames.index("agent"),2]#[1]#[State.turnnames.index("agent"),1] #[1]
        
        print self.longName +" " + str(self.last_aab) + " and " + str(self.last_paab) + " and " + str(self.learn_avgs) + " and numReceived: " + str(numReceived)

        #TODO: check these values
        collabVect = [1.44, 1.11, 0.61]
        abandonVect = [-2.28, -0.48, -0.84]
        
        if(numReceived > 4):
            learn_observ = collabVect
            learn_xobserv[1] = 1
        else:
            learn_observ = abandonVect
            learn_xobserv[1] = 2
            
        #This seems to be a technical hack; it sets up values so that the next agent call works?
        #TODO: avoid if at all possible; probably going to cause issues later.        
        #Note: this is not the only occurrence of this hack
        (learn_aab,learn_paab)=self.agent.get_next_action(self.learn_avgs,exploreTree=False)

        print self.longName,"about to prune",learn_observ,learn_xobserv
        self.learn_avgs=self.agent.propagate_forward([],learn_observ,learn_xobserv,0) #self.last_paab
        
    def updateLastActionWithEmotion(self, numReceived, intensity, emotion):
        self.lastAction = numReceived

        '''
        Following in the line of Asghar and Hoey, we convey only 'abandon' or 
        'collaborate with' for non-message updates to our agent. We round up, so
        that 5 or more coins is 'collaborate with'.
        '''
        
        
        #if(self.turnNumber == 1):
        #    learn_xobserv = [State.turnnames.index("client"),0]
        #else:
        #    learn_xobserv = [State.turnnames.index("agent"),2]#[1]#[State.turnnames.index("agent"),1] #[1]
        learn_xobserv = [State.turnnames.index("agent"),2]#[1]#[State.turnnames.index("agent"),1] #[1]
        
        print self.longName +" " + str(self.last_aab) + " and " + str(self.last_paab) + " and " + str(self.learn_avgs)

        #TODO: check these values
        collabVect = [1.44, 1.11, 0.61]
        abandonVect = [-2.28, -0.48, -0.84]
        
        if(numReceived > 4):
            learn_observ = collabVect
            learn_xobserv[1] = 1
        else:
            learn_observ = abandonVect
            learn_xobserv[1] = 2
            
        
        #TODO: need to add client's feeling here, occasionally.
        pre_agent_avgs = self.agent.getAverageState()
        (aid,cid)=self.agent.get_avg_ids(pre_agent_avgs.f)
        print self.longName,"Before Message: Agent thinks it was most likely a: ",aid
        print self.longName, "Before Message: Agent thought you were most likely a: ",cid
        
        cemot_epa = self.receiveEmotMessage(intensity, emotion)
        print self.longName,"Observed that the other player felt",cemot_epa
        print self.longName,":",self.opponentsName,"felt",cemot_epa
        print self.longName,"about to prune",learn_observ,learn_xobserv
        self.learn_avgs=self.agent.propagate_forward([],learn_observ,learn_xobserv,0,False,None,eTurn.learner,cemot_epa) #self.last_paab
        
        post_agent_avgs = self.agent.getAverageState()
        (aid,cid)=self.agent.get_avg_ids(post_agent_avgs.f)
        print self.longName,"After Message: Agent thinks it is most likely a: ",aid
        print self.longName,"After Message: Agent thought you are most likely a: ",cid  
        
         
    def updateLastActionWithEmotionBasic(self, numReceived, emotion):
        self.lastAction = numReceived

        '''
        Following in the line of Asghar and Hoey, we convey only 'abandon' or 
        'collaborate with' for non-message updates to our agent. We round up, so
        that 5 or more coins is 'collaborate with'.
        '''
        
        
        #if(self.turnNumber == 1):
        #    learn_xobserv = [State.turnnames.index("client"),0]
        #else:
        #    learn_xobserv = [State.turnnames.index("agent"),2]#[1]#[State.turnnames.index("agent"),1] #[1]
        learn_xobserv = [State.turnnames.index("agent"),2]#[1]#[State.turnnames.index("agent"),1] #[1]
        
        print self.longName +" " + str(self.last_aab) + " and " + str(self.last_paab) + " and " + str(self.learn_avgs)

        #TODO: check these values
        collabVect = [1.44, 1.11, 0.61]
        abandonVect = [-2.28, -0.48, -0.84]
        
        if(numReceived > 4):
            learn_observ = collabVect
            learn_xobserv[1] = 1
        else:
            learn_observ = abandonVect
            learn_xobserv[1] = 2
            
        
        pre_agent_avgs = self.agent.getAverageState()
        (aid,cid)=self.agent.get_avg_ids(pre_agent_avgs.f)
        print self.longName,"Before Message: Agent thinks it was most likely a: ",aid
        print self.longName, "Before Message: Agent thought you were most likely a: ",cid
        
        cemot_epa = self.receiveEmotMessageBasic(emotion)
        print self.longName,"Observed that the other player felt",cemot_epa
        print self.longName,":",self.opponentsName,"felt",cemot_epa
        print self.longName,"about to prune",learn_observ,learn_xobserv
        
        #This seems to be a technical hack; it sets up values so that the next agent call works?
        #TODO: avoid if at all possible; probably going to cause issues later.        
        #Note: this is not the only occurrence of this hack\
        print "EmoBayesActorToo---begin ignore"
        (learn_aab,learn_paab)=self.agent.get_next_action(self.learn_avgs,exploreTree=False)
        print "EmoBayesActorToo---end ignore"
                                                          
        #print 30*"@", learn_aab,learn_paab
        
        self.learn_avgs=self.agent.propagate_forward([],learn_observ,learn_xobserv,0,False,None,eTurn.learner,cemot_epa) #self.last_paab
        
        post_agent_avgs = self.agent.getAverageState()
        (aid,cid)=self.agent.get_avg_ids(post_agent_avgs.f)
        print self.longName,"After Message: Agent thinks it is most likely a: ",aid
        print self.longName,"After Message: Agent thought you are most likely a: ",cid
           
           
    def increaseTurnNum(self):
        self.turnNumber = self.turnNumber + 1
        
    def reportScore(self):
        print(self.longName + " has " + str(self.score) + " coins.")
        

    def receiveEmotMessage(self, intensity, emotion):
        print self.longName,"Extra message received."
                
        if(emotion == "anger"):
            if(intensity == 0):
                result = "no emotion"
            elif (intensity == 1):
                result = "bitter"
            elif (intensity == 2):
                result = "disapproving"
            elif (intensity == 3):
                result = "mean"
            elif (intensity == 4):
                result = "annoyed"
            elif (intensity == 5):
                result = "angry"
            elif (intensity == 6):
                result = "indignant"
            elif (intensity == 7):
                result = "mad"
            elif (intensity == 8):
                result = "furious"
            elif (intensity == 9):
                result = "irate"
            elif (intensity == 10):
                result = "enraged"
        elif(emotion == "disappointment"):
            if(intensity == 0):
                result = "no emotion"
            elif (intensity == 1):
                result = "upset"
            elif (intensity == 2):
                result = "distressed"
            elif (intensity == 3):
                result = "unhappy"
            elif (intensity == 4):
                result = "discouraged"                
            elif (intensity == 5):
                result = "disappointed"
            elif (intensity == 6):
                result = "discontented"
            elif (intensity == 7):
                result = "downhearted"
            elif (intensity == 8):
                result = "frustrated"
            elif (intensity == 9):
                result = "dissatisfied"
            elif (intensity == 10):
                result = "depressed"
        else:
            result = "no emotion"
            
        
        epaVal = self.agent.lookUpEmotionLabel(result, self.agent.emotdict)
        
        print self.longName,"observed that",self.opponentsName,"felt",result,"with EPA value",epaVal
        return epaVal
    
    def receiveEmotMessageBasic(self, emotion):
        print self.longName,"Extra message received."
                
        if(emotion == "anger"):
            result = "angry"
        elif(emotion == "disappointment"):
            result = "disappointed"
        else:
            result = "no emotion"
            
        
        epaVal = self.agent.lookUpEmotionLabel(result, self.agent.emotdict)
        
        print self.longName,"observed that",self.opponentsName,"felt",result,"with EPA value",epaVal
        return epaVal
   
                
    def receiveMessage(self, intensity, emotion):
        print self.longName,"Extra message received."
                
        if(emotion == "anger"):
            if(intensity == 0):
                #chat with
                print self.longName,"observed that",self.opponentsName,"felt","chat with"
                result = [1.9,0.82,0.71]
            elif (intensity == 1):
                #discipline
                print self.longName,"observed that",self.opponentsName,"felt","discipline"
                result = [0.66,1.76,0.83]
            elif (intensity == 2):
                #tell off
                print self.longName,"observed that",self.opponentsName,"felt","tell off"
                result = [-0.89,0.98,1.63]
            elif (intensity == 3):
                #accuse
                print self.longName,"observed that",self.opponentsName,"felt","accuse"
                result = [-1.03,0.26,0.29]
            elif (intensity == 4):
                #scold
                print self.longName,"observed that",self.opponentsName,"felt","scold"
                result = [-1.25,1.19,1.3]
            elif (intensity == 5):
                #malign
                print self.longName,"observed that",self.opponentsName,"felt","malign"
                result = [-1.49,0.84,0.53]
            elif (intensity == 6):
                #scowl at
                print self.longName,"observed that",self.opponentsName,"felt","scowl at"
                result = [-1.65,0.05,0.12]
            elif (intensity == 7):
                #hound
                print self.longName,"observed that",self.opponentsName,"felt","hound"
                result = [-1.7,-0.19,0.55]
            elif (intensity == 8):
                #scream at
                print self.longName,"observed that",self.opponentsName,"felt","scream at"
                result =   [-1.79,0.45,2.03]                                      
            elif (intensity == 9):
                #snarl at
                print self.longName,"observed that",self.opponentsName,"felt","snarl at"
                result = [-1.89,0.07,0.58]
            else:
                #berate
                print self.longName,"observed that",self.opponentsName,"felt","berate"
                result = [-1.89,-0.19,0.83]

        else:
            if(intensity == 0):
                #discuss something with
                print self.longName,"observed that",self.opponentsName,"felt","discuss something with"
                result = [1.53,1.19,0.18]
            elif (intensity == 1):
                #oppose
                print self.longName,"observed that",self.opponentsName,"felt","oppose"
                result = [0.05,0.83,0.87]
            elif (intensity == 2):
                #lecture
                print self.longName,"observed that",self.opponentsName,"felt","lecture"
                result = [-0.28,0.31,0.35]
            elif (intensity == 3):
                #say farewell to
                print self.longName,"observed that",self.opponentsName,"felt","say farewell to"
                result = [-0.3,0.27,-1.03]
            elif (intensity == 4):
                #rebuff
                print self.longName,"observed that",self.opponentsName,"felt","rebuff"
                result = [-0.4,0.47,0.31]
            elif (intensity == 5):
                #scrutinize
                print self.longName,"observed that",self.opponentsName,"felt","scrutinize"
                result = [-1.11,-0.47,-0.48]
            elif (intensity == 6):
                #disparage
                print self.longName,"observed that",self.opponentsName,"felt","disparage"
                result = [-1.29,-0.71,-0.17]
            elif (intensity == 7):
                #demote
                print self.longName,"observed that",self.opponentsName,"felt","demote"
                result = [-1.31,0.07,-0.77]
            elif (intensity == 8):
                #denigrate
                print self.longName,"observed that",self.opponentsName,"felt","denigrate"
                result = [-1.73,-0.13,-0.08]                 
            elif (intensity == 9):
                #demean
                print self.longName,"observed that",self.opponentsName,"felt","demean"
                result = [-1.83,-0.33,-0.06]
            else:
                #degrade
                print self.longName,"observed that",self.opponentsName,"felt","degrage"
                result = [-2.35,-0.28,-0.23]
        
        return result
    
   
             
class PDEmotAgentB(EmotionalAgent):
    def __init__(self,*args,**kwargs):

        super(PDEmotAgentB, self).__init__(self,*args,**kwargs)
        #x for the PDEmotAgent is a tuple - see pd/pdpomdp3.spudd
        #the first value is the turn (always this way for any Agent)
        #the second value is the agent's play (null, cooperate or defect)
        #the third value is the client's play (null, cooperate or defect)


        self.xvals=["null","coop","defect"]

        self.action_names = ["wait","cooperate","defect"]
        self.x_avg=[0,0,0]
        
        #probability distribution over play
        self.px = [1.0,0.0,0.0]
        #probability the client will cooperate or defect, for each of the
        #est found actions
        #self.client_cooppd = [0.5,0.5]
        self.client_cooppd = {}
        self.client_cooppd[0] = [0.0,0.5,0.5]  #wait, so we draw randomly
        #affective action is closer to collaborate, so more likely agent will cooperate
        self.client_cooppd[1] = [0.0,1.0,0.0]  #this was 0.9,0.1 for some reason -- probably just to make it so there can be some inconsistency in the client and it won't be totally missed
        #affective action is closer to abandon, so more likely
        self.client_cooppd[2] = [0.0,0.0,1.0]

        self.numDiscActions=3    #wait, cooperate, defect

    def print_params(self):
        EmotionalAgent.print_params(self)
        print "probability the client will cooperate: ",self.client_cooppd


    def initialise_x(self,initx=None):
        if not initx:
            initpx=self.px
            initturn=State.turnnames.index("agent")  #hard-coded agent start
        else:
            initpx=initx[1]
            initturn=State.turnnames.index(initx[0])
        #draw a sample from initx 
        a_initx=list(NP.random.multinomial(1,initpx)).index(1)
        c_initx=list(NP.random.multinomial(1,initpx)).index(1)
        return [initturn,a_initx,c_initx]


    #this gets the most likely client actions which would be most
    #consistent with the action fb as taken, but only consider cooperate and defect
    #as the "wait" action is only for use on client turn 
    def get_paab_dist(self,fb):
        mindist = -1
        mini = 0
        for i in range(2):
            thedist = raw_dist(self.fixed_policy[i+1],fb)
            if i==0 or thedist < mindist:
                mindist = thedist
                mini = i
        return (mindist,mini+1)

    #gets the distribution over client actions according to consistency with fb
    def get_paab_distro(self,fb):
        thedist = []
        for i in range(2):
            thedist.append(raw_dist(self.fixed_policy[i+1],fb))
        
        thedistro = map(lambda x: math.exp(-0.125*x),thedist)
        totweight = sum(thedistro)
        if totweight < 1e-12:
            thedistro = map(lambda x: 0.01,thedist)
            totweight = sum(thedistro)
        return map(lambda x: x/totweight,thedistro)
        

    #get the fb that is most consistent with the value of paab given
    #assumes fixed_policy is set with the values appropriately
    def get_consistent_fb(self,paab):
        
        wait_fb = self.fixed_policy[0]   #[0,0,0]  #not relevant since only happens on client turn
        cooperate_fb = self.fixed_policy[1] #[1.44,1.11,0.61]  #collaborate with
        defect_fb = self.fixed_policy[2]  #[-2.28,-0.48,-0.84]  #abandon 
        
        if paab == 0:
            aab = wait_fb
        elif paab == 1:
            aab = cooperate_fb
        else:
            aab = defect_fb
        return aab


    
    #agent can take an f_b that is consistent with his interpretation of the identities
    #however, this f_b is not sent to the other agent as such, instead the consistent_fb is 
    #sent according to the chosen paab of the agent (e.g. if it cooperates, cooperate_fb is received by the client)
    #we assume though that the agent updates his belief according to his chosen f_b ... that is sort of fucked up
    #if this oracle function is not overridden from Agent class, then the agent will use the fixed_policy 
    #(notice that that is commented out below), and so will always take one of two actions both during
    #POMCP planning and during execution.  This puts the "cognitive" before the "affective" though and means
    #that there is a disconnect between what the agent is considering as action and what is consistent with 
    #his interpretation of the identities.  For example, if he thinks both he and client are "friends", then
    #he can choose to defect as he predicts the client will cooperate, and he will get higher reward with no
    #penalty (there is no reward for deflection specifically)

    def oracle(self,state,rollout=False,samplenum=None):
        #continuous component is just a 3D EPA vector which is the null value on client turn
        #the discrete component of the action is class dependent
        #here, if it is the client's turn, we simply use the null action for both
        #and in any case, the propositional action is always the same (0 = null)
        (a,paab)  = self.get_null_action()

        if state.get_turn()=="agent":
            #this orale is not for use with the fixed policy
            #if not self.fixed_policy==None:
            #    paab = self.get_prop_action(state,rollout,samplenum)
            #     return (self.fixed_policy[paab],paab)
            #the first sample returned is the default (ACT) action
            #don't want to do this anymore either because the deafult action is not so relevant here
            #we are starting with values of fb that are close to optimal for the identities, and then recovering paab from that
            #if not rollout and samplenum==0:
            #    (a,paab)=self.get_default_action(state)
            #else:
            if True:
                #afterwards, it is a random selection
                #and paab is always 0 anyways
                #isiga_pomcp is much smaller than isiga
                usesiga=self.isiga_pomcp
                #when doing a rollout, want to cast a wider net?
                if rollout:
                    usesiga=self.isiga
                fsampler = FVarSampler(usesiga, self.isigf_unconstrained_b, \
                                       state.tau, state.f, self, \
                                       state.get_turn())
                tmpfv = fsampler.sampleNewFVar()

                a = map(lambda x: float(x), tmpfv[3:6])
                
                #find closest propositional action to this fb value and we add that
                (mindist,mini) = self.get_paab_dist(tmpfv[3:6])
                paab = mini
                #print "tmpfv was : ",tmpfv[3:6]," mini is ",mini," paab is ",paab
        return (a,paab)


    #overloaded from Agent as I want to make sure the first
    #action returned is the one that is "consistent" with the paab chosen
    
    #get the predicted actions for the client, based on
    #what the agent would normally do in the same situation
    #def get_default_predicted_action(self,state):
    #    #default ACT action selectors (see Bayesact paper)
    #    paab = self.get_prop_action(state)
    #    aab = self.get_consistent_fb(paab)
    #    return (aab,paab)

        
    #default propositional action policy
    def get_prop_action(self,state,rollout=False,samplenum=0):
        #for POMCP use this because it will be calling this during rollouts - this is the rollout policy
        #for propositional actions
        if self.use_pomcp:
            if rollout:
                return NP.random.randint(self.numDiscActions-1)+1   #only use the two that are relevant - cooperate (1) and defect (2)
            else:
                return (samplenum%(self.numDiscActions-1))+1 #loop through them one by one, but only (1) and (2)
        else:
            if state.get_turn() == "client":
                return 0  #wait
            else:
                return 1  #cooperate

    #aab is the affective part of the action, paab is the propositional part
    def sampleXvar(self,f,tau,state,aab,paab):
        turn = state.get_turn()
        ag_play = state.x[1]
        cl_play = state.x[2]
        new_ag_play = 0
        new_cl_play = 0
        #client action is independent of agent action, since the turns are fixed
        #this is "previous turn" in fact
        if turn == "client":  
            #new_cl_play = list(NP.random.multinomial(1,self.client_cooppd)).index(1)  #random choice for client
            #the client will act the most consistently with his value of fb
            #compute distance from cooperate and defect, and pick randomly according to the closer one
            #mini here will be 1=cooperate and 2=defect  ... so awkward
            
            ##old way:
            
            #(mindist,mini) = self.get_paab_dist(f[3:6])

            #print 100*"%"
            #print "client does fb: ",f[3:6]
            #print "closest action is ",self.action_names[mini]," at a distance of ",mindist
            #could use it directly, or draw sample
            #new_cl_play = mini
            #old way: was like this
            
            #new_cl_play = list(NP.random.multinomial(1,self.client_cooppd[mini])).index(1)  #random choice for client

            #print "new cl play: ",new_cl_play
            thedistro = self.get_paab_distro(f[3:6])
            #print "the distro: "
            #print thedistro
            
            new_cl_play = list(NP.random.multinomial(1,thedistro)).index(1)  #random choice for client weighted by different options
            new_cl_play = new_cl_play + 1  #deal with wait action

            #print "newer client play: ",new_cl_play



        else:
            new_cl_play = 0  #was cl_play ?? why? Should reset on agent turn, so this is correct now 

        if paab == 0:  #wait
            if turn == "client":  
                new_ag_play = ag_play
            else:
                new_ag_play = 0  #always goes to null on wait
        elif paab == 1: #cooperate
            if turn == "client":
                new_ag_play = ag_play   #stays the same - carry over to next time step
            else:
                new_ag_play = 1  #cooperate
        elif paab == 2: #defect
            if turn == "client":
                new_ag_play = ag_play
            else:
                new_ag_play = 2  #defect

        #print 20*"samplexvar"
        #print f
        #print [turn,state.get_turn(),ag_play,cl_play]
        #print [state.invert_turn(),new_ag_play,new_cl_play]
        return [state.invert_turn(),new_ag_play,new_cl_play]
        
    #this must be in the class
    #xobs[1] is the client action observation, but its deterministic for now
    #we could implement an observation function here if not deterministic
    def evalSampleXvar(self,sample,xobs,oldsample=[]):
        turn  = sample.get_turn()
        if turn == "agent":  #this is whose turn it is *next* #confusing
            if sample.x[0]==xobs[0] and sample.x[2] == xobs[1]:  #+1 was here   #plus one?????????? I think this is right and seems to work
                return 1.0
            else:
                return 0.0
        else:
            return 1.0  #we don't model agent action as observable
        

    #an observation sample is [turn, client_play]
    def sampleXObservation(self,sample):
        #need to subtract one from here because sample.x[2] is 0=wait, 1=cooperate and 2=defect
        #WARNING!!! What is sample.x[2] is 0 ???  yuck yuck - there is no observation for this
        #WHY IS THIS WAIT THING EVEN HERE ??
        #CHECK THIS _ SHOULD THIS BE [sample.x[0],sample.x[2]-1]  - but that breaks things elsewhere for some reason
        #sample.x 
        #if sample.x[2] == 0:   ## will this ever happen?  - no because its ignored in evalSampleXvar
        #    xobs = 0
        #else:
        #     xobs = sample.x[2]-1
        xobs = sample.x[2]   #0,1,2 observations now
        return [sample.x[0],xobs] #no noise

    def reward(self,sample,action=None):
        # a generic deflection-based reward that can be removed eventually
        fsample=sample.f.transpose()
        freward = -1.0*NP.dot(sample.f-sample.tau,sample.f-sample.tau)
        # a state-based reward -  based on current state
        if sample.x[1] == 0 or sample.x[2] == 0:   #someone has not acted
            xreward = 0.0
        elif sample.x[1] == 1 and sample.x[2] == 1:  #cooperate-cooperate
            xreward = 10.0
        elif sample.x[1] == 1 and sample.x[2] == 2:  #cooperate-defect
            xreward = -1.0
        elif sample.x[1] == 2 and sample.x[2] == 1:  #defect-cooperate
            xreward = 11.0
        elif sample.x[1] == 2 and sample.x[2] == 2:  #defect-defect
            xreward = 1.0
            
        return xreward #+freward 



    #----------------------------------------------------------------------------------
    #POMCP functions
    #----------------------------------------------------------------------------------
    #these functions are used by the POMCP class to call the agent and get a sample
    #this is the "blackbox simulator" used in POMCP
    
    #this version of propagate sample first draws the X value and finds which action the client
    #takes, then sets the fb value to be consistent with that 
    #but actually we want to do this the other way around and samples fb that is consistent with 
    #the client's identity and THEN sample X according to that in sampleXvar
    # so THIS FUNCTION IS NOT USED ANYWHERE!
    def propagateSampleSetFb(self,state,action):
        #continuous component is in the first member of the action tuple - this is encoded here in this class, not in pomcp class
        aab = action[0]

        #propositional action is the second member of the action tuple
        paab = action[1]

        #if agent turn, observ is ignored - but not in POMCP so this is awkward
        observ=NP.array([])



        #does not depend on f or tau here, so we leave those out - 
        #choose a random action for the client?
        #does not depend on f or tau here, so we leave those out - 
        #this gets us the client's action
        xsample = self.sampleXvar([],[],state,aab,paab)

            
        #sample a next state - but instead of using SampleNext, we do it by hand since we have to 
        #get fb to be constrained to be what xample[2] says the agent did (i.e. cooperate is fb=[+++] etc)
        if state.get_turn() == "client":
            acttotake = xsample[2]+1  #cooperate or defect as an action
            caab = self.get_consistent_fb(acttotake)
            fVarSampler = FVarSampler(self.isiga, self.isigf, state.tau, state.f, \
                                      self, "agent", caab)
            #kludge to get h and c to be properly initialised for client turn
            #so we are re-doing this calculation which was already done in FVarSampler ... sort of sux
            (fVarSampler.h, fVarSampler.c) = self.clientMappings.getHC(state.tau);
            fVarSampler.c = fVarSampler.c.transpose()
            f=NP.concatenate((state.f[0:3],caab,state.f[6:9]))
            (fVarSampler.mu_n, fVarSampler.sig_n) = fVarSampler._computeMuSig(f, self.isiga, self.isigf["agent"])
        else:
            fVarSampler = FVarSampler(self.isiga, self.isigf, state.tau, state.f, \
                                      self, state.get_turn(), aab)
        

        #sample the fvar, but here this should be done with fb clamped to the value of acttotake on client turn
        fsample = fVarSampler.sampleNewFVar()

        
        if state.get_turn() == "client":
            #sample an observation from fsample
            observ=self.sampleObservation(fvars,fsample,self.gamma_value_pomcp)

        #sample from T using the H and C matrices we computed from
        #    tau in sampleNewFVar
        tsample = sampleTvars(tvars, fVarSampler.h, fVarSampler.c, fsample)


        newsample = State(fsample, tsample, xsample, fVarSampler.weight)

        xobserv = self.sampleXObservation(newsample)

        newreward = self.reward(state,(aab,paab))  #actually is action independent

        #turn is given as a noise-free observation here embedded in x
        return (newsample,(observ,xobserv),newreward)


    #returns the closest observation match to obs in obsSet
    #this needs to be in this class, as the comparison depends on the structure of the observation vector
    def bestObservationMatch(self,obs,obsSet,obsSetData):
        firstone=True
        bestdist=-1
        besto=-1
        for oindex in range(len(obsSet)):
            o=obsSet[oindex]
            if obs[1][0]==o[1][0] and obs[1][1]==o[1][1]:
                odist = math.sqrt(raw_dist(obs[0],o[0]))
                if firstone or odist<bestdist:
                    firstone=False
                    besto=oindex
                    bestdist=odist
        return (besto,bestdist)
        
    def observationDist(self,obs1,obs2):
        if obs1[1][0] == obs2[1][0]: #turns have to match
            odist= math.sqrt(raw_dist(obs1[0],obs2[0]))
            if obs1[1][1]==obs2[1][1]:
                return odist
            else:
                #but, since in the pdagent, it may easily be the case that the agent does not
                #have a sample for the observation (propositional) taken by the client,
                #we have to account for this and return some kind of value here
                return 1000*odist;
        else:
            #turns don't match, something is wrong
            return -2