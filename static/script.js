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
                var url = "/cart/add";

                search = (key, inputArray) => {
                    for (let i=0; i < inputArray.length; i++) {
                        if (inputArray[i].dish === key) {
                          return inputArray[i];
                        }
                    }
                }

                let found = search(product_id, lst);
                if (found == undefined)
                {
                    lst.push({dish:product_id,quantity:1});
                }
                else
                    {
                        for (var i in lst) {
                            if (lst[i].dish == product_id) {
                                lst[i].quantity = lst[i].quantity+1;
                                break;
                            }
                        }
                    }
                var json2 =JSON.stringify(lst);
                localStorage.setItem("lst", json2);
                $(".count").html("Блюд: " + lst.length);
                return false;
            });

            $(".dish-list").click(function(){
                 var url = "/cart";
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