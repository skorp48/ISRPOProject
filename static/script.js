
$(document).ready(function(){
            var lst = [];
            var her = localStorage.getItem ("lst");
            if (localStorage.getItem ("lst") != null){
                jsonstr = localStorage.getItem ("lst");
                lst = JSON.parse(jsonstr);
            }
            $(".count").html("Блюд: " + lst.length);
	        $(".cont-item-plate-ok").click(function(){
	            var product_id = this.dataset.id;
                lst.push({dish:product_id,quantity:1});
                var json2 =JSON.stringify(lst);
                localStorage.setItem("lst", json2);
                $(".count").html("Блюд: " + lst.length);
                return false;
            });

            $(".dish-list").click(function(){
                 var url = "/check_cart";
                 var jsonstr = null;
                 if (localStorage.getItem ("lst") != null){
                    jsonstr = localStorage.getItem ("lst");
                 }
                 if (jsonstr != null){
                     $.ajax(url, {
                       method: 'POST',
                       data: {dishlst:jsonstr},
                       success: function(response){
                            document.write(response);
                       },
                       error : function(exeption){
                            console.log(exeption);
                       }
                    });
                 }
                return false;
            })

        });