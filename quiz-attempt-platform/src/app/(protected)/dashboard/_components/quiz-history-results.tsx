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

export const QuizHistoryResultsComponent = () => {
  return (
    <Suspense>
   <Card className="col-span-1 md:col-span-2 lg:col-span-3">
          <CardHeader className="flex items-center justify-between pb-4">
            <CardTitle>Recent Quiz Results</CardTitle>
            <BarChartIcon className="w-6 h-6 text-gray-500 dark:text-gray-400" />
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Quiz</TableHead>
                  <TableHead>Score</TableHead>
                  <TableHead>Date</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell>Biology Quiz</TableCell>
                  <TableCell>85%</TableCell>
                  <TableCell>April 30, 2023</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Math Test</TableCell>
                  <TableCell>92%</TableCell>
                  <TableCell>April 25, 2023</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>English Essay</TableCell>
                  <TableCell>88%</TableCell>
                  <TableCell>April 20, 2023</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>History Exam</TableCell>
                  <TableCell>90%</TableCell>
                  <TableCell>April 15, 2023</TableCell>
                </TableRow>
              </TableBody>
            </Table>
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