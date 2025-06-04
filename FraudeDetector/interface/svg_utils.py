import math
from typing import List, Tuple, Optional

def desenhar_grafo_svg(nos: List[str], arestas: List[Tuple[str, str]], destaque: Optional[List[str]] = None, width=600, height=600) -> str:
    """
    Gera um SVG simples de um grafo.
    - nos: lista de IDs dos nós
    - arestas: lista de tuplas (origem, destino)
    - destaque: lista de IDs de nós a destacar (opcional)
    """
    n = len(nos)
    if n == 0:
        return "<svg width='{}' height='{}'></svg>".format(width, height)
    raio = min(width, height) // 2 - 50
    cx, cy = width // 2, height // 2
    pos = {}
    for i, no in enumerate(nos):
        ang = 2 * math.pi * i / n
        x = cx + raio * math.cos(ang)
        y = cy + raio * math.sin(ang)
        pos[no] = (x, y)
    svg = [f"<svg width='{width}' height='{height}' style='background:#f9f9f9'>"]
    for origem, destino in arestas:
        x1, y1 = pos[origem]
        x2, y2 = pos[destino]
        svg.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#888' stroke-width='2' marker-end='url(#arrow)' />")
    svg.append("""
    <defs>
      <marker id='arrow' markerWidth='10' markerHeight='10' refX='10' refY='5' orient='auto' markerUnits='strokeWidth'>
        <path d='M0,0 L10,5 L0,10 L2,5 z' fill='#888' />
      </marker>
    </defs>
    """)
    for no in nos:
        x, y = pos[no]
        cor = '#ff4136' if destaque and no in destaque else '#0074d9'
        svg.append(f"<circle cx='{x}' cy='{y}' r='18' fill='{cor}' stroke='#333' stroke-width='2' />")
        svg.append(f"<text x='{x}' y='{y+5}' text-anchor='middle' font-size='13' fill='#fff'>{no}</text>")
    svg.append("</svg>")
    return ''.join(svg) 