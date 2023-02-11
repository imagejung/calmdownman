$(document).ready(function () {});

function login() {
  $.ajax({
    type: "POST",
    url: "/login",
    data: {
      id_give: $("#login_id").val(),
      pw_give: $("#login_pw").val(),
    },
    success: function (response) {
      alert(response["msg"]);
      window.location.href = "/index";
    },
  });
}
function login() {
  $.ajax({
    type: "POST",
    url: "/login",
    data: {
      id_give: $("#login_id").val(),
      pw_give: $("#login_pw").val(),
    },

    success: function (response) {
      if (response["result"] == "로그인 성공!") {
        alert(response["result"]);
        window.location.href = "/index";
      } else {
        alert(response["result"]);
      }
    },
  });
}

function signup() {
  window.location.href = "/signup";
}
