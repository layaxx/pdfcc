function isInvalidColor(color) {
	color = color.toLowerCase();
	if (color.length !== 7) {
		console.log('Input has invalid length ' + color.length);
		return true;
	} else if (color.charAt(0) != '#') {
		console.log('Input does not start with #');
		return true;
	}
	for (let i = 1; i < 7; i++) {
		let code = color.charCodeAt(i);
		if (code < 48 || (code > 57 && code < 97) || code > 102) {
			console.log('Input is not a valid color, contains invalid character ' + color.charAt(i));
			return true;
		}
	}
	return false;
}

$('#analysis_result').hide();
$('#progress').hide();
let status = 'analyse';
// prevent reload
window.addEventListener('beforeunload', function(e) {
	// Cancel the event
	e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
	// Chrome requires returnValue to be set
	e.returnValue = '';
});
$('#button-submit').prop('disabled', false);
$('#button-submit').prop('value', 'Send PDF');
// form upload
$('#id_ajax_upload_form').submit(function(e) {
	e.preventDefault();
	$form = $(this);
	$('#progress').show();
	var formData = new FormData(this);
	if (status === 'analyse') {
		$('#progress').text('Uploading data to Server...');
		$('#progress').removeClass('alert-danger');
		$('#progress').addClass('alert-light');
		$.ajax({
			url: window.location.pathname,
			type: 'POST',
			data: formData,
			success: function(response) {
				$('.error').remove();
				console.log(response);
				if (response.error) {
					$('#progress').text('There was an error: ' + response.message);
					$('#progress').removeClass('alert-light');
					$('#progress').addClass('alert-danger');
					$.each(response.errors, function(name, error) {
						error = '<small class="text-muted error">' + error + '</small>';
						$form.find('[name=' + name + ']').after(error);
					});
				} else {
					for (entry in response.analysis_result) {
						let colorcode = response.analysis_result[entry][0];
						let pages = response.analysis_result[entry][1];
						let div_outer = document.createElement('div');
						div_outer.style = 'width: 180px;';
						let div_inner = document.createElement('div');
						div_inner.className = 'colorcode';
						div_inner.style = 'background-color: ' + colorcode;
						let text_colorcode = document.createElement('p');
						text_colorcode.innerText = colorcode;
						let left_side = document.createElement('div');
						left_side.className = 'left-side';
						left_side.style = 'display: none; background-color: ' + colorcode;
						left_side.id = colorcode.substring(1, 7) + '_l';
						let right_side = document.createElement('div');
						right_side.className = 'right-side';
						right_side.style = 'display: none;';
						right_side.id = colorcode.substring(1, 7) + '_r';
						div_inner.append(left_side);
						div_inner.append(right_side);
						div_inner.append(text_colorcode);
						div_outer.append(div_inner);
						let text_pages = document.createElement('p');
						text_pages.innerText = pages;
						text_pages.style = 'margin-left: 10px;';
						div_outer.append(text_pages);
						let label = document.createElement('label');
						label.for = colorcode;
						label.style = 'text-align: left';
						label.innerText = 'replace with:';
						let input = document.createElement('input');
						input.id = colorcode;
						input.name = colorcode;
						input.type = 'text';
						input.className = 'floating-input';
						input.placeholder = ' ';
						div_input = document.createElement('div');
						div_input.className = 'floating-label';
						span1 = document.createElement('span');
						span1.className = 'highlight';
						div_input.append(input, span1, label);
						div_outer.append(div_input);
						$('#analysis_result').append(div_outer);
					}
					$('#analysis_result').show();
					$('#id_pdf').hide();
					$('#progress-1').addClass('list-group-item-secondary');
					$('#progress-1').removeClass('list-group-item-primary');
					$('#progress-2').addClass('list-group-item-primary');
					status = 'process';
					$('#progress').text('Uploading sucessfull. Please specify colors to be substituted.');
					// verify inputs
					$('input').each(function(index) {
						$(this).on('focusout', function() {
							let alertIsActive = !($(this).parent().next()[0] === undefined);
							if ($(this)[0].value) {
								if (isInvalidColor($(this)[0].value)) {
									if (!alertIsActive) {
										error =
											'<div class="alert alert-danger form-error" role="alert">Invalid Input.</div>';
										$(this).parent().after(error);
										$('#button-submit').prop('disabled', true);
										$('#submit-status').text('There is at least one error on input fields.');
									}
								} else if (alertIsActive) {
									$(this).parent().next().remove();
									$('#button-submit').prop('disabled', false);
									$('#submit-status').text('');
									$(this.id + '_r').css('background-color', this.value);
									$(this.id + '_r').show();
									$(this.id + '_l').show();
								} else {
									$(this.id + '_r').css('background-color', this.value);
									$(this.id + '_r').show();
									$(this.id + '_l').show();
								}
							} else if (alertIsActive) {
								$(this).parent().next().remove();
								$('#button-submit').prop('disabled', false);
								$('#submit-status').text('');
								$(this.id + '_r').hide();
								$(this.id + '_l').hide();
							}
						});
					});
				}
			},
			cache: false,
			contentType: false,
			processData: false
		});
	} else {
		$('#progress').text('Uploading data to Server...');
		$('#progress').removeClass('alert-danger');
		$('#progress').addClass('alert-light');
		$.ajax({
			url: window.location.pathname,
			type: 'POST',
			data: formData,
			success: function(response) {
				$('.error').remove();
				console.log(response);
				if (response.error) {
					$('#progress').text('There was an error: ' + response.message);
					$('#progress').removeClass('alert-light');
					$('#progress').addClass('alert-danger');
					$([ document.documentElement, document.body ]).animate(
						{
							scrollTop: $('#progress').offset().top
						},
						200
					);
				} else {
					$('#progress-2').addClass('list-group-item-secondary');
					$('#progress-2').removeClass('list-group-item-primary');
					$('#progress-3').addClass('list-group-item-success');
					$('#progress').text('Successfully Substituted ' + response.noc + ' Colors in your PDF.');
					$('#row-result').show();
					$('#download-anchor').attr('href', 'data:application/pdf;base64,' + response.b64);
					$('#row-form').hide();
				}
			},
			cache: false,
			contentType: false,
			processData: false
		});
	}
});
// end
