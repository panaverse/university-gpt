"use client";
import { QuizAttemptHeader } from "./quiz-header";
import { QuestionCard } from "./question-card";
import { QuizAttemptFooter } from "./quiz-footer";
import { useQuizStore } from "@/stores/quiz-store";
import { redirect } from "next/navigation";
import { DEFAULT_LOGIN_REDIRECT } from "@/lib/routes";

export const AttemptWindow = () => {
  const { quizData, currentQuestionIndex, setCurrentQuestionIndex, nextQuestion } = useQuizStore(state => ({
    quizData: state.quizData,
    currentQuestionIndex: state.currentQuestionIndex,
    setCurrentQuestionIndex: state.setCurrentQuestionIndex,
    nextQuestion: state.nextQuestion
  }));
  console.log(" data found", quizData);

  if (!quizData?.quiz_questions || !quizData?.quiz_questions.length) {
    console.log("No quiz data found", quizData);
    // Optionally redirect
    // redirect(DEFAULT_LOGIN_REDIRECT);
    return <></>;
  }

  const question = quizData.quiz_questions[currentQuestionIndex];

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    console.log(`Option ${event.target.value} selected`);
  };

  const handleFinish = () => {
    console.log("Finish Quiz");
    // Implement finish logic here
  };

  const handleNext = () => {
    console.log("Next Question");
    nextQuestion(); // Using Zustand's method now
  };

  return (
    <div className="bg-white dark:bg-gray-800 shadow-lg rounded-lg w-full p-8">
      <QuizAttemptHeader
        title={quizData.quiz_title}
        remainingQuestions={quizData.quiz_questions.length - currentQuestionIndex - 1}
        timeStart={quizData.time_start}
        timeLimit={quizData.time_limit}
        questionScore={question.points}
      />
      <QuestionCard
        question={question.question_text}
        options={question.options.map(option => ({
          value: option.id.toString(),
          label: option.option_text,
        }))}
        questionType={question.question_type}
        onChange={handleOptionChange}
      />
      <QuizAttemptFooter
        timeStart={quizData.time_start}
        totalPoints={quizData.total_points}
        onFinish={handleFinish}
        onNext={handleNext}
      />
    </div>
  );
};
