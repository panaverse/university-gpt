import { create } from 'zustand';
import { persist } from 'zustand/middleware';

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
}

export interface QuizData {
  quiz_title: string;
  quiz_questions: Question[];
  total_points: number;
  time_start: string;
  time_limit: string;
}

interface QuizState {
  quizData: QuizData | null;
  currentQuestionIndex: number;
  setQuizData: (data: QuizData) => void;
  setCurrentQuestionIndex: (index: number) => void;
  nextQuestion: () => void;
  clearQuizOnTimeout: () => void;
  clearQuizData: () => void;
}

export const useQuizStore = create<QuizState>()(
  persist(
    (set, get) => ({
      quizData: null,
      currentQuestionIndex: 0,
      setQuizData: (data) => set({ quizData: data, currentQuestionIndex: 0 }),
      setCurrentQuestionIndex: (index) => set({ currentQuestionIndex: index }),
      nextQuestion: () => {
        const { currentQuestionIndex, quizData } = get();
        if (quizData && currentQuestionIndex < quizData.quiz_questions.length - 1) {
          const newQuestions = quizData.quiz_questions.slice();
          newQuestions.splice(currentQuestionIndex, 1); // Remove the current question
          set({ 
            quizData: {...quizData, quiz_questions: newQuestions},
            currentQuestionIndex: currentQuestionIndex // Adjust index if necessary
          });
        }
      },
      clearQuizOnTimeout: () => {
        set({ quizData: null, currentQuestionIndex: 0 });
      },
      clearQuizData: () => set({ quizData: null, currentQuestionIndex: 0 }), // Method to clear quiz data
    }),
    { name: 'quiz-attempt-store' }
  )
);
