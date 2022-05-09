function likePost(postId){
    xhr = XMLHttpRequest()
    if(xhr.readyState == 4 && xhr.status == 200){
        //update the like count and change like button color
    }

    xhr.open("GET", "post/like/"+ postId, true)
    xhr.setRequestHeader("Content-Type", "application/x-www-urlencoded")
    xhr.send("post_id="+ postId)
}

function validate_ask_form(){
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    if (!form.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()
      alert('validaty failed')
      return false;
    }

    form.classList.add('was-validated')

    return true;
}

//get question comment.
function js_get_comment(question_id, comment_id){
    var comment_textarea = document.getElementById('editQuestionCommentTextarea')

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
            comment_textarea.textContent = xhr.responseText
            set_comment_edit_form_attr(question_id, comment_id)
            return true;
        }
        else{
            //TODO: show a popup message with error.
        }
    }
    xhr.open('GET', '/question/comment/get/'+ comment_id)
    xhr.send()
    return false;
}

function set_comment_edit_form_attr(question_id, question_comment_id){
    var form = document.getElementById('editQuestionCommentForm')
    form.action = "/question/comment/edit/" +question_id +"/" + question_comment_id +"/"
}


