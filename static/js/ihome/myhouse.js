$(document).ready(function(){
    $.get("/api/auth", function(data){
        if ("4101" == data.errcode) {
            location.href = "/login.html";
        } else if ("4002" == data.errcode){
            $(".auth-warn").show();
            return;
        } else if ("0" == data.errcode) {
            if ("" == data.data.real_name || "" == data.data.id_card || null == data.data.real_name || null == data.data.id_card) {
                $(".auth-warn").show();
                return;
            }
            $.get("/api/myhouseinfo", function(result){
                $("#houses-list").html(template("houses-list-tmpl", {houses:result.houses}));
            });
        }
    });
});