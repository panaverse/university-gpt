import React, { useState, useEffect } from 'react';
import { useQuizStore } from "@/stores/quiz-store"; // Import Zustand store
import { useRouter } from 'next/navigation';
import useResultStore from '@/stores/quiz-attempt-result';

interface QuizTimerProps {
  timeStart: string;  // UTC start time in ISO 8601 format
  timeLimit: string;  // Duration in ISO 8601 format, e.g., 'P3D'
}

const QuizTimer: React.FC<QuizTimerProps> = ({ timeStart, timeLimit }) => {
  const [remainingTime, setRemainingTime] = useState<string>('');
  const finishQuiz = useQuizStore(state => state.finishQuiz);
  const router = useRouter();

  useEffect(() => {
    const startTime = new Date(timeStart + 'Z');  // Parse as UTC
    const duration = parseISODuration(timeLimit);
    const endTime = new Date(startTime.getTime() + duration);

    let timer: NodeJS.Timeout;

    function updateRemainingTime() {
      const now = new Date();
      const timeLeft = endTime.getTime() - now.getTime();

      if (timeLeft > 0) {
        const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeLeft / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((timeLeft / (1000 * 60)) % 60);
        const seconds = Math.floor((timeLeft / 1000) % 60);

        let displayTime = '';
        if (days > 0) displayTime += `${days}d `;
        if (hours > 0 || displayTime) displayTime += `${hours}h `;
        if (minutes > 0 || displayTime) displayTime += `${minutes}m `;
        displayTime += `${seconds}s`;

        setRemainingTime(displayTime);
      } else {
        setRemainingTime('Time is up!');
        clearInterval(timer);
        handleQuizCompletion();
      }
    }

    updateRemainingTime();
    timer = setInterval(updateRemainingTime, 1000);

    return () => clearInterval(timer);
  }, [timeStart, timeLimit, finishQuiz, router]);

  async function handleQuizCompletion() {
    try {
      const data = await finishQuiz();
      // @ts-ignore
      useResultStore.getState().setResults(data); 
      router.push("/dashboard/quiz-result");
    } catch (error) {
      console.error("Error on finishing the quiz:", error);
    }
  }

  function parseISODuration(duration: string): number {
    const regex = /^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/;
    const matches = duration.match(regex);

    const days = matches?.[1] ? parseInt(matches[1], 10) * 86400000 : 0;
    const hours = matches?.[2] ? parseInt(matches[2], 10) * 3600000 : 0;
    const minutes = matches?.[3] ? parseInt(matches[3], 10) * 60000 : 0;
    const seconds = matches?.[4] ? parseInt(matches[4], 10) * 1000 : 0;

    return days + hours + minutes + seconds;
  }

  return (
    <div>
      <h1>Remaining Time: {remainingTime}</h1>
    </div>
  );
};

export default QuizTimer;
