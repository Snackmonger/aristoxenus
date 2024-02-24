from src.permutation import tetrad_variants, triad_variants

from src.rendering import render_plain


for variant in tetrad_variants():
    for k, v in variant.items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                if isinstance(vv, int):
                    print(k, kk, render_plain(vv))
        elif isinstance(v, int):
            print(k, render_plain(v))
