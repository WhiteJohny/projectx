from aiogram.types import User, Chat

TEST_USER = User(id=123, is_bot=False, first_name="Test", last_name="Bot", username="testbot", language_code='ru-RU',
                 is_premium=True, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None,
                 supports_inline_queries=None)

TEST_CHAT = Chat(id=12, type="private", username=TEST_USER.username, first_name=TEST_USER.first_name,
                 last_name=TEST_USER.last_name)
