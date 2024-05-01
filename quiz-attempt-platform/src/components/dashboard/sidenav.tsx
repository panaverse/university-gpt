import Link from "next/link";
import NavLinks from "@/components/dashboard/nav-links";
import { PowerCircleIcon } from "lucide-react";
import { LogoutButton } from "@/components/auth/logout-button";

export default function SideNav() {
  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
      <Link
        className="mb-2 flex h-20 items-end justify-start rounded-md bg-blue-600 p-4 md:h-40"
        href="/dashboard"
      >
        <div className="w-32 text-white md:w-40 text-2xl font-semibold  drop-shadow-md">
          🔐 CAl AI
        </div>
      </Link>
      <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
        <NavLinks />
        <div className="hidden h-auto w-full grow rounded-md bg-gray-50 md:block"></div>

          <LogoutButton>
            <div className="flex h-[48px] w-full grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3">
              <PowerCircleIcon className="w-6" />
              <div className="hidden md:block">Sign Out</div>
            </div>
          </LogoutButton>

      </div>
    </div>
  );
}
