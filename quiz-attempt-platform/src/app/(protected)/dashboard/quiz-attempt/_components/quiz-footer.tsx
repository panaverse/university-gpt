import { Button } from '@/components/ui/button';

interface QuizFooterProps {
    timeStart: string;
    totalPoints: number;
    onFinish: () => void;
    onNext: () => void;
  }

export const QuizAttemptFooter: React.FC<QuizFooterProps> = ({ timeStart, totalPoints, onFinish, onNext }) => (
    <div className="mt-8 flex items-center justify-between">
      <div className="flex items-center space-x-2 text-gray-500 dark:text-gray-400">
        <span>Time Start: {timeStart}</span>
        <span>•</span>
        <span>Total Points: {totalPoints}</span>
      </div>
      <div className="flex space-x-4">
        <Button onClick={onFinish} variant="outline">Finish</Button>
        <Button onClick={onNext}>Save & Next</Button>
      </div>
    </div>
  );
  