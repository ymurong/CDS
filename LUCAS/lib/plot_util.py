from typing import Dict


def nudge(pos: Dict, x_shift: int, y_shift: int) -> Dict:
    """
    shift positions in networkx graph
    """
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in pos.items()}
