"""Basic tests for Quick Design MCP server."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_skills_load():
    from src.core.prompt_builder import list_available_skills
    skills = list_available_skills()
    assert len(skills) >= 5, f"Expected 5+ skills, got {len(skills)}"
    ids = [s["id"] for s in skills]
    assert "pitch_deck" in ids
    assert "dashboard" in ids
    assert "ferrari_automotive" in ids
    print(f"✓ test_skills_load ({len(skills)} skills)")


def test_design_systems_load():
    from src.core.prompt_builder import list_available_design_systems
    systems = list_available_design_systems()
    assert len(systems) >= 4, f"Expected 4+ systems, got {len(systems)}"
    print(f"✓ test_design_systems_load ({len(systems)} systems)")


def test_design_system_fuzzy_match():
    from src.core.prompt_builder import load_design_system
    ds = load_design_system("linear")
    assert "#08090a" in ds or "#0f1011" in ds, "Linear design system should contain dark colors"
    print("✓ test_design_system_fuzzy_match")


def test_prompt_builder():
    from src.core.prompt_builder import build_prompt
    prompt = build_prompt("pitch_deck", "default", "Test product brief")
    assert "Test product brief" in prompt
    assert "DESIGN SYSTEM" in prompt
    assert "SKILL" in prompt
    print("✓ test_prompt_builder")


def test_renderer_html_save():
    import tempfile
    os.environ.setdefault("OUTPUT_DIR", tempfile.mkdtemp())
    from src.core.renderer import save_html
    path = save_html("<html><body>test</body></html>", "unit-test")
    assert path.exists()
    assert path.stat().st_size > 0
    path.unlink()
    print("✓ test_renderer_html_save")


def test_pptx_builder():
    import tempfile
    os.environ.setdefault("OUTPUT_DIR", tempfile.mkdtemp())
    from src.core.pptx_builder import create_pptx
    slides = [
        {"title": "Test Deck", "content": ["Bullet one", "Bullet two"]},
        {"title": "Slide 2", "content": ["Item A"]},
    ]
    path = create_pptx(slides, "test")
    assert path.exists()
    assert path.stat().st_size > 10000
    path.unlink()
    print("✓ test_pptx_builder")


if __name__ == "__main__":
    test_skills_load()
    test_design_systems_load()
    test_design_system_fuzzy_match()
    test_prompt_builder()
    test_renderer_html_save()
    test_pptx_builder()
    print("\n✅ All tests passed!")
