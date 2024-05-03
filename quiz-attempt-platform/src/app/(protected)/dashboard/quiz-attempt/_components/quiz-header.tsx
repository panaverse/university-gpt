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
          <span className='flex'> <b>Questions Left: </b> {remainingQuestions}</span>
          <span className='text-blue-500'>•</span>
          <QuizTimer timeLimit={timeLimit} timeStart={timeStart} />
          <span className='text-blue-500'>•</span>
          <span className='flex'><b className='hidden md:flex'> Question Score:</b> <b className='md:hidden flex'> Score:</b> {questionScore}</span>
        </div>
      </div>
    </div>
  );



