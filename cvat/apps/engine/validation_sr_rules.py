# %%
import numpy as np
import pandas as pd
from collections import Counter
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import timeit

start = timeit.default_timer()

# %%
#filename = "input_folder/2019.05.29_at_17.47.20_camera-mi_324.rrec_ObjectLabels.json"



def tool_validation(filename):

    # %%
    file_df = pd.read_json(filename)
    df = pd.json_normalize(file_df['Sequence'], 
    
                       record_path=['Labels','Devices','Channels','ObjectLabels','FrameObjectLabels'], 
    
                       meta =[['SequenceDetails'],
                              ['Labels','SourceType'],
                              ['Labels','Devices','DeviceName'],
                              ['Labels','Devices','Channels','ObjectLabels','FrameNumber'],
                              ['Labels','Devices','Channels','ObjectLabels','TimeStamp']
                             ])
    
    
    
    # %%
    """
    # pre processing (droping and sorting and lists to string value)
    """
    
    # %%
    drop_columns = ['pulse','SequenceDetails','Labels.SourceType','Labels.Devices.DeviceName','shape.Algo Generated','shape.Manually Corrected','shape.type']
    df = df.drop(drop_columns,axis=1)
    
    # %%
    df['Labels.Devices.Channels.ObjectLabels.FrameNumber'] = df['Labels.Devices.Channels.ObjectLabels.FrameNumber'].astype(int)
    df['Trackid'] = df['Trackid'].astype(int)
    df = df.sort_values(by=['Trackid','Labels.Devices.Channels.ObjectLabels.FrameNumber'], ascending=[True,True])
    df['category'] = df['category'].astype(str)
    
    list_to_first_element_columns = ["attributes.SR_DISABLED","attributes.SR_SIGN_EMBEDDED","attributes.SR_FOR_OTHER_ROAD","attributes.SR_FLASHING","attributes.SR_TWISTED",
                                     "attributes.SR_SIGN_CLASS","attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING",
                                     "attributes.SR_CONTAMINATED","attributes.SR_PARTLY","attributes.SR_MAIN_ID","attributes.SR_INVISIBLE","attributes.SR_INVALID"]
    
    
    #for item in list_to_first_element_columns:
      #  df[item] = df[item].apply(lambda x: str(x).replace('[','').replace(']','').replace("'",''))
    
    try:
        for item in list_to_first_element_columns:
            df[item] = df[item].apply(lambda x: str(x).replace('[','').replace(']','').replace("'",''))
    except Exception as e:
        print(e)    
        
    # %%
    # list(df.columns)
    
    # %%
    """
    # Rule 1
    ## Filter Category Column and select “Signs” and validate the Sign class column whether any sign class
    containing “sup” is set. If yes, highlight the same as False
    """
    
    # %%
    condition = ((df['category'] == 'Signs') & df['attributes.SR_SIGN_CLASS'].str.contains("Sup"))
    df['flag_1'] = np.where(condition,'false','true')
    
    print("Executed Rule 1")
    # %%
    """
    # Rule 2
    ## Filter Category Column and select “Supplementary Signs” and validate the Sign class column has only either “Not readable: or “ contains Suppl”. If yes, highlight the same as false
    """
    
    # %%
    condition = ((df['category'] == 'Supplementary Sign') & (df['attributes.SR_SIGN_CLASS'].str.contains("Not_Readable") | df['attributes.SR_SIGN_CLASS'].str.contains("Supp")))
    df['flag_2'] = np.where(condition,'false','true')
    print("Executed Rule 2")
    # %%
    """
    # Rule 3
    ## If SR_Lane direction exist, multimounting and SR_Flashing should be “TRUE” wherever false please highlight as Check
    """
    
    # %%
    
    condition = ((df['attributes.SR_FLASHING'] == 'true') & (df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING'] == 'true'))
    if 'attributes.SR_Lane' in list(df.columns):
        df['flag_3'] = np.where(condition,"true",'check')
    else:
        df['flag_3'] = np.where(condition,"Not Exist","Not Exist")
    print("Executed Rule 3")
    # %%
    """
    # Rule 4
    ## When SR_FLASHING is ticked as “TRUE”, SR_SIGN_EMBEDDED also should be “TRUE”
    """
    
    # %%
    condition = ((df['attributes.SR_FLASHING'] == 'true') & (df['attributes.SR_SIGN_EMBEDDED'] == 'true'))
    df['flag_4'] = np.where(condition,'true','false')
    print("Executed Rule 4")
    # %%
    """
    # Rule 5
    ## When SR_INVALID is “ON_Vehicle”, SR_SIGN_EMBEDDED should be ticked as “TRUE”
    """
    
    # %%
    condition = (df['attributes.SR_INVALID'].str.contains('On_Vehicle') & (df['attributes.SR_SIGN_EMBEDDED'] == 'true'))
    df['flag_5'] = np.where(condition,'true','false')
    print("Executed Rule 5")
    # %%
    """
    # Rule 6
    ## When SR_INVALID is “Informative”, SR_SIGN_EMBEDDED and SR_SIGN_ON_MULTI_SIGN_MOUNTING both should be “TRUE”
    """
    
    # %%
    condition = (df['attributes.SR_INVALID'].str.contains('Informative') & (df['attributes.SR_SIGN_EMBEDDED'] == 'true') & (df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING'] == 'true'))
    df['flag_6'] = np.where(condition,'true','false')
    print("Executed Rule 6")
    # %%
    """
    # Rule 7
    ## When SR_INVALID is “Informative”, SR_SIGN_LANE_DISTANCE should be “None”
    """
    
    # %%
    # again lane_distance 
    if 'attributes.SR_SIGN_LANE_DISTANCE' in list(df.columns):
        condition = (df['attributes.SR_INVALID'].str.contains("Informative") & (df['attributes.SR_SIGN_LANE_DISTANCE'] == "NaN"))
        df['flag_7'] = np.where(condition,"true","false")
    else:
        condition = (df['attributes.SR_INVALID'].str.contains("Informative"))
        df['flag_7'] = np.where(condition,"SR_LANE Not Exists","SR_LANE Not Exists")
    
    print("Executed Rule 7")
    # %%
    """
    # Rule 8
    ## Sr_Sign class contains “Rear side” then SR_Embedded, SR_Flashing ,SR_Invalid Should be False
    """
    
    # %%
    condition = (df['attributes.SR_SIGN_CLASS'].str.contains('Rear Side') & (df['attributes.SR_SIGN_EMBEDDED'] == 'false') & (df['attributes.SR_FLASHING'] == 'false') & (df['attributes.SR_INVALID'] == 'false'))
    df['flag_8'] = np.where(condition,'true','false')
    print("Executed Rule 8")
    # %%
    """
    # Rule 9
    ## Category- Supplementary signs, Flashing Should be False. If true- Please highlight as check
    """
    
    # %%
    condition = ((df['category'] == 'Supplementary Sign') & (df['attributes.SR_FLASHING'] == 'false'))
    df['flag_9'] = np.where(condition,'true','check')
    print("Executed Rule 9")
    # %%
    """
    # Rule 10
    ## Each track ID should contains “width” or ”height” approximately “5.0” or above should be TRUE
    """
    
    # %%
    condition = ((df['width'] >= 5.0) & (df['height'] >= 5.0))
    df["flag_10"] = np.where(condition,"true","false")
    print("Executed Rule 10")
    # %%
    """
    # Rule 11
    ##  If width or height <5, then SR_Partly should be True else highlight as check
    """
    
    # %%
    condition = (((df['width'] < 5.0) | (df['height'] < 5.0)) & (df['attributes.SR_PARTLY'] == 'true'))
    df["flag_11"] = np.where(condition,"true","check")
    print("Executed Rule 11")
    # %%
    """
    # Rule 12
    ## Accuracy validation- Height- 
    If (Track ID in second row= Track id in first row, Height value in second row- Height in First row, “End”), 
    highlight wherever the difference in value is less than or equal to -1 and give comment as check and 
    End row as end
    """
    
    
    # %%

    df["rule_12"] = "NA"
    
    df=df.sort_values('Trackid')
    df['rule_12'] = df.height.diff(-1)    
   # df['rule_12'] = (~df.duplicated(subset=['Trackid'], keep='last')).astype(int)
    df['rule_12'] = np.where(df.duplicated(subset=['Trackid'], keep='last'),  df['rule_12'],'End')

    
    print("Executed Rule 12")
    # %%
    """
    # Rule 13
    ## Accuracy validation- Width- If (Track ID in second row= Track id in first row, Width value in second 
    row- Width in First row, “End”), highlight wherever the difference in value is less than or equal to -1 
    and give comment as check and End row as end
    """
    
    # %%
    
    df["rule_13"] = "NA"
    
    df['rule_13'] = df.width.diff(-1)    
   # df['rule_12'] = (~df.duplicated(subset=['Trackid'], keep='last')).astype(int)
    df['rule_13'] = np.where(df.duplicated(subset=['Trackid'], keep='last'),  df['rule_13'],'End')
    
    print("Executed Rule 13")
    # %%
    """
    # Rule 14
    ## All frames between SR- Invisible -Start and Stop frames except start and stop frame, SR-Partly should be false.
    """
    
    # %%
    if 'attributes.SR_INVISIBLE' in df.columns:
        condition = ((df['attributes.SR_INVISIBLE'] == 'Invisible_Start') & (df['attributes.SR_PARTLY'] == 'false'))
        df['flag_14'] = np.where(condition,'true','check')
        condition = ((df['attributes.SR_INVISIBLE'] == 'Invisible_Stop') & (df['attributes.SR_PARTLY'] == 'false'))
        df['flag_14'] = np.where(condition,'true','check')
        
        
        condition = ((df['attributes.SR_SIGN_CLASS'] == 'Info_Direction') & (df['attributes.SR_SIGN_CLASS'] == 'Info_Direction_Yellow'))
        df['flag_14'] = np.where(condition,'true','check')
    else:
        df['flag_14']="NA"
    
    print("Executed Rule 14")
    # %%
    """
    # Rule 15
    ## If Sign class= Info direction or Info direction yellow then SR_invalid should be none.
    """
    
    # %%
    df["Rule15_flag"]=""
    for row in range(len(df)):
        if df['attributes.SR_SIGN_CLASS'].loc[row]=='Info_Direction' or df['attributes.SR_SIGN_CLASS'].loc[row]=='Info_Direction_Yellow' :
            if df['attributes.SR_INVALID'].loc[row]=='None':        
                df["Rule15_flag"].loc[row]="True"
            else:
                df["Rule15_flag"].loc[row]="False"
        else:
            df["Rule15_flag"].loc[row]="NA"
    
    print("Executed Rule 15")
    

    # %%
    """
    # Rule 16
    ## If sign class= Info direction or Info direction yellow, then those track ids should not be main ID for any supplementary signs
    """
    
    # %%
    # df["Rule16_flag"]=""
    # for row in range(len(df)):
    #     if df['attributes.SR_SIGN_CLASS'].loc[row]=='Info_Direction' or df['attributes.SR_SIGN_CLASS'].loc[row]=='Info_Direction_Yellow' :
    #         if df['category'].loc[row]=='Supplementary Sign': 
    #             if str(df['Trackid'])!= df['attributes.SR_MAIN_ID']:
    #                 df["Rule16_flag"].loc[row]="True"
    #             else:
    #                 df["Rule16_flag"].loc[row]="False"
    #         else:
    #             df["Rule16_flag"].loc[row]="NA"
    #     else:
    #         df["Rule16_flag"].loc[row]="NA"
    
    
    if 'attributes.SR_MAIN_ID' in df.columns:
        df['Rule16_flag']='NA'
        df.loc[((df['attributes.SR_SIGN_CLASS']=='Info_Direction')|(df['attributes.SR_SIGN_CLASS']=='Info_Direction_Yellow')) & (df['category']=='Supplementary Sign') &(df['Trackid']!='attributes.SR_MAIN_ID'),'Rule16_flag'] = 'True'
        df.loc[((df['attributes.SR_SIGN_CLASS']=='Info_Direction')|(df['attributes.SR_SIGN_CLASS']=='Info_Direction_Yellow')) & (df['category']=='Supplementary Sign') &(df['Trackid']=='attributes.SR_MAIN_ID'),'Rule16_flag'] = 'True'
    else:
        df['Rule16_flag']='NA'
    print("Executed Rule 16")
    
    # %%
    """
    # Rule 17
    ## If category is sign and sign class contains” _inv”, then SR_Flashing should be true else highlight as check
    """
    
    # %%
    df["Rule17_flag"]="NA"
    condition = ((df['category'] == 'Signs') & ("_Inv" in df['attributes.SR_SIGN_CLASS']) & (df['attributes.SR_FLASHING'] == 'true'))
    df['Rule17_flag'] = np.where(condition,'true','check')
    df.loc[((df['category']!='Signs')|("_Inv" in df['attributes.SR_SIGN_CLASS'] )),'Rule17_flag'] = 'NA'
    
    #---------------------------------------completed----------------------
    # df["Rule17_flag"]=""
    # for row in range(len(df)):
    #     if df['category'].loc[row]=='Signs' :
    #         if "_Inv" in df['attributes.SR_SIGN_CLASS'].loc[row]: 
    #             if df['attributes.SR_FLASHING'].loc[row] == 'true':
    #                 df["Rule17_flag"].loc[row]="True"
    #             else:
    #                 df["Rule17_flag"].loc[row]="check"
    #         else:
    #             df["Rule17_flag"].loc[row]="NA"
    #     else:
    #         df["Rule17_flag"].loc[row]="NA"
    #         #---------------------------------------completed----------------------
    # print("Executed Rule 17")
    # %%
    """
    # Rule 18
    ## If track ID has more than one sign class the same needs to be highlighted
    """
    
    # %%
    
    track_id_list_18 = df['Trackid'].tolist()
    track_id_list_18 = set(track_id_list_18)
    track_id_list_18 = sorted(track_id_list_18)
    
    trackid_not_unique_18=[]
    for val_18 in track_id_list_18:
        df_18=df[df["Trackid"]==val_18]
        val_18_list=df_18['attributes.SR_SIGN_CLASS'].tolist()
        if (len(np.unique(val_18_list))==1) == False:
            trackid_not_unique_18.append(val_18)
            
    df["Rule18"]="NA"
    
    df['Rule18'] = np.where(df['Trackid'].isin(trackid_not_unique_18), 'check','true') 
    
    #for val_18_unique in trackid_not_unique_18:
        #condition = ((df['Trackid'] == val_18_unique))
       # df['Rule18'] = np.where(condition,'check','true')
    
    
    
    print("Executed Rule 18")
    # %%
    """
    # Rule 19
    ## All attributes except SR_Invisible ,SR_Partly should be same for entire track id
    """
    if 'attributes.SR_MAIN_ID' in df.columns:    
        track_id_list_19 = df['Trackid'].tolist()
        track_id_list_19 = set(track_id_list_19)
        track_id_list_19 = sorted(track_id_list_19)
        
        trackid_not_unique_19=[]
        for val_19 in track_id_list_19:
            df_19=df[df["Trackid"]==val_19]
            val_19_list=df_19['attributes.SR_DISABLED'].tolist()
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
            
            val_19_list=[]
            val_19_list=df_19['attributes.SR_SIGN_EMBEDDED'].tolist()
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
                
            val_19_list=[]
            val_19_list=df_19['attributes.SR_FOR_OTHER_ROAD'].tolist()
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
        
            val_19_list=[]        
            val_19_list=df_19['attributes.SR_FLASHING'].tolist()
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
        
            val_19_list=[]        
            val_19_list=df_19['attributes.SR_TWISTED'].tolist()
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
        
            val_19_list=[]        
            val_19_list=df_19['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING'].tolist()
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
        
            val_19_list=[]        
            val_19_list=df_19['attributes.SR_SIGN_CLASS'].tolist()  
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
        
            val_19_list=[]        
            val_19_list=df_19['attributes.SR_CONTAMINATED'].tolist() 
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
        
            val_19_list=[]        
            val_19_list=df_19['attributes.SR_MAIN_ID'].tolist() 
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
        
            val_19_list=[]        
            val_19_list=df_19['attributes.SR_INVALID'].tolist() 
            if (len(np.unique(val_19_list))==1) == False:
                trackid_not_unique_19.append(val_19)
                
        trackid_not_unique_19=list(set(trackid_not_unique_19))
                
        df["Rule19"]="NA"
        
        df['Rule19'] = np.where(df['Trackid'].isin(trackid_not_unique_19), 'check','true') 
        
    else:
        df['Rule19']='NA'    
    
    
    
    print("Executed Rule 19")
    
    
    
    # %%
    
    
    # %%
    """
    # Rule 20
    ## If the category is Sign and Sign class= Other Rectangular, highlight the same
    """
    
    # %%
    condition = ((df['category'] == 'Signs') & (df['attributes.SR_SIGN_CLASS'] == 'Other_Rectangular_Sign_Similar'))
    # df['category'].unique()
    df['flag_20'] = np.where(condition,"Same","NA")
    print("Executed Rule 20")
    # %%
    """
    # Rule 21
    ## If the category is supplementary and sign class= other supplementary sign, highlight the same
    """
    
    # %%
    condition = ((df['category'] == 'Supplementary Sign') & (df['attributes.SR_SIGN_CLASS'] == 'Other_Supplementary_Sign'))
    df['flag_21'] = np.where(condition,'Same','NA')
    print("Executed Rule 21")
    # %%
    """
    # Rule 22
    ## If the main class-signs is having an attribute SR_Other Road= True then supplementary sign for that
    main id should also have SR_other road = True 
    """
    
    # %%
    
    if 'attributes.SR_MAIN_ID' in df.columns: 
        df["Rule22_flag"]="NA"    
        df_other_road_22=df[df["attributes.SR_FOR_OTHER_ROAD"]=='true']
        df_other_road_22=df_other_road_22[df_other_road_22["category"]=="Signs"]    
            
        df_other_road_22_list=df_other_road_22["Trackid"].tolist()    
        df_other_road_22_list=list(set(df_other_road_22_list))
        df_other_road_22_list=sorted(df_other_road_22_list)
        df_other_road_22_list = [str(item) for item in df_other_road_22_list]
          
        #df_supple_22 = df[df['attributes.SR_MAIN_ID'].isin(df_other_road_22_list)]    
        
        condition = ((df['attributes.SR_MAIN_ID'].isin(df_other_road_22_list)) & (df['attributes.SR_FOR_OTHER_ROAD'] == 'true'))
        df['Rule22_flag'] = np.where(condition,'true','false')
        
        #for row in range(len(df)):
            #if df["category"].loc[row]=="Signs":
              #  df["Rule22_flag"].loc[row]="NA"
              
        df.loc[(df["category"]=="Signs"), 'Rule22_flag']='NA'
    
    else:
        df["Rule22_flag"]="NA" 
            
      
      
    print("Executed Rule 22")
    
    # %%
    """
    # Rule 23
    ##  If the sign class have multi mounting= True and SR_Other road= True, all sign class in that 
    frame with multi mounting =True should have SR_other road= True and the same is applicable for false.
    """
    
    # %%
    
    df['rule_23a'] = 'NA'
    df.loc[df['category']!='Signs','rule_23a']='NA'  
    df.loc[((df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='true') & (df['category'] == 'Signs') & (df['attributes.SR_FOR_OTHER_ROAD']=='true')),'rule_23a']='true'
    frames=df.loc[((df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='true') & (df['category'] == 'Signs') & (df['attributes.SR_FOR_OTHER_ROAD']=='true')),'Labels.Devices.Channels.ObjectLabels.FrameNumber']
    df.loc[df['Labels.Devices.Channels.ObjectLabels.FrameNumber'].isin(frames) &((df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='true') & (df['attributes.SR_FOR_OTHER_ROAD']!='true')),'rule_23a']='false'

    # df["Rule23a_flag"]="NA"
    # list_framenumbers_23a=[]
    # for row in range(len(df)):
    #     if df["category"].loc[row]== "Signs":
    #         if df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING'].loc[row] != 'true':
    #             if df['attributes.SR_FOR_OTHER_ROAD'].loc[row] == 'true': 
    #                 list_framenumbers_23a.append(df['Labels.Devices.Channels.ObjectLabels.FrameNumber'])
    # list_framenumbers_23a=list_framenumbers_23a[0].tolist()
    # list_framenumbers_23a=sorted(list_framenumbers_23a)  
    
    # for i,r in df.iterrows():
    #     for val in list_framenumbers_23a:
    #         if val == r['Labels.Devices.Channels.ObjectLabels.FrameNumber']:
    #             if r['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='true':
    #                 if df['attributes.SR_FOR_OTHER_ROAD'].loc[row] == 'true': 
    #                     df.loc[i,'Rule23a_flag'] = 'true'
    #                 else:
    #                     df.loc[i,'Rule23a_flag'] = 'false'       
                        
                        
    '''condition = ((df['Labels.Devices.Channels.ObjectLabels.FrameNumber'].isin(list_framenumbers_23a)) & (df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING'] == 'true') & (df['attributes.SR_FOR_OTHER_ROAD'] == 'true'))             
    df['Rule23a_flag'] = np.where(condition, 'check','true')         

    for row in range(len(df)):
            if if val != r['Labels.Devices.Channels.ObjectLabels.FrameNumber']:
                if "_Inv" in df['attributes.SR_SIGN_CLASS'].loc[row]: 
                    if df['attributes.SR_FLASHING'].loc[row] == 'true':
                        df["Rule17_flag"].loc[row]="True"
                    else:
                        df["Rule17_flag"].loc[row]="check"
                else:
                    df["Rule17_flag"].loc[row]="NA"
            else:
                df["Rule17_flag"].loc[row]="NA"    '''
    
    #RULE 23b
    
    # df["Rule23b_flag"]="NA"
    # list_framenumbers_23b=[]
    # for row in range(len(df)):
    #     if df['attributes.SR_SIGN_ON_MULTI_SIGNo documentatiN_MOUNTING'].loc[row] != 'true':
    #         if df['attributes.SR_FOR_OTHER_ROAD'].loc[row] == 'false': 
    #             list_framenumbers_23b.append(df['Labels.Devices.Channels.ObjectLabels.FrameNumber'])
    # list_framenumbers_23b=list_framenumbers_23b[0].tolist()
    # list_framenumbers_23b=sorted(list_framenumbers_23b)  
    
    # for i,r in df.iterrows():
    #     for val in list_framenumbers_23b:
    #         if val == r['Labels.Devices.Channels.ObjectLabels.FrameNumber']:
    #             if r['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='true':
    #                 if df['attributes.SR_FOR_OTHER_ROAD'].loc[row] == 'false': 
    #                     df.loc[i,'Rule23b_flag'] = 'true'
    #                 else:
    #                     df.loc[i,'Rule23b_flag'] = 'false'

    df['rule_23b'] = 'NA'
    df.loc[df['category']!='Signs','rule_23a']='NA'  
    df.loc[((df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='true') & (df['category'] == 'Signs') & (df['attributes.SR_FOR_OTHER_ROAD']=='false')),'rule_23b']='true'
    frames=df.loc[((df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='true') & (df['category'] == 'Signs') & (df['attributes.SR_FOR_OTHER_ROAD']=='false')),'Labels.Devices.Channels.ObjectLabels.FrameNumber']
    df.loc[df['Labels.Devices.Channels.ObjectLabels.FrameNumber'].isin(frames) &((df['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='true') & (df['attributes.SR_FOR_OTHER_ROAD']=='true')),'rule_23b']='false'


    print("Executed Rule 23")
    # %%
    """
    # Rule 24
    ## 	If the category is sign in a frame and ShapeX – first coordinate for all signs are with a 
    difference of +/-  10, Multimounting should be True else highlight as check
 """
    
    # %%


    # df["Rule24_flag"]=""
    # def findPair(arr,n):
    #     pairs=[]
    #     size = len(arr)
    #     i,j = 0,1
    #     while i < size and j < size:
    #         if i != j and arr[j]-arr[i] <= n:
    #             #print("Pair found (",arr[i],",",arr[j],")")
    #             pairs.append(arr[i])
    #             pairs.append(arr[j])
    #             return pairs
    #         elif arr[j] - arr[i] > n:
    #             j+=1
    #         else:
    #             i+=1
    #     #print("No pair found")
    #     return pairs
    
    
    
    # df_signs_24=df[df["category"]=="Signs"]
    # frame_numbers_24= df_signs_24['Labels.Devices.Channels.ObjectLabels.FrameNumber'].tolist()     
    # frame_numbers_24=[k for k, v in Counter(frame_numbers_24).items() if v > 1] 
    # frame_numbers_24=sorted(frame_numbers_24)
    
    # for val_24 in frame_numbers_24:
    #     df_24=df[df['Labels.Devices.Channels.ObjectLabels.FrameNumber']==val_24]
    #     x_coordinates_24=df_24["shape.x"].tolist()
    #     x_coordinates_24 = [item[0] for item in x_coordinates_24]
    #    # print("----------------------", x_coordinates_24)
    #     pairs=findPair(x_coordinates_24, 10) 
    #     #print("pairssssssss",pairs)
    #     if len(pairs)>1:
    
        
    #         for val_pair in pairs:
    #             for row in range(len(df)):
    #                 if df["shape.x"][0][0]==val_pair:
    #                     if df[attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING]=="true":
    #                         df["Rule24_flag"].loc[row]="True"
    #                     else:
    #                         df["Rule24_flag"].loc[row]="false"
                            
    #                 else:
    #                     df["Rule24_flag"].loc[row]="NA"
                
        
    #condition = ((df["shape.x"][0][0].isin(pairs)) & (df[attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING] == 'true'))
   # df['Rule24'] = np.where(condition, 'check','true') 
    
   
    print("Executed Rule 24")
    # %%
    """
    # Rule 25
    ## If a Frame has only one sign and One Supplementary sign, Multimounting should be false else check.
    """
    
    # %%

    df["Rule25_flag"]="NA"
    from collections import Counter
    df2=df.loc[df['category'] == "Signs"] 
    df3=df.loc[df['category'] == "Supplementary Sign"] 
    list_framenumbers_signs=df2['Labels.Devices.Channels.ObjectLabels.FrameNumber'].tolist()
    list_framenumbers_signs_nr=[k for k,v in Counter(list_framenumbers_signs).items() if v==1]
    
    
    list_framenumbers_supple=df3['Labels.Devices.Channels.ObjectLabels.FrameNumber'].tolist()
    list_framenumbers_supple_nr=[k for k,v in Counter(list_framenumbers_supple).items() if v==1]
    
    list_framenumbers_signs_as_set = set(list_framenumbers_signs_nr)
    intersection = list_framenumbers_signs_as_set.intersection(list_framenumbers_supple_nr)
    intersection_as_list = list(intersection)
    
    
    for i,r in df.iterrows():
        for val in intersection_as_list:
            if val == r['Labels.Devices.Channels.ObjectLabels.FrameNumber']:
                if r['attributes.SR_SIGN_ON_MULTI_SIGN_MOUNTING']=='false':
                    df.loc[i,'Rule25_flag'] = 'false'
                else:
                    df.loc[i,'Rule25_flag'] = 'check'

    
    print("Executed Rule 25")
    # %%
    """
    # Rule 26
    ## If SR_Disabled = True, then SR_Flashing should be False else highlight check
    """
    
    # %%
    # condition = ((df['attributes.SR_Disabled'] == 'true') & (df['attributes.SR_FLASHING'] == 'false'))
    # df['flag_26'] = np.where(condition,'true','check')
    
    df["Rule26_flag"]="NA"
    condition = ((df['attributes.SR_DISABLED'] == 'true') & (df['attributes.SR_FLASHING']=='false'))
    df['Rule26_flag'] = np.where(condition,'true','check')
    df.loc[((df['attributes.SR_DISABLED']!='true')),'Rule26_flag'] = 'NA'


    # df["Rule26_flag"]=""
    # for row in range(len(df)):
    #     if df['attributes.SR_DISABLED'].loc[row] == 'true':
    #         if df['attributes.SR_FLASHING'].loc[row] == 'FALSE': 
    #             df["Rule26_flag"].loc[row]="True"
    #         else:
    #             df["Rule26_flag"].loc[row]="Check"
    #     else:
    #         df["Rule26_flag"].loc[row]="NA"
    
    print("Executed Rule 26")
    # %%
    """
    # Rule 27
    ##  If sign class=Other octagon, highlight as check
    """
    
    # %%
    # df["Rule26_flag"]=""
    # for row in range(len(df)):
    #     if df['attributes.SR_DISABLED'].loc[row] == 'true':
    #         if df['attributes.SR_FLASHING'].loc[row] == 'FALSE': 
    #             df["Rule26_flag"].loc[row]="True"
    #         else:
    #             df["Rule26_flag"].loc[row]="Check"
    #     else:
    #         df["Rule26_flag"].loc[row]="NA"
    
    condition = df['attributes.SR_SIGN_CLASS'].str.contains('Other_Octagon')
    df['flag_27'] = np.where(condition,'Check','NA')

    
    print("Executed Rule 27")
    # %%
    """
    # Rule 28
    ##  If the sign class contains city, the SR_Other road should be false else highlight as check.
    """
    
    # %%
    condition = (df['attributes.SR_SIGN_CLASS'].str.contains('City') & (df['attributes.SR_FOR_OTHER_ROAD'] == 'false'))
    df['flag_28'] = np.where(condition,'true','check')
    

    print("Executed Rule 28")
    # %%
    
    
    #if "false" or "check" in df:
        
    writer = pd.ExcelWriter(filename.replace('.json','.xlsx'), engine='xlsxwriter')
    
    df.to_excel(writer, sheet_name='Validation_Result')
    # df_rules_meta.to_excel(writer, sheet_name = 'Definition')
    workbook  = writer.book
    worksheet = writer.sheets['Validation_Result']
    
    
    writer.save()
    
    stop = timeit.default_timer()
    print('Execution time: ', stop - start)
    
    
    
    
#tool_validation(filename)