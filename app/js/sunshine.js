//
// Routines for sunshine landing page
//
(function (sunshine) {

    sunshine.sliceAndSumOthers = function(array, begin, end, labelid, labelmsg) {
	autre = {};
	autre[sunshine.settings.montantAvantages] = parseInt(array[end][sunshine.settings.montantAvantages]);
	autre[sunshine.settings.nbAvantages] = parseInt(array[end][sunshine.settings.nbAvantages]);
	autre[sunshine.settings.nbConventions] = parseInt(array[end][sunshine.settings.nbConventions]);
	autre[sunshine.settings.nbAvantagesConventions] = parseInt(array[end][sunshine.settings.nbAvantagesConventions]);
	console.log(autre);
	for (i = end + 1 ; i < array.length ; i++ ) {
	    autre[sunshine.settings.montantAvantages] += parseInt(array[i][sunshine.settings.montantAvantages]);
	    autre[sunshine.settings.nbAvantages] += parseInt(array[i][sunshine.settings.nbAvantages]);
	    autre[sunshine.settings.nbConventions] += parseInt(array[i][sunshine.settings.nbConventions]);
	    autre[sunshine.settings.nbAvantagesConventions] += parseInt(array[i][sunshine.settings.nbAvantagesConventions]);
	}
	autre[labelid] = labelmsg;
	array[end] = autre;
	return _(array).slice(begin, end + 1);
    };

    sunshine.charts = {};
    sunshine.data = {};

    sunshine.settings = {
        montantAvantages: 'MONTANT AVANTAGES',
        nbAvantages: 'NB AVANTAGES',
        nbConventions: 'NB CONVENTIONS',
        nbAvantagesConventions: 'NB TOTAL CONVENTIONS + AVANTAGES'
    };

    sunshine.makeDoughnut = function (id, data) {
        /*var ctx = document.getElementById(id).getContext("2d");
         var chart = new Chart(ctx).Doughnut(data);
         var legend = $("#" + id + "-legend").append(chart.generateLegend());
         sunshine.charts[id] = chart;
         return chart;*/

        //Donut chart example
        nv.addGraph(function () {
          var chart = nv.models.pieChart()
            .x(function (d) {
              return d.label
            })
            .y(function (d) {
              return d.value
            })
            .showLabels(true)     //Display pie labels
            .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
            .labelType("value") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
            .donut(true)          //Turn on Donut mode. Makes pie chart look tasty!
            .donutRatio(0.35)     //Configure how big you want the donut hole size to be.
          ;

          d3.select("#" + id + " svg")
            .datum(data)
            .transition().duration(350)
            .call(chart);

          nv.utils.windowResize(chart.update);

          return chart;
        });
    };

    sunshine.makeHistogram = function (id, data) {

        nv.addGraph(function() {
          var chart = nv.models.multiBarHorizontalChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .barColor(function(d) { return d.color })
            .margin({top: 5, right: 5, bottom: 15, left: 190})
            .tooltips(true)
            .showLegend(false)
            .showControls(false)
            .showValues(true)
            .valueFormat(sunshine.utils.formatShortMoney)
          ;

          chart.yAxis
            .tickFormat(sunshine.utils.formatShortMoney)
            .showMaxMin(false);

          d3.select('#' + id + " svg")
            .datum([{key: "Laboratoire", values: data}])
            .transition().duration(350)
            .call(chart);

          nv.utils.windowResize(chart.update);

          return chart;
        });
    };


    sunshine.makeTop = function (id, data) {
        return $('#' + id + "-top").bootstrapTable({
            data: data
        });
    };

    sunshine.doughnut = function (id, data, value) {
        var self = {
            id: id,
            data: data
        };
    };

    // Load data files
    sunshine.load = function (name) {
        return $.ajax("data/" + name, {contentType: "text/csv charset=utf-8"}).then(function (data) {
            var parsed = Papa.parse(data, {header: true});
            sunshine.data[name] = parsed;
            return parsed;
        });
    };

    sunshine.stats = function (data, dimensions) {
        data = _.chain(data);

        var self = {};

        function sumRows(left, right) {
            var total = {};
            _.forEach(sunshine.settings, function (value) {
                total[value] = sunshine.utils.safeFloat(left[value]) + sunshine.utils.safeFloat(right[value]);
            });
            return total;
        }

        _.forEach(dimensions, function (dimension) {
            self[dimension] = data
                .groupBy(dimension)
                .map(function (groupedData, group) {
                    var results = _.reduce(groupedData, sumRows);
                    results[dimension] = group;
                    return results;
                })
                .sortBy(sunshine.settings.montantAvantages)
                .reverse()
                .value();
        });

        self.TOTAL = _.reduce(self[dimensions[0]], sumRows);

        return self;
    };

    //
    //
    // Load data, draw charts, tables, etc.
    //
    //
    sunshine.drawGlobalAndLaboStats = function () {
        sunshine.load("labos.departements.csv").done(function (response) {
            var stats = sunshine.stats(response.data, ['LABO']);
            var totalMontantAvantages = new countUp("montant-avantages", 0, stats.TOTAL[sunshine.settings.montantAvantages]);
            totalMontantAvantages.start();
            var nbAvantages = new countUp("nb-avantages", 0, stats.TOTAL[sunshine.settings.nbAvantages]);
            nbAvantages.start();
            var nbConventions = new countUp("nb-conventions", 0, stats.TOTAL[sunshine.settings.nbConventions]);
            nbConventions.start();
            var chartData = sunshine.sliceAndSumOthers(stats.LABO, 0, 15, 'LABO', 'Autres labos')
                .map(function (labo) {
                    return {
                        value: labo[sunshine.settings.montantAvantages],
                        color: sunshine.scale.LABO(labo.LABO),
                        label: labo.LABO
                    };
                })
                .value();
            sunshine.makeHistogram("labos", chartData);
            sunshine.makeTop("labos", stats.LABO);
        });
        sunshine.load("metiers.departements.csv").done(function (response) {
            var stats = sunshine.stats(response.data, ['METIER']);
            document.stats = stats;
            var chartData = sunshine.sliceAndSumOthers(stats.METIER, 1, 10, 'METIER', 'Autres qualifications')
                .map(function (metier) {
                    return {
                        value: metier[sunshine.settings.montantAvantages],
                        color: sunshine.scale.METIER(metier.METIER),
                        label: metier.METIER
                    };
                })
                .value();
            var chart = sunshine.makeDoughnut("praticiens", chartData);
        });
        sunshine.load("beneficiaires.top.csv").done(function (response) {
            //var stats = sunshine.stats(response.data, ['BENEFICIAIRE']);
            var table = sunshine.makeTop("beneficiaires", response.data);
        });
    };

    //
    //
    // Color scales
    //
    //
    sunshine.scale = {};
    sunshine.scale.METIER = function (name) {
        var colors = {
            "Médecin": "#1f77b4",
            "Asso de prof. de santé": "#aec7e8",
            "Pharmacien": "#ff7f0e",
            "Infirmier": "#ffbb78",
            "Fondation": "#2ca02c",
            "Asso d'usager de santé": "#98df8a",
            "Chirurgien-dentiste": "#d62728",
            "Dentiste": "#d62728",
            "Interne": "#ff9896",
            "Etudiant": "#9467bd",
            "Préparateur en pharmacie": "#c5b0d5",
            "Autres types de personne morale": "#8c564b",
            "Manipulateur électroradio": "#c49c94",
            "Etablissement de santé": "#e377c2",
            "Opticien-lunetier": "#f7b6d2",
            "Audioprothésiste": "#7f7f7f",
            "Sage-femme": "#c7c7c7",
            "Prothésiste et orthésiste pour l’appareillage des personnes handicapées": "#bcbd22",
            "Masseur-kinésithérapeute": "#dbdb8d",
            "Diététicien": "#17becf",
            "Technicien de laboratoire médical": "#9edae5"
        };
        if (_.isUndefined(colors[name])) {
            return "#d9d9d9";
        } else {
            return colors[name];
        }
    };

    sunshine.scale.LABO = function (name) {
        var colors = {
            "NOVARTIS PHARMA": "#1f77b4",
            SERVIER: "#aec7e8",
            GLAXOSMITHKLINE: "#ff7f0e",
            MSD: "#ffbb78",
            "JANSSEN CILAG": "#2ca02c",
            ASTRAZENECA: "#98df8a",
            SANOFI: "#d62728",
            PFIZER: "#ff9896",
            "ASTELLAS PHARMA": "#9467bd",
            "BOEHRINGER INGELHEIM": "#c5b0d5",
            "DAIICHI SANKYO": "#8c564b",
            LUNDBECK: "#c49c94",
            ROCHE: "#e377c2",
            GUERBET: "#f7b6d2",
            BAYER: "#7f7f7f",
            MEDTRONIC: "#c7c7c7",
            "PIERRE FABRE": "#bcbd22",
            "BIOGEN IDEC": "#dbdb8d",
            "ST JUDE MEDICAL": "#17becf",
            "ALK-Abello": "#9edae5"
        };

        if (_.isUndefined(colors[name])) {
            return "#d9d9d9";
        } else {
            return colors[name];
        }
    };

    //
    //
    // Utils routines
    //
    //
    sunshine.utils = {};
    sunshine.utils.safeFloat = function (string) {
        if (_.isUndefined(string) || _.isEmpty(string + "")) {
            return 0;
        } else {
            return parseFloat(string);
        }
    };

    sunshine.utils.formatNumber = function (number) {
        return (+(+number).toFixed(0)).toLocaleString();
    };

    sunshine.utils.formatMoney = function (number) {
        return sunshine.utils.formatNumber(number) + " €";
    };
    sunshine.utils.formatShortMoney = function (number) {
        return (+(+number/1000000).toFixed(2)).toLocaleString() + " M€";
    };

    //
    //
    // Draw everything
    //
    //
    sunshine.draw = function () {
        sunshine.drawGlobalAndLaboStats();
    };

    $(document).ready(sunshine.draw);

})(window.sunshine = window.sunshine || {});
