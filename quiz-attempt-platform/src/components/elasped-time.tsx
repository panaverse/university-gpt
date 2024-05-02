import React, { useEffect, useState } from 'react';

interface TimeProps {
  timeStart: string; // ISO string format
  timeLimit: string; // ISO 8601 duration format
}

const ElapsedTimeDisplay: React.FC<TimeProps> = ({ timeStart, timeLimit }) => {
  const [remainingTime, setRemainingTime] = useState('');

  useEffect(() => {
    const startTime = new Date(timeStart);
    const totalTime = parseISODuration(timeLimit);
    const endTime = new Date(startTime.getTime() + totalTime);

    const updateRemainingTime = () => {
      const now = new Date();
      let timeLeft = endTime.getTime() - now.getTime();
      if (timeLeft < 0) {
        timeLeft = 0; // Ensure time left doesn't go negative
      }

      const hours = Math.floor(timeLeft / (1000 * 60 * 60));
      const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

      setRemainingTime(`${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);

      if (timeLeft === 0) {
        clearInterval(intervalId);
      }
    };

    const intervalId = setInterval(updateRemainingTime, 1000);

    return () => {
      clearInterval(intervalId);
    };
  }, [timeStart, timeLimit]);

  return (
    <div>
      Remaining Time: {remainingTime}
    </div>
  );
};

// Helper function to parse ISO 8601 durations
function parseISODuration(duration: string): number {
  const regex = /P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/;
  const matches = duration.match(regex);
  if (!matches) {
    console.error("Invalid duration format:", duration);
    return 0;
  }
  
  const days = (parseInt(matches[1] || '0', 10) * 86400);
  const hours = (parseInt(matches[2] || '0', 10) * 3600);
  const minutes = (parseInt(matches[3] || '0', 10) * 60);
  const seconds = parseInt(matches[4] || '0', 10);
  return (days + hours + minutes + seconds) * 1000; // total milliseconds
}

export default ElapsedTimeDisplay;
