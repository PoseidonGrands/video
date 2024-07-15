;

var account_login_ops = {
    init:function (){
        this.eventBind()
    },
    eventBind:function (){
        $(".login_wrap .do-login").click(function (){
            console.log('登录')
            let loginBtn = $(this);
            if(loginBtn.hasClass('disabled')){
                console.log('请不要重复点击！')
            }
            let loginName = $(".login_wrap input[id='login_user']").val();
            let loginPwd = $(".login_wrap input[id='login_pwd']").val();
            if(loginName.length < 3 || loginPwd.length < 3){
                console.log('无效字段值');
            }

            // 禁用点击，防止重复提交
            loginBtn.addClass('disabled');

            // 获取需要跳转的url
            let to_url = $('.to_url').text();

            $.ajax({
                url: 'http://localhost:8001/account/login',
                type: 'POST',
                data: {
                    loginName: loginName,
                    loginPwd: loginPwd,
                    toUrl: to_url
                },
                dataType: 'json',
                success: function (res){
                    console.log('登录成功')
                    //成功获得响应，按钮恢复点击
                    loginBtn.removeClass('disabled')
                    // 跳转页面
                    window.location.href = res.redirectUrl;
                }
            })

        })
    }
}

$(document).ready(function (){
    console.log('ready')
    account_login_ops.init()
})