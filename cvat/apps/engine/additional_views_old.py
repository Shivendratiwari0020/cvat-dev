from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404



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
        # tshape = labtr.trackedshape_set.create(points=labtr.trackedshape_set.last().points,frame=int(request.data.get('end_frame')),type='rectangle')
        # att = AttributeSpec.objects.get(id=labtr.label_id)
        # tshape.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_val"))
        att = AttributeSpec.objects.get(id=request.data.get('attribute_id'))
        ltt = LabeledTrack.objects.get(id=int(request.data.get('AnnotationId')))
        tshape = ltt.trackedshape_set.first() # FIXME i ah
        t_start_obj = TrackedShape.objects.create(track=tshape.track,points=tshape.points,type=tshape.type,frame=int(request.data.get('start_frame')))
        t_end_obj = TrackedShape.objects.create(track=tshape.track,points=tshape.points,type=tshape.type,frame=int(request.data.get('end_frame')))
        t_start_obj.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_val"))
        t_end_obj.trackedshapeattributeval_set.create(spec = att,value=request.data.get("attribute_previous_val"))
        return Response({"message":"true"})

class GetProjectMode(viewsets.ModelViewSet):
    queryset = AdditionalProjectInfo.objects.filter()
    serializer_class = AdditionalProjectTypeInfoSerializer
    
    def retrieve(self,request,pk):
        project_type = get_object_or_404(self.queryset, project_id=Job.objects.get(id=pk).get_project_id())
        serializer = self.serializer_class(project_type)
        return Response(serializer.data)





