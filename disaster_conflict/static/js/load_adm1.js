fetch("/api/geojson/adm1")
  .then(r => r.json())
  .then(geojson => {
      adm1Layer = L.geoJSON(geojson, {
          style: {
              color: "#555",
              weight: 1,
              fillOpacity: 0.7
          },
          onEachFeature: (feature, layer) => {
              layer.bindTooltip(feature.properties.shapename2);
          }
      }).addTo(map);

      updateYear(2022);
  });
