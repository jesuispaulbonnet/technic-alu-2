const num_image_range = 12;

$(document).ready(function() {
    let lightbox_gallery;
    // Init Ractive
    let ractive_gallery = Ractive({
        el: '#gallery_container',
        template: '#gallery_images',
        data: {
            images: [],
            max_images: 0
        }
    });
    window.ractive_gallery = ractive_gallery;
    // Function to add more images into the gallery
    ractive_gallery.on('add_gallery_images', () => {
        ractive_gallery.set(
            'max_images',
            ractive_gallery.get('max_images') + num_image_range
        );
        if (lightbox_gallery) {
            lightbox_gallery.destroy();
        }
        lightbox_gallery = $('#gallery_container .gallery_links').simpleLightbox({
            'navText': [
                '<i class="fa fa-angle-left"></i>',
                '<i class="fa fa-angle-right"></i>',
            ]
        });
    });
    // Add images related to the page
    $.ajax({
        url: get_base_url() + '/api/gallery_images',
        method: 'GET',
        data: {page_id: $('#page_id').attr('value')},
        dataType: 'json'
    }).done((response) => {
        if (response.data) {
            ractive_gallery.set('images', response.data);
            ractive_gallery.fire('add_gallery_images');
        }
    });
});

function get_base_url() {
    let current_href = window.location.href;
    let current_path = window.location.pathname;
    return current_href.replace(current_path, '');
}
