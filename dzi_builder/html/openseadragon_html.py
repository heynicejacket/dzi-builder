from dzi_builder.core.constants import (
    BASE_LAYER,
    OPACITY_TOGGLE_DIV,
    OSD_VIEWER_ID,
    SITE_NAME
)

from dzi_builder.core.toolkit import (
    create_file
)


def make_site(layer_path, layer_list):
    """
    Given a layer path and a list of layer names, generates the necessary html/css/js files for OpenJavascript to load
    a dzi file on the web.

    See /layers/openseadragon/readme.txt - requires OpenSeadragon files here: https://openseadragon.github.io/#download
    :param layer_path:      str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :param layer_list:      list, required      list of layer names, e.g. ['river', 'base', 'grid']
    :return:                none
    """
    html_path = layer_path + 'html\\'
    osd_path = html_path + 'openseadragon\\'

    readme = 'download the zip from https://openseadragon.github.io/#download, drop openseadragon files here.\n\n' \
             'download the zip from https://jquery.com/download/, drop jquery file here; you will likely need\n' \
             'to modify the html file to point to the correct jquery-#.#.#.min.js (line 5 in viewer.html).'
    create_file(osd_path, 'README.txt', readme)

    make_openseadragon_html(html_path, layer_list)
    make_openseadragon_css(html_path)


def make_openseadragon_html(html_path, layer_list, viewer_id=OSD_VIEWER_ID, opacity_div=OPACITY_TOGGLE_DIV):
    """
    Generates HTML file with JS necessary for a basic implementation of a Deep Zoom Image, based on a list of layer
    names, div name for OpenSeadragon viewer, and div name for OpenSeadragon layer opacity toggle buttons.

    :param html_path:       str, required       path to generate html file, e.g. '\\layers\\html\\'
    :param layer_list:      list, required      list of layer names, e.g. ['river', 'base', 'grid']
    :param viewer_id:       str, optional       div name for OpenSeadragon viewer
    :param opacity_div:     str, optional       div name for OpenSeadragon layer opacity toggle buttons
    :return:                none
    """
    toggle_button_layers = ''
    script_layers = ''
    script_toggle_layers = ''
    script_sources_layers = ''

    layers_len = len(layer_list) - 1
    layer_ct = 0

    try:
        layer_list.insert(0, layer_list.pop(layer_list.index(BASE_LAYER)))
    except ValueError:
        pass

    for layer in layer_list:
        # generate openseadragon map layer variables
        layer_fmt = '            var {0} = \'dzi/{0}.dzi\'\n'.format(layer)
        script_layers += layer_fmt

        # generate openseadragon tileSources
        suffix = ',' if layer_ct < layers_len else ''
        opacity = 1 if layer == BASE_LAYER else 0
        js_layers = """
                    {{
                        x: 0,
                        y: 0,
                        opacity: {0},
                        tileSource: {1}
                    }}{2}""".format(opacity, layer, suffix)

        if layer != BASE_LAYER:
            # generate toggle buttons html
            sep = ' - ' if layer_ct < layers_len else ''
            button_fmt = '            <a class="{0}Toggle">{0}</a>{1}\n'.format(layer, sep)
            toggle_button_layers += button_fmt

            # generate toggle buttons jquery functionality
            layer_fmt = """
                var {0}Opacity = 0;
                $('.{0}Toggle').on('click', function() {{
                    if ({0}Opacity === 0) {{
                        {0}Opacity = 1;
                    }} else {{
                        {0}Opacity = 0;
                    }}
                    {0}Fade(viewer.world.getItemAt({1}), {0}Opacity);
                }});
                var {0}Fade = function(image, opacity) {{
                    image.setOpacity({0}Opacity);
                    OpenSeadragon.requestAnimationFrame(frame);
                }};
                """.format(layer, layer_ct)

            script_toggle_layers += layer_fmt

        script_sources_layers += js_layers
        layer_ct += 1

    html_str = """
<html>
    <head>
        <link href='{0}.css' rel='stylesheet'/>
        <script src="openseadragon/openseadragon.min.js"></script>
        <script src="openseadragon/jquery.min.js"></script>
    </head>
    <body>
        <div id="{1}">
{2}        </div>
        <div id='{4}'></div>
        <script>
            // map layers
{3}
            // openseadragon viewer
            var viewer = OpenSeadragon({{
                id: '{4}',
                prefixUrl: 'openseadragon/images/',
                toolbar: '{1}',
                zoomInButton: 'zoom-in',
                zoomOutButton: 'zoom-out',
                homeButton: 'home',
                fullPageButton: 'full-page',
                tileSources: [{5}
                ]
            }});

            // jquery button functionality {6}
        </script>
    </body>
</html>""".format(
            SITE_NAME,
            opacity_div,
            toggle_button_layers,
            script_layers,
            viewer_id,
            script_sources_layers,
            script_toggle_layers
        )

    create_file(html_path, '{}.html'.format(SITE_NAME), html_str)


def make_openseadragon_css(html_path, viewer_id=OSD_VIEWER_ID, opacity_div=OPACITY_TOGGLE_DIV):
    """
    Generates CSS file necessary for a basic implementation of a Deep Zoom Image, based on a list of layer names, div
    name for OpenSeadragon viewer, and div name for OpenSeadragon layer opacity toggle buttons.

    :param html_path:       str, required       path to generate css file, e.g. '\\layers\\html\\'
    :param viewer_id:       str, optional       div name for OpenSeadragon viewer
    :param opacity_div:     str, optional       div name for OpenSeadragon layer toggle buttons
    :return:                none
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
}}""".format(viewer_id, opacity_div)

    create_file(html_path, '{}.css'.format(SITE_NAME), css_str)
