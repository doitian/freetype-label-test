import freetype as ft
from PIL import Image


def main(stroke=0):
    """executable entry."""
    face = ft.Face('./WenQuanYiMicroHei.ttf')
    face.set_char_size(48*64)
    if stroke == 0:
        flags = ft.FT_LOAD_DEFAULT
    else:
        flags = ft.FT_LOAD_DEFAULT | ft.FT_LOAD_NO_BITMAP
    face.load_char('心', flags)
    slot = face.glyph
    glyph = slot.get_glyph()

    if stroke > 0:
        stroker = ft.Stroker()
        stroker.set(
            64,
            ft.FT_STROKER_LINECAP_ROUND,
            ft.FT_STROKER_LINEJOIN_ROUND,
            0
        )
        glyph.stroke(stroker, True)

    blyph = glyph.to_bitmap(ft.FT_RENDER_MODE_NORMAL, ft.Vector(0, 0), True)
    bitmap = blyph.bitmap
    width, rows, pitch = bitmap.width, bitmap.rows, bitmap.pitch

    print({
        'width': slot.metrics.width >> 6,
        'height': slot.metrics.height >> 6,
        'horiBearingX': slot.metrics.horiBearingX >> 6,
        'horiBearingY': slot.metrics.horiBearingY >> 6,
        'horiAdvance': slot.metrics.horiAdvance >> 6,
        'bitmapWidth': bitmap.width,
        'bitmapHeight': bitmap.rows
        })
    img = Image.new("L", (width, rows), "black")
    pixels = img.load()

    for y in range(img.size[1]):
        offset = y * pitch
        for x in range(img.size[0]):
            pixels[x, y] = 255 - bitmap.buffer[offset + x]

    img.show()


if __name__ == '__main__':
    main()
    main(2)
