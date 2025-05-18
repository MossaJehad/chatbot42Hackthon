domain_knowledge = """
42Amman is a tuition-free, peer-to-peer coding school in Jordan.
It is part of the 42 Network, a global community of innovative coding campuses.
There are no teachers, no classes, and no traditional exams.
Students learn through project-based learning and collaboration.

Location: Amman, Jordan.
Opening year: 2024.
Campus name: 42 Amman.
Core program: 18-month software engineering curriculum.
Partner: Luminus Education.
"""

def build_prompt(user_input):
    return domain_knowledge + "\nQ: " + user_input + "\nA:"
