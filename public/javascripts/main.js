$(document).ready(function() {
    $('.button.back').on('click',function(){
        var urlparam = getParameterByName('directory');
    if(urlparam != '' && urlparam != 'images/cluster')
       window.history.back(); 
    });
    $('.button.next').on('click',function(){
       window.history.forward(); 
    });
    var GammaSettings = {
    // order is important!
        viewport : [ {
            width : 1200,
            columns : 5
        }, {
            width : 900,
            columns : 4
        }, {
            width : 500,
            columns : 3
        }, {
            width : 320,
            columns : 2
        }, {
            width : 0,
            columns : 2
        } ]
    };
    Gamma.init( GammaSettings, fncallback );
    var page = 0;
    function fncallback() {
        $( '#loadmore' ).show().on( 'click', function() {
            ++page;
            items = ['<li><div data-alt="img03" data-description="<h3>Sky high</h3>" data-max-width="1800" data-max-height="1350"><div data-src="images/xxxlarge/3.jpg" data-min-width="1300"></div><div data-src="images/xxlarge/3.jpg" data-min-width="1000"></div><div data-src="images/xlarge/3.jpg" data-min-width="700"></div><div data-src="images/large/3.jpg" data-min-width="300"></div><div data-src="images/medium/3.jpg" data-min-width="200"></div><div data-src="images/small/3.jpg" data-min-width="140"></div><div data-src="images/xsmall/3.jpg"></div><noscript><img src="images/xsmall/3.jpg" alt="img03"/></noscript></div></li>'];
            var newitems = items[0]

            Gamma.add( $( newitems ) );
        } );
    }
    if(getParameterByName('directory')!=''){
        $.getJSON( "/cluster", {directory: getParameterByName('directory')}, function( json ) {
            for(var i=0;i<json.directories.length;i++){
                //console.log(json.directories[i]);
                var splitO = json.directories[i].rep.split('/');
                var img_name = splitO[splitO.length-1];
                var img_desc = '<h3>'+img_name+'</h3>';
                var dir_name = json.directories[i].name;
                var img_src =  dir_name+'/'+ json.directories[i].rep;
                var html = '<li cluster="'
                        + dir_name+'"><div data-alt="'
                        + img_name+'" data-description="'
                        + img_desc+'" data-max-width="660" data-max-height="540"><div data-src="'
                        + img_src+'" data-min-width="200"></div></div></li>';
                Gamma.add($(html));
            }
            $(window).resize(); //triggers resize and redraws DOM
            if(json.files.length==0){
                $('ul.gamma-gallery').unbind();
                $('ul.gamma-gallery').on('click', sendNewPageRequest);
            }
            else { //leaf level
                for(var i=0;i<json.files.length;i++){
                    //console.log(json.directories[i]);
                    var splitO = json.files[i].split('/');
                    var img_name = splitO[splitO.length-1];
                    var img_desc = '<h3>'+img_name+'</h3>';
                    var img_src =  json.files[i];
                    var dir_name = '';
                    var html = '<li cluster="'
                            + dir_name+'"><div data-alt="'
                            + img_name+'" data-description="'
                            + img_desc+'" data-max-width="660" data-max-height="540"><div data-src="'
                            + img_src+'" data-min-width="200"></div></div></li>';
                    Gamma.add($(html));
                }
                $(window).resize(); //triggers resize and redraws DOM
            }
      });
    }
});
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
function sendNewPageRequest(event) {
    if(event.target.nodeName != 'UL'){
        var p = $(event.target).parent();
        while(p.attr('class')!= 'masonry-brick'){
            p = p.parent();
        }
    }
    var cluster = p.attr('cluster');
    window.location.href = "http://localhost:3000?directory="+cluster;
}