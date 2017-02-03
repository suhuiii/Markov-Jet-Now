function getVars(vars){
	return vars
}

function updateDisplay(text){
	var words = text.split(/\s/);
	var i = 1;
	var string = "";

	for(j in words){
		if((string.length + words[j].length) > 25){
			$('#display_'+ i).val(string).change();
			i++;
			string = ""
		}
			string += words[j];
			string += " ";
	}
	$('#display_'+ i).val(string).change();
}

$( document ).ready(function() {
	var $banner_display = $('.banner_display');
	
	$banner_display.flapper({
		width: 25,
		chars_preset:'alpha',
		align: 'left',
		on_anim_start: onAnimStart,
		on_anim_end: onAnimEnd
	})

	// $('#display_top').val('G-ERTI by').change();
	// $('#display_bottom').val(vars).change();

	updateDisplay(vars);
	$('#more').click(function(){
		$.ajax({
			type: "GET",
			url: '/more',
			dataType:'JSON',
			success: function(response){
				$("#text").html(response.text)
				$('#display_top').val('').change();
				$('#display_top').val('G-ERTI by').change();
				$('#display_bottom').val(response.name).change();
			}
		});
	})

	$('#save').click(function(){
		var current_text = {
			text: $("#text").text(),
			name: $('#display_bottom').val()
		}

		$.ajax({
			type: "POST",
			url: '/save',
			dataType:'JSON',
			contentType: "application/json",
			data: JSON.stringify(current_text,null, '\t'),
			success: function(data){console.log(data);}
		});
	})

});
var onAnimStart = function(e) {
	$('.activity').addClass('active');
};

var onAnimEnd = function(e) {
	$('.activity').removeClass('active');
};	


