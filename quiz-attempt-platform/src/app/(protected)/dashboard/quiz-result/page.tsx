"use client";
import useResultStore from "@/stores/quiz-attempt-result";
import { useRouter } from "next/navigation";

const ResultsPage = () => {
  const results = useResultStore((state) => state.results);
  const router = useRouter();
  // If Results are Null for 5 seconds, show error message
  if (!results) {
    setTimeout(() => {
      if (typeof window !== "undefined") {
        router.push("/dashboard");
      }
    }, 5000);

    return <div>Loading...</div>;
  }

  return (
    <QuizComponent
      attempt_score={results.attempt_score}
      total_points={results.total_points}
      time_finish={results.time_finish}
      time_start={results.time_start}
    />
  );
};

export default ResultsPage;

function QuizComponent({
  time_start,
  time_finish,
  attempt_score,
  total_points,
}: {
  time_start: string;
  time_finish: string;
  attempt_score: number;
  total_points: number;
}) {
  const { minutes, seconds } = calculateTimeTaken(time_start, time_finish);

  const percentage = calculatePercentage(attempt_score, total_points);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Results</h1>
        <div className="grid grid-cols-2 gap-4">
          <div className="col-span-2 sm:col-span-1">
            <p className="text-gray-500 dark:text-gray-400 mb-1">
              Total Time Spent
            </p>
            <p className="font-medium">
              {minutes} minutes, {seconds} seconds
            </p>
          </div>
          <div className="col-span-2 sm:col-span-1">
            <p className="text-gray-500 dark:text-gray-400 mb-1">Score</p>
            <p className="font-medium">{percentage}%</p>
          </div>
          <div className="col-span-2">
            <p className="text-gray-500 dark:text-gray-400 mb-1">
              Total Points
            </p>
            <p className="font-medium">
              {attempt_score} / {total_points}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

const calculateTimeTaken = (time_start: string, time_finish: string) => {
  const startDate = new Date(time_start).getTime();
  const finishDate = new Date(time_finish).getTime();
  const timeDifference = finishDate - startDate; // Difference in milliseconds
  const minutes = Math.floor(timeDifference / 60000);
  const seconds = Math.floor((timeDifference % 60000) / 1000);
  return { minutes, seconds };
};

function calculatePercentage(attemptScore: any, totalScore: any) {
  return (attemptScore / totalScore) * 100;
}
