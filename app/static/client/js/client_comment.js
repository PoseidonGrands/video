;

baseUrl = 'http://localhost:8001/'
let commentOps = {
    init: function(){
        this.eventBind()
    },
    eventBind: function(){
        $('.comment-area .comment-submit').click(function() {
            let comment = $('.comment-area .comment-content').val()
            let videoId = $('#video-id').val()
            let userId = $('#user-id').val()
            let token = $('#token').val()

            if(!comment){
                alert('评论不能为空')
                return
            }

            console.log(comment, videoId, token)
            $.ajax({
                url: baseUrl + 'client/comment_commit',
                type: 'post',
                data: {
                    comment: comment,
                    video_id: videoId,
                    user_id: userId,
                    csrfmiddlewaretoken: token
                },
                dataType: 'json',
                success: (res)=> {
                    console.log('res', res)
                    updateCommentList(res)
                }
            })
        })
    },
}
function updateCommentList(res){
    console.log('uodate...')
    let commentList = $('.comment-container .comment-list')
    let newEle = `
                        <p>${res.data.username}</p>
                        <p>${res.data.content}</p>`
    commentList.append(newEle)
    console.log(newEle)
}



$(document).ready(function(){
    commentOps.init()
})