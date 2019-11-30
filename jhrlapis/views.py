import json

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.crawler import Crawler


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def getStart(request):
    crawler = Crawler()
    data = {
        'jsid' : crawler.getJsid(),
        'yzmUrl' : crawler.getYzm(),
        #'yzmHeader' : crawler.getYzmHeader()
    }
    return Response(data)

@api_view(['GET'])
def getYzm(request):
    jsid = request.GET.get('jsid')
    crawler = Crawler(jsid)
    return HttpResponse(crawler.getYzmBin(),content_type="image/png")


@api_view(['POST'])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    yzm = request.POST.get('yzm')
    jsid = request.POST.get('jsid')
    crawler = Crawler(jsid)
    resl = crawler.login(username,password,yzm)
    return Response(resl)


@api_view(['GET'])
def getSettings(request):
    jsid = request.GET.get('username')
    res = {
        'schoolStartDate': "2019-9-16",
        'schoolTotalWeeks': "16"
    }
    return Response(res)


@api_view(['GET'])
def getKb(request):
    xq = request.GET.get('xq')
    xn = request.GET.get('xn')
    jsid = request.GET.get('jsid')
    crawler = Crawler(jsid)
    res = crawler.getKb(xn,xq)
    return HttpResponse(res)