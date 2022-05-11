import numpy as np
import pandas as pd

data = dict()
data['operations'] = {"Safety":np.array([4,6,4,3,4,3]),"Fuel storage":np.array([3,1,5,6,2,1]),"Refuelling":np.array([2,5,6,3,1,2]),"Maintenance":np.array([3,6,5,4,3,5]),"Weights":np.array([0.25,0.4,0.2,0.15]),"value":0.20}
data['performance'] = {"Weight":np.array([7,1,5,6,4,1]),"Drag":np.array([7,1,4,6,5,1]),"Speed":np.array([7,1,7,7,6,1]),"Range":np.array([7,1,6,5,4,1]),"Weights":np.array([0.25,0.25,0.25,0.25]),"value":0.30}
data['cost'] = {"Development":np.array([4,4,2,3,3,4]),"Manufacturing":np.array([4,1,5,5,2,2]),"Maintenance":np.array([3,6,3,3,2,2]),"Fuel":np.array([4,1,6,2,5,5]),"Weights":np.array([0.05,0.15,0.2,0.6]),"value":0.15}
data['sustainability'] = {"CCforeground":np.array([6,7,5,1,7,7]),"CCbackground":np.array([7,4,1,3,7,7]),"Toxicity":np.array([1,5,2,3,7,7]),"Noise Pollution":np.array([2,6,2,2,6,6]),"Durability":np.array([2,4,2,2,7,5]),"Weights":np.array([0.25,0.25,0.15,0.2,0.15]),"value":0.35}


def winner(data):
    winner = np.zeros(6)
    for category in data:
        i=0
        subwinner = np.zeros(6)
        for key in data[category]:
            if key!='Weights' and key!='value':
                subwinner+=data[category][key]*data[category]['Weights'][i]
            i+=1
        winner+=subwinner*data[category]['value']
    f=np.where( winner == max(winner))[0][0]
    return f

def sensitivity(data):
    original = winner(data)
    change = data
    max = 7
    min = 1
    changedweights = np.array([[0.20,0.3,0.15,0.35],[0.25,0.25,0.25,0.25],[0.30,0.3,0.25,0.15],[0.20,0.2,0.2,0.4],[0.20,0.4,0.2,0.2]])
    weightsensetivity = np.zeros((len(changedweights),6))
    weightnumber = 0
    for weight in changedweights:
        changes = 0
        z = 0
        for category in change:
            change[category]['value']= weight[z]
            z+=1
        if winner(change) != original:
            print(f'design {winner(change)+1} wins if the weightage is {weight}')
        newdata = change
        for category in change:
            for key in change[category]:
                if key!='Weights' and key!='value':
                    for f in range(len(change[category][key])):
                            for i in range(-1,2,2):
                                change[category][key][f]+=i*0.5
                                changes+=1
                                if winner(change)!=original and min <= change[category][key][f] <= max:
                                    # print(f'in the {key} of {category} if you {i} the {f+1}th variable which was'
                                    #       f' \n originally {data[category][key][f]} the winner becomes design {winner(change)+1} for a weightage distribution of {weight}')
                                    weightsensetivity[weightnumber][f]+=1
                            change = newdata
        weightsensetivity[weightnumber][4]= 204-sum(weightsensetivity[weightnumber])
        weightnumber+=1
    print(weightsensetivity)
    pass



sensitivity(data)