import Link from "next/link";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

const navigation = [
  { id: 1, title: "Home", url: "/" },
  { id: 2, title: "Login", url: "/login" },
  { id: 3, title: "Register", url: "/register" },
];

const AuthLayout = ({
  children,
}: {
  children?: React.ReactNode;

}) => {
  // const cookies_user_data = cookies().has("user_data");

  // if (cookies_user_data ) {
  //   console.log("[auth] No user data in cookies. Redirecting to login.");
  //   redirect("/dashboard");
  // }

  

  return (
      <div className="h-full min-h-screen flex flex-col items-center justify-start bg-gradient-to-r from-custom-purple to-custom-blue">
      <nav className="mt-6 w-fit items-center bg-white/10 space-x-6 border font-mono border-zinc-300 m-2 bg-gradient-to-b from-zinc-100 to to-blue-50/80 shadow-lg rounded-lg px-6 py-3 text-xs text-gray-900 font-medium md:flex md:space-x-8 lg:text-sm">
        {navigation.map((item) => {
          return (
            <Link
              key={item.id}
              href={item.url}
              className="hover:underline underline-offset-2"
            >
              {item.title}
            </Link>
          );
        })}
      </nav>
      <div className="flex h-full w-full mx-auto my-auto items-center justify-center">
        {children}
      </div>
      </div>
  );
};

export default AuthLayout;
