import { create } from "zustand";

interface QuizAttemptResult {
    quiz_id: number;
    time_start: string;
    time_finish: string;
    attempt_score: number;
    id: number;
    updated_at: string;
    time_limit: string;
    student_id: number;
    status: string;
    total_points: number;
    quiz_key: string;
    created_at: string;
}

interface ResultStoreState {
    results: QuizAttemptResult | null;
    setResults: (results: QuizAttemptResult) => void;
    clearResults: () => void;
}




const useResultStore = create<ResultStoreState>((set) => ({
    results: null,
    setResults: (results: QuizAttemptResult) => set({ results: results }),
    clearResults: () => set({ results: null }),
}));

export default useResultStore;
