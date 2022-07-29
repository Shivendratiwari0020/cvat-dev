import h5py
import os
import json
import pandas as pd
#from h5_extract import h5_extract_start

class output_conversion_cls:

    def h5_extract_start(self,input_h5_file):
        for filename in os.listdir(input_h5_file):
            if filename.endswith(".txt"):
                filename_json=os.path.join(input_h5_file,filename)
                f = open(filename_json)
                data = json.load(f)    
                devicename=data["devicename"]
                channelname=data["channelname"]
                frame_timestamp_dict = data["frame_timestamp_dict"]
                frame_timestamp_dict = {int(k):int(v) for k,v in frame_timestamp_dict.items()}
                
        print(devicename,channelname,frame_timestamp_dict)
                
        return devicename,channelname,frame_timestamp_dict

# class output_conversion_cls:

#     def h5_extract_start(self,input_h5_file):
#         for filename in os.listdir(input_h5_file):
#             if filename.endswith(".h5"):
#                 #print(filename)
#                 fn=filename.split(".h5")[0]
#                 #print(fn)
#                 filename=os.path.join(input_h5_file,filename)
#                 hdf = h5py.File(filename,'r')
#                 keys = []
#                 with hdf as f: # open file
#                     f.visit(keys.append)

#                 devicename=keys[0]
#                 channelname=keys[1].split("/")[1]

#                 timestamp = keys[2:]

#                 timestamp = [i.split("/")[2] for i in timestamp]
#                 frame_numbers = list(range(1, len(timestamp)+1))
#                 frame_timestamp_dict = {frame_numbers1:timestamp1 for timestamp1,frame_numbers1 in zip(timestamp,frame_numbers)}

#         #print(devicename,channelname,frame_timestamp_dict)
#         return devicename,channelname,frame_timestamp_dict

    def output_conversion_objectlabel(self, labelfile_input_path, input_h5_file, task_name, login_name):
        devicename,channelname,frame_timestamp_dict=occ.h5_extract_start(input_h5_file)

        f = open(labelfile_input_path)
        data = json.load(f)
        scenelabel=[d for d in data["categories"] if d["name"] == "Scene_Label"]
        print(scenelabel,"scenelabel")
        scenelabel=scenelabel[0]
        scenelabel_id=scenelabel["id"]


        df = pd.DataFrame(data["annotations"])
        df_objectlabels=df[df['category_id'] != scenelabel_id]
        df_objectlabels=df_objectlabels.reset_index()

        Labels=[]
        Labels_dict={}

        Devices=[]
        Devices_dict={}

        Channels=[]
        Channels_dict={}


        #f = open(labelfile_input_path)
        #data = json.load(f)

        #df = pd.DataFrame(data["annotations"])
        df_objectlabels=df_objectlabels.drop(['segmentation', 'area', 'iscrowd'], axis = 1, errors='ignore')

        ObjectLabels=[]

        col_one_list = df_objectlabels['image_id'].tolist()
        col_one_list=set(col_one_list)
        col_one_list=list(col_one_list)

        trackid_shape=100000

        for img_id in col_one_list:
            ObjectLabels_dict={}
            df_img_id = df_objectlabels[df_objectlabels['image_id']==img_id]
            df_img_id_list=df_img_id[df_img_id['image_id']==img_id].to_dict('records')
            FrameObjectLabels_list=[]

            for dict_df_img_id_list in df_img_id_list:
                #print(dict_df_img_id_list["category_id"])

                FrameObjectLabels_dict={}
                shape={}
                x,y,w,h=dict_df_img_id_list["bbox"]

                FrameObjectLabels_dict["width"]=w
                FrameObjectLabels_dict["height"]=h


                xmin,ymin,xmax,ymax=x,y,x+w,y+h
                x=[xmin,xmax,xmax,xmin]
                y=[ymin,ymax,ymax,ymin]
                y=[ymin,ymax,ymax,ymin]

                shape["Algo Generated"]= "NO"
                shape["Manually Corrected"]="YES"
                shape["type"]="Box"
                shape["thickness"]=2
                shape["x"]=x
                shape["y"]=y

                for dicti in data["categories"]:
                    for key, value in dicti.items():
                        if dict_df_img_id_list["category_id"] == value:
                            category=(dicti["name"])




                attributes=dict_df_img_id_list["attributes"]

                #if "track_id" in attributes:
                #    trackid=attributes["track_id"]
                #else:
                 #   trackid=-1


                if "track_id" in attributes:
                    trackid=attributes["track_id"]
                    #print("--------------------trackkid", trackid)
                else:
                    trackid_shape=trackid_shape+1
                    trackid=trackid_shape+1
                   # print("...............else", trackid)
                #trackid=trackid+1


                rem_list = ['occluded', 'rotation', 'keyframe', "track_id"]
                attributes = {key: attributes[key] for key in attributes if key not in rem_list}


                #for key in rem_list:
                    #attributes.pop(key)
                #[attributes.pop(key) for key in rem_list]

                for key in attributes:
                    attribute_value=[]
                    attributes[key]=str(attributes[key])
                    attribute_value.append(attributes[key])
                    attributes[key]=attribute_value

                FrameObjectLabels_dict["category"]=category
                FrameObjectLabels_dict["Trackid"]=trackid



                FrameObjectLabels_dict["attributes"]=attributes
                FrameObjectLabels_dict["pulse"]=0
                FrameObjectLabels_dict["shape"]=shape
                #print(FrameObjectLabels_dict)

                FrameObjectLabels_list.append(FrameObjectLabels_dict)

            #print(FrameObjectLabels_list)
           # break

            ObjectLabels_dict["TimeStamp"]=frame_timestamp_dict[img_id]
            ObjectLabels_dict["FrameNumber"]=img_id
            ObjectLabels_dict["FrameObjectLabels"]=FrameObjectLabels_list

            ObjectLabels.append(ObjectLabels_dict)


        Channels_dict["ChannelName"]= channelname##STATIC
        Channels_dict["ObjectLabels"]=ObjectLabels
        Channels.append(Channels_dict)

        Devices_dict["DeviceName"]="MFC520"  ##STATIC
        Devices_dict["Channels"]=Channels
        Devices.append(Devices_dict)

        Labels_dict["SourceType"]="Image"
        Labels_dict["Devices"]=Devices
        Labels.append(Labels_dict)

        Sequence=[]
        SequenceDetails_dict={}
        SequenceDetails={}


        SequenceDetails["FileName"]=task_name
        SequenceDetails["Status"]="Intermediate"
        SequenceDetails["Username"]=login_name
        SequenceDetails["FolderName"]=task_name
        SequenceDetails["Task"]=task_name
        SequenceDetails["CANvAS Version"]="3.5.2"
        SequenceDetails["LabelType"]=""

        SequenceDetails_dict["SequenceDetails"]=SequenceDetails
        SequenceDetails_dict["Labels"]=Labels

        Sequence.append(SequenceDetails_dict)

        main=[]
        main_dict={}
        main_dict["Sequence"]=Sequence


        main.append(main_dict)

        main_json=json.dumps(main[0])
        output_write_file = input_h5_file+"SR_ObjectLabels.json"
        with open(output_write_file, "w") as f:
           f.write(main_json)

        #remove last 4 from attributes
        #check timestamp, frame number match
        #merge code
        #append starting few line of the code
        #trackid

    def get_min_max_vals(self,frame_number_list):
        minmax_list=[]
        minmax_list.append(frame_number_list[0])
        for i in range(len(frame_number_list)-1):
            if frame_number_list[i+1]==frame_number_list[i]+1:
                continue
            else:
                minmax_list.append(frame_number_list[i])
                minmax_list.append(frame_number_list[i+1])
        minmax_list.append(frame_number_list[-1])
        return minmax_list

    def output_conversion_scenelabel(self, labelfile_input_path, input_h5_file, task_name, login_name):
        devicename,channelname,frame_timestamp_dict=occ.h5_extract_start(input_h5_file)
        f = open(labelfile_input_path)
        data = json.load(f)
        scenelabel=[d for d in data["categories"] if d["name"] == "Scene_Label"]
        scenelabel=scenelabel[0]
        scenelabel_id=scenelabel["id"]

        df = pd.DataFrame(data["annotations"])
        df_scenelabel=df[df['category_id'] == scenelabel_id]
        df_scenelabel=df_scenelabel.reset_index()



        df_scenelabel=df_scenelabel.drop(['segmentation', 'area', 'iscrowd','bbox', 'category_id','index'], axis = 1, errors='ignore')


        Labels=[]
        Labels_dict={}

        Devices=[]
        Devices_dict={}

        Channels=[]
        Channels_dict={}

        d_f=pd.DataFrame()
        for x in range(len(df_scenelabel)):
            #print(x)
            dct={}
            new={}
            d1=df_scenelabel['attributes'][x]
            dct = {k:[v] for k,v in d1.items()}
            new=pd.DataFrame.from_dict(dct)
            d_f=d_f.append(new)

        d_f=d_f.reset_index()
        df_new=df_scenelabel.join(d_f)
        df_filter=df_new.drop(['attributes', 'occluded', 'rotation','id', 'index','keyframe','track_id'], axis = 1, errors='ignore')

        columns_list=list(df_filter.columns)
        columns_list.remove("image_id")

        SceneLabels={}
        # attribute=[]



        for column in columns_list:
            attribute=[]
            #print(column)
            list_unique=list(df_filter[column].unique())
            for value in list_unique:
                frame_number_list=df_filter.loc[df_filter[column] == value, 'image_id']
                frame_number_list=list(frame_number_list)
                minmax_list=occ.get_min_max_vals(frame_number_list)
                for vali in range(0,len(minmax_list),2):
                    attribute_dict={}
                    starttimestamp,endtimestamp=minmax_list[vali],minmax_list[vali+1]
                    #print(starttimestamp,endtimestamp)
                    starttimestamp=frame_timestamp_dict[starttimestamp]
                    endtimestamp=frame_timestamp_dict[endtimestamp]


                    attribute_dict["endtimestamp"]=endtimestamp
                    attribute_dict["starttimestamp"]=starttimestamp
                    attribute_dict["value"]=value
                    attribute.append(attribute_dict)

            SceneLabels[column]=attribute



        Channels_dict["ChannelName"]=channelname
        Channels_dict["SceneLabels"]=SceneLabels
        Channels.append(Channels_dict)

        Devices_dict["Channels"]=Channels
        Devices_dict["DeviceName"]=devicename
        Devices.append(Devices_dict)

        Labels_dict["SourceType"]="Image"
        Labels_dict["Devices"]=Devices
        Labels.append(Labels_dict)

        Sequence=[]
        SequenceDetails_dict={}
        SequenceDetails={}


        SequenceDetails["FileName"]=task_name
        SequenceDetails["Status"]="Intermediate"
        SequenceDetails["Username"]=login_name
        SequenceDetails["FolderName"]=task_name
        SequenceDetails["Task"]=task_name
        SequenceDetails["CANvAS Version"]="3.5.2"
        SequenceDetails["LabelType"]=""

        SequenceDetails_dict["Labels"]=Labels
        SequenceDetails_dict["SequenceDetails"]=SequenceDetails


        Sequence.append(SequenceDetails_dict)

        main=[]
        main_dict={}
        main_dict["Sequence"]=Sequence


        main.append(main_dict)

        main_json=json.dumps(main[0])
        output_write_file = input_h5_file+"SR_SceneLabels.json"
        with open(output_write_file, "w") as f:
           f.write(main_json)



# labelfile_input_path=r'C:\Users\105926\Downloads\full\annotations\instances_default.json'
# input_h5_file=r'C:\Users\105926\Documents\Output_Conversion'
task_name="SR"
login_name="1"

occ=output_conversion_cls()
# occ.output_conversion_objectlabel(labelfile_input_path, input_h5_file, task_name, login_name)
# occ.output_conversion_scenelabel(labelfile_input_path, input_h5_file, task_name, login_name)






