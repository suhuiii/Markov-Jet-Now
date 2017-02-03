function getVars(vars){
	return vars
}

function getImage(name){
	switch(name){
		case "Arthur": return "http://1.bp.blogspot.com/-Tndp7u3unlc/UKPURHrkKiI/AAAAAAAAA0Q/gIXlwcgwMOw/s1600/217.jpg";
		case "Martin": return "http://www.cabinpressurefans.co.uk/wp-content/uploads/2011/08/martin_crieff1.jpg";
		case "Douglas": return "http://www.cabinpressurefans.co.uk/wp-content/uploads/2011/08/douglas_richardson1.jpg";
		case "Carolyn": return "http://www.cabinpressurefans.co.uk/wp-content/uploads/2011/08/carolyn_knapp_shappey1.jpg";
		case "Herc": return "https://www.comedy.co.uk/images/library/people/180x200/a/anthony_head_2.jpg";
		case "Mr. Birling": return "https://cdn0.iconfinder.com/data/icons/sports-android-l-lollipop-icon-pack/24/rugby-128.png";
	}
}

$(document).ready(function() {
	$('img.rounded-circle').attr('src', getImage(vars));
	var $banner_display = $('.banner_display');
	
	$banner_display.flapper({
		width: 11,
		chars_preset:'alpha',
		align: 'left',
		on_anim_start: onAnimStart,
		on_anim_end: onAnimEnd
	})

	$('#display_top').val('  MJN Air').change();
	

	$('#more').click(function(){
		$('#display_top').val(' ').change();
		$.ajax({
			type: "GET",
			url: '/more',
			dataType:'JSON',
			success: function(response){
				$('img.rounded-circle').attr('src', getImage(response.name));
				$("#text").html(response.text);
				$('#name').html(response.name);
				$('#display_top').val('  MJN Air').change();
				history.pushState({more:"more"},"","/");
			}
		});
	})

	$('#save').click(function(){
		var current_text = {
			text: $("#text").text(),
			name: $('#name').html()
		}

		$.ajax({
			type: "POST",
			url: '/save',
			dataType:'JSON',
			contentType: "application/json",
			data: JSON.stringify(current_text, null, '\t'),
			success: function(data){
				$('#dialog_url').val(data['url']);
				$('#modal_url').modal()}
			});
	})

	$('#copy').click(function(){
		document.querySelector('#dialog_url').select();
		document.execCommand('copy');
	})
});
var onAnimStart = function(e) {
	$('.activity').addClass('active');
};

var onAnimEnd = function(e) {
	$('.activity').removeClass('active');
};	


