import pytest
from django_llm_chat.chat import Chat
from django.contrib.auth import get_user_model
from django_llm_chat.chat import create_litellm_user


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="12345")


@pytest.fixture
def model_name() -> str:
    return "ollama_chat/qwen3:4b"


@pytest.fixture
def chat(db):
    return Chat.create()


@pytest.fixture
def litellm_user():
    return create_litellm_user()


@pytest.fixture
def readingpal_user(db):
    User = get_user_model()
    return User.objects.create_user(username="readingpal", password="12345")


@pytest.fixture
def user_query() -> str:
    return "Summarize the text please."


@pytest.fixture
def article_text() -> str:
    return """Advance your subject-matter expertise
Learn in-demand skills from university and industry experts
Master a subject or tool with hands-on projects
Develop a deep understanding of key concepts
Earn a career certificate from EDUCBA

Specialization - 3 course series
This Specialization equips learners with practical expertise in Linux administration, Python programming, and Bash scripting to automate and manage modern IT environments. Through hands-on projects and guided lessons, participants will master Linux commands, process automation, text processing, GUI development, and database integration. The program blends scripting fundamentals with enterprise-level solutions, preparing learners for roles in system administration, DevOps, and cloud automation.

Applied Learning Project

Learners will complete hands-on projects such as developing automation scripts, creating interactive system tools, optimizing text processing pipelines, and deploying Bash solutions for real-world scenarios. These projects ensure learners can confidently apply Linux, Python, and Bash skills to solve authentic IT challenges in enterprise and cloud settings."""
