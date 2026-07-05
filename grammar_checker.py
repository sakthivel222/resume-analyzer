# grammar_checker.py
# Grammar and weak-phrase detection using LanguageTool

import language_tool_python


def check_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)

    issues = []
    weak_verbs = ["responsible for", "worked on", "helped with", "involved in", "duty of"]

    for match in matches[:20]:  # limit to top 20 to keep UI clean
        issues.append({
            "message": match.message,
            "context": match.context,
            "suggestion": match.replacements[:3]
        })

    weak_phrases_found = []
    text_lower = text.lower()
    for phrase in weak_verbs:
        if phrase in text_lower:
            weak_phrases_found.append(phrase)

    return {
        "total_issues": len(matches),
        "issues": issues,
        "weak_phrases": weak_phrases_found
    }
