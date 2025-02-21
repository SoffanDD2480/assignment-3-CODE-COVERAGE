from collections import defaultdict
from unittest.mock import AsyncMock, MagicMock, patch

import arrow
import discord
import pytest

from bot.constants import Channels
from bot.exts.filtering._filter_lists.filter_list import AtomicList
from bot.exts.filtering._filters.filter import Filter
from bot.exts.filtering._settings_types.actions.infraction_and_notification import Infraction
from bot.exts.filtering.filtering import Filtering


pytest_plugins = "pytest_asyncio"

@pytest.fixture
def filtering_cog():
    """Fixture to create an instance of Filtering with mocked dependencies."""
    instance = Filtering(bot=MagicMock())
    instance.bot.get_channel = MagicMock()
    instance.filter_lists = defaultdict(lambda: defaultdict(AtomicList))  # Mock filter lists
    return instance


@pytest.mark.asyncio
@patch("bot.exts.filtering.filtering.is_mod_channel", return_value=True)
async def test_send_report_no_channel(mock_is_mod, filtering_cog):
    """Test that the function defaults to #mod-meta when no channel is given."""
    mock_channel = AsyncMock(spec=discord.TextChannel)
    filtering_cog.bot.get_channel.return_value = mock_channel

    with patch("arrow.utcnow", return_value=arrow.get("2025-02-18T12:00:00")):
        await filtering_cog.send_weekly_auto_infraction_report(channel=None)

    filtering_cog.bot.get_channel.assert_called_once_with(Channels.mod_meta)
    mock_channel.send.assert_called_once()


@pytest.mark.asyncio
@patch("bot.exts.filtering.filtering.is_mod_channel", return_value=False)
async def test_send_report_non_mod_channel(mock_is_mod, filtering_cog):
    """Test that the function exits early if the channel is not a mod channel."""
    mock_channel = AsyncMock(spec=discord.TextChannel)

    await filtering_cog.send_weekly_auto_infraction_report(channel=mock_channel)

    mock_channel.send.assert_not_called()


@pytest.mark.asyncio
@patch("bot.exts.filtering.filtering.is_mod_channel", return_value=True)
async def test_send_report_no_filters(mock_is_mod, filtering_cog):
    """Test that the function sends 'Nothing to show' when no auto-infraction filters are found."""
    mock_channel = AsyncMock(spec=discord.TextChannel)

    with patch("arrow.utcnow", return_value=arrow.get("2025-02-18T12:00:00")):
        await filtering_cog.send_weekly_auto_infraction_report(channel=mock_channel)

    mock_channel.send.assert_called_once_with("**Auto-infraction filters added since 2025-02-11**\n\nNothing to show")


@pytest.mark.asyncio
@patch("bot.exts.filtering.filtering.is_mod_channel", return_value=True)
async def test_send_report_with_filters(mock_is_mod, filtering_cog):
    """Test that the function correctly formats and sends a report when filters are found."""
    mock_channel = AsyncMock(spec=discord.TextChannel)

    # Crea un mock filter con date recenti
    mock_filter = MagicMock(spec=Filter)
    mock_filter.created_at = arrow.utcnow().shift(days=-1)
    mock_filter.updated_at = arrow.utcnow().shift(days=-1)
    mock_filter.overrides = [{"infraction_type": Infraction.KICK}]
    mock_filter.__str__ = MagicMock(return_value="test_filter")

    # Configura la struttura dei filter_lists
    mock_sublist = MagicMock()
    mock_sublist.label = "test_list"
    mock_sublist.default = MagicMock(return_value=Infraction.NONE)
    mock_sublist.filters = {"test_filter": mock_filter}

    filtering_cog.filter_lists["main_list"] = {"sublist": mock_sublist}

    with patch("arrow.utcnow", return_value=arrow.get("2025-02-18T12:00:00")):
        await filtering_cog.send_weekly_auto_infraction_report(channel=mock_channel)

    expected_message = (
        "**Auto-infraction filters added since 2025-02-11**\n\n"
        "**Test_List**\n"
        "test_filter (KICK)"
    )

    mock_channel.send.assert_called_once_with(expected_message)
