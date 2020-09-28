from dzi_builder.core.toolkit import (
    create_file
)


def make_site(layer_path, layer_list):
    """

    :param layer_path:
    :param layer_list:
    :return:
    """
    html_path = layer_path + 'html\\'
    osd_path = html_path + 'openseadragon\\'

    readme = 'download the zip from https://openseadragon.github.io/#download, drop openseadragon files here.\n\n' \
             'download the zip from https://jquery.com/download/, drop jquery file here; you will likely need\n' \
             'to modify the html file to point to the correct jquery-#.#.#.min.js (line 5 in viewer.html).'
    create_file(osd_path, 'README.txt', readme)

    make_openseadragon_html(html_path, layer_list)
    make_openseadragon_css(html_path)


def make_openseadragon_html(html_path, layer_list, viewer_id='layerMap', opacity_toggle_div='toggleButtons'):
    """

    :param html_path:
    :param layer_list:
    :param viewer_id:
    :param opacity_toggle_div:
    :return:
    """
    toggle_button_layers = ''
    script_layers = ''
    script_toggle_layers = ''
    script_sources_layers = ''

    layers_len = len(layer_list) - 1
    layer_ct = 0

    for layer in layer_list:
        # generate toggle buttons html
        sep = ' - ' if layer_ct < layers_len else ''
        button_fmt = '            <a class="{0}Toggle">{0}</a>{1}\n'.format(layer, sep)
        toggle_button_layers += button_fmt

        # generate openseadragon map layer variables
        layer_fmt = '            var {0} = \'dzi/{0}.dzi\'\n'.format(layer)
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

        script_sources_layers += js_layers
        layer_ct += 1

    html_str = """
<html>
    <head>
        <link href='viewer.css' rel='stylesheet'/>
        <script src="openseadragon/openseadragon.min.js"></script>
        <script src="openseadragon/jquery.min.js"></script>
    </head>
    <body>
        <div id="{0}">
{1}        </div>
        <div id='{3}'></div>
        <script>
            // map layers
{2}
            // openseadragon viewer
            var viewer = OpenSeadragon({{
                id: '{3}',
                prefixUrl: 'openseadragon/images/',
                toolbar: '{0}',
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
            opacity_toggle_div,
            toggle_button_layers,
            script_layers,
            viewer_id,
            script_sources_layers,
            script_toggle_layers
        )

    create_file(html_path, 'viewer.html', html_str)


def make_openseadragon_css(html_path, viewer_id='layerMap', opacity_toggle_div='toggleButtons'):
    """

    :param html_path:
    :param viewer_id:
    :param opacity_toggle_div:
    :return:
    """
    css_str = """
a {{
    cursor: pointer;
}}

#{0} {{
    height: 90%;
}}

#{1} {{
    text-align: center;
    height: 30px;
}}""".format(viewer_id, opacity_toggle_div)

    create_file(html_path, 'viewer.css', css_str)
