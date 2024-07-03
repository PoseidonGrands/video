let videoDetailUrlBase = 'http://localhost:8001/dashboard/manage/video_detail/'
let performerUrlBase = 'http://localhost:8001/dashboard/manage/video_detail_performer/'

let videoDetailOps = {
    init: function (){
        this.eventBind()
    },
    eventBind: function (){
        $('.submit-add-episode').click(function (){
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

        $('.submit-add-star').click(function (){
            videoId = $('.video-id').text()
            starName = $('#star-name').val()
            starIdentify = $('#star-identify').val()
            $.ajax({
                url: performerUrlBase + videoId,
                type: 'POST',
                data: {
                    'video_id': videoId,
                    'star_identify': starIdentify,
                    'star_name': starName
                },
                dataType: 'json',
                success: function (res){
                    if(res.code === 200){
                        window.location.href = videoDetailUrlBase + videoId
                    }else{
                        window.location.href = videoDetailUrlBase + videoId + res.error
                    }
                }
            })
        })

    }
}


$(document).ready(function(){
    videoDetailOps.init()
})