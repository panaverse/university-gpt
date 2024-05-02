import { redirect } from "next/navigation";
import { auth, auth_user_info } from "@/lib/auth";
import { AttemptWindow } from "./_components/attempt-window";

const page = async () => {
  const session = await auth();
  if (!session) {
    console.log("[session] No cookies. Redirecting...");
    redirect("/login");
  }

  const user_info = await auth_user_info();

  console.log("user_info", user_info);

  return (
    <main className="flex flex-col items-center justify-center w-screen h-screen bg-gray-100 dark:bg-gray-900">
      <AttemptWindow/>
    </main>
  );
};

export default page;
