let videoDetailUrlBase = 'http://localhost:8001/dashboard/manage/video_detail/'
let performerUrlBase = 'http://localhost:8001/dashboard/manage/video_detail_performer/'

let videoDetailOps = {
    init: function (){
        this.eventBind()
    },
    eventBind: function (){
        $('.submit-add-episode').click(function (){
            let videoId = $('.video-id').text()
            let videoUrl = $('#video-url').val()
            let videoNumber = $('#video-number').val()
            console.log('number:', videoNumber)
            $.ajax({
                url: videoDetailUrlBase + videoId,
                type: 'POST',
                data: {
                    'video_url': videoUrl,
                    'video_id': videoId,
                    'video_number': videoNumber,
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

        $('.submit-add-star').click(function (){
            let videoId = $('.video-id').text()
            let starName = $('#star-name').val()
            let starIdentify = $('#star-identify').val()
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