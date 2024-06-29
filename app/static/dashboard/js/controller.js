let host = 'http://localhost:8001'

let dashboard_ops = {
    init: function (){
        this.eventBind()
        // 获取存储的navIndex
        active_index = localStorage.getItem('activeNavIndex');
        // 跳转到首页时该值为空
        if (localStorage.getItem('activeNavIndex') !== null) {
            $(".nav-left .list-group a").eq(active_index).addClass('active')
        }
    },
    eventBind: function (){
        // 点击左上角跳转回首页
        $(".page-dashboard .nav-top .navbar-brand").click(function (){
            localStorage.setItem('activeNavIndex', null);
            window.location.href = host + '/dashboard/index'
        })

        $(".nav-left .list-group a:eq(0)").click(function (){
            localStorage.setItem('activeNavIndex', 0);
            window.location.href = host + '/dashboard/manage/admin';
        })

        $(".nav-left .list-group a:eq(1)").click(function (){
            localStorage.setItem('activeNavIndex', 1);
            window.location.href = host + '/dashboard/manage/user';
        })

        $(".nav-left .list-group a:eq(2)").click(function (){
            localStorage.setItem('activeNavIndex', 2);
            window.location.href = host + '/dashboard/manage/video';
        })
    }

}



$(document).ready(function (){
    dashboard_ops.init()
})