import { Suspense } from "react";
import { CardTitle, CardHeader, CardContent, Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export const QuizOverViewComponent = () => {
  return (
    <Suspense>
      <></>
      {/* <Card>
          <CardHeader className="flex items-center justify-between pb-4">
            <CardTitle>Overall Score</CardTitle>
            <TrophyIcon className="w-6 h-6 text-gray-500 dark:text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold">92%</div>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              You're doing great!
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex items-center justify-between pb-4">
            <CardTitle>Quizzes Completed</CardTitle>
            <CheckCircleIcon className="w-6 h-6 text-gray-500 dark:text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold">18</div>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Keep up the great work!
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex items-center justify-between pb-4">
            <CardTitle>Upcoming Assessments</CardTitle>
            <CalendarIcon className="w-6 h-6 text-gray-500 dark:text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">Math Quiz</div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Due: May 15, 2023
                  </p>
                </div>
                <Button size="sm" variant="outline">
                  Prepare
                </Button>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">English Essay</div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Due: June 1, 2023
                  </p>
                </div>
                <Button size="sm" variant="outline">
                  Prepare
                </Button>
              </div>
            </div>
          </CardContent>
        </Card> */}
    </Suspense>
  );
};



function CalendarIcon(props: any) {
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
        <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
        <line x1="16" x2="16" y1="2" y2="6" />
        <line x1="8" x2="8" y1="2" y2="6" />
        <line x1="3" x2="21" y1="10" y2="10" />
      </svg>
    );
  }
  
  function CheckCircleIcon(props: any) {
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
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
      </svg>
    );
  }
  
  
  function TrophyIcon(props: any) {
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
        <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
        <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
        <path d="M4 22h16" />
        <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22" />
        <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" />
        <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z" />
      </svg>
    );
  }
  