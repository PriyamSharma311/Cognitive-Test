# src/career/career_mapper.py

from typing import Dict, List


def recommend_career_fields(scores: Dict[str, int]) -> Dict:
    """
    Recommend career fields based on cognitive scores (0–100).

    Designed to be:
    - Inclusive (disability-aware)
    - Explainable
    - Compatible with RAG-based explanations
    """

    recommendations: List[Dict] = []

    # -----------------------------
    # NORMALIZE (SAFETY)
    # -----------------------------
    scores = {k: int(v) for k, v in scores.items()}

    reasoning = scores.get("reasoning", 0)
    attention = scores.get("attention", 0)
    language = scores.get("language", 0)
    executive = scores.get("executive", 0)
    memory = scores.get("memory", 0)

    # -----------------------------
    # DATA / ANALYTICS
    # -----------------------------
    if reasoning >= 60:
        recommendations.append({
            "field": "Data & Analytics",
            "fit_level": "Primary" if reasoning >= 70 else "Secondary",
            "roles": [
                "Data Analyst",
                "Business Analyst",
                "Research Assistant"
            ],
            "strengths_used": ["Reasoning", "Attention"],
            "why": (
                "Your logical thinking supports data interpretation, "
                "pattern recognition, and structured analysis."
            )
        })

    # -----------------------------
    # SOFTWARE / ENGINEERING
    # -----------------------------
    if reasoning >= 65 and executive >= 55:
        recommendations.append({
            "field": "Software & Engineering",
            "fit_level": "Primary" if reasoning >= 75 else "Secondary",
            "roles": [
                "Software Developer",
                "QA Engineer",
                "Systems Engineer"
            ],
            "strengths_used": ["Reasoning", "Executive Function"],
            "why": (
                "Problem-solving ability combined with planning skills "
                "supports structured technical and engineering work."
            )
        })

    # -----------------------------
    # COMMUNICATION / EDUCATION
    # -----------------------------
    if language >= 60:
        recommendations.append({
            "field": "Communication & Education",
            "fit_level": "Primary" if language >= 75 else "Secondary",
            "roles": [
                "Teacher",
                "Content Writer",
                "Trainer",
                "Instructional Designer"
            ],
            "strengths_used": ["Language"],
            "why": (
                "Strong language skills support explaining ideas, "
                "teaching concepts, and clear communication."
            )
        })

    # -----------------------------
    # OPERATIONS / MANAGEMENT
    # -----------------------------
    if executive >= 60:
        recommendations.append({
            "field": "Operations & Management",
            "fit_level": "Primary" if executive >= 75 else "Secondary",
            "roles": [
                "Project Coordinator",
                "Operations Analyst",
                "Product Associate"
            ],
            "strengths_used": ["Executive Function", "Attention"],
            "why": (
                "Planning, organization, and task coordination align "
                "well with operational and management roles."
            )
        })

    # -----------------------------
    # MEMORY-SUPPORTED ROLES
    # -----------------------------
    if memory >= 65:
        recommendations.append({
            "field": "Knowledge & Support Roles",
            "fit_level": "Secondary",
            "roles": [
                "Documentation Specialist",
                "Compliance Assistant",
                "Knowledge Coordinator"
            ],
            "strengths_used": ["Memory"],
            "why": (
                "Strong recall and information retention support roles "
                "that rely on accuracy and consistency."
            )
        })

    # -----------------------------
    # FALLBACK (IMPORTANT)
    # -----------------------------
    if not recommendations:
        recommendations.append({
            "field": "Guided Skill Development",
            "fit_level": "Foundational",
            "roles": [
                "Internships",
                "Apprenticeships",
                "Assisted Learning Programs"
            ],
            "strengths_used": [],
            "why": (
                "Your profile suggests focusing on foundational skills "
                "with structured guidance and gradual progression."
            )
        })

    # -----------------------------
    # CAREER CONFIDENCE SCORE
    # -----------------------------
    avg_score = sum(scores.values()) / len(scores)

    if avg_score >= 75:
        confidence = 90
    elif avg_score >= 60:
        confidence = 75
    elif avg_score >= 45:
        confidence = 60
    else:
        confidence = 40

    return {
        "recommended_fields": recommendations,
        "career_confidence": confidence,
        "score_summary": scores
    }
