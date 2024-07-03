let addVideoAreaShow = false

let ops = {
    init: function (){
        this.eventBind()
    },
    eventBind: function () {
        $('.video_container .add_video').click(function (){
            let video_main = $('.video_container .video_edit_main')
            if(addVideoAreaShow){
                video_main.hide()
                addVideoAreaShow = false
            }else{
                video_main.show()
                addVideoAreaShow = true
            }
        }),
        $('.video_container .video_edit_main .submit').click(function (){
            let name = $('#videoNameInput').val()
            let info = $('#videoInfoInput').val()
            let image = $('#videoImageInput').val()
            let videoType = $('#video_type').val()
            let from = $('#video_from').val()
            let nationality = $('#nationality_type').val()
            console.log(name, info, image, videoType, from, nationality)

            $.ajax({
                url: 'http://localhost:8001/dashboard/manage/video_external',
                type: 'POST',
                data: {
                    name: name,
                    info: info,
                    image: image,
                    videoType: videoType,
                    from: from,
                    nationality: nationality
                },
                dataType: 'json',
                success: function (res){
                    console.log(res.redirectUrl)
                    window.location.href = res.redirectUrl
                }
            })
        })
    }
}


$(document).ready(function(){
    ops.init()
})

/**
 * 扫黑风暴
 * 该剧描绘了中央第三十六督导组在组长骆山河的带领下来到被黑恶势力盘踞多年的绿藤市，开展扫黑除恶专项斗争。
 * https://puui.qpic.cn/vcover_vt_pic/0/mzc00200lxzhhqz1628216915340/260
 * 警匪打黑
 * 腾讯视频
 * 内地
 */