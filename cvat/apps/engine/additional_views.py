from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .crop_images_label_corrector import label_generator_crop
from .serializers import *


# class ProjectExtraViewSet(viewsets.ModelViewSet):
#     queryset = AdditionalProjectInfo.objects.filter()
#     serializer_class = AdditionalProjectInfoSerializer

#     def retrieve(self, request, pk):
#         # Job.objects.get(id=pk).get_project_id()
#         # queryset = Catfolder.objects.filter(projectid=60)
#         # pk=Job.objects.get(id=pk).get_project_id()
#         data = []
#         # serializer_class = AdditionalProjectInfoSerializer(self.queryset.filter(project_id=Job.objects.get(id=pk).get_project_id()),many=True)
#         # for item in serializer_class.data[0].get("corrector_schema").keys():
#         #     data.append(serializer_class.data[0].get("corrector_schema").get(item)[1])

#         return Response(data)

# start of label corrector

class GetCroppedImages(viewsets.ViewSet):

    @action(detail=True, methods=['GET', 'OPTIONS', 'POST','PUT'])
    def frame_data(self,request,pk):
        task_id = Job.objects.get(id=pk).get_task_id()
        image_folder = settings.BASE_DIR+"/data/data/"+str(task_id)+"/raw/"

        # track_id = 291
        track_id = request.GET.get("track_id")
        
        print(track_id,"track_idtrack_idtrack_idtrack_idtrack_id")
        instance_trackedshape = TrackedShape.objects.filter(track_id=track_id).values()
        instance_labeledtrack = LabeledTrack.objects.filter(id=track_id).values()

        # instance_trackedshape = TrackedShape.objects.filter(track_id=labe_id).values()
        # instance_labeledtrack = LabeledTrack.objects.filter(id=labe_id).values()

        list_of_instance_trackedshape = list(instance_trackedshape)
        list_of_instance_labeledtrack = list(instance_labeledtrack)
        print("image_folder", image_folder, "list_of_instance_trackedshape", list_of_instance_trackedshape, "list_of_instance_labeledtrack", list_of_instance_labeledtrack)


        data = label_generator_crop(image_folder, list_of_instance_trackedshape, list_of_instance_labeledtrack)

        # data = "hello"
        return Response(data)


class ProjectExtraViewSet(viewsets.ModelViewSet):
    queryset = AdditionalProjectInfo.objects.filter()
    serializer_class = AdditionalProjectInfoSerializer

    def retrieve(self, request, pk):
        # Job.objects.get(id=pk).get_project_id()
        # queryset = Catfolder.objects.filter(projectid=60)
        # pk=Job.objects.get(id=pk).get_project_id()
        data = []
        serializer_class = AdditionalProjectInfoSerializer(self.queryset.filter(project_id=Job.objects.get(id=pk).get_project_id()),many=True)
        for item in serializer_class.data[0].get("corrector_schema").keys():
            data.append(serializer_class.data[0].get("corrector_schema").get(item)[1])

        return Response(data)

# end of laebl corrector

class BulkUpdate(viewsets.ModelViewSet):
    # queryset = AdditionalProjectInfo.objects.filter()
    queryset = ''
    serializer_class = SaveTrackSerializer
# <'job_id': ['3'], 'trackid': ['33'], 'start_frame': ['333'], 'end_frame': ['33'], 'attribute_name': ['33'], 'attribute_val': ['33']}>

    @action(detail=True, methods=['OPTIONS', 'POST','PUT'], url_path=r'data')
    def data(self, request,pk):
        # data = request.data
        # trackid = int(request.data.get('trackid',1)) - 1
        # labtr = LabeledTrack.objects.filter(job_id=int(request.data.get('job_id')))[trackid]
        # # create_labeled_shape_frames_with_last_points = range(int(request.data.get('start_frame')),int(request.data.get('end_frame')))
        # tshape = labtr.trackedshape_set.create(points=labtr.trackedshape_set.last().points,frame=int(request.data.get('start_frame')),type='rectangle')
        # tshape_last = labtr.trackedshape_set.create(points=labtr.trackedshape_set.last().points,frame=int(request.data.get('end_frame')),type='rectangle')
        # if int(labtr.trackedshape_set.last().frame)  > int(request.data.get('end_frame')):
        #     frr = int(request.data.get('end_frame')) + 1
        #     tshape_frame_last = labtr.trackedshape_set.create(points=labtr.trackedshape_set.last().points,frame=frr,type='rectangle')
        #     tshape_frame_last.trackedshapeattributeval_set.create(spec = att)
        # # att = AttributeSpec.objects.get(id=labtr.label_id)
        # att = AttributeSpec.objects.filter(name=request.data.get("attribute_name")).last()
        # tshape.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_val").lower())
        # tshape_last.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_val").lower())
        # att = AttributeSpec.objects.filter(name=request.data.get("attribute_name")).last()
        # tshape = TrackedShape.objects.get(id=int(request.data.get('AnnotationId')))
        att = AttributeSpec.objects.get(id=request.data.get('attribute_id'))
        ltt = LabeledTrack.objects.get(id=int(request.data.get('AnnotationId')))
        tshape = ltt.trackedshape_set.first() # FIXME i ah
        t_start_obj = TrackedShape.objects.create(track=tshape.track,points=tshape.points,type=tshape.type,frame=int(request.data.get('start_frame')))
        t_end_obj = TrackedShape.objects.create(track=tshape.track,points=tshape.points,type=tshape.type,frame=int(request.data.get('end_frame')))
        t_start_obj.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_val"))
        t_end_obj.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_previous_val"))
        return Response({"message":True})

class LabelCorrectorAttrSave(viewsets.ModelViewSet):
    # queryset = AdditionalProjectInfo.objects.filter()
    queryset = ''
    serializer_class = LabelSaveSerializer
    # <'job_id': ['3'], 'trackid': ['33'], 'start_frame': ['333'], 'end_frame': ['33'], 'attribute_name': ['33'], 'attribute_val': ['33']}>
# attribute_id,frame,track_id
    @action(detail=True, methods=['OPTIONS', 'GET', 'POST','PUT'])
    def data(self, request,pk):
        att = AttributeSpec.objects.get(id=request.data.get('attribute_id'))
        ltt = LabeledTrack.objects.get(id=int(request.data.get('AnnotationId')))
        tshape = ltt.trackedshape_set.first() # FIXME i ah
        t_start_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=int(request.data.get('frame')))
        tr_att = t_start_obj[0].trackedshapeattributeval_set.get_or_create(spec = att,value = request.data.get("attribute_val","false"))
        # tr_att[0].value = request.data.get("attribute_val")
        # tr_att[0].save()
        prev_val = request.data.get('attributre_previous_value')
        next_frame_id = int(request.data.get('frame')) + 1
        t_next_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=next_frame_id)
        tr_att = t_next_obj[0].trackedshapeattributeval_set.get_or_create(spec = att,value = prev_val)
        
        # t_start_obj = TrackedShape.objects.create(track=tshape.track,points=tshape.points,type=tshape.type,frame=int(request.data.get('start_frame')))
        # t_end_obj = TrackedShape.objects.create(track=tshape.track,points=tshape.points,type=tshape.type,frame=int(request.data.get('end_frame')))
        # t_start_obj.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_val"))
        # t_end_obj.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_previous_val"))
        return Response({"message":True})

    
class SaveSRVisibleData(viewsets.ViewSet):
    queryset = ''
    serializer_class = LabelSaveSerializer
    
    @action(detail=True, methods=['GET', 'OPTIONS', 'POST','PUT'])
    def sr_visible(self,request,pk):
        # task_id = Job.objects.get(id=pk).get_task_id()
        if request.method == "POST":
            frame = int(request.data.get("frame"))
            label_id = int(request.data.get("AnnotationId"))
            value  = request.data.get("attribute_val") 
            label = LabeledTrack.objects.get(id=label_id)
            att = AttributeSpec.objects.get(id=request.data.get('attribute_id'))
            tshape = label.trackedshape_set.first()

            if value == "Invisible_Start":
                new_frame = frame - 1
                if new_frame < 0:new_frame = 0  
                t_start_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=new_frame)
                new_att = t_start_obj[0].trackedshapeattributeval_set.get_or_create(spec = att)
                if new_att[0].value == "Invisible_Stop":
                    new_att[0].value = "Invisible_Stop_And_Start"
                else:
                    new_att[0].value = "Invisible_Start"
                new_att[0].save()
                t_start_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=frame)
                t_start_obj[0].outside = 1
                t_start_obj[0].save()

                next_frame = frame + 1
                t_start_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=next_frame)
                t_start_obj[0].outside = 0
                t_start_obj[0].save()
                new_att = t_start_obj[0].trackedshapeattributeval_set.get_or_create(spec = att)
                new_att[0].value = "Invisible_Stop"
                new_att[0].save()

            if value == "Invisible_Stop":
                t_start_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=frame)
                t_start_obj[0].outside = 0
                t_start_obj[0].save()
                new_att = t_start_obj[0].trackedshapeattributeval_set.get_or_create(spec = att)
                new_att[0].value = "Invisible_Stop"
                new_att[0].save()

            if value == "Invisible_Stop_And_Start":
                new_frame = frame - 1
                if new_frame < 0:new_frame = 0  
                t_start_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=new_frame)
                new_att = t_start_obj[0].trackedshapeattributeval_set.get_or_create(spec = att)
                if new_att[0].value == "Invisible_Stop":
                    new_att[0].value = "Invisible_Stop_And_Start"
                else:
                    new_att[0].value = "Invisible_Start"
                new_att[0].save()
                t_start_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=frame)
                t_start_obj[0].outside = 1
                t_start_obj[0].save()
                new_frame = frame + 1
                t_start_obj = TrackedShape.objects.get_or_create(track=tshape.track,points=tshape.points,type=tshape.type,frame=new_frame)
                t_start_obj[0].outside = 0
                t_start_obj[0].save()
                new_att = t_start_obj[0].trackedshapeattributeval_set.get_or_create(spec = att)
                new_att[0].value = "Invisible_Stop"
                new_att[0].save()
            return Response({"message":"true"})
        else:
            return Response({"message":""})

class GetProjectMode(viewsets.ModelViewSet):
    queryset = AdditionalProjectInfo.objects.filter()
    serializer_class = AdditionalProjectTypeInfoSerializer
    
    def retrieve(self,request,pk):
        project_type = get_object_or_404(self.queryset, project_id=Job.objects.get(id=pk).get_project_id())
        serializer = self.serializer_class(project_type)
        return Response(serializer.data)