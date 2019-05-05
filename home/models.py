from django.db import models
from django.utils.functional import cached_property
from django.conf import settings

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    InlinePanel,
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailgeowidget.edit_handlers import GeoPanel
from wagtailgeowidget.helpers import geosgeometry_str_to_struct


def get_base_context():
    context = {}
    context['gallery_pages'] = GalleryPage.objects.live().in_menu()
    context['contact_page'] = ContactPage.objects.live().in_menu().first()
    return context


class HomePage(Page):
    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context.update(get_base_context())
        return context

    presentation_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        InlinePanel('carousel_images', label="Carousel Images"),
        FieldPanel('presentation_text', classname="full"),
        InlinePanel('presentation_blocks', label="Page d'accueil sections"),
    ]


class CarouselImage(Orderable):
    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name='carousel_images'
    )

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('subtitle'),
    ]


class PresentationBlock(Orderable):
    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name='presentation_blocks'
    )

    description = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('description', classname="full"),
    ]


class GalleryPage(Page):
    def get_context(self, request):
        context = super(GalleryPage, self).get_context(request)
        context.update(get_base_context())
        return context

    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        InlinePanel('gallery_images', label="Gallery Images"),
    ]


class GalleryImage(Orderable):
    page = ParentalKey(
        GalleryPage,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    caption = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='gallery_image'
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class ContactPage(Page):
    def get_context(self, request):
        context = super(ContactPage, self).get_context(request)
        context.update(get_base_context())
        context.update({
            'api_key': settings.GOOGLE_MAPS_V3_APIKEY
        })
        return context

    map_address = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    zoom = models.IntegerField(null=True)

    address = RichTextField(blank=True)
    contact = RichTextField(blank=True)
    other_info = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('map_address'),
            GeoPanel('location', address_field='map_address'),
            FieldPanel('zoom'),
        ], ('Google Map configuration')),
        FieldPanel('address', classname="full"),
        FieldPanel('contact', classname="full"),
        FieldPanel('other_info', classname="full"),
        InlinePanel('receiver_emails', label="Adresses emails receveurs"),
    ]

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point['y']

    @property
    def lng(self):
        return self.point['x']


class ReceiverEmails(Orderable):
    page = ParentalKey(
        ContactPage,
        on_delete=models.CASCADE,
        related_name='receiver_emails'
    )

    email = models.CharField(max_length=250)

    panels = [
        FieldPanel('email'),
    ]


class MarquePage(Page):
    def get_context(self, request):
        context = super(MarquePage, self).get_context(request)
        context.update(get_base_context())
        return context

    text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('text', classname="full"),
        InlinePanel('marque_blocks', label="Marque sections"),
    ]


class MarqueBlock(Orderable):
    page = ParentalKey(
        MarquePage,
        on_delete=models.CASCADE,
        related_name='marque_blocks'
    )

    description = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('description', classname="full"),
    ]


class MentionLegalPage(Page):
    def get_context(self, request):
        context = super(MentionLegalPage, self).get_context(request)
        context.update(get_base_context())
        return context

    text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('text', classname="full"),
    ]


class TexteEtImagesPage(Page):
    def get_context(self, request):
        context = super(TexteEtImagesPage, self).get_context(request)
        context.update(get_base_context())
        return context

    content_panels = Page.content_panels + [
        InlinePanel('texte_ou_images', label="Texte ou image"),
    ]


class TexteOuImage(Orderable):
    page = ParentalKey(
        TexteEtImagesPage,
        on_delete=models.CASCADE,
        related_name='texte_ou_images'
    )

    text = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True,
    )

    panels = [
        FieldPanel('text'),
        ImageChooserPanel('image'),
    ]
