import { redirect } from "next/navigation";
import { auth, auth_user_info } from "@/lib/auth";
import { StartQuizComponent } from "./_components/start-quiz";
import { QuizOverViewComponent } from "./_components/quiz-overview";
import { QuizHistoryResultsComponent } from "./_components/quiz-history-results";
import { QuizHeaderComponent } from "./_components/header";
import { AllRoles } from "@/lib/nav-links";
import { allAttemptedQuizzes } from "@/global-actions/all-quizzes-attempt";

type TempCode = {
  code: string;
};

// Function to get temporary code
async function getTempCode(user_id: number) {
  const res = await fetch(
    `${process.env.BACKEND_AUTH_SERVER_URL}/api/v1/oauth/temp-code?user_id=${user_id}`,
    {
      cache: "no-store",
    }
  );
  const data = await res.json();
  return data as TempCode;
}

const page = async ({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) => {

  const session = await auth();
  if (!session) {
    console.log("[session] No cookies. Redirecting...");
    redirect("/login");
  }

  const user_info = await auth_user_info();

  const redirect_uri = searchParams.redirect_uri;
  const state = searchParams.state;

  if (redirect_uri && state && session && user_info?.is_superuser === true) {
    // Check if the user is logged in and is_superuser
      const user_id = user_info?.id as number;
      const tempCode = await getTempCode(user_id);
      redirect(redirect_uri + `?code=${tempCode.code}` + `&state=${state}`);
  }

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
        {allQuizAttempts && <QuizHistoryResultsComponent allQuizAttempts={allQuizAttempts} />}
      </main>
    </>
  );
};

export default page;
