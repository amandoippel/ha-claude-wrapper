from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import CONF_URL, DEFAULT_URL, DOMAIN


class ClaudeWrapperConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """One-field config flow: the base URL of the claude-auto-voice-wrapper service."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        errors: dict[str, str] = {}
        if user_input is not None:
            return self.async_create_entry(title="Claude Wrapper", data=user_input)

        schema = vol.Schema({vol.Required(CONF_URL, default=DEFAULT_URL): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
