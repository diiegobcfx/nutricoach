#!/usr/bin/env python3
"""Generate simple PNG icons for the PWA using only stdlib."""
import struct, zlib, base64

def make_png(size, bg=(5, 150, 105), fg=(255,255,255)):
    """Create a minimal valid PNG with a leaf-like shape."""
    w = h = size
    raw = []
    cx, cy = w // 2, h // 2
    r = int(w * 0.38)
    for y in range(h):
        row = [0]
        for x in range(w):
            # rounded rect background
            dx = abs(x - cx) - r + int(r * 0.25)
            dy = abs(y - cy) - r + int(r * 0.25)
            corner_r = int(r * 0.25)
            in_rect = (abs(x - cx) <= r and abs(y - cy) <= r)
            in_corner = (dx > 0 and dy > 0 and (dx*dx + dy*dy) > corner_r*corner_r)
            if in_rect and not in_corner:
                # leaf icon (simple diamond)
                lx = abs(x - cx)
                ly = abs(y - cy)
                leaf_r = int(r * 0.55)
                if lx + ly < leaf_r:
                    row += list(fg) + [255]
                else:
                    row += list(bg) + [255]
            else:
                row += [0, 0, 0, 0]
        raw.append(bytes(row))

    def chunk(name, data):
        c = struct.pack('>I', len(data)) + name + data
        return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)

    idat_data = zlib.compress(b''.join(raw))
    png = (
        b'\x89PNG\r\n\x1a\n' +
        chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) +
        chunk(b'IDAT', idat_data) +
        chunk(b'IEND', b'')
    )
    return png

for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    data = make_png(size)
    with open(f'/home/claude/nutricoach/public/{name}', 'wb') as f:
        f.write(data)
    print(f'Generated {name} ({len(data)} bytes)')
