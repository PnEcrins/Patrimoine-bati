function onEachFeature(feature, layer) {
    layer.bindPopup(feature.properties.name);
    layer.on("click", function(ev) {
        layer.openPopup();
    })
}

$(window).on('entity:map', function (e, data) {
    var map = data.map;

    var layerType = JSON.parse($('#areas_type').text());
    layerType.forEach(element => {
        var layer = new L.ObjectsLayer(null, {
            indexing: false,
            modelname: element.name,
            // style: style,
            onEachFeature: onEachFeature
        });
        
        map.layerscontrol.addOverlay(layer, element.name, tr("Zonages"));
    });


    map.on('layeradd', function (e) {
        var options = e.layer.options || { 'modelname': 'None' };
        for (var i = 0; i < layerType.length; i++) {
            if (!layerType[i].isActive) {
                if (options.modelname == layerType[i].name) {
                    console.log('YES LOAD');
                    
                    e.layer.load(layerType[i].url);
                    layerType[i].isActive = true;
                }
            }
        }
    });


        

});