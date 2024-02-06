import enum

# Enum for QuestionDifficulty
class QuestionDifficultyEnum(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

# Enum for QuestionType
class QuestionTypeEnum(str, enum.Enum):
    # Single Select MCQ
    single_select_mcq = "single_select_mcq"
    # Multiple Select MCQ
    multiple_select_mcq = "multiple_select_mcq"
    # Free Text
    free_text = "free_text"
    # Coding Problem
    coding_problem = "coding_problem"