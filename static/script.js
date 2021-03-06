function animateNumbers(elem, new_val) {
	$(elem).each(function (key, item) {
		$({
			val_i: parseInt($(item).text().split(' ').join(''))
		}).animate({
			val_i: parseInt(new_val)
		}, {
			duration: 500,
			easing: 'swing',
			step: function () {
				$(item).text(number_format(this.val_i, 0, '.', ' '));
			},
			complete: function () {
				$(item).text(number_format(new_val, 0, '.', ' '));
			}
		});
	});
}

function renderCount()
{
    var cnt=0;
    jsonstr = localStorage.getItem ("lst");
    lst = JSON.parse(jsonstr);
    for (var i in lst) {
        cnt += lst[i].quantity;
        }

    $(".count").html(cnt);
}

function PopUpShow(){
        $("#popup1").show();
    }
//Функция скрытия PopUp
function PopUpHide(){
        $("#popup1").hide();
    }

$(document).ready(function(){
            var lst = [];
            var her = localStorage.getItem ("lst");
            if (localStorage.getItem ("lst") != null){
                jsonstr = localStorage.getItem ("lst");
                lst = JSON.parse(jsonstr);
            }
            //$(".count").html("Блюд: " + lst.length);
            renderCount()

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
                var jsonstr = null;
                 if (localStorage.getItem ("lst") != null){
                    jsonstr = localStorage.getItem ("lst");
                 }
                if (jsonstr != null){
                     $.ajax(url, {
                       method: 'POST',
                       data: {dishlst:jsonstr},
                       success: function(response){
                            //document.write(response);
                            //location.reload();
                       },
                       error : function(exeption){
                            console.log(exeption);
                       }
                    });
                 }
                renderCount();
                var cart = $('.cart');
                var imgtodrag = $($(this).closest('.cont-item')[0].children[0]).eq(0);

    			if (imgtodrag) {
    				var imgclone = imgtodrag.clone()
    					.offset({
    						top: imgtodrag.offset().top,
    						left: imgtodrag.offset().left
    					})
    					.css({
    						'opacity': '0.5',
    						'position': 'absolute',
    						'width': imgtodrag.width(),
    						'height': imgtodrag.height(),
    						'z-index': '100'
    					})
    					.appendTo($('body'))
    					.animate({
    						'top': cart.offset().top + 10,
    						'left': cart.offset().left + 10,
    						'width': 75,
    						'height': 32
    					}, 500);

    				imgclone.animate({
    					'width': 0,
    					'height': 0
    				}, function () {
    					$(this).detach()
    				});
    			}
                return false;
            });

            $(".cart-cnt--down").click(function(){
                var item=$(this).closest('tr')[0];
                var product_id= item.dataset.id;
                var new_val=0;
                //var url = "/cart";
                var url = "/cart/add";
                if (localStorage.getItem ("lst") != null){
                jsonstr = localStorage.getItem ("lst");
                lst = JSON.parse(jsonstr);
                }
                for (var i in lst) {
                            if (lst[i].dish == product_id) {
                                lst[i].quantity = lst[i].quantity-1;
                                new_val=lst[i].quantity;
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
                       success: function(){
                           if(new_val==0){
                               item.parentNode.removeChild(item);
                           }
                           else
                           {
                               $(item).find('span')[0].textContent=new_val;
                           }
                            //document.write(response);
                            //location.reload();
                       },
                       error : function(exeption){
                            console.log(exeption);
                       }
                    });
                 }
                 renderCount();
                return false;
            })

            $(".cart-cnt--del").click(function(){
                var item=$(this).closest('tr')[0];
                var product_id= item.dataset.id;
                var url = "/cart/add";
                if (localStorage.getItem ("lst") != null){
                jsonstr = localStorage.getItem ("lst");
                lst = JSON.parse(jsonstr);
                }
                for (var i in lst) {
                            if (lst[i].dish == product_id) {
                                lst.splice(i,1);
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
                       success: function(){
                           item.parentNode.removeChild(item);
                            //document.write(response);
                            //location.reload();
                       },
                       error : function(exeption){
                            console.log(exeption);
                       }
                    });
                 }
                 renderCount();
                return false;
            })
            $(".cart-cnt--up").click(function(){
                var item=$(this).closest('tr')[0];
                var product_id= item.dataset.id;
                var new_val=0;
                //var url = "/cart";
                var url = "/cart/add";
                if (localStorage.getItem ("lst") != null){
                jsonstr = localStorage.getItem ("lst");
                lst = JSON.parse(jsonstr);
                }
                for (var i in lst) {
                            if (lst[i].dish == product_id) {
                                lst[i].quantity = lst[i].quantity+1;
                                new_val=lst[i].quantity;
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
                       success: function(){
                            $(item).find('span')[0].textContent=new_val;
                            //document.documentElement.innerHTML = response;
                            //document.write(response);
                            //location.reload();
                       },
                       error : function(exeption){
                            console.log(exeption);
                       }
                    });
                 }
                 renderCount();
                return false;
            })

            // $(".cart-search-ok").click(function(){
            //      var url = "/cart/search";
            //      var jsonstr = null;
            //      if (localStorage.getItem ("lst") != null){
            //         jsonstr = localStorage.getItem ("lst");
            //      }
            //      if (jsonstr != null){
            //          $.ajax(url, {
            //           method: 'POST',
            //           data: {dishlst:jsonstr},
            //           success: function(response){
            //                 document.write(response);

            //           },
            //           error : function(exeption){
            //                 console.log(exeption);
            //           }
            //         });
            //      }
            //     return false;
            // })
        });