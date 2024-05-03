import { Suspense } from "react";
import { LogoutButton } from "@/components/auth/logout-button";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { PowerCircleIcon } from "lucide-react";
import { AllRoles, navLinks } from "@/lib/nav-links";


export const QuizHeaderComponent = ({email, userRole}:{email: string | undefined, userRole: AllRoles}) => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <header className="flex items-center justify-between h-16 px-6 border-b">
        <div className="flex items-center gap-4">
          <Link
            className="flex items-center gap-2 text-lg font-semibold"
            href="/dashboard"
          >
            <BookIcon className="w-6 h-6" />
            <span>QuizPro</span>
          </Link>
          <nav className={`md:flex gap-6 text-sm font-medium`}>
            {navLinks.filter(link => link.roles.includes(userRole)).map((link, index) => (
              <Link key={index} href={link.href} className="text-gray-900 hover:text-gray-700 dark:text-gray-100 dark:hover:text-gray-300">
                {link.title}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <Button className="rounded-lg" size="sm" variant="ghost">
            <p className="px-1">{email ? email : "User" }</p>
          </Button>
          <LogoutButton>
            <div className="flex h-[32px] w-full grow items-center justify-center gap-1 rounded-md bg-gray-50 p-1 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-1.5 md:px-2">
              <PowerCircleIcon className="w-3" />
              <div className="hidden md:block">Sign Out</div>
            </div>
          </LogoutButton>
        </div>
      </header>
    </Suspense>
  );
};

function BookIcon(props: any) {
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
        <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
      </svg>
    );
  }
  