import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import tkinter as tk
from json import dumps,load as json_load
import info

def load_image(save_name):
    image=cv2.imread(save_name)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB).astype(np.uint8)
    return image

def display_image(image,win_name="image",show_time=0,destroy=True):
    image=cv2.cvtColor(cv2.UMat(image),cv2.COLOR_RGB2BGR)
    cv2.imshow(win_name,image)
    if(show_time>=0) : cv2.waitKey(show_time)
    if(destroy) : cv2.destroyWindow(win_name)

def get_filenames(path,start,stop,sort=True):
    filenames=[os.path.join(path,eles) for eles in os.listdir(path)]
    if(sort) : filenames=sorted(filenames,key=lambda x:(len (x),x))[start:stop+1]
    return filenames



def test_label(image,label,type_="vertices"):
    image=np.array(image,dtype=np.uint8)
    if(type_=="vertices"):
        for l in label:
            l=np.array(l,dtype=np.int32)
            image=cv2.polylines(image,[l],True,(0,0,255),thickness=2)
    elif(type_=="bbox"):
        for l in label:
            l=np.array(l,dtype=np.int32)
            xmin,ymin,width,height=l.ravel()
            xmax,ymax=xmin+width,ymin+height
            image=cv2.polylines(image,[np.array([[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]],dtype=np.int32)],True,(0,0,255),thickness=2)
    elif(type_=="single_points"):
        for l in label:
            l=np.array(l,dtype=np.int32)
            l=l.reshape(-1,2).tolist()
            color=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
            for x,y in l : cv2.circle(image,(x,y),radius=3,color=color,thickness=-1)
    elif(type_=="bbox+text"):
        for l in label:
            l1=np.array(l[0:-1],dtype=np.int32)
            l2="".join(l[-1])
            xmin,ymin,width,height=l1.ravel()
            xmax,ymax=xmin+width,ymin+height
            image=cv2.polylines(image,[np.array([[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]],dtype=np.int32)],True,(0,0,255),thickness=2)
            cv2.putText(image,l2,org=(xmin,ymin),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
    elif(type_=="vertices+text"):
        for l in label:
            l1=np.array(l[0:-1],dtype=np.int32)
            l2="".join(l[-1])
            image=cv2.polylines(image,[l1],True,(0,0,255),thickness=2)
            cv2.putText(image,l2,org=(l1[0][0],l1[0][1]),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
    elif(type_=="single_points+text"):
        for l in label:
            l1=np.array(l[0:-1],dtype=np.int32)
            l1=l1.reshape(-1,2).tolist()
            color=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
            l2="".join(l[-1])
            for x,y in l1 : cv2.circle(image,(x,y),radius=3,color=color,thickness=-1)
            cv2.putText(image,l2,org=(l1[0][0],l1[0][1]),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
    elif(type_=="text"):
        i=0
        ydist=30
        for l in label:
            l=l[0]
            cv2.putText(image,l,org=(image.shape[0]//2,image.shape[1]//2+i*ydist),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
            i+=1
    else:
        image=None
    return image



def list_to_xml(label,label_type):
    return NotImplementedError

def list_to_json_dict(label,label_type):
    if(label_type=="text"):
        new_label=[ {'object'+str(i+1):{'label_type':label_type,'text':label[i][0]} } for i in range(len(label)) ]
    elif(label_type=="bbox"):
        new_label=[ {'object'+str(i+1):{'label_type':label_type,'xmin,ymin':tuple(label[i][0]),'xmax,ymax':tuple(label[i][1])} } for i in range(len(label)) ]
    elif(label_type=="vertices"):
        new_label=[ {   'object'+str(i+1): dict( [['label_type',label_type]]+[['x'+str(j+1)+',y'+str(j+1),tuple(label[i][j])] for j in range(len(label[i]))])    } for i in range(len(label)) ] 
    elif(label_type=="single_points"):
        new_label=[ {   'object'+str(i+1): dict( [['label_type',label_type]]+[['x'+str(j+1)+',y'+str(j+1),tuple(label[i][j])] for j in range(len(label[i]))])    } for i in range(len(label)) ]
    elif(label_type=="bbox+text"):
        new_label=[ {'object'+str(i+1):{'label_type':label_type,'text':label[i][-1],'xmin,ymin':tuple(label[i][0]),'xmax,ymax':tuple(label[i][1])} } for i in range(len(label)) ]
    elif(label_type=="vertices+text"):
        new_label=[ {   'object'+str(i+1): dict( [['label_type',label_type]]+[['text',label[i][-1]]]+[['x'+str(j+1)+',y'+str(j+1),tuple(label[i][j])] for j in range(len(label[i])-1)])    } for i in range(len(label)) ]
    elif(label_type=="single_points+text"):
        new_label=[ {   'object'+str(i+1): dict( [['label_type',label_type]]+[['text',label[i][-1]]]+[['x'+str(j+1)+',y'+str(j+1),tuple(label[i][j])] for j in range(len(label[i])-1)])    } for i in range(len(label)) ]
    else:
        new_label=None
    return new_label

def list_to_string(label,sep=","):
    new_label=[]
    for i in range(len(label)):
        new_label.append([])
        for eles in label[i]:
            if(type(eles)==type('a')) : new_label[i].append(eles)
            else : new_label[i].extend(eles)

    for i in range(len(new_label)):
        for j in range(len(new_label[i])-1):
            new_label[i].insert(2*j-1,sep)
    new_label=[objects+["\n"] for objects in new_label]
    new_label=[t for objects in new_label for t in objects]
    
    new_label="".join(list(map(str,new_label)))
    return new_label

def save_label(label,save_name,label_type):
    ext="."+save_name.split('.')[1]
    if(ext==".json"):
        label=list_to_json_dict(label,label_type)
        label=dumps(label)
        with open(save_name,"w") as file : file.write(label)
    elif(ext==".txt"):
        label=list_to_string(label,sep=" ")
        with open(save_name,"w") as file : file.write(label)
    elif(ext==".csv"):
        label=list_to_string(label,sep=",")
        with open(save_name,"w") as file : file.write(label)
    elif(ext==".xml"):
        return NotImplementedError



def main():

    label_type=info.label_type
    image_read_path=info.image_read_path
    label_write_path=info.label_write_path
    start=info.start
    stop=info.stop
    label_ext=info.label_ext
    multiple=info.multiple

    print("\nPress left mouse click or any other keyboard key to mark a point.\nPress right mouse click or backspace to delete a point.\nPress middle mouse button or enter to stop the input.")

    filenames=get_filenames(image_read_path,start,stop,True)
    for i in range(len(filenames)):

        img=plt.imread(filenames[i]); plt.imshow(img); plt.draw()
        label=[]
        while(True):
            
            if(label_type=="text"):
                curr=plt.ginput(n=0,timeout=0.001,show_clicks=False,mouse_add=1,mouse_stop=2,mouse_pop=3)
            else:
                curr=plt.ginput(n=0,timeout=0,show_clicks=True,mouse_add=1,mouse_stop=2,mouse_pop=3)
                if(len(curr)==0 or curr is None) : break
                
            if(label_type in ["bbox","bbox+text"]):
                curr=list(map(list,curr))
                curr[1][0],curr[1][1]=curr[1][0]-curr[0][0],curr[1][1]-curr[0][1]
                curr=[(curr[0][0],curr[0][1]),(curr[1][0],curr[1][1])]
                
            if(label_type in ["text","bbox+text","vertices+text","single_points+text"]):
                root=tk.Tk(); root.withdraw()
                curr.append(tk.simpledialog.askstring(title="Enter Text",prompt="text:"))
                plt.close(); plt.imshow(img); plt.draw()
                
            if(label_type=="text"):
                if(len(curr[0])==0 or curr is None) : break

            label.append(curr)
            if(not multiple) : break

        image=load_image(filenames[i])
        image=test_label(image,label,type_=label_type)
        display_image(image)

        save_name=label_write_path+"".join(filenames[i].replace(image_read_path,"").split(".")[0])+label_ext
        save_label(label,save_name,label_type)


if(__name__=="__main__") : main()