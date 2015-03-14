//
// Routines for sunshine landing page
//
(function(sunshine) {

    sunshine.charts = {};
    sunshine.data = {};

    // Load data files
    sunshine.load = function(url) {
        Papa.parse(url, {
            download: true,
            complete: function(results) {
                console.log("Csv " + url + " loaded : ", results);
            }
        })
    };

    sunshine.makeDoughnut = function(id, data) {
        var ctx = document.getElementById(id).getContext("2d");
        sunshine.charts.labos = new Chart(ctx).Doughnut(data);
    };


    // Load csv and make a chart
    sunshine.test = function() {
        console.log("Test loading of csv");
        sunshine.load("/data/labos.departements.csv");
        console.log("Test doughnut chart");
        var data = [
            {
                value: 300,
                color:"#F7464A",
                highlight: "#FF5A5E",
                label: "Red"
            },
            {
                value: 50,
                color: "#46BFBD",
                highlight: "#5AD3D1",
                label: "Green"
            },
            {
                value: 100,
                color: "#FDB45C",
                highlight: "#FFC870",
                label: "Yellow"
            }
        ];
        sunshine.makeDoughnut("labos", data);
    };

    $(document).ready(sunshine.test);

})(window.sunshine = window.sunshine || {});