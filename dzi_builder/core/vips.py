import subprocess


verbose = True
layer_path = 'C:\\localtemp\\layers\\'
exe_path = '"C:\\Program Files\\vips-dev-8.6\\bin\\"'
offset_width = 3000
ll = ['base', 'grid', 'river']


def create_row(columns, layer_list, vips_path):
    i = 0
    layer = 0
    while i < columns - 1:
        tile_to_add = '{}-{}.png'.format(layer_list[layer], tile_number(i, 1))
        print(tile_to_add)
        temp_offset_width = offset_width
        current_row_output = 'row{}output{}.png'.format(0, i)
        if i == 0:
            prior_row_output = '{}-{}.png'.format(layer_list[layer], tile_number(i))
            print(prior_row_output)
        else:
            prior_row_output = 'row{}output{}.png'.format(0, i - 1)

        goto = 'cd {}'.format(vips_path)
        mogrify = 'vips merge {0}{3} {0}{2} {0}{4} horizontal {1} 0'.format(
            'C:\\localtemp\\layers\\',
            temp_offset_width,
            prior_row_output,
            tile_to_add,
            current_row_output
        )
        print(mogrify)

        sp_call = subprocess.run(goto, capture_output=verbose, text=verbose)
        print(sp_call .stdout) if verbose else None

        sp_out = subprocess.run(mogrify, capture_output=verbose, text=verbose)
        print(sp_out.stdout) if verbose else None

        temp_offset_width += offset_width
        i += 1


def tile_number(a, mod=0):
    if a + mod < 10:
        i = '00' + str(a + mod)
    elif a + mod >= 10 & a + mod < 100:
        i = '0' + str(a + mod)
    else:
        i = str(a + mod)

    return i


create_row(3, ll, exe_path)
