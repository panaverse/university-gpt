import { redirect } from "next/navigation";
import { auth, auth_user_info } from "@/lib/auth";
import { StartQuizComponent } from "./_components/start-quiz";
import { QuizOverViewComponent } from "./_components/quiz-overview";
import { QuizHistoryResultsComponent } from "./_components/quiz-history-results";
import { QuizHeaderComponent } from "./_components/header";
import { allAttemptedQuizzes } from "@/global-actions/all-quizzes-attempt";
import { AllRoles, navLinks } from "@/lib/nav-links";

const page = async () => {
  const session = await auth();
  if (!session) {
    console.log("[session] No cookies. Redirecting...");
    redirect("/login");
  }

  const user_info = await auth_user_info();

  const allQuizAttempts = await allAttemptedQuizzes({
    token: session.access_token,
  });

  return (
    <>
      <QuizHeaderComponent
        email={user_info?.email}
        userRole={user_info?.role ? (user_info?.role as AllRoles) : "student"}
      />
      <main className="flex-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
        <StartQuizComponent />
        <QuizOverViewComponent />
        <QuizHistoryResultsComponent allQuizAttempts={allQuizAttempts} />
      </main>{" "}
    </>
  );
};

export default page;
