//
// Routines for sunshine landing page
//
(function (sunshine) {

    sunshine.charts = {};
    sunshine.data = {};

    sunshine.settings = {
        montantAvantages: 'MONTANT AVANTAGES',
        nbAvantages: 'NB AVANTAGES',
        nbConventions: 'NB CONVENTIONS',
        nbAvantagesConventions: 'NB TOTAL CONVENTIONS + AVANTAGES'
    };

    sunshine.makeDoughnut = function (id, data) {
        console.log("Draw chart with data :", data);
        var ctx = document.getElementById(id).getContext("2d");
        var chart = new Chart(ctx).Doughnut(data);
        var legend = $("#" + id + "-legend").append(chart.generateLegend());
        sunshine.charts.labos = chart;
        return chart;
    };

    sunshine.makeTop = function(id, data) {
        console.log("Make top", id);
        return $('#' + id + "-top").bootstrapTable({
            data: data
        });
    };

    sunshine.doughnut = function(id, data, value) {
        var self = {
            id: id,
            data: data
        };
    };

    // Load data files
    sunshine.load = function (name) {
        return $.get("data/" + name).then(function (data) {
            var parsed = Papa.parse(data, {header: true});
            console.log("Csv parsed", parsed);
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
                .map(function (groupedDate, group) {
                    var results = _.reduce(groupedDate, sumRows);
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
    // Color scales
    //
    //
    sunshine.scale = {};
    sunshine.scale.LABO = function(name) {
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
            "PIERRE FABRE MEDICAMENT": "#bcbd22",
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

    sunshine.utils.formatNumber = function(number) {
        return (+(+number).toFixed(0)).toLocaleString();
    };

    sunshine.utils.formatMoney = function(number) {
        return sunshine.utils.formatNumber(number) + " €";
    };

    //
    //
    // Tests
    //
    //
    sunshine.draw = function () {
        console.log("Test doughnut chart");
        sunshine.load("labos.departements.csv").done(function (response) {
            var stats = sunshine.stats(response.data, ['LABO']);
            var totalMontantAvantages = new countUp("montant-avantages", 0, stats.TOTAL[sunshine.settings.montantAvantages]);
            totalMontantAvantages.start();
            var nbAvantages = new countUp("nb-avantages", 0, stats.TOTAL[sunshine.settings.nbAvantages]);
            nbAvantages.start();
            var nbConventions = new countUp("nb-conventions", 0, stats.TOTAL[sunshine.settings.nbConventions]);
            nbConventions.start();
            var chartData = _(stats.LABO)
                .slice(0, 15)
                .map(function (labo) {
                    return {
                        value: labo[sunshine.settings.montantAvantages],
                        color: sunshine.scale.LABO(labo.LABO),
                        label: labo.LABO
                    };
                })
                .value();
            var chart = sunshine.makeDoughnut("labos", chartData);
            var table = sunshine.makeTop("labos", stats.LABO);
        });

    };

    $(document).ready(sunshine.draw);

})(window.sunshine = window.sunshine || {});
