from dataclasses import dataclass, field
import json
import os

from django.conf import settings
from django.template import Library

register = Library()
_manifest_cache: tuple[int, dict] | None = None


@dataclass
class ViteManifestContext:
    css_files: list[str] = field(default_factory=list)
    js_files: list[str] = field(default_factory=list)
    modulepreloads: list[str] = field(default_factory=list)


@dataclass
class ViteManifestWalkState:
    entries: set[str] = field(default_factory=set)
    css_files: set[str] = field(default_factory=set)
    js_files: set[str] = field(default_factory=set)
    modulepreloads: set[str] = field(default_factory=set)


def append_once(target_list, seen_set, file_path):
    if file_path in seen_set:
        return

    seen_set.add(file_path)
    target_list.append(file_path)


def load_manifest():
    global _manifest_cache

    manifest_path = settings.VITE_MANIFEST
    manifest_mtime_ns = os.stat(manifest_path).st_mtime_ns

    if _manifest_cache is not None:
        cached_mtime_ns, cached_manifest = _manifest_cache
        if cached_mtime_ns == manifest_mtime_ns:
            return cached_manifest

    with open(manifest_path, "r") as manifest_file:
        manifest = json.load(manifest_file)

    _manifest_cache = (manifest_mtime_ns, manifest)
    return manifest


def walk_manifest(manifest, entry_point, context=None, state=None):
    if context is None:
        context = ViteManifestContext()
    if state is None:
        state = ViteManifestWalkState()

    if entry_point in state.entries:
        return context

    entry = manifest[entry_point]
    referenced_file = entry["file"]
    is_entry = entry.get("isEntry", False)
    state.entries.add(entry_point)
    for css_file in entry.get("css", []):
        append_once(context.css_files, state.css_files, css_file)
    if is_entry:
        if referenced_file.endswith(".css"):
            append_once(context.css_files, state.css_files, referenced_file)
        elif referenced_file.endswith(".js"):
            append_once(context.js_files, state.js_files, referenced_file)
    elif referenced_file.endswith(".js"):
        append_once(
            context.modulepreloads,
            state.modulepreloads,
            referenced_file,
        )

    for imported_file in entry.get("imports", []):
        walk_manifest(manifest, imported_file, context, state)
    return context


@register.inclusion_tag("vite/vite.html")
def vite(entry_point):
    manifest = load_manifest()
    return {"manifest": walk_manifest(manifest, entry_point)}
