import pytest
from django_llm_chat.chat import Chat, DuplicateSystemMessageError
from django_llm_chat.models import (
    Chat as ChatDBModel,
    Message,
    LLMCall,
)


def test_create_chat(db):
    Chat.create()
    assert ChatDBModel.objects.count() == 1

    chat = ChatDBModel.objects.first()

    assert chat.input_tokens_count == 0
    assert chat.output_tokens_count == 0


def test_create_user_query(user, chat):
    msg = chat.create_user_message(text="hi", user=user)

    assert msg.user == user
    assert msg.chat == chat.chat_db_model
    assert Message.objects.count() == 1


def test_send_to_llm(model_name, article_text, readingpal_user, user, chat, user_query):
    system_msg = chat.create_system_message("You are an artist!", user)
    first_user_msg = chat.create_user_message(text=article_text, user=readingpal_user)
    ai_msg, second_user_msg, _ = chat.send_user_msg_to_llm(
        model_name=model_name, text=user_query, user=user
    )

    assert Message.objects.count() == 4, "1 system, 2 user, 1 LLM"
    assert Message.objects.filter(type=Message.Type.ASSISTANT).count() == 1
    assert Message.objects.filter(type=Message.Type.USER).count() == 2
    assert Message.objects.filter(type=Message.Type.SYSTEM).count() == 1

    assert first_user_msg.chat == chat.chat_db_model
    assert system_msg.chat == chat.chat_db_model
    assert second_user_msg.chat == chat.chat_db_model
    assert ai_msg.chat == chat.chat_db_model

    for msg in Message.objects.all():
        assert msg.chat == chat.chat_db_model
        assert len(msg.llmcall_set.all()) == 1

    chat_db_model = ChatDBModel.objects.get(id=chat.chat_db_model.id)
    assert chat_db_model.input_tokens_count > 1
    assert chat_db_model.output_tokens_count > 1

    assert LLMCall.objects.count() == 1

    llm_call_db_model = LLMCall.objects.first()

    assert len(llm_call_db_model.messages.all()) == 4, (
        "Two user messages plus one LLM message plus one system message"
    )
    assert llm_call_db_model.input_tokens_count > 1
    assert llm_call_db_model.output_tokens_count > 1
    assert llm_call_db_model.response_data
    assert "message" in llm_call_db_model.response_data
    assert "id" in llm_call_db_model.response_data
    assert "model" in llm_call_db_model.response_data
    assert "usage" in llm_call_db_model.response_data


def test_adding_system_message_more_than_once(chat, user):
    chat.create_system_message("You are an artist!", user)
    with pytest.raises(DuplicateSystemMessageError):
        chat.create_system_message("You are a doctor!", user)
