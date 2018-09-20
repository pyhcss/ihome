function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errcode) {
            location.href = "/";
        }
    })
}

$(function(){
    $.get("/api/myinfo", function(data) {
        if ("4101" == data.errcode) {
            location.href = "/login.html";
        }
        else if ("0" == data.errcode) {
            $("#user-name").html(data.data.name);
            $("#user-mobile").html(data.data.mobile);
            $("#user-email").html(data.data.email);
            if (data.data.avatar) {
                $("#user-avatar").attr("src", data.data.avatar);
            }
        }
    }, "json");
});