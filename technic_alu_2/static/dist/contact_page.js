$(document).ready(function() {
    // Init Ractive
    let ractive_contact_form = Ractive({
        el: '#contact_form_container',
        template: '#contact_form',
        data: {
            form: {},
        },
        computed: {
          form_completed: function() {
            return validate_form(this.get('form'));
          }
      }
    });
    window.ractive_contact_form = ractive_contact_form;
    // Function to add more images into the gallery
    ractive_contact_form.on('send_message', () => {
      ractive_contact_form.set({
          'form_loading': true
      });
      let csrftoken = get_cookie('csrftoken');
      $.ajaxSetup({
          beforeSend: function(xhr) {
              xhr.setRequestHeader('X-CSRFToken', csrftoken);
          }
      });
      $.ajax({
          url: get_base_url() + '/api/send_message/',
          method: 'POST',
          data: JSON.stringify(ractive_contact_form.get('form')),
          dataType: 'json'
      }).done((response) => {
          if (response.data) {
              ractive_contact_form.set({
                  'form_sent': true
              });
              Materialize.toast('Le message a été envoyé', 4000);
          }
      }).fail((response) => {
          Materialize.toast(
              'Le message n\'a pas pu être envoyé, ' +
              's\'il vous plaît veuillez réessayer plus tard',
              4000
          );
          console.error(response);
      }).complete(() => {
          ractive_contact_form.set({
              'form_loading': false
          });
      });
    });

    ractive_contact_form.observe('form.phone_number', function (phone_number) {
      if (phone_number && !isNaN(phone_number) && phone_number.length === 10) {
        let phone_number_array = [];
        for (var i = 0; i < 10; i = i + 2) {
            phone_number_array.push(phone_number.substring(i, i + 2));
        }
        phone_number = phone_number_array.join(' ');
        ractive_contact_form.set('form.phone_number', phone_number);
      }
    });
});

function validate_form(form) {
    return (
      form &&
      form.name &&
      form.subject &&
      form.message &&
      form.phone_number &&
      form.email &&
      is_email(form.email) &&
      is_fr_phone_number(form.phone_number)
    );
}

function is_email(value) {
    if (value && typeof value === 'string') {
        return value.match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i);
    }
    return false;
}

function is_fr_phone_number(value) {
    if (value) {
      value = value.replace(new RegExp(' ', 'g'), '');
      if (!isNaN(value) && value.length === 10) {
          return true;
      }
    }
    return false;
}

function get_base_url() {
    let current_href = window.location.href;
    let current_path = window.location.pathname;
    return current_href.replace(current_path, '');
}

function get_cookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = $.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
