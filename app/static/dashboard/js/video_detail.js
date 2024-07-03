let videoDetailUrlBase = 'http://localhost:8001/dashboard/manage/video_detail/'

let videoDetailOps = {
    init: function (){
        this.eventBind()
    },
    eventBind: function (){
        $('.submit').click(function (){
            videoUrl = $('#video-url').val()
            videoId = $('.video-id').text()
            $.ajax({
                url: videoDetailUrlBase + videoId,
                type: 'POST',
                data: {
                    'video_url': videoUrl,
                    'video_id': videoId,
                },
                dataType: 'json',
                success: function (res){
                    if(res.code === 200){
                        window.location.href = videoDetailUrlBase + videoId
                    }else{
                        window.location.href = videoDetailUrlBase + videoId + '?error=' + res.msg
                    }
                }
            })
        })



    }
}


$(document).ready(function(){
    videoDetailOps.init()
})