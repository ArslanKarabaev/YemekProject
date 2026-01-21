
<!-- /static/js/script.js -->
function vote(commentId, action) {
    fetch("/chernovik/vote/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: `comment_id=${commentId}&action=${action}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`like-${commentId}`).innerText = data.likes;
        document.getElementById(`dislike-${commentId}`).innerText = data.dislikes;
    })
    .catch(error => console.error("Ошибка:", error));
}

function getCSRFToken() {
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}
