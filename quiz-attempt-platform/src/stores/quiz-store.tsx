import { create } from "zustand";
import { persist } from "zustand/middleware";
import { produce } from "immer";
import { toast } from "sonner";

interface Option {
  id: number;
  option_text: string;
}

interface Question {
  id: number;
  question_text: string;
  points: number;
  question_type: "single_select_mcq" | "multiple_select_mcq";
  options: Option[];
  selectedOptions?: number[]; // Track selected option IDs
}

export interface QuizData {
  quiz_title: string;
  quiz_questions: Question[];
  total_points: number;
  time_start: string;
  time_limit: string;
  answer_sheet_id: number;
}

interface QuizState {
  quizData: QuizData | null;
  currentQuestionIndex: number;
  isLoading: boolean;  // Add loading state here
  setQuizData: (data: QuizData) => void;
  submitAnswerAndUpdateQuestion: () => Promise<{ status: string; data?: any; error?: string }>;
  finishQuiz: () => Promise<void>;
  moveToNextQuestion: () => void;
  clearQuizData: () => void;
  setLoading: (loading: boolean) => void;  // Action to update loading state
}

export const useQuizStore = create<QuizState>()(
  persist(
    (set, get) => ({
      quizData: null,
      currentQuestionIndex: 0,
      isLoading: false,  // Initial state
      setQuizData: (data) =>
        set(
          produce((draft) => {
            draft.quizData = data;
            draft.currentQuestionIndex = 0;
          })
        ),
      submitAnswerAndUpdateQuestion: async () => {
        const { quizData, currentQuestionIndex } = get();

        if (!quizData || !quizData.quiz_questions[currentQuestionIndex]) {
          return { status: "no-quiz", error: "No quiz or question data available." };  // Handling undefined quiz data
        }
      
          const currentQuestion = quizData.quiz_questions[currentQuestionIndex];
          const selectedOptionsIds = currentQuestion.selectedOptions || [];

          const requestBody = {
            quiz_answer_sheet_id: quizData.answer_sheet_id,
            question_id: currentQuestion.id,
            question_type: currentQuestion.question_type,
            selected_options_ids: selectedOptionsIds,
          };
          try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_URL}/api/save-answer`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(requestBody),
            });
            set({ isLoading: true });  // Set loading before processing

            if (!response.ok) {
              throw new Error("Failed to submit answer");
            }

            toast("Answer submitted successfully");
            // Move to the next question or finish if it was the last one
            if (currentQuestionIndex < quizData.quiz_questions.length - 1) {
              get().moveToNextQuestion();
              return { status: "next" };  // Indicating the quiz continues
            } else {
              const result = await get().finishQuiz(); // Ensure this waits for the last submission
              return { status: "finished", data: result };  // Return result data on finish
            }
          } catch (error: any) {
            console.error("Error submitting answer:", error);
            toast("Failed to submit answer, please try again.");
            return { status: "error", error: error.message }; // Ensure error cases return a consistent type

          } finally {
            set({ isLoading: false });  // Reset loading after processing
          }
        
      },
      moveToNextQuestion: () =>
        set(
          produce((draft) => {
            if (draft.quizData && draft.currentQuestionIndex < draft.quizData.quiz_questions.length - 1) {
              draft.currentQuestionIndex += 1;
            }
          })
        ),
      finishQuiz: async () => {
        const { quizData } = get();
        if (quizData) {
          const requestBody = { quiz_answer_sheet_id: quizData.answer_sheet_id };
          
          try {
            set({ isLoading: true });
            const response = await fetch(`${process.env.NEXT_PUBLIC_URL}/api/finish-quiz`, {
              method: "PATCH",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
              throw new Error("Failed to finish quiz");
            }

            const data = await response.json();
            toast("Quiz finished successfully!");
            // Handle redirection or data processing here if needed
            // Example: navigate('/results-page', { state: { resultData: data } });
            set(
              produce((draft) => {
                draft.quizData = null;
                draft.currentQuestionIndex = 0;
              })
            );
            return data;
          } catch (error) {
            console.error("[STORE]Error finishing quiz:", error);
            toast("Error finishing quiz, please contact support.");
          } finally {
            set({ isLoading: false });
          }
        }
      },
      clearQuizData: () =>
        set(
          produce((draft) => {
            draft.quizData = null;
            draft.currentQuestionIndex = 0;
          })
        ),
        setLoading: (loading) => set({ isLoading: loading })  // Simple action to update loading state
      }),

    { name: "quiz-attempt-store" }
  )
);
