function likePost(postId){
    xhr = XMLHttpRequest()
    if(xhr.readyState == 4 && xhr.status == 200){
        //update the like count and change like button color
    }

    xhr.open("GET", "post/like/"+ postId, true)
    xhr.setRequestHeader("Content-Type", "application/x-www-urlencoded")
    xhr.send("post_id="+ postId)
}