import time
import io
import cv2
import h5py
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from multiprocessing import Pool
import os
import json

a = time.time()
fn = ""
print("-----------------------------------===========================================")
print("Conversion STARTED")
def converter_webm(filename): 
    final_dict={}
    print("-----------------------------------===========================================")
    print("Conversion STARTED",filename)
    input_path = os.path.dirname(filename)
    # output_path = input_path.rstrip("/raw")
    output_path = input_path
    print(output_path)
    if filename.endswith(".h5"):
        fn=filename.split(".h5")[0]
        print("-----------------fnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",fn)
        #fn=fn.split("/")[-1]
        print(fn)
        hdf = h5py.File(filename,'r')
        keys = []
        with h5py.File(filename, 'r') as f:
            f.visit(keys.append)

        devicename=keys[0]
        channelname=keys[1].split("/")[1]

        

        timestamp = keys[2:]

        timestamp = [i.split("/")[2] for i in timestamp]
        frame_numbers = list(range(1, len(timestamp)+1))
        frame_timestamp_dict = {frame_numbers1:timestamp1 for timestamp1,frame_numbers1 in zip(timestamp,frame_numbers)}
        final_dict["devicename"]=devicename
        final_dict["channelname"]=channelname
        final_dict["frame_timestamp_dict"]=frame_timestamp_dict

        txtfilename=fn+".txt"        
        file1 = open(txtfilename,"w")
        file1.write(json.dumps(final_dict))

        keys=keys[2:]

        print(final_dict)
        print(output_path+"/"+fn+'.webM')
        list_of_array=map(lambda x:hdf[x][:], keys)

        save_val = [output_path+"/"+str(i) for i in range(len(keys))]
        new_obj = list(zip(list(list_of_array),save_val))
        with Pool(6) as pool:
           res = Pool(6).starmap(iw, new_obj)
            # print(res)
        # all_img = [iw(i,j) for i,j in new_obj]
        # print(all_img)
        os.chdir(output_path)
        # time.sleep(500)
        #ffmpeg_output = "ffmpeg -framerate 10 -pattern_type glob -i '*.jpeg' -c:v libx264 -pix_fmt yuv420p "+ str(fn) +".mp4"
        # ffmpeg_output = 'ffmpeg -framerate 12 -i "%d.jpeg" -c:v libx264 -pix_fmt yuv420p '+ str(fn) +'.mp4'
        # ffmpeg_output = 'ffmpeg -framerate 12 -i "%d.jpeg" -c:v libx264 -pix_fmt yuv420p '+ str(fn) +'.mp4'
        #ffmpeg_output = 'ffmpeg -framerate 12 -i "%d.jpeg" -c:v libx264 -pix_fmt yuv420p '+ str(fn) +'.mp4'
        ffmpeg_output = 'ffmpeg -hwaccel cuda -framerate 12 -i "%d.jpeg" -c:v libx264 -pix_fmt yuv420p '+ str(fn) +'.mp4'
        os.system(ffmpeg_output)

        ends=(".jpeg", ".h5")
        for f in os.listdir(output_path):
            if not f.endswith(ends):
                continue
            os.remove(os.path.join(output_path, f))


        # excute_command(output_path,fn)



import time
def iw(arr,obj):
    img = Image.open(io.BytesIO(arr))
    # sharpened1 = img.filter(ImageFilter.SHARPEN);
    # sharpened2 = sharpened1.filter(ImageFilter.SHARPEN);
    # sharpened2.save(str(obj)+".jpeg")
    # from wand.image import Image
    # with Image(filename = str(obj)+".jpeg") as img:
    #     img.sharpen(radius = 100, sigma = 50)
    #     img.save(filename = str(obj)+".jpeg")

    thrshld=30

    if np.mean(img) < thrshld:

       enhancer = ImageEnhance.Brightness(img)
       factor = 12.5 
       im_output = enhancer.enhance(factor)

       sharpened1 = im_output.filter(ImageFilter.SHARPEN);
       sharpened2 = sharpened1.filter(ImageFilter.SHARPEN);
       sharpened2.save(str(obj)+".jpeg")  

    else:
       sharpened1 = img.filter(ImageFilter.SHARPEN);
       sharpened2 = sharpened1.filter(ImageFilter.SHARPEN);
       sharpened2.save(str(obj)+".jpeg")       
    # return True

print(time.time()-a)

print("imagessssssssssstime", time.time()-a)
#os.system("ffmpeg -framerate 30 -pattern_type glob -t 100 -i '*.jpeg' -c:v libx264 -pix_fmt yuv420p out.mp4")
#zipit = "zip -r out "+bigh5+" -i '*.jpeg'"
#os.system(zipit)
#ffmpeg -framerate 10 -pattern_type glob -i '*.jpeg' -c:v libx264 -pix_fmt yuv420p bigh5.mp4
def excute_command(dirname,fff):
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    os.chdir(dirname)
    #ffmpeg_output = "ffmpeg -framerate 10 -pattern_type glob -i '*.jpeg' -c:v libx264 -pix_fmt yuv420p "+ str(fff) +".mp4"
    #os.system(ffmpeg_output)
    # import ffmpeg
    aa=time.time()
    print("video", time.time())
    print("HERE ALL THE IMAGES ARE PRINTED NOW VIDEO PART")
    (
    ffmpeg
    .input(dirname+'/*.jpeg', pattern_type='glob', framerate=10)
    .output(fff)
    .run()
    )
    print("HERE ALL THE IMAGES ARE PRINTED NOW VIDEO PART")

    bb=time.time()
    print("ffmpegggggssssssssssstime", bb-aa)
    #zipit = "zip -r out "+fff+" -i '*.jpeg'"
    #print(zipit)
    #print("is created###########################################################")
    #time.sleep(10)
    #os.system(zipit)
    # os.system("rm -rf *.jpeg")
    # return True
