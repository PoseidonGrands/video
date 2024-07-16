;

baseUrl = 'http://localhost:8001/'
loginUrl = 'http://localhost:8001/client/login'
let regOpt = {
    init: function (){
        this.eventBind()
    },

    eventBind: function (){
        $('.reg_wrap .do-reg').click(function() {
            let username = $('#login_user').val()
            let login_pwd = $('#login_pwd').val()
            let login_pwd_repeat = $('#login_pwd_repeat').val()
            let token = $('#django-csrf-token').val()
            let redirectUrl = $('#current-url').val()

            if(login_pwd !== login_pwd_repeat){
                alert('两次输入的密码不一致，请重新输入')
            }

            $.ajax({
                url: baseUrl + 'client/reg',
                type: 'post',
                data: {
                    username: username,
                    password: login_pwd,
                    csrfmiddlewaretoken: token
                },
                dataType: 'json',
                success: function(res){
                    if(res.code == 200){
                        console.log('注册成功', res)
                    //     跳转到登录页面
                         window.location.href = loginUrl
                    }else{
                        window.location.href = redirectUrl + res.error
                    }
                }
            })
        })
    }
}


$(document).ready(function(){
    regOpt.init()
})