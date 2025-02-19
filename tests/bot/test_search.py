import pytest
from unittest import mock
from bot.exts.filtering._ui.search import search_criteria_converter
from discord.ext.commands import BadArgument

# Mocked dependencies to bypass the circular import issue
@pytest.fixture
def mock_parse_value():
    # We will patch the function correctly depending on where parse_value is located
    with mock.patch('bot.exts.filtering._ui.ui', return_value=10):
        
        yield

@pytest.fixture
def mock_alert_view():
    with mock.patch('bot.exts.filtering._ui.ui.AlertView', autospec=True):
        yield

# Test case 1: Valid input data with a filter that matches the expected settings and filter settings
def test_search_criteria_converter_valid(mock_parse_value):
    filter_lists = {}
    loaded_filters = {'filter_name': mock.MagicMock()}
    loaded_settings = {'setting_1': ('', '', int)}  # Mock setting format for int
    loaded_filter_settings = {}
    filter_type = None
    input_data = "setting_1=10"

    settings, filter_settings, filter_type = search_criteria_converter(
        filter_lists, loaded_filters, loaded_settings, loaded_filter_settings, filter_type, input_data
    )

    assert settings == {'setting_1': 10}
    assert filter_settings == {}
    assert filter_type is None

# Test case 2: Valid input with a filter type that doesn't match the loaded filter
def test_search_criteria_converter_invalid_filter(mock_parse_value):
    filter_lists = {}
    loaded_filters = {"valid_filter": mock.MagicMock()}  # Only a "valid_filter" exists
    loaded_settings = {}
    loaded_filter_settings = {}
    filter_type = None
    input_data = "non_existent_filter/setting=value"

    # Simulate a scenario where the filter type doesn't match the loaded filters
    with pytest.raises(BadArgument, match="There's no filter type named 'non_existent_filter'."):
        search_criteria_converter(
            filter_lists, loaded_filters, loaded_settings, loaded_filter_settings, filter_type, input_data
        )

# Test case 3: Invalid with an invalid setting
def test_invalid_setting():
    filter_lists = {}
    loaded_filters = {}
    loaded_settings = {"valid_setting": (None, None, str)}  # Only one valid setting
    loaded_filter_settings = {}
    filter_type = None
    
    # Input string contains an invalid setting "invalid_setting"
    input_data = "invalid_setting=value"
    
    with pytest.raises(BadArgument, match=r"'invalid_setting' is not a recognized setting."):
        search_criteria_converter(
            filter_lists,
            loaded_filters,
            loaded_settings,
            loaded_filter_settings,
            filter_type,
            input_data
        )
        

# Test case 4: Valid input data with template application
def test_search_criteria_no_input_data(mock_parse_value):
    filter_lists = {}
    loaded_filters = {}
    loaded_settings = {}  
    loaded_filter_settings = {}
    filter_type = None
    input_data = ""

    settings, filter_settings, filter_type = search_criteria_converter(
        filter_lists, loaded_filters, loaded_settings, loaded_filter_settings, filter_type, input_data
    )

    assert settings == {}  # Template settings should be applied
    assert filter_settings == {}
    assert filter_type == None  # Template filter type should be returned
