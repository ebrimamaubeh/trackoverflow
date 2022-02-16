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
