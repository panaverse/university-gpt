import QuizTimer from '@/components/elasped-time';

interface QuizHeaderProps {
    title: string;
    remainingQuestions: number;
    questionScore: number;
    timeStart: string;
    timeLimit: string;
  }
  
export const QuizAttemptHeader: React.FC<QuizHeaderProps> = ({ title, remainingQuestions, questionScore, timeLimit, timeStart }) => (
    <div className="mb-auto">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
        Quiz: {title}
      </h1>
      <div className="flex items-center justify-between mt-4 mb-6">
        <div className="flex items-center space-x-2 text-gray-500 dark:text-gray-400">
          <span>Remaining Questions: {remainingQuestions}</span>
          <span>•</span>
          {/* <span>Time Elapsed: {elapsedTime}</span> */}
          {/* <ElapsedTimeDisplay timeStart={timeStart} timeLimit={timeLimit} /> */}
          <QuizTimer timeLimit={timeLimit} timeStart={timeStart} />
          <span>•</span>
          <span>Question Score: {questionScore}</span>
        </div>
      </div>
    </div>
  );



