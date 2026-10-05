from hcis.services.epistemic import claim_can_auto_verify
def test_hearsay_cannot_auto_verify():
    assert claim_can_auto_verify("RUMORED") is False
    assert claim_can_auto_verify("REPORTED") is False
