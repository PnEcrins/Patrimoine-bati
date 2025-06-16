console.log("test")

function ChangeColors(e, data) {
    window.objectsLayer.options.style = setColor
    console.log(data)
}

function setColor(feature) {
    return {
        weight: 3,
        opacity: 2,
        color: feature.properties.color,
        stroke: feature.properties.color
    }
}

function InitReportStatusLegend(e, data) {
    if (data.modelname != 'bati')
        return;
    var map = data.map;

    var legend = L.control({ position: 'bottomleft' });
    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'legend-statuses');
        div.style.background = 'rgba(255, 255, 255, 0.9)';
        div.style.padding = '8px 12px';
        div.style.borderRadius = '6px';
        div.style.boxShadow = '0 2px 6px rgba(0,0,0,0.15)';
        div.style.minWidth = '120px';

        var header = ['<span style="text-align: center; display: block; font-weight: bold;">' + tr("Status") + '</span>'];
        var inner = [];

        // Green circle for "Validé"
        inner.push(
            '<span style="display: flex; align-items: center; margin-bottom: 4px;">' +
            '<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:#48EE15;margin-right:8px;border:1px solid #888;"></span>' +
            tr("Validé") +
            '</span>'
        );
        // Red circle for "Non validé"
        inner.push(
            '<span style="display: flex; align-items: center;">' +
            '<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:red;margin-right:8px;border:1px solid #888;"></span>' +
            tr("Non validé") +
            '</span>'
        );

        div.innerHTML = header + inner.join('');
        return div;
    };
    legend.addTo(map);

    $(".legend-statuses")[0].style.display = 'none'; // init as hidden, use selector in controls overlay to display

    var LegendLayer = L.Class.extend({
        onAdd: function (map) {
            $(".legend-statuses").toggle();
        },
        onRemove: function (map) {
            $(".legend-statuses").toggle();
        },
    });
    control = new LegendLayer()
    map.layerscontrol.addOverlay(control, tr("Legend"));
    map.addLayer(control); //init as visible
}

$(window).on('entity:map:list', ChangeColors)
$(window).on('entity:map:list', InitReportStatusLegend);