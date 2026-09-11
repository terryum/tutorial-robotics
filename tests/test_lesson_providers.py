from pai_lab.providers import discover_lesson_providers, extended_catalog, provider_for


def test_public_checkout_has_no_private_provider() -> None:
    assert discover_lesson_providers() == ()
    assert extended_catalog() == ()
    assert provider_for("T11") is None
