import re
from bot.exts.filtering._ui.filter import description_and_settings_converter
import bot.exts.filtering._ui.ui as ui

# For testing, set SINGLE_SETTING_PATTERN so that 
# strings containing an "=" are recognized as settings.
ui.SINGLE_SETTING_PATTERN = re.compile(r".+=.+")



class TestFilterList:
    """Test implementation for filter_list[list_type]."""
    def __init__(self, defaults):
        self._defaults = defaults
        self.filters = {}

    def default(self, setting):
        return self._defaults.get(setting)
    
class TestFilter:
    """Test filter type."""
    name = "test"

    @staticmethod
    def extra_fields_type():
        return TestExtraFields()

class TestExtraFields:
    """Extra fields implementation for test."""
    def __init__(self):
        self.x = 0

    def model_dump(self):
        return {"x": self.x}


list_type = "test_list"
filter_list = {list_type: TestFilterList(defaults={"a": 0})}

loaded_settings = {"a": ("", "", int)}

loaded_filter_settings = {"test": {"x": ("", "", int)}}



# Tests:
def test_empty_input():
    """
    Test empty input.
    """
    description, settings, filter_settings = description_and_settings_converter(
        filter_list, list_type, TestFilter, loaded_settings, loaded_filter_settings, ""
    )
    assert description == ""
    assert settings == {}
    assert filter_settings == {}


def test_only_description():
    """
    Test for when input string lacks SINGLE_SETTING_PATTERN, here '='.
    Input interpreted as only description.
    """
    test_input_data = "description"
    description, settings, filter_settings = description_and_settings_converter(
        filter_list, list_type, TestFilter, loaded_settings, loaded_filter_settings, test_input_data
    )
    assert description == test_input_data
    assert settings == {}
    assert filter_settings == {}


def test_filter_list_setting_override():
    """
    Test for when the input is a valid filter list setting and the parsed value is different
    from the default, returned as an override.
    """
    test_input_data = "a=1"
    description, settings, filter_settings = description_and_settings_converter(
        filter_list, list_type, TestFilter, loaded_settings, loaded_filter_settings, test_input_data
    )
    assert description == ""
    assert settings == {"a": 1}
    assert filter_settings == {}


def test_filter_extra_field_override():
    """
    Test for when the input is a valid filter extra field setting and the parsed value
    is different from the default, returned as an extra field override.
    """
    test_input_data = "test/x=2"
    description, settings, filter_settings = description_and_settings_converter(
        filter_list, list_type, TestFilter, loaded_settings, loaded_filter_settings, test_input_data
    )
    assert description == ""
    assert settings == {}
    assert filter_settings == {"x": 2}
    