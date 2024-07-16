;

baseUrl = 'http://localhost:8001/'
let loginOpt = {
    init: function (){
        this.eventBind()
    },

    eventBind: function (){
        $('.login_wrap .do-login').click(function() {
            let username = $('#login_user').val()
            let login_pwd = $('#login_pwd').val()
            let token = $('#django-csrf-token').val()
            let redirectUrl = $('#current-url').val()

            console.log('login:', username)

            $.ajax({
                url: baseUrl + 'client/login',
                type: 'post',
                data: {
                    username: username,
                    password: login_pwd,
                    csrfmiddlewaretoken: token
                },
                dataType: 'json',
                success: function(res){
                    if(res.code == 200){
                        console.log('登录成功', res)
                    //     跳转到我的页面
                         window.location.href = baseUrl + 'client/mine'
                    }else{
                        window.location.href = redirectUrl + res.error
                    }
                }
            })
        })
    }
}


$(document).ready(function(){
    loginOpt.init()
})