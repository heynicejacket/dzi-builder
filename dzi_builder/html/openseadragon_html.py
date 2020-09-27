def make_openseadragon_html(layer_list, dzi_location):
    viewer_id = 'layerToggleMap'

    toggle_button_layers = ''
    script_layers = ''
    script_toggle_layers = ''
    script_sources_layers = ''

    layers_len = len(layer_list) - 1
    layer_ct = 0

    for layer in layer_list:
        # generate toggle buttons html
        button_fmt = '            <a class="{0}Toggle">{0} </a>\n'.format(layer)
        toggle_button_layers += button_fmt

        # generate openseadragon map layer variables
        layer_fmt = '            var mapBase = \'dzi/{}.dzi\'\n'.format(layer)
        script_layers += layer_fmt

        # generate openseadragon tileSources
        suffix = ',' if layer_ct < layers_len else ''
        opacity = 1 if layer == 'base' else 0
        js_layers = """
                    {{
                        x: 0,
                        y: 0,
                        opacity: {0},
                        tileSource: {1}
                    }}{2}""".format(opacity, layer, suffix)

        script_sources_layers += js_layers
        layer_ct += 1

        # generate toggle buttons jquery functionality
        if layer != 'base':
            layer_fmt = """
                var {0}Opacity = 0;
                $('.{0}Toggle').on('click', function() {{
                    {0}Opacity = ({0}Opacity + 0.5) % 1;
                    {0}Fade(viewer.world.getItemAt(1), ({0}Opacity === 0.5 ? 0.5 : 0));
                }});
                var {0}Fade = function(image, opacity) {{
                    image.setOpacity({0}Opacity);
                    OpenSeadragon.requestAnimationFrame(frame);
                }};
                """.format(layer)

            script_toggle_layers += layer_fmt

    html_str = """
<html>
    <head>
        <link href='css/test.css' rel='stylesheet'/>
        <script src="openseadragon/openseadragon.min.js"></script>
        <script src="openseadragon/openseadragon-scalebar.js"></script>
        <script src="openseadragon/jquery.min.js"></script>
    </head>
    <body>
        <div id="mapToolbar">
{0}        </div>
        <script>
            // map layers
{1}
            // openseadragon viewer
            var viewer = OpenSeadragon({{
                id: '{2}',
                prefixUrl: '{3}',
                toolbar: 'mapToolbar',
                zoomInButton: 'zoom-in',
                zoomOutButton: 'zoom-out',
                homeButton: 'home',
                fullPageButton: 'full-page',
                tileSources: [{4}
                ]
            }});

            // jquery button functionality {5}
        </script>
    </body>
</html>""".format(
            toggle_button_layers,
            script_layers,
            viewer_id,
            dzi_location,
            script_sources_layers,
            script_toggle_layers
        )

    html = open('C:\\localtemp\\layers\\index.html', 'w')
    html.write(html_str)
    html.close()


def make_openseadragon_css():
    css_str = """
a {
    cursor: pointer;
}

#playermap {
    height: 90%;
}

#toolbarPlayerMap {
    text-align: center;
    height: 30px;
}"""

    css = open('C:\\localtemp\\layers\\index.css', 'w')
    css.write(css_str)
    css.close()
