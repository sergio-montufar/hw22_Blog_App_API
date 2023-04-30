from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import Blog
from django.views import View
from .helpers import GetBody

# Create your views here.
class BlogView(View):
  # BLOG - INDEX ROUTE
  def get(self, request):
    all = Blog.objects.all()
    serialized = serialize("json", all)
    finalData = json.loads(serialized)
    return JsonResponse(finalData, safe=False)

  # BLOG - CREATE ROUTE
  def post(self, request):
    body = GetBody(request)
    print(body)
    blog = Blog.objects.create(name=body["name"], age=body["age"])
    finalData = json.loads(serialize("json", [blog]))
    return JsonResponse(finalData, safe=False)

class BlogViewID(View):
  # BLOG - SHOW ROUTE
  def get(self, request, id):
    try:
      blog = Blog.objects.get(id=id)
      finalData = json.loads(serialize("json", [blog]))
      return JsonResponse(finalData, safe=False)
    except ObjectDoesNotExist:
      return JsonResponse({"error": "Not Found", "code": 500})
  # BLOG - UPDATE ROUTE
  def put(self, request, id):
    try:
      body = GetBody(request)
      Blog.objects.filter(id=id).update(**body)
      blog = Blog.objects.get(id=id)
      finalData = json.loads(serialize("json", [blog]))
      return JsonResponse(finalData, safe=False)
    except ObjectDoesNotExist:
      print(f"Could not update blog at the id of {id}, blog does not exist")
      return JsonResponse({"error": "Cannot update blog, blog does not exist", "code": 500})

  # BLOG - DELETE ROUTE
  def delete(self, request, id):
    try:
      blog = Blog.objects.get(id=id)
      blog.delete()
      finalData = json.loads(serialize("json", [blog]))
      return JsonResponse(finalData, safe=False)
    except ObjectDoesNotExist:
      return JsonResponse({"error": "Cannot delete blog, blog does not exist", "code" : 500})
