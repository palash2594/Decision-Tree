import math

def entropy(pos, neg):
    total = pos+neg
    return  -(pos/(total)*math.log(pos/(total),2) + neg/total*math.log(neg/total,2))

def agg_ent(ent1, ent2, n1, n2):
    total = n1 + n2
    return (n1/total * ent1) + (n2/total * ent2)

def gain(total_ent, att_ent):
    return total_ent - att_ent


if __name__ == '__main__':
    print(agg_ent(entropy(3, 1), entropy(1,4), 4, 5))



