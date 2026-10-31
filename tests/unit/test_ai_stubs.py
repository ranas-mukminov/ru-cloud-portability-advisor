from ru_cloud_portability_advisor.ai.base import NoopAIProvider


def test_noop_ai_provider():
    provider = NoopAIProvider()
    assert "not configured" in provider.complete("hello").lower()
    assert "not configured" in provider.chat([]).lower()
