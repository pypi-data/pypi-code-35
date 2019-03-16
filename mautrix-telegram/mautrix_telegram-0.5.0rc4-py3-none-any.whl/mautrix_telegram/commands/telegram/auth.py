# -*- coding: future_fstrings -*-
# mautrix-telegram - A Matrix-Telegram puppeting bridge
# Copyright (C) 2018 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Any, Dict, Optional
import asyncio

from telethon.errors import (
    AccessTokenExpiredError, AccessTokenInvalidError, FirstNameInvalidError, FloodWaitError,
    PasswordHashInvalidError, PhoneCodeExpiredError, PhoneCodeInvalidError,
    PhoneNumberAppSignupForbiddenError, PhoneNumberBannedError, PhoneNumberFloodError,
    PhoneNumberOccupiedError, PhoneNumberUnoccupiedError, SessionPasswordNeededError)

from ... import puppet as pu, user as u
from ...commands import command_handler, CommandEvent, SECTION_AUTH
from ...util import format_duration, ignore_coro


@command_handler(needs_auth=False,
                 help_section=SECTION_AUTH,
                 help_text="Check if you're logged into Telegram.")
async def ping(evt: CommandEvent) -> Optional[Dict]:
    me = await evt.sender.client.get_me() if await evt.sender.is_logged_in() else None
    human_tg_id = f"@{me.username}" if me.username else f"+{me.phone}"
    if me:
        return await evt.reply(f"You're logged in as {human_tg_id}")
    else:
        return await evt.reply("You're not logged in.")


@command_handler(needs_auth=False, needs_puppeting=False,
                 help_section=SECTION_AUTH,
                 help_text="Get the info of the message relay Telegram bot.")
async def ping_bot(evt: CommandEvent) -> Optional[Dict]:
    if not evt.tgbot:
        return await evt.reply("Telegram message relay bot not configured.")
    bot_info = await evt.tgbot.client.get_me()
    mxid = pu.Puppet.get_mxid_from_id(bot_info.id)
    displayname = bot_info.first_name
    return await evt.reply("Telegram message relay bot is active: "
                           f"[{displayname}](https://matrix.to/#/{mxid}) (ID {bot_info.id})\n\n"
                           "To use the bot, simply invite it to a portal room.")


@command_handler(needs_auth=False, management_only=True,
                 help_section=SECTION_AUTH,
                 help_args="<_phone_> <_full name_>",
                 help_text="Register to Telegram")
async def register(evt: CommandEvent) -> Optional[Dict]:
    if await evt.sender.is_logged_in():
        return await evt.reply("You are already logged in.")
    elif len(evt.args) < 1:
        return await evt.reply("**Usage:** `$cmdprefix+sp register <phone> <full name>`")

    phone_number = evt.args[0]
    if len(evt.args) == 2:
        full_name = evt.args[1], ""
    else:
        full_name = " ".join(evt.args[1:-1]), evt.args[-1]

    await _request_code(evt, phone_number, {
        "next": enter_code_register,
        "action": "Register",
        "full_name": full_name,
    })
    return None


async def enter_code_register(evt: CommandEvent) -> Dict:
    if len(evt.args) == 0:
        return await evt.reply("**Usage:** `$cmdprefix+sp <code>`")
    try:
        await evt.sender.ensure_started(even_if_no_session=True)
        first_name, last_name = evt.sender.command_status["full_name"]
        user = await evt.sender.client.sign_up(evt.args[0], first_name, last_name)
        ignore_coro(asyncio.ensure_future(evt.sender.post_login(user), loop=evt.loop))
        evt.sender.command_status = None
        return await evt.reply(f"Successfully registered to Telegram.")
    except PhoneNumberOccupiedError:
        return await evt.reply("That phone number has already been registered. "
                               "You can log in with `$cmdprefix+sp login`.")
    except FirstNameInvalidError:
        return await evt.reply("Invalid name. Please set a Matrix displayname before registering.")
    except PhoneCodeExpiredError:
        return await evt.reply(
            "Phone code expired. Try again with `$cmdprefix+sp register <phone>`.")
    except PhoneCodeInvalidError:
        return await evt.reply("Invalid phone code.")
    except Exception:
        evt.log.exception("Error sending phone code")
        return await evt.reply("Unhandled exception while sending code. "
                               "Check console for more details.")


@command_handler(needs_auth=False, management_only=True,
                 help_section=SECTION_AUTH,
                 help_text="Get instructions on how to log in.")
async def login(evt: CommandEvent) -> Optional[Dict]:
    override_sender = False
    if len(evt.args) > 0 and evt.sender.is_admin:
        evt.sender = await u.User.get_by_mxid(evt.args[0]).ensure_started()
        override_sender = True
    if await evt.sender.is_logged_in():
        return await evt.reply(f"You are already logged in as {evt.sender.human_tg_id}.")

    allow_matrix_login = evt.config.get("bridge.allow_matrix_login", True)
    if allow_matrix_login and not override_sender:
        evt.sender.command_status = {
            "next": enter_phone_or_token,
            "action": "Login",
        }

    nb = "**N.B. Logging in grants the bridge full access to your Telegram account.**"
    if evt.config["appservice.public.enabled"]:
        prefix = evt.config["appservice.public.external"]
        url = f"{prefix}/login?token={evt.public_website.make_token(evt.sender.mxid, '/login')}"
        if allow_matrix_login:
            if override_sender:
                return await evt.reply(
                    "This bridge instance allows you to log in inside or outside of Matrix, but "
                    "logging in as another user is only possible via the web interface.\n\n"
                    f"Please visit [the login page]({url}) to log in as "
                    f"[{evt.sender.mxid}](https://matrix.to/#/{evt.sender.mxid}).\n\n")
            return await evt.reply(
                "This bridge instance allows you to log in inside or outside Matrix.\n\n"
                "If you would like to log in within Matrix, please send your phone number or bot "
                "auth token here.\n"
                "If you would like to log in outside of Matrix, please visit [the login page]"
                f"({url}).\n\n"
                "Logging in outside of Matrix is recommended if you have two-factor authentication "
                "enabled, because in-Matrix login would save your password in the message history."
                f"\n\n{nb}")
        if override_sender:
            return await evt.reply(
                "This bridge instance does not allow logging in inside Matrix, and logging in as "
                "another user inside Matrix isn't possible anyway.\n\n"
                f"Please visit [the login page]({url}) to log in as "
                f"[{evt.sender.mxid}](https://matrix.to/#/{evt.sender.mxid}).")
        return await evt.reply(
            "This bridge instance does not allow logging in inside Matrix.\n\n"
            f"Please visit [the login page]({url}) to log in.\n\n"
            f"{nb}")
    elif allow_matrix_login:
        if override_sender:
            return await evt.reply(
                "This bridge instance does not allow you to log in outside of Matrix. "
                "Logging in as another user inside Matrix is not currently possible.")
        return await evt.reply(
            "This bridge instance does not allow you to log in outside of Matrix.\n\n"
            "Please send your phone number or bot auth token here to start the login process.\n\n"
            f"{nb}")
    return await evt.reply("This bridge instance has been configured to not allow logging in.")


async def _request_code(evt: CommandEvent, phone_number: str, next_status: Dict[str, Any]
                        ) -> Dict:
    ok = False
    try:
        await evt.sender.ensure_started(even_if_no_session=True)
        await evt.sender.client.sign_in(phone_number)
        ok = True
        return await evt.reply(f"Login code sent to {phone_number}. Please send the code here.")
    except PhoneNumberAppSignupForbiddenError:
        return await evt.reply(
            "Your phone number does not allow 3rd party apps to sign in.")
    except PhoneNumberFloodError:
        return await evt.reply(
            "Your phone number has been temporarily blocked for flooding. "
            "The ban is usually applied for around a day.")
    except FloodWaitError as e:
        return await evt.reply(
            "Your phone number has been temporarily blocked for flooding. "
            f"Please wait for {format_duration(e.seconds)} before trying again.")
    except PhoneNumberBannedError:
        return await  evt.reply("Your phone number has been banned from Telegram.")
    except PhoneNumberUnoccupiedError:
        return await  evt.reply("That phone number has not been registered. "
                                "Please register with `$cmdprefix+sp register <phone>`.")
    except Exception:
        evt.log.exception("Error requesting phone code")
        return await evt.reply("Unhandled exception while requesting code. "
                               "Check console for more details.")
    finally:
        evt.sender.command_status = next_status if ok else None


@command_handler(needs_auth=False)
async def enter_phone_or_token(evt: CommandEvent) -> Optional[Dict]:
    if len(evt.args) == 0:
        return await evt.reply("**Usage:** `$cmdprefix+sp enter-phone-or-token <phone-or-token>`")
    elif not evt.config.get("bridge.allow_matrix_login", True):
        return await evt.reply("This bridge instance does not allow in-Matrix login. "
                               "Please use `$cmdprefix+sp login` to get login instructions")

    # phone numbers don't contain colons but telegram bot auth tokens do
    if evt.args[0].find(":") > 0:
        try:
            await _sign_in(evt, bot_token=evt.args[0])
        except Exception:
            evt.log.exception("Error sending auth token")
            return await evt.reply("Unhandled exception while sending auth token. "
                                   "Check console for more details.")
    else:
        await _request_code(evt, evt.args[0], {
            "next": enter_code,
            "action": "Login",
        })
    return None


@command_handler(needs_auth=False)
async def enter_code(evt: CommandEvent) -> Optional[Dict]:
    if len(evt.args) == 0:
        return await evt.reply("**Usage:** `$cmdprefix+sp enter-code <code>`")
    elif not evt.config.get("bridge.allow_matrix_login", True):
        return await evt.reply("This bridge instance does not allow in-Matrix login. "
                               "Please use `$cmdprefix+sp login` to get login instructions")
    try:
        await _sign_in(evt, code=evt.args[0])
    except Exception:
        evt.log.exception("Error sending phone code")
        return await evt.reply("Unhandled exception while sending code. "
                               "Check console for more details.")
    return None


@command_handler(needs_auth=False)
async def enter_password(evt: CommandEvent) -> Optional[Dict]:
    if len(evt.args) == 0:
        return await evt.reply("**Usage:** `$cmdprefix+sp enter-password <password>`")
    elif not evt.config.get("bridge.allow_matrix_login", True):
        return await evt.reply("This bridge instance does not allow in-Matrix login. "
                               "Please use `$cmdprefix+sp login` to get login instructions")
    try:
        await _sign_in(evt, password=" ".join(evt.args))
    except AccessTokenInvalidError:
        return await evt.reply("That bot token is not valid.")
    except AccessTokenExpiredError:
        return await evt.reply("That bot token has expired.")
    except Exception:
        evt.log.exception("Error sending password")
        return await evt.reply("Unhandled exception while sending password. "
                               "Check console for more details.")
    return None


async def _sign_in(evt: CommandEvent, **sign_in_info) -> Dict:
    try:
        await evt.sender.ensure_started(even_if_no_session=True)
        user = await evt.sender.client.sign_in(**sign_in_info)
        existing_user = u.User.get_by_tgid(user.id)
        if existing_user and existing_user != evt.sender:
            await existing_user.log_out()
            await evt.reply(f"[{existing_user.displayname}]"
                            f"(https://matrix.to/#/{existing_user.mxid})"
                            " was logged out from the account.")
        ignore_coro(asyncio.ensure_future(evt.sender.post_login(user), loop=evt.loop))
        evt.sender.command_status = None
        name = f"@{user.username}" if user.username else f"+{user.phone}"
        return await evt.reply(f"Successfully logged in as {name}")
    except PhoneCodeExpiredError:
        return await evt.reply("Phone code expired. Try again with `$cmdprefix+sp login`.")
    except PhoneCodeInvalidError:
        return await evt.reply("Invalid phone code.")
    except PasswordHashInvalidError:
        return await evt.reply("Incorrect password.")
    except SessionPasswordNeededError:
        evt.sender.command_status = {
            "next": enter_password,
            "action": "Login (password entry)",
        }
        return await evt.reply("Your account has two-factor authentication. "
                               "Please send your password here.")


@command_handler(needs_auth=True,
                 help_section=SECTION_AUTH,
                 help_text="Log out from Telegram.")
async def logout(evt: CommandEvent) -> Optional[Dict]:
    if await evt.sender.log_out():
        return await evt.reply("Logged out successfully.")
    return await evt.reply("Failed to log out.")
