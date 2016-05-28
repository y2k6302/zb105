// JavaScript Document

/* 視窗滑動 */
$(function(){
					
		$("#Top").click(function(){

		$("html,body").animate({scrollTop:0},500);

						//$("html,body").animate({scrollTop:0},900,"easeOutBounce");

		return false;

		});

});
				
$(function(){
					
		$("#One").click(function(){

		$("html,body").animate({scrollTop:850},500);

						//$("html,body").animate({scrollTop:0},900,"easeOutBounce");

		return false;

		});

});
				
				
$(function(){
					
		$("#Two").click(function(){

		$("html,body").animate({scrollTop:1650},500);

						//$("html,body").animate({scrollTop:0},900,"easeOutBounce");

		return false;

		});

});

$(function(){
					
		$("#Third").click(function(){

		$("html,body").animate({scrollTop:2400},500);

						//$("html,body").animate({scrollTop:0},900,"easeOutBounce");

		return false;

		});

});

$(function(){
					
		$("#Forth").click(function(){

		$("html,body").animate({scrollTop:1400},500);

						//$("html,body").animate({scrollTop:0},900,"easeOutBounce");

		return false;

		});

});

/* 按鈕特效 */
$(function(){
						//當滑鼠滑入時將div的class換成divOver
		$('.guideconnect').hover(function(){
		$(this).addClass('guideover');		
			},function(){
								//滑開時移除divOver樣式
								$(this).removeClass('guideover');	
			}
		);
});				 


/* 圖片輪播 */
jQuery(document).ready(function($) {   
$('#slider').cycle({   
		fx:    'fade',  //特效           speed:  7500,
		timeout:  2000,
		random:  1
		});
});

