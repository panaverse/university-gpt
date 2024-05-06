import { Button } from "@/components/ui/button";
import { useQuizStore } from "@/stores/quiz-store";

interface QuizFooterProps {
  timeStart: string;
  totalPoints: number;
  onFinish: () => Promise<void>;
  onNext: () => void;
  isLastQuestion: boolean;
}

export const QuizAttemptFooter: React.FC<QuizFooterProps> = ({
  timeStart,
  totalPoints,
  onFinish,
  onNext,
  isLastQuestion,
}) => {
  const isLoading = useQuizStore((state) => state.isLoading);

  return (
    <div className="mt-8 flex items-center justify-between">
      <div className="flex items-center space-x-2 text-gray-500 dark:text-gray-400">
        <span>
          <b>Total Points:</b> {totalPoints}
        </span>
        <span className="text-blue-400">•</span>
        <span className="hidden md:flex">
          {" "}
          <b>Time Start:</b>{" "}
          {new Date(timeStart).toLocaleString("en-GB", {
            day: "numeric",
            month: "long",
            year: "numeric",
          })}{" "}
          At {new Date(timeStart).toLocaleTimeString()} UTC{" "}
        </span>
      </div>
      <div className="flex space-x-4">
        {isLastQuestion && (
          <Button onClick={onFinish} variant="outline" disabled={isLoading}>
            Save & Finish
          </Button>
        )}
        {!isLastQuestion && (
          <Button onClick={onNext} disabled={isLoading}>
            Save & Next
          </Button>
        )}
      </div>
    </div>
  );
};
