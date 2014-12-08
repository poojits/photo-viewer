$(document).ready(function() {
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
    $.getJSON( "/cluster" , {directory: "root"}, function( json ) {
        var items = "";
        for(var i=0;i<json.directories.length;i++){
            console.log(json.directories[i]);
            var splitO = json.directories[i].rep.split('/');
            var img_name = splitO[splitO.length-1];
            var img_desc = '<h3>'+img_name+'</h3>';
            var dir_name = json.directories[i].name;
            var img_src =  dir_name+'/'+ json.directories[i].rep;
            var html = '<li><div data-alt="'
                    + img_name+'" data-description="'
                    + img_desc+'" data-max-width="1800" data-max-height="1350"><div data-src="'
                    + img_src+'" data-min-width="200"></div></div></li>';
            items = items.concat(html);
        }
        console.log(items);
        //'<li><div data-alt="img03" data-description="<h3>Sky high<\\/h3>" data-max-width="1800" data-max-height="1350"><div data-src="images/medium/3.jpg" data-min-width="200"><\/div><\/div><\/li>'];
        Gamma.add( $( items));
  });
});