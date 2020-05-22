def update_prediction(probablity,review):
    for key in list(probablity.keys()):
        if review>0:
            for i in range(review):
                if (probablity[key]+1)<100:
                    probablity[key]+=1
        else:
            for i in range(abs(review)):
                if (probablity[key]-1)>0:
                    probablity[key]-=1
    return probablity 
