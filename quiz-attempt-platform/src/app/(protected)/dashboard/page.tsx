import { redirect } from "next/navigation";
import { auth, auth_user_info } from "@/lib/auth";
import { StartQuizComponent } from "./components/start-quiz";
import { QuizOverViewComponent } from "./components/quiz-overview";
import { QuizHistoryResultsComponent } from "./components/quiz-history-results";
import { QuizHeaderComponent } from "./components/header";

const page = async () => {
  const session = await auth();
  if (!session) {
    console.log("[session] No cookies. Redirecting...");
    redirect("/login");
  }

  const user_info = await auth_user_info();

  console.log("user_info", user_info);

  return (
    <>
      <QuizHeaderComponent email={user_info?.email} />
      <main className="flex-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
        <StartQuizComponent />
        <QuizOverViewComponent />
        <QuizHistoryResultsComponent />
      </main>    </>
  );
};

export default page;