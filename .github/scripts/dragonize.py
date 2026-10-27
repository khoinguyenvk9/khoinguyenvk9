"""Turn a Platane/snk snake SVG into a fire dragon, in place.

Usage: python3 dragonize.py file.svg [file.svg ...]
"""
import re
import sys

STEP_MS = 99  # one cell of travel in snk's default timing (~0.6% of 16500ms)

STYLE = """
:root{--cs:#ff4d00;--c1:#ffd6a5;--c2:#ffb066;--c3:#ff7a1a;--c4:#d9480f}
.s{filter:drop-shadow(0 0 2px #ff6a00)}
rect.s.s0{fill:none;filter:none}
.s.s1{fill:#ff5a00}.s.s2{fill:#ff8a00}.s.s3{fill:#ffc400}
.dh.s0{animation-name:s0,pulse;animation-duration:16500ms,1.1s;
  animation-timing-function:linear,ease-in-out;
  animation-iteration-count:infinite,infinite;animation-direction:normal,alternate}
@keyframes pulse{from{filter:drop-shadow(0 0 1px #ff4d00)}to{filter:drop-shadow(0 0 6px #ffb300)}}
.fl{transform-box:fill-box;transform-origin:left center;animation:flame .18s ease-in-out infinite alternate}
@keyframes flame{from{transform:scale(.55,.8);opacity:.7}to{transform:scale(1.15,1.1);opacity:1}}
.em{transform:translate(48px,-16px);animation-name:s3;animation-duration:16500ms;
  animation-timing-function:linear;animation-iteration-count:infinite;filter:blur(.4px)}
.em circle{animation:ember .5s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}
@keyframes ember{from{opacity:.25;transform:scale(.6)}to{opacity:.95;transform:scale(1.2)}}
"""

# Dragon head, ~16x16, facing right, drawn inside the cell the snake head occupies.
HEAD = (
    '<g class="s s0 dh">'
    '<polygon points="3,4 1,-1 6,3" fill="#ffc400"/>'
    '<polygon points="6,3.5 5,-1.5 9,3.2" fill="#ffc400"/>'
    '<polygon points="1,4.5 10,3 17,7 17,10.5 10,13 1,12" fill="#ff3d00"/>'
    '<polygon points="10,12.5 17,10.5 16,12.5 11,14" fill="#c92a00"/>'
    '<circle cx="10" cy="7" r="1.7" fill="#fff"/><circle cx="10.5" cy="7" r=".8" fill="#111"/>'
    '<circle cx="15.4" cy="8" r=".6" fill="#7a1d00"/>'
    '<polygon class="fl" points="17,8 23,6 21,8.3 24,9.3 17,10.2" fill="#ffd34d"/>'
    '</g>'
)

EMBERS = "".join(
    f'<g class="s em" style="animation-delay:{(i + 1) * STEP_MS}ms">'
    f'<circle cx="7.5" cy="7.5" r="{r}" fill="{c}"/></g>'
    for i, (r, c) in enumerate([(3.2, "#ff8a00"), (2.4, "#ff5a00"), (1.6, "#ffd34d")])
)


def dragonize(svg: str) -> str:
    if "</svg>" not in svg or "class=\"s s0\"" not in svg:
        raise ValueError("not a snk snake svg")
    svg = svg.replace("</style>", STYLE + "</style>", 1)
    return svg.replace("</svg>", EMBERS + HEAD + "</svg>")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path) as f:
            out = dragonize(f.read())
        with open(path, "w") as f:
            f.write(out)
