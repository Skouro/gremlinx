# Standar library
from __future__ import annotations
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Union,
)

# Third libraries

# Local imports


def hasLabel(
    *labels: str,
    traversal: Any,
    vertex: Union[str, Tuple[str, str]],
) -> bool:
    if isinstance(vertex, str):
        data = traversal.graph.nodes[vertex]
    else:
        data = traversal.graph[vertex[0]][vertex[1]]
    return all(data.get(f'label_{label}') for label in labels) or all(
        any(
            key.startswith('label') and value == label
            for key, value in data.items()) for label in labels)


def has(
    *args: Any,
    traversal: Any,
    vertex: Union[str, Tuple[str, str]],
) -> bool:
    label: Optional[str] = None
    prop: Optional[str] = None
    value: Optional[Any] = None

    if len(args) == 1:
        prop = args[0]
    elif len(args) == 2:
        prop = args[0]
        value = args[1]
    elif len(args) == 3:
        label = args[0]
        prop = args[1]
        value = args[2]
        if traversal.sources_is_edges:
            raise Exception
    else:
        raise Exception
    result = False

    def __has(*args: Any, ) -> bool:
        _result = False
        if traversal.sources_is_vertex:
            v_id = args[0]
            _result = traversal.graph.nodes[v_id].get(
                prop) == value if value else bool(
                    traversal.graph.nodes[v_id].get(prop))

        elif traversal.sources_is_edges:
            v_out, v_in = args
            _result = traversal.graph[v_out][v_in].get(
                prop) == value if value else bool(
                    traversal.graph[v_out][v_in].get(prop))

        return _result

    if label:
        result = hasLabel(label, traversal=traversal, vertex=vertex)

    if traversal.sources_is_vertex and value and label:
        result = result and __has(vertex)
    elif traversal.sources_is_vertex:
        result = __has(vertex)
    elif traversal.sources_is_edges:
        result = __has(*vertex)
    return result


def out(
    *labels: Any,
    traversal: Any,
    vertex: Union[str, Tuple[str, str]],
) -> Tuple[str, ...]:
    childs: Tuple[str, ...] = tuple(traversal.graph.adj[vertex])
    return tuple(child for child in childs if (all(
        hasLabel(label, vertex=(vertex, child), traversal=traversal)
        for label in labels) if labels else True))


def values(
    *propertis: Any,
    traversal: Any,
    vertex: Union[str, Tuple[str, str]],
) -> Union[Any, Dict[str, Any]]:
    if traversal.sources_is_edges:
        out, ingress = vertex  # type: ignore
        source = traversal.graph[out][ingress]
    else:
        source = traversal.graph.nodes[vertex]
    if propertis:
        source = {
            key: value
            for key, value in source.items() if key in propertis
        }
    return source


def fold(
    *,
    vertex: Union[str, Tuple[str, str]],
) -> Union[Any, Dict[str, Any]]:
    if isinstance(vertex, dict):
        values = tuple(vertex.values())
        if len(values) == 1:
            return values[0]
        return values

    return vertex
