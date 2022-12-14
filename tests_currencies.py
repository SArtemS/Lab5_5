from main import Currencies


def test_wrong_id(ID = "Wrong ID"):
    assert Currencies().get_specific_currency(ID) == {ID: None}
test_wrong_id()
