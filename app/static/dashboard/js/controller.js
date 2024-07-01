let host = 'http://localhost:8001'

let dashboardOps = {
    init: function (){
        this.eventBind()
        // 获取存储的navIndex
        active_index = localStorage.getItem('activeNavIndex');
        // 跳转到首页时该值为空，不会设置active
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

        // 设置导航栏每个item的高亮状态
        $(".nav-left .list-group a:eq(0)").click(function (){
            localStorage.setItem('activeNavIndex', 0);
            window.location.href = host + '/dashboard/manage/admin';
        })

        $(".nav-left .list-group a:eq(1)").click(function (){
            localStorage.setItem('activeNavIndex', 1);
            window.location.href = host + '/dashboard/manage/user';
        })

        $(".nav-left .list-group .dropdown-menu a:eq(0)").click(function (){
            localStorage.setItem('activeNavIndex', 2);
            window.location.href = host + '/dashboard/manage/video_external';
        })

        $(".nav-left .list-group .dropdown-menu a:eq(1)").click(function (){
            localStorage.setItem('activeNavIndex', 3);
            window.location.href = host + '/dashboard/manage/video_custom';
        })
    }
}


$(document).ready(function (){
    dashboardOps.init()
})