from __future__ import annotations

import logging

import aiohttp

from homeassistant.components import conversation
from homeassistant.components.conversation import (
    ConversationEntity,
    ConversationInput,
    ConversationResult,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_URL, REQUEST_TIMEOUT

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities([ClaudeWrapperConversationEntity(entry)])


class ClaudeWrapperConversationEntity(ConversationEntity):
    """Forwards each Assist turn to the claude-auto-voice-wrapper HTTP service.

    HA's own conversation_id already tracks one phone call end-to-end (hass-sip
    reuses one context per call), so it doubles as the wrapper's session key —
    that is what keeps one Claude Code process alive per call instead of one
    per turn.
    """

    _attr_has_entity_name = True
    _attr_name = "Claude"

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_conversation"

    @property
    def supported_languages(self) -> str:
        return conversation.MATCH_ALL

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        call_id = user_input.conversation_id or "default"
        base_url = self._entry.data[CONF_URL].rstrip("/")
        url = f"{base_url}/message/{call_id}"
        session = async_get_clientsession(self.hass)

        response = intent.IntentResponse(language=user_input.language)
        try:
            async with session.post(
                url,
                json={"text": user_input.text},
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            ) as resp:
                data = await resp.json()
                if resp.status != 200:
                    raise RuntimeError(data.get("error", f"HTTP {resp.status}"))
                reply_text = data["text"]
        except Exception as err:  # noqa: BLE001 - surfaced to the caller as speech
            _LOGGER.error("claude-auto-voice-wrapper call failed: %s", err)
            response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                "Sorry, ik kon Claude niet bereiken.",
            )
            return ConversationResult(response=response, conversation_id=call_id)

        response.async_set_speech(reply_text)
        return ConversationResult(response=response, conversation_id=call_id)
