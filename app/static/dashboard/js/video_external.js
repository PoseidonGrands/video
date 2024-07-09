let ops = {
    init: function (){
        this.eventBind()
    },
    eventBind: function () {
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