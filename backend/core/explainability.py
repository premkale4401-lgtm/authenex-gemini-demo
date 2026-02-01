def generate_explanation(data: dict, ai_probability: float) -> str:
    """
    Converts forensic findings into a human-readable explanation.
    """

    findings = data.get("findings", [])

    if not findings:
        return (
            f"Deepfake probability {round(ai_probability, 2)}%. "
            "No strong manipulation indicators were detected."
        )

    explanation = (
        f"Deepfake probability {round(ai_probability, 2)}% based on: "
        + "; ".join(findings)
    )

    return explanation
