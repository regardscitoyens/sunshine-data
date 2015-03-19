(function (sunshine) {
    
    sunshine.colorCluster = {
        "0": "#999999",
        "1": "#FF00FF",
        "2": "#00FF00",
        "3": "#FFFF00",
        "4": "#0000FF",
        "5": "#FF0000"
    };

    sunshine.startSigma = function () {
      sunshine.sigma = new sigma({
        container: 'reseau',
        settings: {
          clone: false,
          immutable: false,
          nodesPowRatio: 0.5,
          edgesPowRatio: 1,
          zoomMin: 0.01,
          zoomMax: 4,
          singleHover: true,
        //  drawEdges: false,
          defaultLabelColor: '#333'
        }
      });
      sunshine.load("labos.nodes.clusters.csv").done(function(res){
        var graph = {nodes: [], edges: []},
            rand255 = function(){
              return (Math.random()*255).toFixed();
            };
        res.data.forEach(function(n){
          if (_.isEmpty(n.label)) return;
          var tmpcolor = sunshine.scale.LABO(n.label);
          graph.nodes.push({
            id: n.label,
            label: n.label,
            x: Math.random(),
            y: Math.random(),
            size: n.montants,
            color: sunshine.colorCluster[n.combo_cluster]
            //color: (tmpcolor == "#d9d9d9" ? sunshine"rgb("+rand255()+","+rand255()+","+rand255()+")" : tmpcolor)
          });
        });
        sunshine.load("labos.edges.csv").done(function(res){
          var nodeid = 0;
          res.data.forEach(function(e){
            if (_.isEmpty(e.node1) || _.isEmpty(e.node2)) return;
            graph.edges.push({
              id: nodeid++,
              source: e.node1,
              target: e.node2,
              weight: e.weight,
              color: "#d0d0d0"
            });
          });
          sunshine.sigma.graph.read(graph);
          sunshine.sigma.startForceAtlas2({
            edgeWeightInfluence: 0.1,
            slowDown: 6,
            startingIterations: 50,
            iterationsPerRender: 5,
            barnesHutOptimize: true
          });
        });
      });
    };

    $(document).ready(sunshine.startSigma);

})(window.sunshine = window.sunshine || {});
