import json
import os

import pytest

from vite.templatetags import vite_tags
from vite.templatetags.vite_tags import load_manifest, walk_manifest


@pytest.fixture
def manifest():
    yield json.loads("""
        {
            "_shared-B7PI925R.js": {
                "file": "assets/shared-B7PI925R.js",
                "name": "shared",
                "css": ["assets/shared-ChJ_j-JJ.css"]
            },
            "_shared-ChJ_j-JJ.css": {
                "file": "assets/shared-ChJ_j-JJ.css",
                "src": "_shared-ChJ_j-JJ.css"
            },
            "logo.svg": {
                "file": "assets/logo-BuPIv-2h.svg",
                "src": "logo.svg"
            },
            "baz.js": {
                "file": "assets/baz-B2H3sXNv.js",
                "name": "baz",
                "src": "baz.js",
                "isDynamicEntry": true
            },
            "views/bar.js": {
                "file": "assets/bar-gkvgaI9m.js",
                "name": "bar",
                "src": "views/bar.js",
                "isEntry": true,
                "imports": ["_shared-B7PI925R.js"],
                "dynamicImports": ["baz.js"]
            },
            "views/foo.js": {
                "file": "assets/foo-BRBmoGS9.js",
                "name": "foo",
                "src": "views/foo.js",
                "isEntry": true,
                "imports": ["_shared-B7PI925R.js"],
                "css": ["assets/foo-5UjPuW-k.css"]
            }
        }
    """)


def test_walking_manifest(manifest):
    foo_result = walk_manifest(
        manifest,
        "views/foo.js",
    )
    assert foo_result.css_files == [
        "assets/foo-5UjPuW-k.css",
        "assets/shared-ChJ_j-JJ.css",
    ]
    assert foo_result.js_files == ["assets/foo-BRBmoGS9.js"]
    assert foo_result.modulepreloads == ["assets/shared-B7PI925R.js"]

    bar_result = walk_manifest(
        manifest,
        "views/bar.js",
    )
    assert bar_result.css_files == [
        "assets/shared-ChJ_j-JJ.css",
    ]
    assert bar_result.js_files == ["assets/bar-gkvgaI9m.js"]
    assert bar_result.modulepreloads == ["assets/shared-B7PI925R.js"]


def test_load_manifest_reloads_when_mtime_changes(tmp_path, settings):
    manifest_path = tmp_path / "manifest.json"
    settings.VITE_MANIFEST = str(manifest_path)
    vite_tags._manifest_cache = None

    manifest_path.write_text(
        json.dumps({"js/blog.ts": {"file": "js/blog.v1.js", "isEntry": True}})
    )
    first_manifest = load_manifest()

    manifest_path.write_text(
        json.dumps({"js/blog.ts": {"file": "js/blog.v2.js", "isEntry": True}})
    )
    stat_result = os.stat(manifest_path)
    os.utime(
        manifest_path,
        ns=(stat_result.st_atime_ns, stat_result.st_mtime_ns + 1),
    )

    second_manifest = load_manifest()

    assert first_manifest["js/blog.ts"]["file"] == "js/blog.v1.js"
    assert second_manifest["js/blog.ts"]["file"] == "js/blog.v2.js"
    assert first_manifest is not second_manifest
