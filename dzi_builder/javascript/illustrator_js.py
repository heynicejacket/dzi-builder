def js_create_artboards(app, path, transparent_png, width, height):
    js = """
        function createSheetsFromFile(layerPath, transparentOut, widthScale, heightScale) {{
            var exportFolderPath = layerPath;
            var layerCount = app.activeDocument.layers.length;
            var layerDict = {{}};
        
            for (var l = 0; l < layerCount; l++) {{
                layerDict[app.activeDocument.layers[l].name] = l;
            }}
        
            hideAllLayers(layerDict);
            for (var key in layerDict) {{
                app.activeDocument.layers.getByName(key).visible = true;
        
                if (transparentOut == 1) {{
                    saveTransparency(exportFolderPath, key, widthScale, heightScale)
                }} else {{
                    exportArtboard(exportFolderPath, key);
                }}
        
                app.activeDocument.layers.getByName(key).visible = false;
            }}
        }}
        
        function exportArtboard(path, layerName) {{
            var dest = path + layerName;
            var tile = new File(dest);
            var saveOptions = new IllustratorSaveOptions();
        
            saveOptions.saveMultipleArtboards = true;
            app.activeDocument.saveAs(tile, saveOptions);
        }}
        
        function hideAllLayers(layerDict) {{
            for (var key in layerDict) {{
                app.activeDocument.layers.getByName(key).visible = false;
            }}
        }}
        
        function saveTransparency(layerPath, layerName, widthScale, heightScale) {{
            var activeDocument = app.activeDocument;
            for (var a = 0; a < activeDocument.artboards.length; a++) {{
                var activeArtboard = activeDocument.artboards[a];
                activeDocument.artboards.setActiveArtboardIndex(a);
        
                // error-proofing against programs further in the pipeline that count 1, 10, 2, ...
                if (a < 10) {{
                    i = '00' + a.toString();
                }} else if (a >= 10 && a < 100) {{
                    i = '0' + a.toString();
                }} else {{
                    i = a.toString();
                }}
        
                var fileName = layerName + "-" + i;
                var destinationFile = File(layerPath + fileName);
        
                var type = ExportType.PNG24;
                var options = new ExportOptionsPNG24();
                options.horizontalScale = widthScale;
                options.verticalScale = heightScale;
                options.antiAliasing = true;
                options.artBoardClipping = true;
                options.transparency = true;
                activeDocument.exportFile(destinationFile, type, options);
            }}
        }}
        
        createSheetsFromFile('{}', {}, {}, {})
    """.format(path, transparent_png, height, width)
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
