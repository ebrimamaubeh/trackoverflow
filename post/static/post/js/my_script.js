function hide_post_comment_form(){
    comment_div = document.getElementById('post_comment_div')
    
    if(comment_div.style.display === 'none'){
        comment_div.style.display = 'block';
    }else{
        comment_div.style.display = 'none';
    }
}

(function(){
    form_div = document.getElementById('post_comment_div')
    form_div.style.display = 'none'
})();