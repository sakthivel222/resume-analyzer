# grammar_checker.py

import language_tool_python

def check_grammar(text):
    weak_verbs = [
        "responsible for",
        "worked on",
        "helped with",
        "involved in",
        "duty of"
    ]

    # Detect weak phrases even if grammar checking fails
    weak_phrases_found = []
    text_lower = text.lower()

    for phrase in weak_verbs:
        if phrase in text_lower:
            weak_phrases_found.append(phrase)

    try:
        tool = language_tool_python.LanguageTool("en-US")
        matches = tool.check(text)

        issues = []

        for match in matches[:20]:
            issues.append({
                "message": match.message,
                "context": match.context,
                "suggestion": match.replacements[:3]
            })

        return {
            "total_issues": len(matches),
            "issues": issues,
            "weak_phrases": weak_phrases_found
        }

    except Exception:
        return {
            "total_issues": 0,
            "issues": [{
                "message": "Grammar checker unavailable on this server.",
                "context": "",
                "suggestion": []
            }],
            "weak_phrases": weak_phrases_found
        }