# -*- coding: utf-8 -*-
"""
Mining Assignment 1
"""

import math

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # metric:
    # metric is in the form of a string. it can be any of the following:
    # "minkowski", "cosine", "pearson"
    #     recall that manhattan = minkowski with r=1, and euclidean = minkowski with r=2
    # defaults to "pearson"
    #
    # r:
    # minkowski parameter
    # set to r for minkowski, and ignored for cosine and pearson
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    def __init__(self, usersItemRatings, metric='pearson', r=1, k=1):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings

        # set self.metric and self.similarityFn
        if metric.lower() == 'minkowski':
            self.metric = metric
            self.similarityFn = self.minkowskiFn
        elif metric.lower() == 'cosine':
            self.metric = metric
            self.similarityFn = self.cosineFn
        elif metric.lower() == 'pearson':
            self.metric = metric
            self.similarityFn = self.pearsonFn
        else:
            print ("    (DEBUG - metric not in (minkowski, cosine, pearson) - defaulting to pearson)")
            self.metric = 'pearson'
            self.similarityFn = self.pearsonFn
        
        # set self.r
        if (self.metric == 'minkowski'and r > 0):
            self.r = r
        elif (self.metric == 'minkowski'and r <= 0):
            print ("    (DEBUG - invalid value of r for minkowski (must be > 0) - defaulting to 1)")
            self.r = 1
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (DEBUG - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
            
    
    #################################################
    # minkowski distance (dis)similarity - most general distance-based (dis)simialrity measure
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def minkowskiFn(self, userXItemRatings, userYItemRatings):
        
        distance = 0
        commonRatings = False 
        
        for item in userXItemRatings:
            # inlcude item rating in distance only if it exists for both users
            if item in userYItemRatings:
                distance += pow(abs(userXItemRatings[item] - userYItemRatings[item]), self.r)
                commonRatings = True
                
        if commonRatings:
            return round(pow(distance,1/self.r), 2)
        else:
            # no ratings in common
            return -2

    #################################################
    # cosince similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def cosineFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x2 = 0
        sum_y2 = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        
        denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)
        if denominator == 0:
            return -2
        else:
            return round(sum_xy / denominator, 3)

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                n += 1
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
       
        if n == 0:
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        
        # YOUR CODE HERE
        
        # for given userX, get the sorted list of users - by most similar to least similar   
       self.userX = userX #set userX to pass it to the contructor
       userXItemRatings = self.usersItemRatings[userX]#make a subet of user ratings, subset is user=userX
 # get the dictionary items for other users with which UserX is compared      
       sim = []#Declare an empty list to append similarity measures calculated by the similiarityFn
       users=list() # An empty list which is appended with user names
       
       
       for i in self.usersItemRatings.keys():
       #iterate through the keys of the dictionary userItemRatings
       #where i takes the value of the key user
            if(i!=userX):
               userYItemRatings = self.usersItemRatings[i]
               #subset of the main dictionary where user!=userX
               #this dictionary contains userY values wih which userX is going to be compared
            else:
               continue
#the conditional statement below only calls values of correlations which are between -1 and +1
#Some of the data points have correlation -2
        
            if(self.similarityFn(userXItemRatings,userYItemRatings)!=-2):
               sim.append(self.similarityFn(userXItemRatings,userYItemRatings))
               
               
            else:
                sim.append(0)
            users.append(i)
       new_dict = dict(zip(users,sim))#dictionary of user:similarity measure relative to userX
       print(new_dict)
       new_list = sorted(new_dict, key = new_dict.get)
       
       if (self.metric=='pearson') or (self.metric== 'cosine'):#higher values for correlations and cosine are more related
           new_list = new_list[::-1]
       new_list = new_list[0:self.k]
       print("Boom",new_list)
       sum_deno = 0
        
       
        # calcualte the weighted average item recommendations for userX from userX's k NNs
        
       if(self.k>1):   #only for k means greater than 1    
           for i in new_list:
               new_dict[i]=(new_dict[i]+1)/2#the correction factor (PC+1)/2 
               sum_deno += new_dict[i]#sum of all correlations is calculated which is the denominator for calculating weights
               
               
           print(i,sum_deno)
       
           for i in new_list:
              new_dict[i] = round(new_dict[i]/sum_deno,2)#dictionary of user:weights 
           
           print(new_dict)
           
       brandnew_dict = dict()#this dictionary which contains artist:recommendation
       brandnew_dict.update(userYItemRatings.items()) #assign last user's artist ratings(from block 1 iterations) to brandnew_dict
  #nested for loop to ensure brandnew_dict has all artists from usersItemRatings and the ratings are 0 for each    
       for i,v in self.usersItemRatings.items():
            for j,l in v.items():
                brandnew_dict[j] = 0
       
   #blank dictionary initially, established keys and values will be updated upon each iteration in the following block of code        
    
       for v in new_list:#for each of the nearest neighbours 
            userYItemRatings = self.usersItemRatings[v]#assign the users ratings to userYItemRatings
            for band in userYItemRatings.keys():#for each artist in userYItemRating
                if band not in userXItemRatings.keys():#condition to check if userX has not rated the artist in userYRatings
                    if self.k > 1: #for nearest neighbours greater than 1assign weights and upddate brandnew_dict otherwise update brandnew_dict without weights
                      brandnew_dict[band] = round(brandnew_dict[band] + (userYItemRatings[band] * new_dict[v]),2)
                    else:
                      brandnew_dict[band] = round((brandnew_dict[band]+userYItemRatings[band]),2)
       recommendation = []
#make a sorted list of recommendations of the type [(artist, rating)]      
#this loop ensures that artisits whose ratings are 0 in brandnew_dict(as they are not updated in the previous block) are not recommended to userX    
       for i,v in brandnew_dict.items():
            if v == 0:
                continue
            else:
                recommendation.append((i,v))
       recommendation = sorted(recommendation, key=lambda x: -x[1])
       print("Recommendations: \n", recommendation)        
         
          
           
          
    
       

        
       
               
               
           
           
     


        
