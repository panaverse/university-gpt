"use client";

import { logout } from "@/global-actions/logout";
import { useRouter } from "next/navigation";

interface LogoutButtonProps {
  children?: React.ReactNode;
};

export const LogoutButton = ({
  children
}: LogoutButtonProps) => {

  const router = useRouter();
  const onClick = () => {
    logout();
    router.push("/");
  };

  return (
    <span onClick={onClick} className="cursor-pointer">
      {children}
    </span>
  );
};
