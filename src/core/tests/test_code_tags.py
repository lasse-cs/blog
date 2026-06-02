from django.template import Context, Template

from core.blocks import CodeBlock, CodeLanguageChoices


def render_template(template_string):
    template = Template(template_string)
    return template.render(Context())


def test_highlight_code_renders_python_tokens():
    rendered = render_template(
        "{% load code_tags %}{{ 'print(1)'|highlight_code:'python' }}"
    )

    assert '<span class="nb">print</span>' in rendered


def test_highlight_code_renders_unknown_language_as_plain_text():
    rendered = render_template(
        "{% load code_tags %}{{ '<script>'|highlight_code:'not-a-language' }}"
    )

    assert rendered == "&lt;script&gt;"


def test_highlight_code_escapes_known_language_code():
    rendered = render_template(
        "{% load code_tags %}{{ '<script>'|highlight_code:'html' }}"
    )

    assert "<script>" not in rendered
    assert "&lt;" in rendered


def test_highlight_code_escapes_code_when_autoescape_is_off():
    rendered = render_template(
        "{% load code_tags %}{% autoescape off %}"
        "{{ '<script>'|highlight_code:'not-a-language' }}"
        "{% endautoescape %}"
    )

    assert rendered == "&lt;script&gt;"


def test_code_block_value_has_content_cache_key():
    block = CodeBlock()
    value = block.to_python({"language": "python", "code": "print(1)"})
    same_value = block.to_python({"language": "python", "code": "print(1)"})
    different_code = block.to_python({"language": "python", "code": "print(2)"})
    different_language = block.to_python({"language": "bash", "code": "print(1)"})

    assert value.cache_key == same_value.cache_key
    assert value.cache_key != different_code.cache_key
    assert value.cache_key != different_language.cache_key


def test_code_block_value_has_language_label():
    block = CodeBlock()
    value = block.to_python({"language": "javascript", "code": "console.log(1)"})

    assert value.language_label == "JavaScript"


def test_code_block_value_language_label_falls_back_to_language():
    block = CodeBlock()
    value = block.to_python({"language": "not-a-language", "code": "print(1)"})

    assert value.language_label == "not-a-language"


def test_code_language_choices_include_supported_languages():
    expected_languages = {
        "go": "Go",
        "javascript": "JavaScript",
        "lua": "Lua",
        "typescript": "TypeScript",
    }

    assert dict(CodeLanguageChoices.choices).items() >= expected_languages.items()
