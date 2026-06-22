import os
import re
import base64
import io
from .read_write_json import read_json

_pixmap_cache: dict = {}


def get_icon_path(icon_code: str, white: bool = False) -> str:
    settings = read_json("settings.json")
    current = settings.get("current_img_list", "weather_icons")
    subfolder = "weather_icons_white" if white else "weather_icons"
    candidate = os.path.join("media", "right_frame", current, f"{icon_code}.svg")
    if os.path.exists(candidate):
        return candidate
    fallback = os.path.join("media", "right_frame", subfolder, f"{icon_code}.svg")
    return fallback


def svg_to_pixmap(path: str, size: int):
    import PyQt6.QtGui as gui
    import PyQt6.QtCore as core

    default = os.path.join("media", "right_frame", "weather_icons", "01d.svg")
    if not path or not os.path.exists(path):
        path = default

    cache_key = f"{path}:{size}"
    if cache_key in _pixmap_cache:
        return _pixmap_cache[cache_key]

    px = _extract_base64_png(path, size)

    # Если base64 не нашли — обычный QSvgRenderer (для простых SVG)
    if px is None or px.isNull():
        px = _render_via_qt(path, size)

    # Последний fallback
    if px is None or px.isNull():
        px = gui.QIcon(default).pixmap(core.QSize(size, size))

    _pixmap_cache[cache_key] = px
    return px

def clear_cache():
    _pixmap_cache.clear()

def _extract_base64_png(path: str, size: int):
    """Извлекает PNG из base64 внутри SVG <image> тега."""
    import PyQt6.QtGui as gui
    import PyQt6.QtCore as core

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Ищем data:image/png;base64 или data:image/jpeg;base64
        match = re.search(
            r'xlink:href=["\']data:image/(png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=\s]+)["\']',
            content
        )
        if not match:
            match = re.search(
                r'href=["\']data:image/(png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=\s]+)["\']',
                content
            )

        if match:
            b64_data = match.group(2).replace("\n", "").replace(" ", "")
            img_bytes = base64.b64decode(b64_data)
            qimg = gui.QImage.fromData(img_bytes)
            if not qimg.isNull():
                px = gui.QPixmap.fromImage(qimg)
                return px.scaled(
                    size, size,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation
                )
    except Exception as e:
        print(f"[_extract_base64_png] {path}: {e}")
    return None


def _render_via_qt(path: str, size: int):
    """Рендерит простой SVG через QSvgRenderer (без <use>/<defs>)."""
    import PyQt6.QtGui as gui
    import PyQt6.QtCore as core
    from PyQt6.QtSvg import QSvgRenderer

    try:
        renderer = QSvgRenderer(path)
        if not renderer.isValid():
            return None
        img = gui.QImage(size, size, gui.QImage.Format.Format_ARGB32)
        img.fill(core.Qt.GlobalColor.transparent)
        painter = gui.QPainter(img)
        renderer.render(painter)
        painter.end()
        if not img.isNull():
            return gui.QPixmap.fromImage(img)
    except Exception as e:
        print(f"[_render_via_qt] {path}: {e}")
    return None