"use client";
import { useEffect } from "react";
import { QuizAttemptHeader } from "./quiz-header";
import { QuestionCard } from "./question-card";
import { QuizAttemptFooter } from "./quiz-footer";
import { useQuizStore } from "@/stores/quiz-store";
import { produce } from "immer";
import { useRouter } from "next/navigation";
import useResultStore from "@/stores/quiz-attempt-result";
import LoadingScreenComponent from "@/components/loading-screens";
import { devLog } from "@/lib/utils";

export const AttemptWindow = () => {
  const { quizData, currentQuestionIndex, submitAnswerAndUpdateQuestion } =
    useQuizStore((state) => ({
      quizData: state.quizData,
      currentQuestionIndex: state.currentQuestionIndex,
      submitAnswerAndUpdateQuestion: state.submitAnswerAndUpdateQuestion,
    }));
  const router = useRouter();
  const finishQuiz = useQuizStore(state => state.finishQuiz);

  useEffect(() => {
    const unsubscribe = useQuizStore.subscribe((state) => {
      if (state.quizData) {
        const options =
          state.quizData.quiz_questions[state.currentQuestionIndex]
            .selectedOptions;
        devLog(`Current selected options state: ${options}`);
      }
    });
    return () => unsubscribe(); // Cleanup subscription when component unmounts or dependencies change
  }, [currentQuestionIndex]); // Re-subscribe when currentQuestionIndex changes

  if (!quizData?.quiz_questions?.length) {
    devLog("No quiz data found", quizData);
    return <LoadingScreenComponent />
  }

  const question = quizData.quiz_questions[currentQuestionIndex];

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const optionId = parseInt(event.target.value, 10);
    const checked = event.target.checked;

    useQuizStore.setState((state) => {
      const questionIndex = state.currentQuestionIndex;
      const currentOptions =
        state?.quizData?.quiz_questions[questionIndex].selectedOptions || [];
      let newOptions;

      if (
        state?.quizData?.quiz_questions[questionIndex].question_type ===
        "multiple_select_mcq"
      ) {
        newOptions = checked
          ? [...currentOptions, optionId]
          : currentOptions.filter((id) => id !== optionId);
      } else {
        newOptions = checked ? [optionId] : [];
      }

      return produce(state, (draft) => {
        if (draft.quizData) {
          draft.quizData.quiz_questions[questionIndex].selectedOptions =
            newOptions;
        }
      });
    });
  };

  const handleNext = async () => {
    try {
      const result = await submitAnswerAndUpdateQuestion();
      if (result.status === "finished") {
        const data = result.data;
        useResultStore.getState().setResults(data);
        router.push("/dashboard/quiz-result");
        devLog("Quiz Finished Redirecting.");
      } else if (result.status === "error") {
        // Handle error, display message
        console.error(result.error);
        // Check if error message is "Quiz Time has Ended or Invalid Quiz Attempt ID to finish the quiz
        if (
          result.error && result.error ===
          "Quiz Time has Ended or Invalid Quiz Attempt ID to finish the quiz"
        ) {
          const data = await finishQuiz();
          // @ts-ignore
          useResultStore.getState().setResults(data); 
          router.push("/dashboard/quiz-result");
        }
      } else {
        devLog("Moving to the next question.");
      }
    } catch (error) {
      console.error(
        "Failed to submit answer or move to the next question:",
        error
      );
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 shadow-lg rounded-lg w-full p-8">
      <QuizAttemptHeader
        key={`header-${currentQuestionIndex}`}
        title={quizData.quiz_title}
        remainingQuestions={
          quizData.quiz_questions.length - currentQuestionIndex - 1
        }
        timeStart={quizData.time_start}
        timeLimit={quizData.time_limit}
        questionScore={question.points}
      />
      <QuestionCard
        key={`question-${currentQuestionIndex}`}
        question={question.question_text}
        options={question.options.map((option) => ({
          id: option.id.toString(),
          option_text: option.option_text,
        }))}
        questionType={question.question_type}
        selectedOptions={
          quizData.quiz_questions[currentQuestionIndex].selectedOptions?.map(
            String
          ) || []
        }
        onChange={handleOptionChange}
      />
      <QuizAttemptFooter
        key={`footer-${currentQuestionIndex}`}
        timeStart={quizData.time_start}
        totalPoints={quizData.total_points}
        onFinish={handleNext}
        onNext={handleNext}
        isLastQuestion={
          currentQuestionIndex === quizData.quiz_questions.length - 1
        }
      />
    </div>
  );
};
