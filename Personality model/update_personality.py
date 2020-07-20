def update_prediction(probablity,review):
    """
        Increase or decrese traits probablity according user revieiew 
        * Takes probablity which was predicted by model and user review in integerform to evaluate how more/less probablity should be     rather    than predicted 
        * Returns  updated probablity
    """
    for key in list(probablity.keys()):
        if review>0:   # checking user positive review 
            for i in range(review):
                if (probablity[key]+1)<100:
                    probablity[key]+=1   # increasing probablity
        else:      # checking user negative review 
            for i in range(abs(review)):
                if (probablity[key]-1)>0:
                    probablity[key]-=1 # reducing probablity 
    return probablity 
