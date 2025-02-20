import unittest
import unittest.mock
from unittest.mock import AsyncMock

import discord

from bot.exts.filtering._filter_context import FilterContext
from bot.exts.filtering._filter_lists.filter_list import FilterList, ListType
from bot.exts.filtering._filters.filter import Filter
from bot.exts.filtering._ui.filter import FilterEditView, MAX_EMBED_DESCRIPTION
from tests import helpers


# --- Dummy classes to simulate filter list and filter type behavior --- #
class DummyExtraFields:
    def model_dump(self):
        # Include the new_setting for testing
        return {
            "setting1": "default1",
            "new_setting": "default_value",
        }


class DummyFilterType(Filter):
    name = "DummyFilter"

    def __init__(self, content: str):
        self.content = content

    def extra_fields_type(self):
        return DummyExtraFields()

    async def triggered_on(self, ctx: FilterContext) -> bool:
        """Mock implementation of the required abstract method."""
        return False


class DummyFilterDefaults:
    def default(self, setting_name: str) -> str:
        return f"default_{setting_name}"

    @property
    def defaults(self):
        """Return a list of dictionaries representing settings groups."""
        return [{"setting1": DummyExtraFields()}, {"setting2": DummyExtraFields()}]


class DummyFilterList(FilterList):
    name = "DummyFilterList"

    def __init__(self):
        self.test = DummyFilterDefaults()

    def get_filter_type(self, content: str):
        # For testing, return None if content is "invalid"
        if content == "invalid":
            return None
        return DummyFilterType(content)

    def __getitem__(self, item: ListType):
        return self.test


class MockResponse:
    def __init__(self, status):
        self.status = status
        self.reason = "Mock Error"  # Attribute required by HTTPException


# --- Minimal dummy embed --- #
def make_dummy_embed():
    embed = discord.Embed(title="Test Embed")

    return embed


# --- Dummy confirm callback --- #
async def dummy_confirm_callback(*args, **kwargs):
    return


# --- Dummy message --- #
def make_dummy_message():
    """Return a dummy message using your helpers with an async edit method."""
    message = helpers.MockMessage()
    channel = helpers.MockTextChannel()
    channel.send = AsyncMock()
    message.channel = channel
    message.edit = AsyncMock()
    return message


# --- Factory functions for interactions and messages --- #
def make_dummy_interaction():
    """Return a dummy interaction using helpers with properly mocked async response methods."""
    interaction = helpers.MockInteraction()

    # Create normal response without exceptions
    response = AsyncMock()
    response.edit_message = AsyncMock(return_value=None)
    response.send_message = AsyncMock(return_value=None)

    interaction.response = response
    interaction.edit = AsyncMock(return_value=None)

    return interaction


# --- Test cases --- #
class TestFilterEditViewUpdateEmbed(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Set up test dependencies inside an async event loop."""
        self.filter_list = DummyFilterList()
        self.list_type = "test"
        self.initial_filter_type = DummyFilterType("initial")
        self.content = None
        self.description = None
        self.settings_overrides = {}
        self.filter_settings_overrides = {}
        self.loaded_settings = {}
        self.loaded_filter_settings = {}
        self.author = helpers.MockUser()
        self.embed = make_dummy_embed()
        self.confirm_callback = dummy_confirm_callback

        # Instantiate `FilterEditView` inside an async context.
        self.view = FilterEditView(
            filter_list=self.filter_list,
            list_type=self.list_type,
            filter_type=self.initial_filter_type,
            content=self.content,
            description=self.description,
            settings_overrides=self.settings_overrides,
            filter_settings_overrides=self.filter_settings_overrides,
            loaded_settings=self.loaded_settings,
            loaded_filter_settings=self.loaded_filter_settings,
            author=self.author,
            embed=self.embed,
            confirm_callback=self.confirm_callback,
        )

        # Ensure the view gets properly stopped after each test
        self.addCleanup(self.view.stop)

    async def test_valid_content_with_description(self):
        interaction = helpers.MockInteraction()
        interaction.__class__ = discord.Interaction  # Force type recognition
        response = unittest.mock.AsyncMock(return_value=None)
        response.edit_message = unittest.mock.AsyncMock(return_value=None)
        interaction.response = response
        interaction.edit = unittest.mock.AsyncMock(return_value=None)

        await self.view.update_embed(interaction, content="hello", description="world")

        self.assertEqual(self.view.content, "hello")
        self.assertEqual(self.view.description, "world")
        self.assertIn("hello", self.view.embed.description)
        self.assertIn("world", self.view.embed.description)
        self.assertTrue(self.view.is_finished())

        response.edit_message.assert_awaited()

    async def test_invalid_content(self):
        """Invalid content (no filter type found) sends an error message and does not update embed."""
        interaction = make_dummy_interaction()

        await self.view.update_embed(interaction, content="invalid")

        interaction.response.send_message.assert_awaited_with(
            ":x: Could not find a filter type appropriate for `invalid`."
        )

        # The embed should remain unchanged.
        self.assertEqual(self.view.embed.description, self.embed.description)
        self.assertFalse(self.view.is_finished())

    async def test_remove_description(self):
        """Setting description to _REMOVE clears the description."""
        # First set a description.
        self.view.description = "old description"

        interaction = make_dummy_interaction()

        await self.view.update_embed(interaction, content="hello", description=self.view._REMOVE)

        self.assertIsNone(self.view.description)
        self.assertIn("hello", self.view.embed.description)
        self.assertNotIn("old description", self.view.embed.description)
        self.assertTrue(self.view.is_finished())

    async def test_embed_description_truncated(self):
        """Long embed descriptions are truncated."""
        interaction = make_dummy_interaction()

        long_text = "a" * (MAX_EMBED_DESCRIPTION + 100)  # Make sure it's longer than max

        await self.view.update_embed(interaction, content=long_text, description=long_text)

        self.assertTrue(len(self.view.embed.description) <= MAX_EMBED_DESCRIPTION)
        self.assertTrue(self.view.embed.description.endswith("[...]"))
        self.assertTrue(self.view.is_finished())

    async def test_setting_with_slash_and_override(self):
        """Settings with a slash update filter_settings_overrides."""
        interaction = make_dummy_interaction()

        # First, set valid content to update filter_type.
        await self.view.update_embed(interaction, content="hello")

        # Now update a setting with a slash. (The default comes from DummyExtraFields.)
        await self.view.update_embed(
            interaction,
            setting_name="DummyFilter/new_setting",
            setting_value="new_value",
        )

        self.assertEqual(self.view.filter_settings_overrides.get("new_setting"), "new_value")
        self.assertTrue(self.view.is_finished())

    async def test_setting_without_slash_and_override(self):
        """Settings without a slash update settings_overrides."""
        interaction = make_dummy_interaction()

        await self.view.update_embed(interaction, content="hello")

        await self.view.update_embed(interaction, setting_name="setting2", setting_value="new_val")

        self.assertEqual(self.view.settings_overrides.get("setting2"), "new_val")
        self.assertTrue(self.view.is_finished())

    async def test_setting_equal_default_removes_override(self):
        """When a setting is updated to its default value, any override is removed."""
        interaction = make_dummy_interaction()

        await self.view.update_embed(interaction, content="hello")

        # First set an override.
        await self.view.update_embed(interaction, setting_name="setting3", setting_value="non_default")

        self.assertEqual(self.view.settings_overrides.get("setting3"), "non_default")

        # Now update with the default value.
        default_val = self.filter_list[self.list_type].default("setting3")
        self.view.settings_overrides["setting3"] = "non_default"

        await self.view.update_embed(interaction, setting_name="setting3", setting_value=default_val)

        self.assertNotIn("setting3", self.view.settings_overrides)
        self.assertTrue(self.view.is_finished())

    async def test_setting_remove(self):
        """Setting a value to _REMOVE removes the override."""
        interaction = make_dummy_interaction()

        self.view.settings_overrides["setting4"] = "some_value"

        await self.view.update_embed(
            interaction,
            content="hello",
            setting_name="setting4",
            setting_value=self.view._REMOVE,
        )

        self.assertNotIn("setting4", self.view.settings_overrides)
        self.assertTrue(self.view.is_finished())

    async def test_message_vs_interaction_edit(self):
        """Tests that a discord.Message and a discord.Interaction are handled appropriately."""
        # Test using a message first
        view1 = self.view.copy()
        message = make_dummy_message()
        message.edit = AsyncMock(return_value=None)  # Add return_value

        await view1.update_embed(message, content="hello", description="msg test")
        message.edit.assert_awaited_once()
        self.assertTrue(view1.is_finished())

        # Test using an interaction
        view2 = self.view.copy()
        interaction = helpers.MockInteraction()
        interaction.__class__ = discord.Interaction  # Force type recognition
        response = unittest.mock.AsyncMock(return_value=None)
        response.edit_message = unittest.mock.AsyncMock(return_value=None)
        interaction.response = response
        interaction.edit = unittest.mock.AsyncMock(return_value=None)

        await view2.update_embed(interaction, content="hello", description="int test")
        interaction.response.edit_message.assert_awaited_once()
        self.assertTrue(view2.is_finished())

    async def test_edit_message_http_exception(self):
        """Test: If editing the message raises an HTTPException, the view does not stop."""
        # Create a new interaction
        interaction = helpers.MockInteraction()

        # Create AsyncMock for both edit methods
        edit_mock = AsyncMock()
        edit_mock.side_effect = discord.errors.HTTPException(
            response=MockResponse(status=400), message="Test HTTP Exception"
        )

        # Set up both possible edit methods to raise the exception
        interaction.edit = edit_mock
        response = AsyncMock()
        response.edit_message = edit_mock
        interaction.response = response

        # Attempt to update the embed, which should trigger the exception
        await self.view.update_embed(interaction, content="hello", description="exception test")

        self.assertFalse(self.view.is_finished(), "View was incorrectly stopped")

        # Verify one of the edit methods was called
        self.assertTrue(edit_mock.called, "Neither edit method was called")


if __name__ == "__main__":
    unittest.main()
