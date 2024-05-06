import { Suspense } from "react";
import { CardTitle, CardHeader, CardContent, Card } from "@/components/ui/card";
import {
  TableHead,
  TableRow,
  TableHeader,
  TableCell,
  TableBody,
  Table,
} from "@/components/ui/table";
import { AllQuizAttempted } from "@/global-actions/all-quizzes-attempt";

export const QuizHistoryResultsComponent = async ({
  allQuizAttempts,
}: {
  allQuizAttempts: AllQuizAttempted;
}) => {


  if (!allQuizAttempts) {
    return (
      <Suspense fallback={<div>Loading...</div>}>
        <Card className="col-span-1 md:col-span-2 lg:col-span-3">
          <CardHeader className="flex items-center justify-between pb-4">
            <CardTitle>Recent Quiz Results</CardTitle>
            <BarChartIcon className="w-6 h-6 text-gray-500 dark:text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-lg">Sleeping!!!</div>
          </CardContent>
        </Card>
      </Suspense>
    );
  }

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Card className="col-span-1 md:col-span-2 lg:col-span-3">
        <CardHeader className="flex items-center justify-between pb-4">
          <CardTitle>Recent Quiz Results</CardTitle>
          <BarChartIcon className="w-6 h-6 text-gray-500 dark:text-gray-400" />
        </CardHeader>
        <CardContent>
          {allQuizAttempts.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Quiz</TableHead>
                  <TableHead>Score (Pts)</TableHead>
                  <TableHead>Percentage</TableHead>
                  <TableHead>Date</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {allQuizAttempts.map((attempt) => {
                  const percentage = (
                    (attempt.attempt_score / attempt.total_points) *
                    100
                  ).toFixed(1); // Calculate percentage and format to 1 decimal place
                  return (
                    <TableRow key={attempt.id}>
                      <TableCell>{attempt.quiz_title}</TableCell>
                      <TableCell>{`${attempt.attempt_score} / ${attempt.total_points}`}</TableCell>
                      <TableCell>{`${percentage}%`}</TableCell>
                      <TableCell>
                        {new Date(attempt.time_finish).toLocaleDateString()}
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          ) : (
            <div className="text-lg">No Quiz Results Available.</div>
          )}
        </CardContent>
      </Card>
    </Suspense>
  );
};

function BarChartIcon(props: any) {
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
      <line x1="12" x2="12" y1="20" y2="10" />
      <line x1="18" x2="18" y1="20" y2="4" />
      <line x1="6" x2="6" y1="20" y2="16" />
    </svg>
  );
}
