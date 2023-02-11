function signup(){
    $.ajax({
        type: "POST",
        url: "/signup/new",
        data: {
            id_give : $('#r-id').val(),
            nickname_give :$('#r-nick').val(),
            pw_give :$('#r-pw').val(),
            pw_pw_give :$('#r-pw2').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                // 메인페이지로 이동URL 기입
                window.location.href = '/'
            } else {
                alert(response['msg'])
            }
        }
    })
}

function check(){
    $.ajax({
        type: "POST",
        url: "/signup/check",
        data: {
            id_give : $('#r-id').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('사용 가능한 아이디 입니다!')
            } else {
                alert(response['msg'])
            }
        }
    })
}

