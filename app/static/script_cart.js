$(document).ready(function(){
            var lst = [];
            var her = localStorage.getItem ("lst");
            if (localStorage.getItem ("lst") != null){
                jsonstr = localStorage.getItem ("lst");
                lst = JSON.parse(jsonstr);
            }
            $(".count").html("Блюд: " + lst.length);

            $(".cart-cnt--down").click(function(){
                var product_id= $(this).closest('tr')[0].dataset.id;
                var url = "/cart";
                if (localStorage.getItem ("lst") != null){
                jsonstr = localStorage.getItem ("lst");
                lst = JSON.parse(jsonstr);
                }
                for (var i in lst) {
                            if (lst[i].dish == product_id) {
                                lst[i].quantity = lst[i].quantity-1;
                                if(lst[i].quantity==0) lst.splice(i,1);
                                break;
                            }
                        }
                var json2 =JSON.stringify(lst);
                localStorage.setItem("lst", json2);
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

            $(".cart-cnt--up").click(function(){
                var product_id= $(this).closest('tr')[0].dataset.id;
                $(document.getElementsByClassName("cart-cnt--down")).closest("tr")[0].dataset.id
                var url = "/cart";
                if (localStorage.getItem ("lst") != null){
                jsonstr = localStorage.getItem ("lst");
                lst = JSON.parse(jsonstr);
                }
                for (var i in lst) {
                            if (lst[i].dish == product_id) {
                                lst[i].quantity = lst[i].quantity+1;
                                break;
                            }
                        }
                var json2 =JSON.stringify(lst);
                localStorage.setItem("lst", json2);
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