let videoDetailUrlBase = 'http://localhost:8001/dashboard/manage/video_detail/'
let performerUrlBase = 'http://localhost:8001/dashboard/manage/video_detail_performer/'
let episodeEditUrlBase = 'http://localhost:8001/dashboard/manage/video_detail_episode_edit/'

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

        $('.episode-edit').click(function (){
            // 每一行的编辑按钮点击后将这一行的数据添加到编辑区域中

            // 获取每一行绑定的数据
            let subId = $(this).attr('data-id')
            let number = $(this).attr('data-number')
            let url = $(this).attr('data-url')

            // 获取元素
            let videoSubId = $('#video-sub-id')
            let videoNumberEdit = $('#video-number-edit')
            let videoUrlEdit = $('#video-url-edit')

            // 将数据添加到编辑区中
            videoSubId.val(subId)
            videoNumberEdit.val(number)
            videoUrlEdit.val(url)

            // 显示编辑区
            $('.edit_episode').show()
        })

        $('.submit-edit-episode').click(function (){
            // 确认提交修改的集数信息
            //获取修改的集数信息
            let videoId = $('.video-id').text()
            let videoSubId = $('#video-sub-id').val()
            let videoUrlEdit = $('#video-url-edit').val()
            let videoNumberEdit = $('#video-number-edit').val()

            console.log(videoId, videoSubId)
            console.log(videoId, videoSubId, videoUrlEdit, videoNumberEdit)

            // 提交到后端修改数据
            $.ajax({
                url: episodeEditUrlBase,
                type: 'post',
                data: {
                    'video_id': videoId,
                    'sub_id': videoSubId,
                    'video_url_edit': videoUrlEdit,
                    'video_number_edit': videoNumberEdit,
                },
                dataType: 'json',
                success: function (res){
                    window.location.href = res.redirectUrl
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