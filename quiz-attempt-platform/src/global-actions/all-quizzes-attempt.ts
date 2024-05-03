export interface QuizAttemptType {
    student_id: number;
    quiz_id: number;
    time_limit: string; // ISO 8601 duration format
    time_start: string; // ISO 8601 date-time format
    time_finish: string; // ISO 8601 date-time format
    status: 'completed' | 'pending' | 'in_progress'; // assuming possible statuses
    total_points: number;
    attempt_score: number;
    quiz_title: string;
    quiz_key: string;
    id: number;
  }
  
  // If you're handling an array of such objects:
type AllQuizAttempted = QuizAttemptType[];


export const allAttemptedQuizzes = async ({token}: {token: string}): Promise<AllQuizAttempted>  => {
    const res = await fetch(`${process.env.QUIZ_ATTEMPT_ASSESMENT_URL}/api/v1/answersheet/all`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
        }
    });
    return await res.json();
    }   