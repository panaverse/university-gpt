import { Suspense } from "react";
import { CardTitle, CardHeader, CardContent, Card } from "@/components/ui/card";
import { StartQuizForm } from "@/components/dashboard/start-quiz-form";

export const StartQuizComponent = () => {
  return (
    <Suspense>
      <Card className="col-span-1 md:col-span-2 lg:col-span-3">
        <CardHeader className="flex items-center justify-center pb-4">
          <CardTitle className="flex tems-center justify-center space-x-4">
            <FileQuestionIcon className="w-6 h-6 text-gray-500 dark:text-gray-400" />
            <>
            Open Quiz
            </>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <StartQuizForm />
        </CardContent>
      </Card>
    </Suspense>
  );
};

function FileQuestionIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
      <path d="M10 10.3c.2-.4.5-.8.9-1a2.1 2.1 0 0 1 2.6.4c.3.4.5.8.5 1.3 0 1.3-2 2-2 2" />
      <path d="M12 17h.01" />
    </svg>
  );
}
