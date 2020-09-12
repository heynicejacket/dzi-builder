def js_create_artboards(app, path):
    js = """
        function createSheetsFromFile(layerPath) {{
            var exportFolderPath = layerPath;
            var layerCount = app.activeDocument.layers.length;
            var layerDict = {{}};
    
            for (var l = 0; l < layerCount; l++) {{
                layerDict[app.activeDocument.layers[l].name] = l;
            }}
    
            hideAllLayers(layerDict);
            for (var key in layerDict) {{
                app.activeDocument.layers.getByName(key).visible = true;
                exportArtboard(exportFolderPath, key);
                app.activeDocument.layers.getByName(key).visible = false;
            }}
        }}
    
        function exportArtboard(path, layerName) {{
            var dest = path + layerName;
            var aiDoc = new File(dest);
            var saveOptions = new IllustratorSaveOptions();
    
            saveOptions.saveMultipleArtboards = true;
            app.activeDocument.saveAs(aiDoc, saveOptions);
        }}
    
        function hideAllLayers(layerDict) {{
            for (var key in layerDict) {{
                app.activeDocument.layers.getByName(key).visible = false;
            }}
        }}
    
        createSheetsFromFile('{}')
    """.format(path)
    app.DoJavaScript(JavaScriptCode=js)


def js_convert_to_svg(app, path):
    js = """
        function exportToSVG(filePath) {{
            var exportOptions = new ExportOptionsSVG();
            exportOptions.embedRasterImages = true;
    
            var type = ExportType.SVG;
            var fileSpec = new File(filePath);
    
            app.activeDocument.exportFile(fileSpec, type, exportOptions);
        }}
    
        exportToSVG('{}')
    """.format(path)
    app.DoJavaScript(JavaScriptCode=js)
