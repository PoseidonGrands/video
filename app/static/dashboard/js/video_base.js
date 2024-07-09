let addVideoAreaShow = false

let baseOps = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $('.video_container .add_video').click(function () {
            let video_main = $('.video_container .video_edit_main')
            if (addVideoAreaShow) {
                video_main.hide()
                addVideoAreaShow = false
            } else {
                video_main.show()
                addVideoAreaShow = true
            }
        })
    }
}

$(document).ready(function(){
    baseOps.init()
})


