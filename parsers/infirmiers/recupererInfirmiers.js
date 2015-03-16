fs = require('fs')
var xml2js = require('xml2js');
var SortedSet = require("collections/sorted-set");
// https://npmjs.org/package/collections

var filePath = 'data/infirmiers.raw';

function read(filePath)
{
	setNoms = new SortedSet();

	var parser = new xml2js.Parser();
	fs.readFile( filePath, function(err, data) {
	    parser.parseString(data, function (err, result) {
	        inscrits = result.map.inscrit;
	        inscrits.forEach( function(inscrit)
	        {
        		fullNameRaw = inscrit.Nom[0];
        		// Retirer les doubles espaces
        		fullNameRaw = fullNameRaw.replace( /  +/g, ' ' );

        		var fullNameArray = fullNameRaw.split(" ");
        		rawCivilite = fullNameArray.pop();
        		var re = /(\w+)/i;
        		civiliteArray = rawCivilite.match(re);
        		if (civiliteArray) {
        			civilite = civiliteArray[0];
        			//console.log(civilite);
        		}
        		//console.log(fullNameRaw);
				//console.log(fullNameArray);
				while (fullNameArray.length > 0)
				{
					fullNameArray.pop();
					setNoms.add(fullNameArray.join(" "));
				}
        		//ville = inscrit.Ville[0];
        		//cp = inscrit.CP[0];
        	})

	        noms = setNoms.toArray();
	        for (nom in noms)
	        {
	        	console.log(noms[nom]);
	        }

	    });
	});	

}

read(filePath);