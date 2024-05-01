
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";

// type TempCode = {
//   code: string;
// };

// Function to get temporary code
// async function getTempCode(user_id: string) {
//   const res = await fetch(
//     `${process.env.BACKEND_AUTH_SERVER_URL}/api/oauth/temp-code?user_id=${user_id}`,
//     {
//       cache: "no-store",
//     }
//   );
//   const data = await res.json();
//   return data as TempCode;
// }

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

  // const redirect_uri = searchParams.redirect_uri;
  // const state = searchParams.state;

  // if (redirect_uri && state && session) {
  //   const user_id = session.user.id;
  //   const tempCode = await getTempCode(user_id);
  //   redirect(redirect_uri + `?code=${tempCode.code}` + `&state=${state}`);
  // }

  return (
    <div className="flex w-full h-screen flex-col md:flex-row items-center justify-center">
      Dashboard
  </div>
   
  );
};

export default page;
