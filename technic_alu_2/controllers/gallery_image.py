from home.models import GalleryImage
from wagtail.images.models import Image


def get_gallery_images_by_page_id(page_id):
    gallery_images = GalleryImage.objects.filter(page=page_id).all()
    return serialize_gallery_images(gallery_images)


def serialize_image(image):
    return {
        'id': image.pk,
        'title': image.title if hasattr(image, 'title') else None,
        'file': image.file.url,
    }


def serialize_gallery_image(gallery_image):
    image = Image.objects.get(pk=gallery_image.image.pk)
    image_thumbnail = image.get_rendition('fill-450x270')
    return {
        'id': gallery_image.pk,
        'caption': gallery_image.caption,
        'image': serialize_image(image),
        'image_thumbnail': serialize_image(image_thumbnail),
    }


def serialize_gallery_images(gallery_images):
    return [
        serialize_gallery_image(gallery_image)
        for gallery_image in gallery_images
    ]
