//form edit_post/postid

$( document ).ready(function() {
    $('.edit_button').click(function ()
{
    var tag = $($(this).parents(".post"));
    var div = tag.children(".comment_body");
    var id = tag.attr("id");
    var str = "/raw/"+id;
 
    $.get(str, function( data ) {
	var text = data;
	 $(div.get(0)).replaceWith('<div class="comment_body"><form method="post" action="edit/'+id+'"><input type="hidden" name="thread_id" value="1"><p><textarea rows="5" cols="45" name="new_content" id="textbox"></textarea></p><p><input id = "sub" type="submit" value="Submit"></p></form></div>');
    var TheTextBox = document.getElementById("textbox");
    TheTextBox.value = text;
    $('#sub').click(function (){
	 setTimeout(function() {document.location = document.URL; } , 500);
    });
    });
});
    
});
		    


