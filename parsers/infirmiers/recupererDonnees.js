var nodeio = require('node.io'), options = {timeout: 10};

exports.job = new nodeio.Job(options, {
    input: ['martin'],
    run: function (keyword) {
        this.getHtml('http://www.ordre-infirmiers.fr/transparence-des-avantages-des-infirmiers.html?secfie=' + encodeURIComponent(keyword), function (err, $) {
            //var results = $('#nom').attr().toLowerCase();

            var output = new Array();

            var results = $('html').rawfulltext;
            this.emit("res :" + results);

            $('div#content td').each(function(td) {
                output.push(td.text); 
            });




            output.push("dede");
            this.emit(output);
            this.emit(keyword + ' has ' + results);
        });
    }
});