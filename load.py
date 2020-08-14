import os
from json import dumps,load as json_load

#helper functions
def get_filenames(path,start,stop,sort=True):
    filenames=[os.path.join(path,eles) for eles in os.listdir(path)]
    if(sort) : filenames=sorted(filenames,key=lambda x:(len (x),x))[start:stop+1]
    return filenames

def string_to_list(label,sep=","):
    new_label=label.split("\n")
    new_label=[t.split(sep) for t in new_label][:-1]
    new_label=[[float(t) if t.replace('.','1').isdecimal() else t for t in objects] for objects in new_label]
    new_label=[[(objects[t],objects[t+1]) if (type(objects[t])==type(1.0)) else objects[t] for t in range(0,len(objects),2)]for objects in new_label]
    return new_label

def json_dict_to_list(label):
    new_label=[]
    for i in range(len(label)):
        obj='object'+str(i+1)
        temp=[]
        for eles in label[i][obj]:
            if(eles=='label_type') : continue
            elem=label[i].get(obj).get(eles)
            if(type(elem)==type([])) : elem=tuple(elem)
            temp.append(elem)
        temp.sort(key= lambda a:type(a)==type('1'))
        new_label.append(temp)

    new_label=[[(objects[t],objects[t+1]) if (type(objects[t])==type(1.0)) else objects[t] for t in range(0,len(objects),1)]for objects in new_label]
    return new_label

def xml_to_list(label):
    return NotImplementedError







#functions to load the labels
def load_labels(path,start=1,stop=100,sort=True):
    filenames=get_filenames(path,start,stop,sort)
    labels=[]
    for filename in filenames : labels.append(load_label(filename))
    return labels

def load_label(save_name):
    ext="."+save_name.split('.')[1]
    if(ext==".txt"):
        with open(save_name,"r") as file : label=file.read()
        label=string_to_list(label,sep=" ")
    elif(ext==".csv"):
        with open(save_name,"r") as file : label=file.read()
        label=string_to_list(label,sep=",")
    elif(ext==".json"):
        with open(save_name,"r") as file : label=json_load(file)
        label=json_dict_to_list(label)
    elif(ext==".xml"):
        return NotImplementedError
    else:
        label=None
    return label


def main():

    save_name=""
    #Returns a single label in form of a list
    label=load_label(save_name)

    path=""
    start=1
    stop=3
    #Returns a list of labels
    labels=load_labels(path,start,stop,sort=True)


if(__name__=="__main__") : main()