$(document).ready(function () {
  listing();
});

function listing() {
  $.ajax({
    type: "GET",
    url: "/write/get",
    data: {},
    success: function (response) {
      let rows = response["write_get"];
      for (let i = 0; i < rows.length; i++) {
        let title = rows[i]["title"];
        let image = rows[i]["image"];
        let comment = rows[i]["comment"];
        let star = rows[i]["star"];
        let num = rows[i]["num"];
        let url = rows[i]["url"];
        let star_image = "⭐".repeat(star);

        let temp_html = `
        <div class="col" id="detailBox">
          <div class="card h-100">
            <a href="/detail/${num}" >
                <img src="${image}" class="card-img-top" >
                <div class="card-body">
                  <h5 class="card-title">${title}</h5>
                  <p>${star_image}</p>
                  <p class="mycomment">${comment}</p>
                </div>
              </div>
            </a>
          </div>
        </div>
      `;

        $("#cards-box").append(temp_html);
      }
    },
  });
}
$("#detailbox").on("click", function ({ num }) {
  location.href = "/detail/" + num;
});

function posting() {
  let url_p = $("#url").val();
  let comment_p = $("#comment").val();
  let star_p = $("#star").val();

  $.ajax({
    type: "POST",
    url: "/write/post",
    data: { url_give: url_p, comment_give: comment_p, star_give: star_p },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}

function open_box() {
  $("#post-box").show();
}

function close_box() {
  $("#post-box").hide();
}

function sign_out() {
  alert("로그아웃!");
  window.location.href = "/";
}
