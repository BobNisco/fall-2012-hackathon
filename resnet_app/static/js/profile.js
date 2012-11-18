$(document).ready(function() {
	
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCookie('csrftoken')

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	function sameOrigin(url) {
		// test that a given url is a same-origin URL
		// url could be relative or scheme relative or absolute
		var host = document.location.host; // host + port
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;
		// Allow absolute or scheme relative URLs to same origin
		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
			(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
			// or any other URL that isn't scheme relative or absolute i.e relative.
			!(/^(\/\/|http:|https:).*/.test(url));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
				// Send the token to same-origin, relative URLs only.
				// Send the token only if the method warrants CSRF protection
				// Using the CSRFToken value acquired earlier
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

	$('.device_reports_link').on('click', function(e) {
		e.preventDefault();
		var el = $(this),
			parent = el.parents('tr'),
			id = parent.data('id'),
			this_modal = $('#device_modal_' + id);
		if (this_modal.length) {
			this_modal.modal();
		} else {
			$.post('/devices/find/', {'id' : id, 'csrftoken' : csrftoken}, function(response) {
				if (response != 'error') {
					$('#content').append(response);
					$('#device_modal_' + id).modal();
				}
			});
		}
	});

	var view_report = $('.view_report'),
		isReport = (view_report.length) ? true : false;

	if (isReport) {
		setInterval( function() {
			$.post('/reports/' + view_report.data('id'), {'csrftoken' : csrftoken}, function(response) {
				$('#content').replaceWith($(response).find('#content'));
			});
		}, 10000 );
	}
}); 
