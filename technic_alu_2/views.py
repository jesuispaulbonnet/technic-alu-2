from django.http import JsonResponse
from technic_alu_2.controllers.gallery_image import get_gallery_images_by_page_id
from technic_alu_2.controllers.send_email import send_email
from wagtail.images.models import Rendition
import json


def get_gallery_images(request):
    page_id = request.GET.get('page_id', None)
    return JsonResponse(
        {
            'data': get_gallery_images_by_page_id(page_id)
        },
        json_dumps_params={'indent': 2}
    )


def send_message(request):
    if request.method == 'POST':
        message = json.loads(request.body)
        result = send_email(message)
        return JsonResponse(
            {
                'data': result
            },
            json_dumps_params={'indent': 2}
        )


def remove_reditions(request):
    if request.method == 'GET':
        Rendition.objects.all().delete()
        return JsonResponse(
            {
                'result': 'OK'
            },
            json_dumps_params={'indent': 2}
        )
