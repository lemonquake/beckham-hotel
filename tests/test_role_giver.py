"""
Unit tests for the Role Giver module, Mod Panel button, filters, and role assignment logic.
"""

import asyncio
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import views.role_giver_view as role_giver

from views.mod_panel_view import ModPanelView, FUNCTION_GUIDE
from views.role_giver_view import (
    RoleGiverHubView,
    RoleGiverConfirmView,
    RoleGiverProgressView,
    calculate_role_giver_stats,
    validate_target_role,
    build_role_giver_embed,
    build_confirm_embed,
    RoleGiverStats,
)


def run(coro):
    return asyncio.run(coro)


class FakeRole:
    def __init__(self, id: int, name: str, position: int = 1, managed: bool = False, is_default: bool = False):
        self.id = id
        self.name = name
        self.position = position
        self.managed = managed
        self._is_default = is_default
        self.members = []

    def is_default(self) -> bool:
        return self._is_default

    @property
    def mention(self) -> str:
        return f"<@&{self.id}>"


class FakePermissions:
    def __init__(self, administrator: bool = False, manage_roles: bool = True, manage_guild: bool = True):
        self.administrator = administrator
        self.manage_roles = manage_roles
        self.manage_guild = manage_guild


class FakeMember:
    def __init__(self, id: int, name: str, roles: list[FakeRole] = None, bot: bool = False, admin: bool = False):
        self.id = id
        self.name = name
        self.roles = list(roles or [])
        self.bot = bot
        self.guild_permissions = FakePermissions(administrator=admin)
        self.add_roles = AsyncMock()


class FakeGuild:
    def __init__(self, id: int = 100, members: list[FakeMember] = None, bot_member: FakeMember = None):
        self.id = id
        self.name = "Test Guild"
        self.members = list(members or [])
        self.member_count = len(self.members)
        self.chunked = True
        self.me = bot_member or FakeMember(999, "Bot", roles=[FakeRole(99, "BotRole", position=50)])
        self.chunk = AsyncMock()


class TestRoleGiver(unittest.TestCase):
    def setUp(self):
        self.target_role = FakeRole(1, "TargetRole", position=10)
        self.admin_role = FakeRole(2, "AdminRole", position=20)
        self.vip_role = FakeRole(3, "VIPRole", position=5)

        self.bot_user = FakeMember(10, "OtherBot", bot=True)
        self.admin_member = FakeMember(11, "AdminUser", roles=[self.admin_role], admin=True)
        self.vip_member = FakeMember(12, "VIPUser", roles=[self.vip_role])
        self.existing_member = FakeMember(13, "ExistingUser", roles=[self.target_role])
        self.eligible_member1 = FakeMember(14, "RegularUser1")
        self.eligible_member2 = FakeMember(15, "RegularUser2")

        self.members = [
            self.bot_user,
            self.admin_member,
            self.vip_member,
            self.existing_member,
            self.eligible_member1,
            self.eligible_member2,
        ]
        self.bot_role = FakeRole(99, "BotHighestRole", position=50)
        self.bot_member = FakeMember(999, "OurBot", roles=[self.bot_role])
        self.bot_member.top_role = self.bot_role
        self.bot_member.guild_permissions = FakePermissions(manage_roles=True)

        self.guild = FakeGuild(100, members=self.members, bot_member=self.bot_member)

    def test_calculate_role_giver_stats_all_filters_enabled(self):
        stats = run(
            calculate_role_giver_stats(
                self.guild,
                self.target_role,
                exclude_bots=True,
                exclude_admins=True,
                excluded_role_ids={self.vip_role.id},
            )
        )
        self.assertEqual(stats.total_members, 6)
        self.assertEqual(len(stats.bots), 1)
        self.assertEqual(stats.bots[0].id, self.bot_user.id)
        self.assertEqual(len(stats.admins), 1)
        self.assertEqual(stats.admins[0].id, self.admin_member.id)
        self.assertEqual(len(stats.role_excluded), 1)
        self.assertEqual(stats.role_excluded[0].id, self.vip_member.id)
        self.assertEqual(len(stats.already_has_role), 1)
        self.assertEqual(stats.already_has_role[0].id, self.existing_member.id)
        self.assertEqual(len(stats.eligible_members), 2)
        eligible_ids = {m.id for m in stats.eligible_members}
        self.assertEqual(eligible_ids, {self.eligible_member1.id, self.eligible_member2.id})

    def test_calculate_role_giver_stats_bots_included(self):
        stats = run(
            calculate_role_giver_stats(
                self.guild,
                self.target_role,
                exclude_bots=False,
                exclude_admins=True,
                excluded_role_ids=set(),
            )
        )
        self.assertEqual(len(stats.bots), 0)
        eligible_ids = {m.id for m in stats.eligible_members}
        self.assertIn(self.bot_user.id, eligible_ids)

    def test_calculate_role_giver_stats_admins_included(self):
        stats = run(
            calculate_role_giver_stats(
                self.guild,
                self.target_role,
                exclude_bots=True,
                exclude_admins=False,
                excluded_role_ids=set(),
            )
        )
        self.assertEqual(len(stats.admins), 0)
        eligible_ids = {m.id for m in stats.eligible_members}
        self.assertIn(self.admin_member.id, eligible_ids)

    def test_validate_target_role_none(self):
        valid, reason = validate_target_role(self.guild, None)
        self.assertFalse(valid)
        self.assertIn("No target role", reason)

    def test_validate_target_role_everyone(self):
        everyone = FakeRole(self.guild.id, "@everyone", position=0, is_default=True)
        valid, reason = validate_target_role(self.guild, everyone)
        self.assertFalse(valid)
        self.assertIn("@everyone", reason)

    def test_validate_target_role_managed(self):
        managed = FakeRole(50, "Server Booster", position=10, managed=True)
        valid, reason = validate_target_role(self.guild, managed)
        self.assertFalse(valid)
        self.assertIn("managed", reason)

    def test_validate_target_role_missing_manage_roles_perm(self):
        self.bot_member.guild_permissions = FakePermissions(manage_roles=False)
        valid, reason = validate_target_role(self.guild, self.target_role)
        self.assertFalse(valid)
        self.assertIn("Manage Roles", reason)

    def test_validate_target_role_hierarchy_violation(self):
        # Target role position is higher than bot's top role position
        higher_role = FakeRole(55, "SuperRole", position=100)
        valid, reason = validate_target_role(self.guild, higher_role)
        self.assertFalse(valid)
        self.assertIn("hierarchy", reason)

    def test_validate_target_role_success(self):
        valid, reason = validate_target_role(self.guild, self.target_role)
        self.assertTrue(valid)
        self.assertEqual(reason, "Valid")

    def test_beckham_member_role_is_blocked_by_actual_role_order(self):
        self.bot_member.top_role.position = 3
        member_role = FakeRole(1559568207495303279, "Member", position=5)
        view = RoleGiverHubView(self.guild, FakeMember(100, "Moderator"), target_role=member_role)
        view.stats = run(calculate_role_giver_stats(self.guild, member_role))
        view._sync_state()
        self.assertTrue(view.assign_roles_button.disabled)
        embed = build_role_giver_embed(self.guild, member_role, True, True, [], view.stats)
        self.assertIn("move **BotHighestRole** above **Member**", embed.description)
        self.bot_member.top_role.position = 6
        view._sync_state()
        self.assertFalse(view.assign_roles_button.disabled)

    def test_administrator_permission_is_sufficient_but_order_still_applies(self):
        self.bot_member.guild_permissions = FakePermissions(administrator=True, manage_roles=False)
        self.assertTrue(validate_target_role(self.guild, self.target_role)[0])
        self.bot_member.top_role.position = 1
        self.assertFalse(validate_target_role(self.guild, self.target_role)[0])

    def test_missing_bot_member_blocks_assignment(self):
        self.guild.me = None
        self.assertFalse(validate_target_role(self.guild, self.target_role)[0])

    def test_equal_positions_use_discord_role_order(self):
        low_id = discord.Role(guild=self.guild, state=None, data={"id": "10", "name": "Bot", "position": 5})
        high_id = discord.Role(guild=self.guild, state=None, data={"id": "20", "name": "Member", "position": 5})
        self.bot_member.top_role = low_id
        self.assertTrue(validate_target_role(self.guild, high_id)[0])
        self.bot_member.top_role = high_id
        self.assertFalse(validate_target_role(self.guild, low_id)[0])

    def test_no_eligible_members_explains_disabled_button(self):
        view = RoleGiverHubView(self.guild, FakeMember(100, "Moderator"), target_role=self.target_role)
        view.stats = RoleGiverStats()
        view._sync_state()
        self.assertTrue(view.assign_roles_button.disabled)
        embed = build_role_giver_embed(self.guild, self.target_role, True, True, [], view.stats)
        self.assertIn("No members are eligible", embed.description)

    def test_member_cache_fetch_fallback(self):
        self.guild.members = []
        self.guild.member_count = len(self.members)
        async def fetch_members(*, limit):
            for member in self.members:
                yield member
        self.guild.fetch_members = fetch_members
        stats = run(calculate_role_giver_stats(self.guild, self.target_role))
        self.assertEqual(stats.total_members, len(self.members))
        self.assertIsNone(stats.scan_error)
        self.guild.chunk.assert_awaited_once()

    def test_incomplete_member_scan_does_not_enable_assignment(self):
        self.guild.member_count += 1
        self.guild.fetch_members = MagicMock(side_effect=RuntimeError("members unavailable"))
        stats = run(calculate_role_giver_stats(self.guild, self.target_role))
        view = RoleGiverHubView(self.guild, FakeMember(100, "Moderator"), target_role=self.target_role)
        view.stats = stats
        view._sync_state()
        self.assertIsNotNone(stats.scan_error)
        self.assertTrue(view.assign_roles_button.disabled)

    def test_selecting_role_enables_give_role_after_scan(self):
        interaction = MagicMock(user=FakeMember(100, "Moderator"))
        interaction.response.defer = AsyncMock()
        async def check():
            view = RoleGiverHubView(self.guild, interaction.user)
            self.assertTrue(view.assign_roles_button.disabled)
            with patch.object(role_giver, "replace_message", new=AsyncMock()):
                view.target_select._values = [self.target_role]
                await view.target_select.callback(interaction)
            self.assertFalse(view.assign_roles_button.disabled)
            self.assertEqual(len(view.stats.eligible_members), 3)
        run(check())

    def test_confirmation_rechecks_permissions_and_prevents_double_assignment(self):
        interaction = MagicMock(user=FakeMember(100, "Moderator"))
        interaction.response.defer = AsyncMock()
        async def check():
            hub = RoleGiverHubView(self.guild, interaction.user, target_role=self.target_role)
            hub.stats = await calculate_role_giver_stats(self.guild, self.target_role)
            confirm = RoleGiverConfirmView(hub)
            with patch.object(role_giver, "replace_message", new=AsyncMock()), patch.object(confirm, "_execute_assignment", new=AsyncMock()) as assign:
                await confirm.confirm_button.callback(interaction)
                await confirm.confirm_button.callback(interaction)
                await asyncio.sleep(0)
            assign.assert_awaited_once()
            blocked = RoleGiverConfirmView(hub)
            self.bot_member.top_role.position = 1
            with patch.object(role_giver, "replace_message", new=AsyncMock()), patch.object(blocked, "_execute_assignment", new=AsyncMock()) as assign:
                await blocked.confirm_button.callback(interaction)
            assign.assert_not_called()
        run(check())

    def test_assignment_reports_failures_and_skips_members_changed_after_preview(self):
        async def check():
            hub = RoleGiverHubView(self.guild, FakeMember(100, "Moderator"), target_role=self.target_role)
            hub.stats = await calculate_role_giver_stats(self.guild, self.target_role)
            self.vip_member.roles.append(self.target_role)
            self.eligible_member2.add_roles.side_effect = discord.Forbidden(SimpleNamespace(status=403, reason="no"), "no")
            interaction = MagicMock(user=hub.user)
            interaction.edit_original_response = AsyncMock()
            with patch.object(role_giver.asyncio, "sleep", new=AsyncMock()):
                await RoleGiverConfirmView(hub)._execute_assignment(interaction, RoleGiverProgressView(), self.target_role, hub.stats)
            self.eligible_member1.add_roles.assert_awaited_once()
            self.vip_member.add_roles.assert_not_called()
            result = interaction.edit_original_response.call_args.kwargs["embed"].description
            self.assertIn("**1** assignments failed", result)
            self.assertIn("Skipped after preview: **1**", result)
        run(check())

    def test_cancelled_assignment_does_not_give_any_roles(self):
        async def check():
            hub = RoleGiverHubView(self.guild, FakeMember(100, "Moderator"), target_role=self.target_role)
            hub.stats = await calculate_role_giver_stats(self.guild, self.target_role)
            progress = RoleGiverProgressView()
            progress.cancelled = True
            interaction = MagicMock(user=hub.user)
            interaction.edit_original_response = AsyncMock()
            await RoleGiverConfirmView(hub)._execute_assignment(interaction, progress, self.target_role, hub.stats)
            for member in self.members:
                member.add_roles.assert_not_called()
        run(check())

    def test_build_embeds(self):
        stats = run(
            calculate_role_giver_stats(
                self.guild,
                self.target_role,
                exclude_bots=True,
                exclude_admins=True,
            )
        )
        embed = build_role_giver_embed(
            self.guild,
            self.target_role,
            exclude_bots=True,
            exclude_admins=True,
            excluded_roles=[self.vip_role],
            stats=stats,
        )
        self.assertIsNotNone(embed)
        self.assertIn("Role Giver", embed.title)

        confirm_embed = build_confirm_embed(self.guild, self.target_role, stats)
        self.assertIsNotNone(confirm_embed)

    def test_mod_panel_has_role_giver_button(self):
        panel = ModPanelView()
        button_map = {child.custom_id: child for child in panel.children if hasattr(child, "custom_id")}
        self.assertIn("beckham_mod_panel:role_giver", button_map)
        rg_btn = button_map["beckham_mod_panel:role_giver"]
        self.assertEqual(rg_btn.label, "Role Giver")
        self.assertEqual(rg_btn.row, 3)

        # Row counts limit check
        for row_idx in range(5):
            count = sum(1 for c in panel.children if getattr(c, "row", None) == row_idx)
            self.assertLessEqual(count, 5, f"Row {row_idx} exceeds 5 buttons limit")

        # Function guide check
        guide_labels = [label for label, _ in FUNCTION_GUIDE]
        self.assertTrue(any("Role Giver" in label for label in guide_labels))

    def test_role_giver_hub_view_component_constraints(self):
        user = FakeMember(100, "Moderator")
        view = RoleGiverHubView(self.guild, user)
        # Check rows
        for row_idx in range(5):
            items_in_row = [c for c in view.children if getattr(c, "row", None) == row_idx]
            # If select menu, at most 1 item
            has_select = any(isinstance(c, (discord.ui.Select, discord.ui.RoleSelect)) for c in items_in_row)
            if has_select:
                self.assertEqual(len(items_in_row), 1)
            else:
                self.assertLessEqual(len(items_in_row), 5)

    def test_role_giver_progress_view_cancellation(self):
        progress_view = RoleGiverProgressView()
        self.assertFalse(progress_view.cancelled)
        interaction = MagicMock()
        interaction.response = MagicMock()
        interaction.response.edit_message = AsyncMock()
        run(progress_view.cancel_button.callback(interaction))
        self.assertTrue(progress_view.cancelled)
        self.assertTrue(progress_view.cancel_button.disabled)


if __name__ == "__main__":
    unittest.main()
