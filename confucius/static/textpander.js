$(document).ready(function(){

	var $textpanderContent = $(".content");
	$(".content").hide();
	$(".headline").click(function(){
		$(this).next().find(".content").slideToggle();
		
		var down = "icon-chevron-down";
		var up = "icon-chevron-up";
		if ($(this).find("." + up).length){
			down = "icon-chevron-down";
			up = "icon-chevron-up";
		}
		else{
			up = "icon-chevron-down";
			down = "icon-chevron-up";
		}
		$(this).find("." + up).toggleClass(down);
		$(this).find("." + up).removeClass(up);
	})

});

