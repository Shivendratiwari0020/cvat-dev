import cv2
import os

def label_generator_crop(image_folder, list_of_instance_trackedshape,list_of_instance_labeledtrack, last_frame):    
    #image_folder=vid.rsplit("\\", 1)[0]

    print("list_of_instance_trackedshape", list_of_instance_trackedshape, "list_of_instance_labeledtrack",list_of_instance_labeledtrack)
    for filename in os.listdir(image_folder):
        if filename.endswith(".mp4"):
            #print(filename)
            vid=os.path.join(image_folder,filename)

    rem_list = ['type', 'occluded', 'z_order', 'rotation', 'id']
    
    
    for dict_ in list_of_instance_trackedshape:
        [dict_.pop(key) for key in rem_list]        
           
    first_frame_track=list_of_instance_labeledtrack[0]["frame"]
    
    last_frame_dict = next((item for item in list_of_instance_trackedshape if item['outside'] == True), None)
    
    #last_frame_track=last_frame_dict["frame"]-1

    if last_frame_dict is None:
        last_frame_track=last_frame
    else:
        last_frame_track=last_frame_dict["frame"]-1
    
    instance_list=list_of_instance_trackedshape

    instance_list = sorted(instance_list, key=lambda d: d['frame'])  
    
    try:
        instance_list = [i for i in instance_list if not (i['outside'] == True)] 
        while instance_list[-1]["frame"]-1 != instance_list[-2]["frame"]:
            for i in range(len(instance_list)):
                try:
                    if instance_list[i+1]["frame"] == instance_list[i]["frame"] +1:
                        continue
                    else:
                        dict_to_append={}
                        dict_to_append["points"]=instance_list[i]["points"]
                        dict_to_append["track_id"]=instance_list[i]["track_id"]
                        dict_to_append["frame"] = instance_list[i]["frame"] +1
                        dict_to_append["outside"]= False
                        instance_list.append(dict_to_append)
                        instance_list = sorted(instance_list, key=lambda d: d['frame']) 
                except Exception as e:
                    print(e)
    except:
        for i in range(len(instance_list)):
            try:
                if instance_list[i+1]["frame"] == instance_list[i]["frame"] +1:
                    continue
                else:
                    dict_to_append={}
                    dict_to_append["points"]=instance_list[i]["points"]
                    dict_to_append["track_id"]=instance_list[i]["track_id"]
                    dict_to_append["frame"] = instance_list[i]["frame"] +1
                    dict_to_append["outside"]= False
                    instance_list.append(dict_to_append)
                    instance_list = sorted(instance_list, key=lambda d: d['frame']) 
            except Exception as e:
                print(e)

    print("midddddddddddddddd", instance_list)      
    instance_list = [i for i in instance_list if not (i['outside'] == True)]            
            
    while instance_list[-1]["frame"]!=last_frame_track:
        dict_to_append={}
        dict_to_append["points"]=instance_list[-1]["points"]
        dict_to_append["track_id"]=instance_list[-1]["track_id"]
        dict_to_append["frame"] = instance_list[-1]["frame"] +1
        dict_to_append["outside"]= False
        instance_list.append(dict_to_append)
        instance_list = sorted(instance_list, key=lambda d: d['frame'])

    print("fina_________________inst", instance_list)
    
    
    def get_image_from_vid(frame_list):
        frame_list=sorted(frame_list)
        frame_set_no = frame_list[0] 
        cap = cv2.VideoCapture(vid)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_set_no)
        success, image = cap.read()
        return image
            
    cropped_img_paths=[]
    for dict_fin in instance_list:
        frame_list=[]
        xmin,ymin,xmax,ymax=dict_fin["points"]
        xmin=int(xmin)
        ymin=int(ymin)
        xmax=int(xmax)
        ymax=int(ymax)
        #img_path_input=os.path.join(image_folder, str(dict_fin["frame"])+".jpeg")
        img_path_output=os.path.join(image_folder, str(dict_fin["frame"])+"_crop.jpeg")
        #img=cv2.imread(img_path_input)
        frame_list.append(dict_fin["frame"])
        img=get_image_from_vid(frame_list)
        crop_img = img[ymin:ymax, xmin:xmax]  
        cv2.imwrite(img_path_output, crop_img)
        cropped_img_paths.append(img_path_output)

    print("ropppeeeeeeeeeeeeeeeeeeeeeeeeed", cropped_img_paths)
    
    
    
    def img_to_base64(img):
        import base64
        with open(img, "rb") as img_file:
            return "data:image/jpeg;base64,"+str(base64.b64encode(img_file.read())).replace("b'","").replace("'","")
        
    list_of_dict_final=[]
    for img_crop in cropped_img_paths:
        dict_final={}
        img_crop_base64=img_to_base64(img_crop)
        frame_num=img_crop.split("\\")[-1]
        frame_num=frame_num.split(".")[0]
        frame_num=frame_num.split("_")[0]
        #dict_final["frame"]=frame_num
        dict_final["frame"]=img_crop.split("_crop.jpeg")[0].split("/")[-1]
        dict_final["img_base64"]=img_crop_base64
        list_of_dict_final.append(dict_final)
        #print("listtttttttttttttttttttttttttttttttttttttttt",list_of_dict_final)

    for f in os.listdir(image_folder):
        if not f.endswith(".jpeg"):
            continue
        os.remove(os.path.join(image_folder, f))
        
    return list_of_dict_final
    
    
    



#image_folder= r"C:\Users\105926\Documents\h5_to_images"
#list_of_instance_trackedshape=[{'type': 'rectangle', 'occluded': False, 'z_order': 0, 'points': [834.7514342895265, 600.5152768512344, 991.7200800533683, 703.9442294863238], 'rotation': 0.0, 'id': 43, 'track_id': 2, 'frame': 33, 'outside': False}, {'type': 'rectangle', 'occluded': False, 'z_order': 0, 'points': [834.7509765625, 600.515625, 973.5, 695.4000000000015], 'rotation': 0.0, 'id': 44, 'track_id': 2, 'frame': 35, 'outside': False}, {'type': 'rectangle', 'occluded': False, 'z_order': 0, 'points': [834.7509765625, 600.515625, 945.5, 685.7000000000007], 'rotation': 0.0, 'id': 45, 'track_id': 2, 'frame': 38, 'outside': False}, {'type': 'rectangle', 'occluded': False, 'z_order': 0, 'points': [834.7509765625, 600.515625, 945.5, 685.7000000000007], 'rotation': 0.0, 'id': 46, 'track_id': 2, 'frame': 43, 'outside': True}]
#list_of_instance_labeledtrack= [{'id': 2, 'job_id': 1, 'label_id': 22, 'frame': 33, 'group': 0, 'source': 'manual'}]


#label_generator_crop(image_folder, list_of_instance_trackedshape,list_of_instance_labeledtrack)