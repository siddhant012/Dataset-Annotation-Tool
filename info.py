#Specify the required values

'''Allowed types are : bbox (bounding box) , vertices (irregular shaped object) , single_points (multiple individual points) , text(only text) , 
                       bbox+text , vertices+text , single_points+text '''
label_type="vertices+text"


'''Read path of images to be annotated and write path of the labels'''
image_read_path=""
label_write_path=""


'''start and stop numbers of the pictures to be annotated in numeric sort order'''
start=1
stop=100

'''Allowed types : ".csv",".txt",".json"
.txt : Space separated text file
.csv : Comma separated text file
.json : json file'''
label_ext=".json"

'''Set this to true if labels are to be recorded for multiple objects in a single picture , False otherwise'''
multiple=False